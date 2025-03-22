import contextlib
import functools
import threading
import time
from collections.abc import Generator
from typing import Any, Callable

import httpx
import ping3
import rich
import rich.table
from alive_progress import alive_bar

from speedtest_cloudflare_cli.models import metadata, result


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
        try:
            ping = ping3.ping("google.com", unit="ms")
            self.latency = ping if ping else "N/A"
        except ping3.errors.PingError as e:
            rich.print(f"Unable to ping the server. => {e}")
            self.latency = "N/A"

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
