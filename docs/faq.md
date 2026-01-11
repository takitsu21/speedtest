# FAQ & Troubleshooting

Common questions and solutions for **speedtest-cli**.

## General Questions

### What is speedtest-cli?

speedtest-cli is a command-line tool for testing your internet connection speed. It uses Cloudflare's global network infrastructure to measure download/upload speeds, latency, jitter, and other network metrics.

### How accurate is speedtest-cli?

speedtest-cli provides accurate measurements when:

- You're connected via Ethernet (Wi-Fi adds variability)
- No other applications are using bandwidth
- Tests are run to nearby Cloudflare servers
- Adequate test file sizes are used

Results may vary slightly from other speed test tools due to different testing methodologies and server locations.

### Which servers does speedtest-cli use?

speedtest-cli uses Cloudflare's global network (speed.cloudflare.com). It automatically connects to the nearest Cloudflare edge server for optimal performance.

### Can I choose a specific server?

Currently, speedtest-cli automatically selects the nearest Cloudflare server. Manual server selection is not supported, but it's on the roadmap for future releases.

### Is my data private?

Yes. speedtest-cli:

- ✅ Uses HTTPS for all connections
- ✅ Doesn't collect personal information
- ✅ Doesn't store browsing history
- ✅ Is open source (auditable)
- ✅ Doesn't send telemetry to developers

The only data transmitted is:
- Test data to/from Cloudflare
- Your IP address (necessary for routing)

### Is speedtest-cli free?

Yes, speedtest-cli is completely free and open source under the MIT License.

### Does it work offline?

No, speedtest-cli requires an active internet connection to test your speed.

---

## Installation Issues

### Command Not Found After Installation

**Problem:** `speedtest-cli: command not found`

**Solutions:**

1. **Ensure installation path is in PATH:**
   
   ```bash
   # For pipx
   pipx ensurepath
   
   # Restart terminal or reload shell
   source ~/.bashrc  # or ~/.zshrc
   ```

2. **Verify installation:**
   
   ```bash
   pipx list  # or uv tool list
   ```

3. **Reinstall:**
   
   ```bash
   pipx uninstall speedtest-cloudflare-cli
   pipx install speedtest-cloudflare-cli
   ```

4. **Use full path:**
   
   ```bash
   ~/.local/bin/speedtest-cli
   ```

### Permission Denied During Installation

**Problem:** Permission errors with pip

**Solutions:**

1. **Use pipx or uv instead (recommended):**
   
   ```bash
   pipx install speedtest-cloudflare-cli
   ```

2. **Install for current user only:**
   
   ```bash
   pip install --user speedtest-cloudflare-cli
   ```

3. **Don't use sudo with pip** (can break system packages)

### Python Version Incompatibility

**Problem:** `Requires Python 3.9+`

**Solutions:**

1. **Check Python version:**
   
   ```bash
   python --version
   ```

2. **Install compatible Python:**
   
   ```bash
   # Ubuntu/Debian
   sudo apt install python3.12
   
   # macOS
   brew install python@3.12
   ```

3. **Use pyenv for multiple Python versions:**
   
   ```bash
   pyenv install 3.12
   pyenv global 3.12
   ```

### Package Not Found on PyPI

**Problem:** `Could not find a version that satisfies the requirement`

**Solution:**

Ensure correct package name:

```bash
# ✅ Correct
pip install speedtest-cloudflare-cli

# ❌ Wrong
pip install speedtest-cli  # Different package!
```

---

## Usage Issues

### Tests Are Very Slow

**Problem:** Speed tests take too long to complete

**Possible Causes & Solutions:**

1. **Large test files on slow connection:**
   
   ```bash
   # Use smaller file sizes
   speedtest-cli -ds 10 -us 5
   ```

2. **Network congestion:**
   - Test during off-peak hours
   - Close bandwidth-heavy applications

3. **Wi-Fi interference:**
   - Switch to Ethernet
   - Move closer to router
   - Test on 5GHz band if available

4. **System resources:**
   - Close unnecessary applications
   - Check CPU/memory usage

### Ping/Latency Test Fails

**Problem:** `Ping test failed` or very high latency

**Solutions:**

1. **ICMP may be blocked:**
   
   speedtest-cli automatically falls back to HTTP latency measurement. This is normal and expected in many environments.

2. **Grant ICMP permissions (Linux):**
   
   ```bash
   # Not recommended for security reasons
   sudo setcap cap_net_raw+ep $(which python3)
   ```

3. **Use HTTP latency instead:**
   
   HTTP latency is displayed automatically and is sufficient for most use cases.

4. **Check firewall:**
   - Ensure outbound HTTPS is allowed
   - Check for corporate firewall rules

### Connection Timeout Errors

**Problem:** `Connection timeout` or `Network unreachable`

**Solutions:**

1. **Check internet connection:**
   
   ```bash
   ping 1.1.1.1
   curl https://speed.cloudflare.com
   ```

2. **Check proxy settings:**
   
   speedtest-cli respects system proxy settings. Ensure they're correct.

3. **Disable VPN temporarily:**
   
   Some VPNs may interfere with speed tests.

4. **Check firewall:**
   
   Allow outbound HTTPS connections to *.cloudflare.com

5. **Try different network:**
   
   Test on different Wi-Fi or Ethernet connection.

### Results Differ from Other Speed Tests

**Problem:** Different results compared to Ookla, Fast.com, etc.

**Explanation:**

This is **normal** and expected because:

- **Different servers**: speedtest-cli uses Cloudflare, others use different networks
- **Different methodologies**: Varying test algorithms
- **Different times**: Network conditions change
- **Different locations**: Server distances vary

**Tips for Consistency:**

1. Run multiple tests:
   
   ```bash
   speedtest-cli --attempts 5
   ```

2. Test at same time of day
3. Use same connection type (Wi-Fi vs Ethernet)
4. Close background applications

### Why Does My Test Size Change Each Time?

**Problem:** Test size varies between runs

**Explanation:**

This is **adaptive mode** (enabled by default). It automatically adjusts test size based on your connection speed

**How It Works:**

1. Runs a quick 5MB probe test
2. Estimates your connection speed
3. Calculates optimal test size for ~7.5 second duration
4. Uses size between 1MB and 200MB

**To Disable:**

```bash
# Use fixed 30MB size
speedtest-cli --no-adaptive

# Or specify manual size
speedtest-cli --download_size 50
```

### How Do I Disable Adaptive Mode?

**Problem:** Want to use fixed test sizes

**Solutions:**

1. **Disable adaptive mode:**
   
   ```bash
   speedtest-cli --no-adaptive
   ```

2. **Specify manual sizes** (automatically disables adaptive):
   
   ```bash
   speedtest-cli --download_size 50 --upload_size 25
   ```

3. **For scripts** expecting fixed sizes:
   
   ```bash
   speedtest-cli --no-adaptive --json-output results.json
   ```

**Use Cases for Disabling:**

- Comparing results with specific test sizes
- Meeting exact test requirements
- Legacy scripts expecting fixed data volumes
- Benchmarking with consistent parameters

### What If the Probe Test Gives Wrong Results?

**Problem:** Probe test estimates incorrect speed

**Explanation:**

The probe test is intentionally short (1-2 seconds) and may not always be perfectly accurate. This is okay because:

- It's designed for a quick estimate, not precision
- Falls back to default 30MB if probe fails
- Main test still provides accurate final results
- Uses min/max boundaries (1MB - 200MB) to prevent extremes

**If Consistently Inaccurate:**

```bash
# Disable adaptive mode
speedtest-cli --no-adaptive

# Or specify exact sizes
speedtest-cli -ds 100 -us 50
```

**Note:** The probe's purpose is to optimize test duration, not to measure your exact speed. The main test provides the accurate measurement.

### Web Dashboard Won't Open

**Problem:** `--web_view` doesn't open browser

**Solutions:**

1. **Manually open HTML file:**
   
   ```bash
   # Linux/macOS
   find /tmp -name "speedtest_dashboard*.html" -exec firefox {} \;
   
   # macOS
   open "$(find /tmp -name 'speedtest_dashboard*.html' | head -1)"
   ```

2. **Check default browser:**
   
   Ensure you have a default browser configured.

3. **Permissions:**
   
   Check that /tmp is writable:
   
   ```bash
   ls -ld /tmp
   ```

4. **Try different browser:**
   
   ```bash
   # Specify browser
   BROWSER=chromium speedtest-cli --web_view
   ```

### JSON Output Not Working

**Problem:** `--json` produces no output or errors

**Solutions:**

1. **Check for syntax errors:**
   
   ```bash
   speedtest-cli --json | jq .
   ```

2. **Redirect errors:**
   
   ```bash
   speedtest-cli --json 2>&1 | tee output.log
   ```

3. **Check file permissions:**
   
   ```bash
   speedtest-cli --json-output results.json
   ls -l results.json
   ```

---

## Performance Issues

### Slower Speeds Than Expected

**Problem:** Test results slower than ISP advertised speeds

**Troubleshooting Steps:**

1. **Use Ethernet connection:**
   
   Wi-Fi typically slower than wired.

2. **Test at different times:**
   
   Network congestion varies throughout day.

3. **Close bandwidth-heavy apps:**
   - Stop downloads/uploads
   - Pause cloud sync (Dropbox, Google Drive)
   - Close streaming services
   - Disable auto-updates

4. **Restart router/modem:**
   
   Power cycle your network equipment.

5. **Check for ISP issues:**
   
   Contact ISP if consistently slow.

6. **Test on different devices:**
   
   Isolate whether issue is device-specific.

7. **Check system resources:**
   
   ```bash
   top  # or htop
   ```

8. **Disable QoS:**
   
   Quality of Service settings may limit speed.

### High Jitter Values

**Problem:** Jitter is high (> 30ms)

**Causes & Solutions:**

1. **Wi-Fi interference:**
   - Switch to Ethernet
   - Change Wi-Fi channel
   - Move closer to router

2. **Network congestion:**
   - Test during off-peak hours
   - Close bandwidth-heavy applications

3. **ISP issues:**
   - Contact ISP if persistent
   - Check for service outages

4. **Router issues:**
   - Restart router
   - Update router firmware
   - Replace old router

### High Ping Latency

**Problem:** Ping is high (> 100ms)

**Possible Causes:**

1. **Geographic distance to server:**
   - Normal if far from Cloudflare edge
   - Check with `metadata.colo`

2. **Network routing:**
   - ISP routing inefficiency
   - Use traceroute to diagnose

3. **VPN/Proxy:**
   - Adds latency
   - Test without VPN

4. **Wi-Fi:**
   - Switch to Ethernet
   - Reduce interference

---

## Docker/Container Issues

### Cannot Pull Docker Image

**Problem:** `Error response from daemon: pull access denied`

**Solutions:**

1. **Use correct image name:**
   
   ```bash
   docker pull ghcr.io/takitsu21/speedtest:latest
   ```

2. **Check network connectivity:**
   
   ```bash
   ping ghcr.io
   ```

3. **Retry pull:**
   
   ```bash
   docker pull --quiet ghcr.io/takitsu21/speedtest:latest
   ```

### Container Doesn't Show Output

**Problem:** Docker container runs but no output

**Solutions:**

1. **Use -it flags:**
   
   ```bash
   docker run --rm -it ghcr.io/takitsu21/speedtest:latest
   ```

2. **Check logs:**
   
   ```bash
   docker logs <container-id>
   ```

3. **Run with shell:**
   
   ```bash
   docker run --rm -it ghcr.io/takitsu21/speedtest:latest sh
   speedtest-cli
   ```

### Docker Permission Denied (Linux)

**Problem:** `permission denied while trying to connect to Docker daemon`

**Solutions:**

1. **Add user to docker group:**
   
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Use Podman (rootless):**
   
   ```bash
   podman run --rm -it ghcr.io/takitsu21/speedtest:latest
   ```

3. **Use sudo (not recommended):**
   
   ```bash
   sudo docker run --rm -it ghcr.io/takitsu21/speedtest:latest
   ```

---

## API/Library Usage Issues

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'speedtest_cloudflare_cli'`

**Solutions:**

1. **Verify installation:**
   
   ```bash
   pip list | grep speedtest
   ```

2. **Install package:**
   
   ```bash
   pip install speedtest-cloudflare-cli
   ```

3. **Check Python path:**
   
   ```python
   import sys
   print(sys.path)
   ```

4. **Use virtual environment:**
   
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install speedtest-cloudflare-cli
   ```

### Type Checking Errors

**Problem:** mypy shows type errors

**Solution:**

Install type stubs if needed:

```bash
pip install types-httpx
```

The library includes type hints, so most IDEs will have proper autocomplete.

---

## Platform-Specific Issues

### Windows Issues

**Problem:** Various Windows-specific issues

**Solutions:**

1. **Use Windows Terminal:**
   
   Download from Microsoft Store for best experience.

2. **PowerShell encoding:**
   
   ```powershell
   [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
   ```

3. **Path issues:**
   
   Add Python Scripts directory to PATH:
   ```
   C:\Users\YourName\AppData\Local\Programs\Python\Python312\Scripts
   ```

4. **ICMP permissions:**
   
   Usually available by default on Windows.

### macOS Issues

**Problem:** macOS-specific issues

**Solutions:**

1. **System Integrity Protection:**
   
   No special configuration needed.

2. **Homebrew Python:**
   
   Use pipx or uv to avoid conflicts.

3. **Terminal permissions:**
   
   Grant Terminal full disk access in System Preferences if needed.

### Linux Issues

**Problem:** Linux-specific issues

**Solutions:**

1. **ICMP permissions:**
   
   ```bash
   # Grant capabilities (optional)
   sudo setcap cap_net_raw+ep $(which python3)
   ```

2. **Snap/Flatpak isolation:**
   
   Use native installation instead.

3. **SELinux:**
   
   May need to adjust policies in rare cases.

---

## Comparing with Other Tools

### vs. Ookla Speedtest

**Differences:**

- **Backend**: Cloudflare vs Ookla servers
- **Open Source**: Yes vs No
- **CLI-first**: Yes vs GUI-first
- **Privacy**: High vs Medium

**When to use speedtest-cli:**
- Command-line workflows
- Automation/scripting
- Privacy concerns
- Cloudflare infrastructure testing

**When to use Ookla:**
- Need server selection
- Prefer GUI
- ISP uses Ookla for official tests

### vs. Fast.com

**Differences:**

- **Backend**: Cloudflare vs Netflix CDN
- **CLI**: Native vs Web-only
- **Metrics**: Comprehensive vs Basic
- **Automation**: Easy vs Difficult

**When to use speedtest-cli:**
- More detailed metrics needed
- CLI automation required
- JSON output needed

**When to use Fast.com:**
- Quick browser test
- Netflix streaming quality

---

## Getting More Help

### Check Documentation

- **[Installation Guide](installation.md)** - Setup help
- **[Usage Guide](usage.md)** - CLI options
- **[Features](features.md)** - Capabilities
- **[API Reference](api-reference.md)** - Library usage

### Report Issues

If you've found a bug:

1. Check [existing issues](https://github.com/takitsu21/speedtest/issues)
2. Create a new issue with:
   - OS and Python version
   - speedtest-cli version
   - Steps to reproduce
   - Error messages
   - Expected vs actual behavior

### Ask Questions

- **[GitHub Discussions](https://github.com/takitsu21/speedtest/discussions)** - Ask questions
- **[GitHub Issues](https://github.com/takitsu21/speedtest/issues)** - Report bugs

### Enable Debug Output

For troubleshooting, run with verbose Python logging:

```bash
python -m speedtest_cloudflare_cli.main --help
```

---

## Common Error Messages

### "Network error: Could not connect to speed.cloudflare.com"

**Cause:** Cannot reach Cloudflare servers

**Solution:**
1. Check internet connection
2. Check firewall settings
3. Try with VPN disabled
4. Verify DNS resolution: `nslookup speed.cloudflare.com`

### "Permission denied: Cannot create file"

**Cause:** No write permissions for output file

**Solution:**
```bash
# Check permissions
ls -la /path/to/output/

# Use writable location
speedtest-cli --json-output ~/results.json
```

### "ModuleNotFoundError"

**Cause:** Package not installed or wrong environment

**Solution:**
```bash
# Verify installation
pip show speedtest-cloudflare-cli

# Reinstall
pip install --force-reinstall speedtest-cloudflare-cli
```

### "Command 'speedtest-cli' not found"

**Cause:** Installation path not in PATH

**Solution:**
See [Command Not Found](#command-not-found-after-installation) above.

---

## Tips for Best Results

### Optimize Test Accuracy

1. **Use Ethernet** instead of Wi-Fi
2. **Close all applications** using bandwidth
3. **Run multiple tests** with `--attempts 3`
4. **Test at different times** to see variance
5. **Restart router** before important tests

### Automation Best Practices

1. **Use silent mode** in scripts
2. **Export to JSON** for parsing
3. **Don't test too frequently** (respect bandwidth)
4. **Handle errors gracefully** in scripts
5. **Log results** for historical tracking

### Performance Tuning

1. **Adjust test sizes** based on connection speed
2. **Use download-only** for quick tests
3. **Enable silent mode** to reduce overhead
4. **Run from containers** for isolation

---

Still have questions? [Open a discussion](https://github.com/takitsu21/speedtest/discussions) on GitHub!
