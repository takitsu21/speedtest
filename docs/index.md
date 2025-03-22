# speedtest-cli

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/speedtest-cli-cloudlfare)
[![Release](https://img.shields.io/github/v/release/takitsu21/speedtest)](https://img.shields.io/github/v/release/takitsu21/speedtest)
[![test](https://github.com/takitsu21/speedtest/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/takitsu21/speedtest/actions/workflows/test.yml)
[![Build status](https://img.shields.io/github/actions/workflow/status/takitsu21/speedtest/deploy.yml?branch=main)](https://github.com/takitsu21/speedtest/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/takitsu21/speedtest)](https://img.shields.io/github/commit-activity/m/takitsu21/speedtest)
[![License](https://img.shields.io/github/license/takitsu21/speedtest)](https://img.shields.io/github/license/takitsu21/speedtest)

Speed CLI tool to test your network connectivity


## Installation

I strongly recommend to use [pipx](https://github.com/pypa/pipx/tree/main) or [uv](https://github.com/astral-sh/uv) to install this tool.
These tools will install the package in an isolated environment and will not interfere with your system packages.

### Using pipx
```bash
pipx install speedtest-cloudflare-cli
```

### Using uv
```bash
uv tool install speedtest-cloudflare-cli
```

### Using pip
> [!WARNING]
>
> It is not recommended to install this package using pip. It will install the package in your system packages and may interfere with other packages.

```bash
pip install speedtest-cloudflare-cli
```

## Usage

Run the following command to test your internet speed.

```bash
speedtest-cli
```

For more information, run the --help command.
```bash
speedtest-cli --help
```

## Running in a container

> [!WARNING]
>
> You may encounter permission issues when running the container due to ping and other network commands. To avoid this, you can run the container with the `--privileged` flag.

### Using Podman

```bash
podman run --rm -it takizz21/speedtest:latest
```

### Using Docker

```bash
docker run --rm -it takizz21/speedtest:latest
```
