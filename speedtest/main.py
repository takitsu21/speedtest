import time
from typing import Any, Callable, Generator

import alive_progress
import httpx
import rich
import rich.table
import rich_click as click
from alive_progress import alive_bar
from alive_progress.styles import showtime
import contextlib

from dataclasses import dataclass
CHUNK_SIZE = 1024 * 1024  # 1MB
DOWNLOAD_SIZE = CHUNK_SIZE * 100  # 10MB
UPLOAD_SIZE = CHUNK_SIZE * 50  # 10MB

URL = "https://speed.cloudflare.com/"

@dataclass
class Result:
    speed: float
    jitter: float
    latency: float

@contextlib.contextmanager
def track_progress() -> Generator[Any, None, None]:
    with alive_bar(None) as bar:
        yield bar


def speedtest_download(url: str, download_size: int, attempts: int) -> None:
    rich.print("Running download test... 🚀")
    total_time = 0
    jitter = 0
    ping_times = []

    with track_progress() as bar:
        for attempt in range(1, attempts):
            start = time.time()
            response = httpx.get(f"{url}/__down", params={"bytes": download_size}, headers={"Connection": "Keep-Alive"})
            response.read()
            elapsed_time = time.time() - start
            for _ in response.iter_bytes(chunk_size=CHUNK_SIZE):
                bar(DOWNLOAD_SIZE / CHUNK_SIZE / 10)
            total_time += elapsed_time
            ping_times.append(elapsed_time)

            if len(ping_times) > 1:
                jitter = abs(ping_times[-1] - ping_times[-2])

            average_time = total_time / attempt
            download_speed_mbps = (download_size * 8) / (average_time * 1024 * 1024)

            bar.text = f"Speed: {download_speed_mbps:.2f} Mbps  | Jitter: {jitter * 1000:.2f} ms"

    average_time = total_time / attempts
    download_speed_mbps = (DOWNLOAD_SIZE * 8) / (average_time * 1024 * 1024)
    # jitter = sum(ping_times) / len(ping_times)  # in milliseconds
    rich.print(f"Download speed => {download_speed_mbps:.2f} Mbps")
    rich.print(f"Jitter: {jitter:.2f} ms")
    rich.print(f"Average latency: {jitter * 10:.2f} ms")
    jitter = sum(ping_times) / attempts
    # table = rich.table.Table(title="Speedtest Results", show_header=True, )
    # table.add_column("Metric", style="cyan")
    # table.add_column("Value", style="magenta")
    # table.add_row("Download Speed", f"{download_speed_mbps:.2f} Mbps")
    # table.add_row("Jitter", f"{jitter:.2f} ms")
    # # table.add_row("Average Latency", f"{sum(ping_times) / attempts:.2f} ms")
    # table.add_row("Pings", f"{ping_times}")
    # rich.print(table)
    return Result(speed=download_speed_mbps, jitter=jitter, latency=jitter * 10)


def speedtest_upload(url: str, upload_size: int, attempts: int) -> Result:
    rich.print("Running upload test... 🚀")
    total_time = 0
    with track_progress() as bar:
        for _ in range(attempts):
            start = time.time()
            response = httpx.post(f"{url}/__up", data=b"0" * upload_size)
            elapsed_time = time.time() - start
            total_time += elapsed_time
            upload_speed_mbps = len(response.content) / CHUNK_SIZE
            bar.text = f"Speed: {upload_speed_mbps:.2f} Mbps"
            for _ in response.iter_bytes(chunk_size=CHUNK_SIZE):
                bar()

    average_time = total_time / attempts
    upload_speed_mbps = (upload_size * 8) / (average_time * 1024 * 1024)
    rich.print(f"Upload speed => {upload_speed_mbps:.2f} Mbps")
    rich.print(f"Jitter: 0.00 ms")
    rich.print(f"Average latency: {average_time:.2f} ms")

    return Result(speed=upload_speed_mbps, jitter=0, latency=0)


def display_results(download_result: Result, upload_result: Result) -> None:
    table = rich.table.Table(title="Speedtest Results", show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Download", style="magenta")
    table.add_column("Upload", style="magenta")

    table.add_row("Speed", f"{download_result.speed:.2f} Mbps", f"{upload_result.speed:.2f} Mbps")
    table.add_row("Jitter", f"{download_result.jitter:.2f} ms", f"{upload_result.jitter:.2f} ms")
    table.add_row("Latency", f"{download_result.latency:.2f} ms", f"{upload_result.latency:.2f} ms")

    rich.print(table)

@click.command()
@click.option("--upload", "-u", is_flag=True, help="Run upload test")
@click.option("--download", "-d", is_flag=True, help="Run download test")
@click.option("--download_size", "-ds", type=int, default=DOWNLOAD_SIZE, help="Download size in MB")
@click.option("--upload_size", "-us", type=int, default=UPLOAD_SIZE, help="Upload size in MB")
@click.option("--attempts", "-a", type=int, default=10, help="Number of attempts")
def main(download: bool, upload: bool, download_size: int, upload_size: int, attempts: int) -> None:
    if download:
        download_result = speedtest_download(URL, download_size=download_size, attempts=attempts)
    if upload:
        upload_result = speedtest_upload(URL, upload_size=upload_size, attempts=attempts)
    if not download and not upload:
        download_result = speedtest_download(url=URL, download_size=download_size, attempts=attempts)
        upload_result = speedtest_upload(url=URL, upload_size=upload_size, attempts=attempts)

    display_results(download_result, upload_result)

if __name__ == "__main__":
    main()
