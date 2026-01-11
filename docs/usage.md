# Usage Guide

This guide covers all the command-line options and common usage patterns for **speedtest-cli**.

## Basic Usage

Run a complete speed test with default settings:

```bash
speedtest-cli
```

This will:

1. Detect your network information (IP, ISP, location)
2. Measure ping latency and jitter
3. Test download speed
4. Test upload speed
5. Display results in a formatted table

## Command-Line Options

### General Options

#### `--version`

Display the version of speedtest-cli and exit.

```bash
speedtest-cli --version
```

**Output:**
```
speedtest-cli, version 1.x.x
```

#### `--help`

Show help message with all available options.

```bash
speedtest-cli --help
```

---

### Test Selection Options

#### `--download` / `-d`

Run **only** the download speed test.

```bash
speedtest-cli --download
# or
speedtest-cli -d
```

**Use Case:** Quick check of your download speed without waiting for upload test.

**Example Output:**
```
Download: 150.5 Mbps
Ping: 12 ms
Jitter: 2 ms
```

#### `--upload` / `-u`

Run **only** the upload speed test.

```bash
speedtest-cli --upload
# or
speedtest-cli -u
```

**Use Case:** Test upload speed for video conferencing or file uploads.

**Example Output:**
```
Upload: 45.3 Mbps
Ping: 12 ms
Jitter: 2 ms
```

!!! tip "Combine Both"
    You can combine both flags to run both tests (same as default):
    ```bash
    speedtest-cli -d -u
    ```

---

### Test Configuration Options

#### `--download_size` / `-ds`

Specify the download size in megabytes (MB).

```bash
speedtest-cli --download_size 50
# or
speedtest-cli -ds 50
```

**Default:** Varies based on implementation  
**Use Case:** 
- Smaller size for quick tests on slow connections
- Larger size for more accurate measurements on fast connections

**Example:**
```bash
# Quick test with 10 MB download
speedtest-cli -d -ds 10

# Thorough test with 100 MB download
speedtest-cli -d -ds 100
```

#### `--upload_size` / `-us`

Specify the upload size in megabytes (MB).

```bash
speedtest-cli --upload_size 25
# or
speedtest-cli -us 25
```

**Default:** Varies based on implementation  
**Use Case:** Similar to download_size, adjust based on your connection speed.

**Example:**
```bash
# Test upload with 5 MB
speedtest-cli -u -us 5
```

#### `--attempts` / `-a`

Specify the number of test attempts.

```bash
speedtest-cli --attempts 3
# or
speedtest-cli -a 3
```

**Default:** 1  
**Use Case:** Run multiple attempts to get average results and reduce variance.

**Example:**
```bash
# Run 5 attempts for more reliable results
speedtest-cli -a 5
```

#### `--adaptive` / `--no-adaptive`

Enable or disable adaptive test sizing based on connection speed.

```bash
# Adaptive mode is enabled by default
speedtest-cli

# Explicitly disable adaptive mode
speedtest-cli --no-adaptive
```

**Default:** Enabled  
**Use Case:** 
- **Enabled (default)**: Automatically adjusts test size for optimal duration
- **Disabled**: Uses fixed 30MB test size (legacy behavior)

**How It Works:**
1. Runs a quick 5MB probe test to estimate your speed
2. Calculates optimal test size for ~7.5 second duration
3. Uses adaptive size (between 1MB and 200MB)

**Example:**
```bash
# Let adaptive mode optimize test size (default)
speedtest-cli

# Output:
# Running probe test to detect connection speed...
# ✓ Detected speed: ~56.1 Mbps
# Adaptive mode: Using 53MB for download test

# Disable adaptive mode to use fixed 30MB
speedtest-cli --no-adaptive

# Note: Manual size specification automatically disables adaptive
speedtest-cli --download_size 50  # Uses exactly 50MB, adaptive disabled
```

**Benefits:**
- **Faster tests** on slow connections (no more waiting for 30MB on 1 Mbps!)
- **More accurate** on fast connections (uses larger test sizes)
- **Consistent duration** (~7-10 seconds regardless of connection speed)

---

### Output Options

#### `--json`

Output results in JSON format to stdout.

```bash
speedtest-cli --json
```

**Example Output:**
```json
{
  "download": 150.5,
  "upload": 45.3,
  "ping": 12,
  "jitter": 2,
  "http_latency": 15,
  "metadata": {
    "ip": "203.0.113.45",
    "isp": "Example ISP",
    "city": "San Francisco",
    "region": "California",
    "country": "US",
    "loc": "37.7749,-122.4194",
    "colo": "SFO"
  }
}
```

**Use Case:** 
- Automation and scripting
- Integration with monitoring systems
- Processing results programmatically

**Example:**
```bash
# Parse JSON with jq
speedtest-cli --json | jq '.download'

# Save to variable in bash
DOWNLOAD_SPEED=$(speedtest-cli --json | jq -r '.download')
echo "Download speed: $DOWNLOAD_SPEED Mbps"
```

#### `--json-output`

Save JSON results to a file.

```bash
speedtest-cli --json-output results.json
```

**Use Case:**
- Logging test results over time
- Storing results for later analysis
- Integration with data analysis tools

**Example:**
```bash
# Save with timestamp
speedtest-cli --json-output "speedtest_$(date +%Y%m%d_%H%M%S).json"

# Append to log file (requires manual JSON array handling)
speedtest-cli --json-output daily_results.json
```

#### `--silent`

Run in silent mode with minimal output.

```bash
speedtest-cli --silent
```

**Use Case:**
- Running in background scripts
- Cron jobs
- When you only care about exit codes or JSON output

**Example:**
```bash
# Combine with JSON output for automation
speedtest-cli --silent --json-output /var/log/speedtest.json

# Use in scripts
if speedtest-cli --silent; then
    echo "Speed test completed successfully"
fi
```

#### `--web_view`

Open results in a web browser with an interactive dashboard.

```bash
speedtest-cli --web_view
```

**Use Case:**
- Visual representation of results
- Sharing results with others
- Seeing location on a map

See the [Web Dashboard Guide](web-dashboard.md) for more details.

---

## Common Usage Patterns

### Quick Download Test

Test only download speed with a smaller file:

```bash
speedtest-cli -d -ds 25
```

### Complete Test with JSON Export

Run a full test and save results:

```bash
speedtest-cli --json-output ~/speedtest_results.json
```

### Multiple Attempts for Accuracy

Run 5 attempts to get average results:

```bash
speedtest-cli -a 5
```

### Automated Monitoring

Silent mode with JSON output for scripts:

```bash
speedtest-cli --silent --json-output /tmp/speedtest.json
```

### Visual Dashboard

Run test and open in browser:

```bash
speedtest-cli --web_view
```

### Custom Download and Upload Sizes

Optimize test duration for your connection:

```bash
# For slow connections (< 10 Mbps)
speedtest-cli -ds 10 -us 5

# For fast connections (> 100 Mbps)
speedtest-cli -ds 100 -us 50
```

### Upload Only Test

Test upload without download:

```bash
speedtest-cli -u -us 25
```

---

## Understanding the Output

### Console Output

When you run speedtest-cli without `--json` or `--silent`, you'll see:

#### 1. Connection Information
```
IP: 203.0.113.45
ISP: Example ISP
Location: San Francisco, California, US
Cloudflare Datacenter: SFO
```

#### 2. Progress Bars

Real-time progress during tests:
```
Downloading... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
Uploading...   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
```

#### 3. Results Table

```
╭─────────────────┬──────────╮
│ Metric          │ Value    │
├─────────────────┼──────────┤
│ Download        │ 150.5 Mbps│
│ Upload          │ 45.3 Mbps │
│ Ping            │ 12 ms    │
│ Jitter          │ 2 ms     │
│ HTTP Latency    │ 15 ms    │
╰─────────────────┴──────────╯
```

### Metrics Explained

- **Download**: Download speed in megabits per second (Mbps)
- **Upload**: Upload speed in megabits per second (Mbps)
- **Ping**: Round-trip time to Cloudflare servers in milliseconds (ms)
- **Jitter**: Variation in ping latency in milliseconds (ms)
- **HTTP Latency**: Time to establish HTTP connection in milliseconds (ms)

### Exit Codes

- `0`: Test completed successfully
- `1`: Test failed (network error, timeout, etc.)

---

## Advanced Examples

### Cron Job for Daily Monitoring

Add to crontab (`crontab -e`):

```bash
# Run speed test daily at 2 AM
0 2 * * * /usr/local/bin/speedtest-cli --silent --json-output /var/log/speedtest/$(date +\%Y\%m\%d).json
```

### Bash Script for Logging

```bash
#!/bin/bash

LOG_DIR="$HOME/speedtest_logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="$LOG_DIR/speedtest_$TIMESTAMP.json"

echo "Running speed test..."
if speedtest-cli --json-output "$OUTPUT_FILE"; then
    echo "Results saved to $OUTPUT_FILE"
    
    # Parse and display key metrics
    DOWNLOAD=$(jq -r '.download' "$OUTPUT_FILE")
    UPLOAD=$(jq -r '.upload' "$OUTPUT_FILE")
    
    echo "Download: $DOWNLOAD Mbps"
    echo "Upload: $UPLOAD Mbps"
else
    echo "Speed test failed!"
    exit 1
fi
```

### Python Integration

```python
import subprocess
import json

# Run speedtest and capture JSON output
result = subprocess.run(
    ['speedtest-cli', '--json'],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    data = json.loads(result.stdout)
    print(f"Download: {data['download']} Mbps")
    print(f"Upload: {data['upload']} Mbps")
    print(f"Ping: {data['ping']} ms")
else:
    print("Speed test failed!")
```

### Performance Alert Script

```bash
#!/bin/bash

# Run test and get download speed
DOWNLOAD=$(speedtest-cli --json --silent | jq -r '.download')

# Alert if speed is below threshold
THRESHOLD=50
if (( $(echo "$DOWNLOAD < $THRESHOLD" | bc -l) )); then
    echo "WARNING: Download speed is ${DOWNLOAD} Mbps (below ${THRESHOLD} Mbps)"
    # Send notification (example using notify-send)
    notify-send "Slow Internet" "Speed is only ${DOWNLOAD} Mbps"
fi
```

---

## Tips and Best Practices

### 1. Minimize Network Activity

Close bandwidth-heavy applications during testing:
- Stop downloads/uploads
- Pause streaming services
- Close cloud sync applications (Dropbox, Google Drive, etc.)

### 2. Use Wired Connection

For most accurate results:
- Use Ethernet instead of Wi-Fi when possible
- Test directly from the device connected to your modem/router

### 3. Multiple Tests

Run several tests at different times:
```bash
# Morning, afternoon, evening tests
for i in {1..3}; do
    speedtest-cli --json-output "test_$i.json"
    sleep 3600  # Wait 1 hour between tests
done
```

### 4. Interpret Results

- **Download/Upload**: Should match your ISP's advertised speeds
- **Ping**: Lower is better (< 20ms is excellent, < 50ms is good)
- **Jitter**: Lower is better (< 5ms is good for gaming/VoIP)

### 5. Troubleshooting Slow Speeds

If results are slower than expected:
1. Test at different times of day
2. Test with wired connection
3. Restart your modem/router
4. Contact your ISP if consistently slow

---

## Next Steps

- **[Features](features.md)** - Learn about all capabilities
- **[Web Dashboard](web-dashboard.md)** - Explore the interactive dashboard
- **[API Reference](api-reference.md)** - Use speedtest-cli as a Python library
- **[FAQ](faq.md)** - Common questions and solutions
