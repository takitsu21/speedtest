#!/usr/bin/env python3
"""
Generate an HTML dashboard from speedtest results using Jinja2 templates.
"""

import tempfile
import webbrowser
from datetime import datetime, timezone
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

JsonResults = dict[str, Any]

TEMPLATES_DIRECTORY = "templates"
TEMPLATE_FILE = "dashboard.j2"


def _prepare_template_data(data: JsonResults) -> JsonResults:
    """Prepare data for the template."""
    now_utc = data.get("timestamp", datetime.now(timezone.utc))
    return {
        "download": data.get("download", {}),
        "upload": data.get("upload", {}),
        "metadata": data.get("metadata", {}),
        "timestamp": now_utc.strftime("%A, %d %B %Y at %H:%M:%S UTC"),
    }


def _generate_dashboard(data: JsonResults) -> str:
    """Generate HTML dashboard from speedtest data using Jinja2 template."""
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIRECTORY), autoescape=select_autoescape(["html", "xml"]))

    # Add custom filters
    env.filters["format_speed"] = lambda x: f"{float(x or 0):.2f}"
    env.filters["format_latency"] = lambda x: f"{float(x or 0):.1f}"

    # Get template
    template = env.get_template(TEMPLATE_FILE)

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
