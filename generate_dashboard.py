#!/usr/bin/env python3
"""
Generate an HTML dashboard from speedtest results using Jinja2 templates.
"""
import json
from datetime import datetime, timezone
from typing import Any
import webbrowser

from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_test_results(filepath: str = 'test.json') -> dict[str, Any]:
    """Load speedtest results from a JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def prepare_template_data(data: dict[str, Any]) -> dict[str, Any]:
    """Prepare data for the template."""
    # Get current timestamp if not in data
    timestamp = data.get('timestamp', datetime.now(timezone.utc).isoformat())
    
    return {
        'download': data.get('download', {}),
        'upload': data.get('upload', {}),
        'metadata': data.get('metadata', {}),
        'timestamp': timestamp
    }


def generate_dashboard(data: dict[str, Any]) -> str:
    """Generate HTML dashboard from speedtest data using Jinja2 template."""
    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # Add custom filters
    env.filters['format_speed'] = lambda x: f"{float(x or 0):.2f}"
    env.filters['format_latency'] = lambda x: f"{float(x or 0):.1f}"
    
    # Get template
    template = env.get_template('dashboard.j2')
    
    # Render template with data
    return template.render(**prepare_template_data(data))

def main():
    # Load test results
    try:
        data = load_test_results()
    except FileNotFoundError:
        print("Error: test.json not found. Please run a speedtest first.")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in test.json - {str(e)}")
        return 1
    
    # Generate and open HTML in browser
    try:
        html = generate_dashboard(data)
        
        # Create a temporary file
        import tempfile
        import webbrowser
        
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as tempfile:
            tempfile.write(html)
            temp_path = tempfile.name
        
        # Open in default web browser
        webbrowser.open(f'file://{temp_path}', new=2)
        
        print(f"Dashboard opened in browser (temporary file: {temp_path})")
        return 0
    except Exception as e:
        print(f"Error generating dashboard: {str(e)}")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
