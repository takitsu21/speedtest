import rich
import rich.table
import rich_click as click

from speedtest.core import speedtest
from speedtest.models import metadata, result

CHUNK_SIZE = 1024 * 1024  # 1MB
DOWNLOAD_SIZE = CHUNK_SIZE * 50  # 50MB
UPLOAD_SIZE = CHUNK_SIZE * 50  # 50MB

URL = "https://speed.cloudflare.com/"


def display_results(download_result: result.Result, upload_result: result.Result, metadata: metadata.Metadata) -> None:
    table = rich.table.Table(title="Speedtest Results", show_header=True, border_style="blue", title_style="bold")
    table.add_column("Metric", style="bold green")
    table.add_column("Download", style="bold yellow")
    table.add_column("Upload", style="bold magenta")

    # Speed test results
    table.add_row("Speed", f"{download_result.speed:.2f} Mbps", f"{upload_result.speed:.2f} Mbps")
    table.add_row("Jitter", f"{download_result.jitter:.2f} ms", f"{upload_result.jitter:.2f} ms")
    table.add_row("Latency", f"{download_result.latency:.2f} ms", f"{upload_result.latency:.2f} ms")
    table.add_row("HTTP Latency", f"{download_result.http_latency:.2f} ms", f"{upload_result.http_latency:.2f} ms")

    # Metadata information
    table_metadata = rich.table.Table(title="Metadata", show_header=True, title_style="bold")
    table_metadata.add_column("Metric", style="bold green")
    table_metadata.add_column("Value", style="yellow")
    table_metadata.add_row("Hostname", metadata.hostname)
    table_metadata.add_row("HTTP Protocol", metadata.http_protocol)
    table_metadata.add_section()
    table_metadata.add_row("Region", metadata.region)
    table_metadata.add_row("City", metadata.city)
    table_metadata.add_row("Postal Code", metadata.postal_code)
    table_metadata.add_row("ISP", metadata.isp)
    table_metadata.add_section()
    table_metadata.add_row("IP Address", metadata.client_ip)
    table_metadata.add_row("IPv6", str(metadata.is_ipv6))
    table_metadata.add_row("Timestamp", metadata.date.isoformat())

    rich.print(table)
    rich.print(table_metadata)


@click.command()
@click.option("--upload", "-u", is_flag=True, help="Run upload test")
@click.option("--download", "-d", is_flag=True, help="Run download test")
@click.option("--download_size", "-ds", type=int, default=DOWNLOAD_SIZE, help="Download size in MB")
@click.option("--upload_size", "-us", type=int, default=UPLOAD_SIZE, help="Upload size in MB")
@click.option("--attempts", "-a", type=int, default=5, help="Number of attempts")
def main(download: bool, upload: bool, download_size: int, upload_size: int, attempts: int) -> None:
    s = speedtest.SpeedTest(url=URL, download_size=download_size, upload_size=upload_size, attempts=attempts)
    if download:
        download_result = s.download_speed()
    if upload:
        upload_result = s.download_speed()
    if not download and not upload:
        download_result = s.download_speed()
        upload_result = s.upload_speed()

    display_results(download_result, upload_result, s.metadata)


if __name__ == "__main__":
    main()
