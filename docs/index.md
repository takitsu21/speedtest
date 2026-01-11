<p align="center">
  <img src="assets/icon.png" alt="Speed Test Icon" width="200"/>
</p>

<h1 align="center">speedtest-cli</h1>

<p align="center">
  <strong>A fast, beautiful command-line tool for testing your network speed</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/pyversions/speedtest-cloudflare-cli" alt="Python Version"/>
  <img src="https://img.shields.io/pypi/v/speedtest-cloudflare-cli" alt="PyPI Version"/>
  <a href="https://github.com/takitsu21/speedtest/releases"><img src="https://img.shields.io/github/v/release/takitsu21/speedtest" alt="Release"/></a>
  <a href="https://github.com/takitsu21/speedtest/actions/workflows/test.yml"><img src="https://github.com/takitsu21/speedtest/actions/workflows/test.yml/badge.svg?branch=main" alt="Tests"/></a>
  <a href="https://github.com/takitsu21/speedtest/blob/main/LICENSE"><img src="https://img.shields.io/github/license/takitsu21/speedtest" alt="License"/></a>
</p>

---

## Overview

**speedtest-cli** is a modern, feature-rich command-line tool that measures your internet connection speed with style. Built on Cloudflare's global infrastructure, it provides accurate speed measurements along with detailed network metrics, all displayed in a beautiful terminal interface.

![SpeedTest Video demo](assets/demo.gif)

## Key Features

- **Accurate Speed Testing** - Powered by Cloudflare's global network for reliable measurements
- **Comprehensive Metrics** - Download/upload speeds, latency, jitter, and HTTP latency
- **Beautiful Interface** - Rich terminal output with progress bars and formatted tables
- **Web Dashboard** - Interactive HTML dashboard with maps and visualizations
- **Flexible Output** - Console display, JSON export, or silent mode for automation
- **Network Details** - ISP information, location data, IPv4/IPv6 support
- **Cross-Platform** - Works on Linux, macOS, and Windows
- **Container Ready** - Available as Docker/Podman image

![SpeedTest dashboard](assets/web_view.png)

## Quick Start

### Installation

Install using [pipx](installation.md#using-pipx) (recommended) or [uv](installation.md#using-uv):

```bash
# Using pipx
pipx install speedtest-cloudflare-cli

# Using uv
uv tool install speedtest-cloudflare-cli
```

See the [Installation Guide](installation.md) for more options.

### Basic Usage

Run a complete speed test:

```bash
speedtest-cli
```

![Speedtest output](assets/speedtest_output.png)

Open results in an interactive web dashboard:

```bash
speedtest-cli --web_view
```

Export results to JSON:

```bash
speedtest-cli --json-output results.json
```

See the [Usage Guide](usage.md) for all available options and examples.

## Why speedtest-cli?

- **Cloudflare Infrastructure** - Leverage one of the world's largest and fastest networks
- **Privacy Focused** - No account required, no tracking, open source
- **Modern Python** - Built with type hints, async support, and modern best practices
- **Beautiful UX** - Powered by [Rich](https://github.com/Textualize/rich) for stunning terminal output
- **Automation Friendly** - JSON output and silent mode for scripts and monitoring

## Quick Links

- **[Installation](installation.md)** - Detailed installation instructions for all platforms
- **[Usage Guide](usage.md)** - Complete guide to all CLI options and features
- **[Features](features.md)** - In-depth look at capabilities and metrics
- **[Web Dashboard](web-dashboard.md)** - Interactive dashboard features
- **[Docker](docker.md)** - Running in containers
- **[API Reference](api-reference.md)** - Using as a Python library
- **[Contributing](contributing.md)** - Development setup and guidelines
- **[FAQ](faq.md)** - Common questions and troubleshooting

## Running in a Container

Pre-built container images are available:

```bash
# Using Podman
podman run --rm -it ghcr.io/takitsu21/speedtest:latest

# Using Docker
docker run --rm -it ghcr.io/takitsu21/speedtest:latest
```

See the [Docker Guide](docker.md) for more details.

## Example Output

When you run `speedtest-cli`, you'll see:

1. **Connection Information** - Your IP, ISP, and location
2. **Progress Tracking** - Real-time progress bars for downloads/uploads
3. **Results Table** - Formatted table with all metrics:
   - Download speed (Mbps)
   - Upload speed (Mbps)
   - Ping latency (ms)
   - Jitter (ms)
   - HTTP latency (ms)

## Support

- **Documentation** - You're reading it!
- **Issues** - [GitHub Issues](https://github.com/takitsu21/speedtest/issues)
- **Discussions** - [GitHub Discussions](https://github.com/takitsu21/speedtest/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/takitsu21/speedtest/blob/main/LICENSE) file for details.
