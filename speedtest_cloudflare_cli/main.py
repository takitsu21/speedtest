#!/usr/bin/env python
from __future__ import annotations

import rich.json
import rich.table
import rich_click as click

from speedtest_cloudflare_cli.core import speedtest
from speedtest_cloudflare_cli.models import metadata, result

DOWNLOAD_SIZE = 50  # 50MB
UPLOAD_SIZE = 50  # 50MB

SPEEDTEST_URL = "https://speed.cloudflare.com/"


def display_results(
    download_result: result.Result | None, upload_result: result.Result | None, metadata: metadata.Metadata
) -> None:
    table = rich.table.Table(title="Speedtest Results", show_header=True, border_style="blue", title_style="bold")
    table.add_column("Metric", style="bold green")
    table.add_column("Download", style="bold yellow")
    table.add_column("Upload", style="bold magenta")

    # Helper function to handle None values
    def safe_value(result: result.Result | None, attr: str) -> str:
        result_attr = getattr(result, attr, None)
        if isinstance(result_attr, float):
            return f"{result_attr:.2f}"
        return "N/A"

    # Speed test results
    table.add_row("Speed", safe_value(download_result, "speed") + " Mbps", safe_value(upload_result, "speed") + " Mbps")
    table.add_row("Jitter", safe_value(download_result, "jitter") + " ms", safe_value(upload_result, "jitter") + " ms")
    table.add_row(
        "Latency", safe_value(download_result, "latency") + " ms", safe_value(upload_result, "latency") + " ms"
    )
    table.add_row(
        "HTTP Latency",
        safe_value(download_result, "http_latency") + " ms",
        safe_value(upload_result, "http_latency") + " ms",
    )

    # Metadata information
    table_metadata = rich.table.Table(title="Metadata", show_header=True, title_style="bold")
    table_metadata.add_column("Metric", style="bold green")
    table_metadata.add_column("Value", style="yellow")

    table_metadata.add_row("Hostname", metadata.hostname or "N/A")
    table_metadata.add_row("HTTP Protocol", metadata.http_protocol or "N/A")
    table_metadata.add_section()
    table_metadata.add_row("Region", metadata.region or "N/A")
    table_metadata.add_row("City", metadata.city or "N/A")
    table_metadata.add_row("Postal Code", metadata.postal_code or "N/A")
    table_metadata.add_row("ISP", metadata.isp or "N/A")
    table_metadata.add_section()
    table_metadata.add_row("IP Address", metadata.client_ip or "N/A")
    table_metadata.add_row("IPv6", str(metadata.is_ipv6) if metadata.is_ipv6 is not None else "N/A")
    table_metadata.add_row("Timestamp", metadata.date.isoformat() if metadata.date else "N/A")

    # Print tables
    rich.print(table)
    rich.print(table_metadata)


@click.command()
@click.option("--upload", "-u", is_flag=True, help="Run upload test")
@click.option("--download", "-d", is_flag=True, help="Run download test")
@click.option("--download_size", "-ds", type=int, default=DOWNLOAD_SIZE, help="Download size in MB")
@click.option("--upload_size", "-us", type=int, default=UPLOAD_SIZE, help="Upload size in MB")
@click.option("--attempts", "-a", type=int, default=5, help="Number of attempts")
@click.option("--json", is_flag=True, help="Output results in JSON format")
def main(*, download: bool, upload: bool, download_size: int, upload_size: int, attempts: int, json: bool) -> None:
    download_size = download_size * speedtest.CHUNK_SIZE
    upload_size = upload_size * speedtest.CHUNK_SIZE
    speedtester = speedtest.SpeedTest(
        url=SPEEDTEST_URL, download_size=download_size, upload_size=upload_size, attempts=attempts
    )
    download_result = None
    upload_result = None
    if download:
        download_result = speedtester.download_speed(silent=json)
    if upload:
        upload_result = speedtester.upload_speed(silent=json)
    if not download and not upload:
        download_result = speedtester.download_speed(silent=json)
        upload_result = speedtester.upload_speed(silent=json)

    if json:
        results = {
            "download": download_result.__dict__ if download_result else None,
            "upload": upload_result.__dict__ if upload_result else None,
            "metadata": speedtester.metadata.__dict__,
        }
        output = rich.json.JSON.from_data(results)
        rich.print(output)
        return
    else:
        display_results(download_result=download_result, upload_result=upload_result, metadata=speedtester.metadata)


if __name__ == "__main__":
    main()
