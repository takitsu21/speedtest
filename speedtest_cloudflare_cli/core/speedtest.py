import concurrent.futures
import contextlib
import functools
import re
import socket
import subprocess
import threading
import time
from collections.abc import Callable, Generator

import httpx
import ping3
from rich.progress import (
    BarColumn,
    Progress,
    TaskID,
    TextColumn,
    TransferSpeedColumn,
)

from speedtest_cloudflare_cli.models import metadata, result

CHUNK_SIZE = 1024 * 1024
CLOUDFLARE_HOST = "speed.cloudflare.com"
PING_COUNT = 3
PING_TIMEOUT = 3

# Adaptive mode constants
PROBE_SIZE_MB = 15  # Size for preliminary probe test (larger for accurate estimation)
PROBE_TIMEOUT_SECONDS = 3.0  # Max seconds for probe test
TARGET_TEST_DURATION = 10.0  # Target duration for main test in seconds
MIN_TEST_SIZE_MB = 1  # Minimum test size
MAX_TEST_SIZE_MB = 500  # Maximum test size for high-speed connections
MIN_REALISTIC_SPEED = 0.1  # Minimum realistic speed in Mbps
MAX_REALISTIC_SPEED = 10000  # Maximum realistic speed in Mbps
PARALLEL_CONNECTIONS = 8  # Number of parallel connections for upload


@functools.cache
def client() -> httpx.Client:
    headers = {"Connection": "Keep-Alive", "Referer": f"https://{CLOUDFLARE_HOST}/"}
    return httpx.Client(headers=headers, timeout=None)  # noqa: S113


def new_client() -> httpx.Client:
    """Create a new HTTP client for parallel connections."""
    headers = {"Connection": "Keep-Alive", "Referer": f"https://{CLOUDFLARE_HOST}/"}
    return httpx.Client(headers=headers, timeout=None)  # noqa: S113


@contextlib.contextmanager
def track_progress(silent: bool = False) -> Generator[Progress]:
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(bar_width=None),
        TransferSpeedColumn(),
        disable=silent,
    ) as progress:
        yield progress


@contextlib.contextmanager
def track_progress_transient(silent: bool = False) -> Generator[Progress]:
    """Progress bar that disappears when done (for probe tests)."""
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(bar_width=None),
        TransferSpeedColumn(),
        disable=silent,
        transient=True,  # Progress bar disappears when done
    ) as progress:
        yield progress


def _fallback_ping() -> float | str:
    # Try system ping
    try:
        out = subprocess.check_output(  # noqa: S603
            ["ping", "-c", str(PING_COUNT), "-W", str(PING_TIMEOUT), CLOUDFLARE_HOST],  # noqa: S607
            stderr=subprocess.DEVNULL,
            text=True,
        )
        m = re.search(r"time=([\d.]+)\s*ms", out)
        if m:
            return float(m.group(1))
    except subprocess.CalledProcessError:
        pass

    # Fallback to TCP latency
    try:
        start = time.perf_counter()
        with socket.create_connection((CLOUDFLARE_HOST, 443), PING_TIMEOUT):
            return (time.perf_counter() - start) * 1000
    except OSError:
        return "N/A"


class SpeedTest:
    def __init__(self, url: str, download_size: int, upload_size: int, attempts: int, timeout: float | None = None):
        self.url = url
        self.download_size = download_size
        self.upload_size = upload_size
        self.attempts = attempts
        self.timeout = timeout  # Timeout per test in seconds (None = no timeout)

        self._ping_thread = threading.Thread(target=self.ping, daemon=True)
        self._ping_thread.start()
        self.latency = None

    def _wait(self) -> None:
        if self._ping_thread.is_alive():
            self._ping_thread.join()

    def _init_connection(self) -> None:
        """Opens a connection to the server and keeps it alive for subsequent requests."""
        client().get(f"{self.url}/__down", params={"bytes": 0})

    def _download(
        self, progress: Progress | None = None, task: TaskID | None = None, deadline: float | None = None
    ) -> None:
        """Download data in streaming chunks to keep the HTTP connection alive."""
        with client().stream("GET", f"{self.url}/__down", params={"bytes": self.download_size}) as response:
            # Consume the body in chunks so the server keeps feeding data.
            for chunk in response.iter_bytes(chunk_size=CHUNK_SIZE):
                if deadline is not None and time.perf_counter() > deadline:
                    break  # Timeout reached, stop downloading
                if progress and task is not None:
                    progress.update(task, description="Downloading... 🚀", advance=len(chunk))

    @functools.cached_property
    def upload_chunk(self) -> bytes:
        """Single reusable chunk for uploads - avoids repeated allocations."""
        return b"0" * CHUNK_SIZE

    def _http_latency(self, **kwargs):
        start = time.perf_counter()
        client().head(f"https://{CLOUDFLARE_HOST}", **kwargs, headers={"Connection": "Close"})
        return (time.perf_counter() - start) * 1000

    def ping(self) -> None:
        try:
            self.latency = ping3.ping(CLOUDFLARE_HOST, unit="ms", timeout=PING_TIMEOUT)
        except (ping3.errors.PingError, PermissionError):
            self.latency = _fallback_ping()

    def _upload(
        self,
        progress: Progress | None = None,
        task: TaskID | None = None,
        deadline: float | None = None,
    ) -> None:
        """Upload data in streaming chunks to keep the HTTP connection alive and update progress."""
        chunk = self.upload_chunk  # Reuse same chunk - no allocation per iteration

        def data_stream():
            bytes_sent = 0
            while bytes_sent < self.upload_size:
                if deadline is not None and time.perf_counter() > deadline:
                    break  # Timeout reached, stop uploading
                remaining = self.upload_size - bytes_sent
                current_chunk = chunk if remaining >= CHUNK_SIZE else chunk[:remaining]
                bytes_sent += len(current_chunk)
                if progress and task is not None:
                    progress.update(task, description="Uploading... 🚀", advance=len(current_chunk))
                yield current_chunk

        # httpx will read the iterator lazily and stream the request body
        with client().stream("POST", f"{self.url}/__up", data=data_stream()) as _response:
            # No need to consume the response body; the context manager ensures the
            # request completes and the connection is released.
            pass

    def _parallel_upload_worker(
        self,
        upload_size: int,
        progress: Progress | None,
        task: TaskID | None,
        deadline: float | None,
        lock: threading.Lock,
    ) -> int:
        """Worker function for parallel upload. Returns bytes uploaded."""
        chunk = self.upload_chunk
        http_client = new_client()
        bytes_uploaded = 0

        try:

            def data_stream():
                nonlocal bytes_uploaded
                while bytes_uploaded < upload_size:
                    if deadline is not None and time.perf_counter() > deadline:
                        break
                    remaining = upload_size - bytes_uploaded
                    current_chunk = chunk if remaining >= CHUNK_SIZE else chunk[:remaining]
                    bytes_uploaded += len(current_chunk)
                    if progress and task is not None:
                        with lock:
                            progress.update(task, description="Uploading... 🚀", advance=len(current_chunk))
                    yield current_chunk

            with http_client.stream("POST", f"{self.url}/__up", data=data_stream()) as _response:
                pass
        finally:
            http_client.close()

        return bytes_uploaded

    def _parallel_upload(
        self,
        progress: Progress | None = None,
        task: TaskID | None = None,
        deadline: float | None = None,
    ) -> None:
        """Upload data using multiple parallel connections to maximize bandwidth."""
        total_size = self.upload_size
        size_per_connection = total_size // PARALLEL_CONNECTIONS
        lock = threading.Lock()

        with concurrent.futures.ThreadPoolExecutor(max_workers=PARALLEL_CONNECTIONS) as executor:
            futures = [
                executor.submit(
                    self._parallel_upload_worker,
                    size_per_connection,
                    progress,
                    task,
                    deadline,
                    lock,
                )
                for _ in range(PARALLEL_CONNECTIONS)
            ]
            concurrent.futures.wait(futures)

    def _compute_network_speed(self, progress: Progress, size_to_process: int, func: Callable) -> result.Result:
        jitter = 0
        times_to_process = []
        jitters = []

        self._init_connection()

        # Calculate deadline if timeout is set
        deadline = time.perf_counter() + self.timeout if self.timeout else None

        # Use indeterminate progress (total=None) when timeout is set since we don't know final size
        total = None if self.timeout else size_to_process * self.attempts
        task = progress.add_task("", total=total)

        for _ in range(self.attempts):
            # Check if we've exceeded the deadline before starting a new attempt
            if deadline is not None and time.perf_counter() > deadline:
                break

            start = time.perf_counter()
            func(progress, task, deadline)  # perform transfer with deadline
            elapsed_time = time.perf_counter() - start
            times_to_process.append(elapsed_time)

            if len(times_to_process) > 1:
                jitter = abs(times_to_process[-1] - times_to_process[-2])
                jitters.append(jitter)

            # Check if we've exceeded the deadline after the attempt
            if deadline is not None and time.perf_counter() > deadline:
                break

        jitter = sum(jitters) / len(jitters) if jitters else (times_to_process[-1] if times_to_process else 0)
        http_latency = self._http_latency()
        speed = progress.tasks[task].speed * 8 / 1_000_000 if progress.tasks[task].speed else 0

        # wait for ping to finish
        if not self.latency:
            self._wait()

        return result.Result(speed=speed, jitter=jitter, latency=self.latency, http_latency=http_latency)

    def download_speed(self, silent: bool, adaptive: bool = False, default_size_mb: int = 30) -> result.Result:
        # Run adaptive sizing if enabled
        if adaptive:
            probe_speed = self._run_probe_test("download", silent=silent)
            adaptive_size = self._calculate_adaptive_size(probe_speed, "download", default_size_mb)
            self.download_size = adaptive_size

        with track_progress(silent=silent) as progress:
            download_result = self._compute_network_speed(
                progress=progress, size_to_process=self.download_size, func=self._download
            )

        return download_result

    def upload_speed(self, silent: bool, adaptive: bool = False, default_size_mb: int = 30) -> result.Result:
        # Run adaptive sizing if enabled
        if adaptive:
            probe_speed = self._run_probe_test("upload", silent=silent)
            adaptive_size = self._calculate_adaptive_size(probe_speed, "upload", default_size_mb)
            self.upload_size = adaptive_size

        with track_progress(silent=silent) as progress:
            upload_result = self._compute_network_speed(
                progress=progress, size_to_process=self.upload_size, func=self._parallel_upload
            )

        return upload_result

    @property
    def metadata(self) -> metadata.Metadata:
        return metadata.Metadata.model_validate(client().get(f"{self.url}/meta").json())

    def _run_probe_test(self, test_type: str, silent: bool = True) -> float | None:
        """
        Run a quick probe test to estimate bandwidth.

        Args:
            test_type: "download" or "upload"
            silent: Whether to suppress progress output

        Returns:
            Estimated speed in Mbps, or None if probe fails
        """
        probe_size = PROBE_SIZE_MB * CHUNK_SIZE
        original_size = self.download_size if test_type == "download" else self.upload_size

        try:
            # Temporarily set size to probe size
            if test_type == "download":
                self.download_size = probe_size
            else:
                self.upload_size = probe_size

            start_time = time.perf_counter()

            # Run single probe attempt with transient progress bar (disappears when done)
            with track_progress_transient(silent=silent) as progress:
                task = progress.add_task("🔍 Probing connection speed...", total=probe_size)

                if test_type == "download":
                    self._init_connection()
                    self._download(progress, task)
                else:
                    self._init_connection()
                    self._upload(progress, task)

                elapsed_time = time.perf_counter() - start_time

                # Check if probe timed out
                if elapsed_time > PROBE_TIMEOUT_SECONDS:
                    return None

                # Calculate speed in Mbps
                speed_mbps = (probe_size * 8) / (elapsed_time * 1_000_000)
                return speed_mbps

        except Exception:
            return None
        finally:
            # Restore original size
            if test_type == "download":
                self.download_size = original_size
            else:
                self.upload_size = original_size

    def _calculate_adaptive_size(self, probe_speed: float | None, test_type: str, default_size_mb: int) -> int:
        """
        Calculate optimal test size based on probe results.

        Args:
            probe_speed: Estimated speed in Mbps from probe test
            test_type: "download" or "upload" for logging
            default_size_mb: Default size in MB if probe fails

        Returns:
            Test size in bytes PER ATTEMPT (accounts for self.attempts)
        """
        # If probe failed or returned invalid speed, use default
        if probe_speed is None:
            return default_size_mb * CHUNK_SIZE

        # Check for unrealistic speeds
        if probe_speed < MIN_REALISTIC_SPEED or probe_speed > MAX_REALISTIC_SPEED:
            return default_size_mb * CHUNK_SIZE

        # Convert Mbps to MBps (megabytes per second)
        speed_MBps = probe_speed / 8

        # Calculate ideal size PER ATTEMPT
        # Use longer duration per attempt for better accuracy (5 seconds per attempt)
        # This ensures each attempt is substantial enough for accurate measurement
        duration_per_attempt = 5.0  # seconds per attempt
        ideal_size_mb = speed_MBps * duration_per_attempt

        # Apply boundaries (minimum 50MB per attempt for accuracy on fast connections)
        final_size_mb = max(50, min(ideal_size_mb, MAX_TEST_SIZE_MB))

        # Round to nearest integer and convert to bytes
        return int(round(final_size_mb)) * CHUNK_SIZE
