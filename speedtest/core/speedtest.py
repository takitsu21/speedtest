import contextlib
import functools
import platform
import re
import shutil
import subprocess
import threading
import time
import urllib
import urllib.parse
from collections.abc import Generator
from typing import Any, Callable

import httpx
import rich
import rich.table
from alive_progress import alive_bar

from speedtest.models import metadata, result


@functools.cache
def client() -> httpx.Client:
    return httpx.Client(headers={"Connection": "Keep-Alive"})


@contextlib.contextmanager
def track_progress() -> Generator[Any, None, None]:
    with alive_bar(None, bar="smooth", spinner="pulse", force_tty=True) as bar:
        yield bar


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

    def _download(self):
        return client().get(f"{self.url}/__down", params={"bytes": self.download_size})

    def _update_progress(self, speed: float, jitter: int, bar: Any) -> None:
        bar.text = f"Speed: {speed:.2f} Mbps  | Jitter: {jitter:.2f} ms"
        bar(speed)

    @functools.cached_property
    def data_blocks(self):
        return b"0" * self.upload_size

    def _http_latency(self, url: str, **kwargs):
        start = time.perf_counter()
        client().head(url, **kwargs)
        return (time.perf_counter() - start) * 1000

    @property
    def download_latency(self):
        return self._http_latency(f"{self.url}/__down", params={"bytes": 0})

    @property
    def upload_latency(self):
        return self._http_latency(f"{self.url}/__up")

    def ping(self) -> None:
        # Determine the command parameters based on the OS
        param = "-n" if platform.system().lower() == "windows" else "-c"
        timeout_param = "-w" if platform.system().lower() == "windows" else "-W"

        try:
            ping_cmd = shutil.which("ping")
            result = subprocess.run(  # noqa: S603
                [ping_cmd, param, "3", timeout_param, "3", urllib.parse.urlparse(self.url).hostname],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                # Extract the time from the output
                output = result.stdout
                if platform.system().lower() == "windows":
                    # Parse the latency line for Windows
                    time_match = re.search(r"Average = (\d+)ms", output)
                else:
                    # Parse the latency line for Linux/Mac
                    time_match = re.search(r"time=(\d+\.?\d*) ms", output)

                if time_match:
                    avg_latency = 0
                    for match in time_match.groups():
                        avg_latency += float(match)
                    self.latency = avg_latency / len(time_match.groups())
                else:
                    rich.print(f"Ping successful, but unable to extract latency. => {output}")

        except FileNotFoundError:
            rich.print("Ping command not found. Ensure it is available on your system.")

    def _upload(self):
        return client().post(f"{self.url}/__up", data=self.data_blocks)

    def _compute_network_speed(self, bar: Any, size_to_process: int, func: Callable) -> result.Result:
        total_time = 0
        jitter = 0
        times_to_process = []
        jitters = []
        for attempt in range(1, self.attempts + 1):
            start = time.perf_counter()
            func()
            elapsed_time = time.perf_counter() - start
            times_to_process.append(elapsed_time)

            if len(times_to_process) > 1:
                jitter = abs(times_to_process[-1] - times_to_process[-2])
                jitters.append(jitter)

            total_time += elapsed_time
            average_time = total_time / attempt
            speed_mbps = (size_to_process * 8) / (average_time * 1024 * 1024)
            self._update_progress(bar=bar, speed=speed_mbps, jitter=jitter)

        jitter = sum(jitters) / len(jitters) if jitters else times_to_process[-1]
        if not self.latency:
            self._wait()

        http_latency = (
            self.download_latency if getattr(func, "__name__", "_download") == "_download" else self.upload_latency
        )
        return result.Result(speed=speed_mbps, jitter=jitter, latency=self.latency, http_latency=http_latency)

    def download_speed(self):
        rich.print("Running download test... 🚀")

        with track_progress() as bar:
            download_result = self._compute_network_speed(
                bar=bar, size_to_process=self.download_size, func=self._download
            )

        return download_result

    def upload_speed(self) -> result.Result:
        rich.print("Running upload test... 🚀")
        with track_progress() as bar:
            upload_result = self._compute_network_speed(bar, self.upload_size, self._upload)

        return upload_result

    @property
    def metadata(self) -> metadata.Metadata:
        return metadata.Metadata.model_validate(client().get(f"{self.url}/meta").json())
