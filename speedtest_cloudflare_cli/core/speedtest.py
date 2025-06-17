import contextlib
import functools
import re
import socket
import subprocess
import threading
import time
from collections.abc import Generator
from typing import Callable

import httpx
import ping3
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from speedtest_cloudflare_cli.models import metadata, result

CHUNK_SIZE = 1024 * 1024
PING_HOST = "google.com"
PING_COUNT = 3
PING_TIMEOUT = 3


@functools.cache
def client() -> httpx.Client:
    return httpx.Client(headers={"Connection": "Keep-Alive"}, timeout=None)  # noqa: S113


@contextlib.contextmanager
def track_progress(silent: bool = False) -> Generator[Progress, None, None]:
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(bar_width=None),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        disable=silent,
    ) as progress:
        yield progress


def _fallback_ping() -> float | str:
    # Try system ping
    try:
        out = subprocess.check_output(
            ["ping", "-c", str(PING_COUNT), "-W", str(PING_TIMEOUT), PING_HOST],
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
        with socket.create_connection((PING_HOST, 443), PING_TIMEOUT):
            return (time.perf_counter() - start) * 1000
    except OSError:
        return "N/A"


class SpeedTest:
    def __init__(self, url: str, download_size: int, upload_size: int, attempts: int):
        self.url = url
        self.download_size = download_size
        self.upload_size = upload_size
        self.attempts = attempts

        self._ping_thread = threading.Thread(target=self.ping, daemon=True)
        self._ping_thread.start()
        self.latency = None

    def _wait(self) -> None:
        if self._ping_thread.is_alive():
            self._ping_thread.join()

    def _download(self, progress: Progress | None = None, task: TaskID | None = None):
        """Download data in streaming chunks to keep the HTTP connection alive."""
        with client().stream("GET", f"{self.url}/__down", params={"bytes": self.download_size}) as response:
            # Consume the body in chunks so the server keeps feeding data.
            for chunk in response.iter_bytes(chunk_size=CHUNK_SIZE):
                if progress and task is not None:
                    progress.update(task, description="Downloading... 🚀", advance=len(chunk))

    @functools.cached_property
    def data_blocks(self):
        return b"0" * self.upload_size

    def _http_latency(self, **kwargs):
        start = time.perf_counter()
        client().head(f"https://{PING_HOST}", **kwargs)
        return (time.perf_counter() - start) * 1000


    def ping(self) -> None:
        try:
            self.latency = ping3.ping(PING_HOST, unit="ms", timeout=PING_TIMEOUT)
        except (ping3.errors.PingError, PermissionError):
            self.latency = _fallback_ping()

    def _upload(
        self,
        progress: Progress | None = None,
        task: TaskID | None = None,
    ) -> None:
        """Upload data in streaming chunks to keep the HTTP connection alive and update progress."""

        def data_stream():
            offset = 0
            while offset < self.upload_size:
                chunk = self.data_blocks[offset : offset + CHUNK_SIZE]
                offset += len(chunk)
                if progress and task is not None:
                    progress.update(task, description="Uploading... 🚀", advance=len(chunk))
                yield chunk

        # httpx will read the iterator lazily and stream the request body
        with client().stream("POST", f"{self.url}/__up", data=data_stream()) as _response:
            # No need to consume the response body; the context manager ensures the
            # request completes and the connection is released.
            pass

    def _compute_network_speed(self, progress: Progress, size_to_process: int, func: Callable) -> result.Result:
        jitter = 0
        times_to_process = []
        jitters = []
        if progress:
            task = progress.add_task("", total=size_to_process * self.attempts)
        for _ in range(self.attempts):
            start = time.perf_counter()
            func(progress, task)  # perform full transfer for this attempt
            elapsed_time = time.perf_counter() - start
            times_to_process.append(elapsed_time)

            if len(times_to_process) > 1:
                jitter = abs(times_to_process[-1] - times_to_process[-2])
                jitters.append(jitter)

        jitter = sum(jitters) / len(jitters) if jitters else times_to_process[-1]

        http_latency = self._http_latency()
        speed = progress.tasks[task].speed * 8 / 1_000_000

        # wait for ping to finish
        if not self.latency:
            self._wait()

        return result.Result(speed=speed, jitter=jitter, latency=self.latency, http_latency=http_latency)

    def download_speed(self, silent: bool) -> result.Result:
        with track_progress(silent=silent) as progress:
            download_result = self._compute_network_speed(
                progress=progress, size_to_process=self.download_size, func=self._download
            )

        return download_result

    def upload_speed(self, silent: bool) -> result.Result:
        with track_progress(silent=silent) as progress:
            upload_result = self._compute_network_speed(progress, self.upload_size, self._upload)

        return upload_result

    @property
    def metadata(self) -> metadata.Metadata:
        return metadata.Metadata.model_validate(client().get(f"{self.url}/meta").json())
