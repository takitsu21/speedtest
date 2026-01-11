# Installation

This guide covers all the ways to install **speedtest-cli** on your system.

## System Requirements

- **Python**: 3.9, 3.10, 3.11, 3.12, or 3.13
- **Operating Systems**: Linux, macOS, Windows
- **Network**: Internet connection with ICMP (ping) access (optional but recommended)

## Recommended Installation Methods

We strongly recommend using **pipx** or **uv** to install speedtest-cli. These tools create isolated environments for each application, preventing dependency conflicts with your system packages.

### Using pipx

[pipx](https://github.com/pypa/pipx) is a tool to help you install and run end-user applications written in Python. It's similar to macOS's brew, JavaScript's npx, and Linux's apt/yum.

#### Install pipx

If you don't have pipx installed:

=== "Linux"
    ```bash
    # Ubuntu/Debian
    sudo apt update
    sudo apt install pipx
    pipx ensurepath
    
    # Fedora
    sudo dnf install pipx
    pipx ensurepath
    
    # Arch Linux
    sudo pacman -S python-pipx
    pipx ensurepath
    ```

=== "macOS"
    ```bash
    brew install pipx
    pipx ensurepath
    ```

=== "Windows"
    ```powershell
    # Using scoop
    scoop install pipx
    pipx ensurepath
    
    # Or using pip
    python -m pip install --user pipx
    python -m pipx ensurepath
    ```

#### Install speedtest-cli

```bash
pipx install speedtest-cloudflare-cli
```

#### Verify Installation

```bash
speedtest-cli --version
```

### Using uv

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver written in Rust. It's the fastest way to install Python packages.

#### Install uv

```bash
# Linux and macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Install speedtest-cli

```bash
uv tool install speedtest-cloudflare-cli
```

#### Verify Installation

```bash
speedtest-cli --version
```

## Alternative Installation Methods

### Using pip

!!! warning "Not Recommended"
    Installing with pip directly can interfere with your system's Python packages. Use pipx or uv instead.

If you still want to use pip:

```bash
# Install for current user only (recommended if using pip)
pip install --user speedtest-cloudflare-cli

# Or install system-wide (requires admin/sudo)
sudo pip install speedtest-cloudflare-cli
```

### From Source

For developers who want to contribute or test the latest changes:

#### Clone the Repository

```bash
git clone https://github.com/takitsu21/speedtest.git
cd speedtest
```

#### Install with uv (Recommended for Development)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync all dependencies including dev dependencies
uv sync

# Run from source
uv run speedtest-cli
```

#### Install with pip

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run
speedtest-cli
```

### Using Container Images

See the [Docker Guide](docker.md) for running speedtest-cli in containers.

## Post-Installation

### Verify Installation

After installation, verify that speedtest-cli is correctly installed:

```bash
speedtest-cli --version
```

You should see output like:
```
speedtest-cli, version 1.x.x
```

### Run Your First Speed Test

```bash
speedtest-cli
```

This will run a complete speed test and display results in your terminal.

### Check Available Options

```bash
speedtest-cli --help
```

## Upgrading

### With pipx

```bash
pipx upgrade speedtest-cloudflare-cli
```

### With uv

```bash
uv tool upgrade speedtest-cloudflare-cli
```

### With pip

```bash
pip install --upgrade speedtest-cloudflare-cli
```

## Uninstalling

### With pipx

```bash
pipx uninstall speedtest-cloudflare-cli
```

### With uv

```bash
uv tool uninstall speedtest-cloudflare-cli
```

### With pip

```bash
pip uninstall speedtest-cloudflare-cli
```

## Troubleshooting

### Command Not Found

If you get a "command not found" error after installation:

1. **Ensure the installation directory is in your PATH**:
   
   ```bash
   # For pipx
   pipx ensurepath
   
   # For uv
   # The installer usually adds this automatically
   ```

2. **Restart your terminal** or reload your shell configuration:
   
   ```bash
   # Bash
   source ~/.bashrc
   
   # Zsh
   source ~/.zshrc
   ```

3. **Check the installation location**:
   
   ```bash
   # For pipx
   pipx list
   
   # For uv
   uv tool list
   ```

### Permission Denied

If you get permission errors:

- **Don't use sudo with pipx or uv** - they install to your user directory
- **Use `--user` flag with pip**: `pip install --user speedtest-cloudflare-cli`
- **Use a virtual environment** instead of system-wide installation

### Python Version Issues

If you have multiple Python versions installed:

```bash
# Specify Python version explicitly
pipx install --python python3.12 speedtest-cloudflare-cli

# Or with uv
uv tool install --python 3.12 speedtest-cloudflare-cli
```

### Network Issues During Installation

If installation fails due to network issues:

```bash
# Retry with increased timeout
pip install --timeout 300 speedtest-cloudflare-cli

# Or use a different index
pip install --index-url https://pypi.org/simple speedtest-cloudflare-cli
```

## Platform-Specific Notes

### Linux

- **ICMP Permissions**: For accurate ping measurements, you may need to set capabilities:
  
  ```bash
  sudo setcap cap_net_raw+ep $(which python3)
  ```
  
  Or run with sudo (not recommended for regular use).

### macOS

- **Homebrew Users**: If you have issues with Python from Homebrew, try using pipx or uv
- **System Integrity Protection**: No special configuration needed

### Windows

- **Windows Terminal**: For best visual experience, use [Windows Terminal](https://aka.ms/terminal)
- **PowerShell**: Works in PowerShell, CMD, and Git Bash
- **ICMP Permissions**: Usually available by default on Windows

## Next Steps

- **[Usage Guide](usage.md)** - Learn all the command-line options
- **[Features](features.md)** - Explore what speedtest-cli can do
- **[Web Dashboard](web-dashboard.md)** - Use the interactive dashboard
- **[FAQ](faq.md)** - Common questions and solutions
