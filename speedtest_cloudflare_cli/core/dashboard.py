#!/usr/bin/env python3
"""
Generate an HTML dashboard from speedtest results using Jinja2 templates.
"""

import tempfile
import webbrowser
from datetime import UTC, datetime
from typing import Any

import httpx
from jinja2 import Template

JsonResults = dict[str, Any]

TEMPLATE_URL = "https://raw.githubusercontent.com/takitsu21/speedtest/refs/heads/main/templates/dashboard.j2"


def _prepare_template_data(data: JsonResults) -> JsonResults:
    """Prepare data for the template."""
    now_utc = data.get("timestamp", datetime.now(UTC))
    return {
        "download": data.get("download", {}),
        "upload": data.get("upload", {}),
        "metadata": data.get("metadata", {}),
        "timestamp": now_utc.strftime("%A, %d %B %Y at %H:%M:%S UTC"),
    }


def _generate_dashboard(data: JsonResults) -> str:
    """Generate HTML dashboard from speedtest data using Jinja2 template."""
    # Set up Jinja2 environment
    template_raw_github = httpx.get(TEMPLATE_URL).text
    template = Template(template_raw_github)

    # Render template with data
    return template.render(**_prepare_template_data(data))


def webbrowser_open_dashboard(data: JsonResults):
    # Load test results
    html = _generate_dashboard(data)

    # Create a temporary file
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as tmp:
        tmp.write(html)
        temp_path = tmp.name

    # Open in new tab web browser
    webbrowser.open(f"file://{temp_path}", new=2)
