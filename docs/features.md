# Features

**speedtest-cli** offers a comprehensive suite of features for testing and analyzing your network connection. This page provides an in-depth look at all capabilities.

## Speed Testing

### Download Speed Test

Measures how fast data can be downloaded from the internet to your device.

**How It Works:**

1. Connects to Cloudflare's speed testing infrastructure
2. Downloads data in chunks over HTTP
3. Measures throughput in real-time
4. Calculates average speed in Mbps (megabits per second)

**Features:**

- Real-time progress bars
- Configurable download size (`--download_size`)
- Multiple attempt support for averaging
- HTTP streaming for accurate measurements

**Use Cases:**

- Verifying ISP advertised speeds
- Troubleshooting slow downloads
- Comparing speeds at different times
- Monitoring connection quality

**Example:**

```bash
# Download test only with 50 MB size
speedtest-cli --download --download_size 50
```

### Upload Speed Test

Measures how fast data can be uploaded from your device to the internet.

**How It Works:**

1. Generates test data locally
2. Uploads to Cloudflare servers via HTTP POST
3. Tracks upload progress
4. Calculates throughput in Mbps

**Features:**

- Configurable upload size (`--upload_size`)
- Efficient data generation
- Progress tracking
- Multiple attempts support

**Use Cases:**

- Testing video conferencing capabilities
- Verifying file upload performance
- Streaming quality assessment
- Cloud backup speed testing

**Example:**

```bash
# Upload test only with 25 MB size
speedtest-cli --upload --upload_size 25
```

---

## Network Metrics

### Ping Latency

Measures round-trip time (RTT) for packets to reach Cloudflare servers and return.

**How It Works:**

- Uses ICMP ping protocol (when available)
- Falls back to HTTP-based latency measurement
- Runs in background thread for better UX
- Measures in milliseconds (ms)

**What It Indicates:**

- **< 20ms**: Excellent (great for gaming, real-time apps)
- **20-50ms**: Good (suitable for most activities)
- **50-100ms**: Fair (may notice lag in real-time apps)
- **> 100ms**: Poor (noticeable delays)

**Use Cases:**

- Gaming performance assessment
- VoIP quality prediction
- Video conferencing suitability
- Real-time application testing

**Fallback Mechanism:**

If ICMP ping is blocked or requires privileges:
- Automatically uses HTTP latency measurement
- Ensures you always get latency data
- Slightly higher values due to HTTP overhead

### Jitter

Measures variation in ping latency over time.

**How It Works:**

- Calculates standard deviation of ping times
- Multiple ping samples analyzed
- Reported in milliseconds (ms)

**What It Indicates:**

- **< 5ms**: Excellent (stable connection)
- **5-15ms**: Good (minor variations)
- **15-30ms**: Fair (noticeable in real-time apps)
- **> 30ms**: Poor (unstable connection)

**Use Cases:**

- VoIP quality assessment
- Online gaming performance
- Video conferencing stability
- Network stability monitoring

**Impact:**

High jitter can cause:
- Choppy voice in calls
- Lag spikes in games
- Buffering in live streams
- Packet loss

### HTTP Latency

Measures time to establish HTTP connection to Cloudflare servers.

**How It Works:**

- Times the HTTP connection handshake
- Includes DNS lookup and TCP connection
- Separate from ICMP ping
- Measured in milliseconds (ms)

**What It Indicates:**

- Overall web browsing responsiveness
- API call performance
- Web application speed

**Difference from Ping:**

- **Ping**: Pure network latency (ICMP)
- **HTTP Latency**: Application-level latency (includes protocol overhead)

---

## Network Information

### IP Address Detection

Automatically detects and displays your public IP address.

**Features:**

- IPv4 detection
- IPv6 detection and support
- Displays both when available

**Example Output:**

```
IP: 203.0.113.45 (IPv4)
IPv6: 2001:0db8:85a3::8a2e:0370:7334
```

### ISP Information

Identifies your Internet Service Provider.

**Information Provided:**

- ISP name
- Autonomous System Number (ASN)
- Organization details

**Example:**

```
ISP: Example Broadband
ASN: AS12345
```

### Geolocation

Determines your geographic location based on IP address.

**Details Provided:**

- City
- Region/State
- Country
- Coordinates (latitude, longitude)

**Example:**

```
Location: San Francisco, California, US
Coordinates: 37.7749, -122.4194
```

**Privacy Note:**

All geolocation is done via Cloudflare's API. No data is stored or transmitted elsewhere.

### Cloudflare Data Center

Shows which Cloudflare edge server (colo) handled your test.

**Example:**

```
Cloudflare Datacenter: SFO
```

**Why It Matters:**

- Indicates routing efficiency
- Shows network path optimization
- Helps diagnose routing issues

---

## Output Formats

### Rich Console Output

Beautiful terminal interface with colors and formatting.

**Features:**

- Color-coded output
- Progress bars with animations
- Formatted tables
- Unicode box drawing
- Emoji indicators (connection quality)

**Powered By:**

[Rich](https://github.com/Textualize/rich) - Python library for rich terminal output

**Example:**

```bash
speedtest-cli
```

### JSON Output

Machine-readable structured data format.

**To Console:**

```bash
speedtest-cli --json
```

**To File:**

```bash
speedtest-cli --json-output results.json
```

**Schema:**

```json
{
  "download": 150.5,        // Mbps
  "upload": 45.3,           // Mbps
  "ping": 12,               // ms
  "jitter": 2,              // ms
  "http_latency": 15,       // ms
  "metadata": {
    "ip": "203.0.113.45",
    "isp": "Example ISP",
    "city": "San Francisco",
    "region": "California",
    "country": "US",
    "loc": "37.7749,-122.4194",
    "colo": "SFO",
    "asn": "AS12345"
  }
}
```

**Use Cases:**

- Automation scripts
- Data analysis
- Monitoring systems
- API integrations
- Long-term logging

### HTML Dashboard

Interactive web-based visualization of results.

**Access:**

```bash
speedtest-cli --web_view
```

**Features:**

- Interactive map with location marker
- Dark/light theme toggle
- Connection quality indicators
- Responsive design
- All metrics displayed
- Beautiful visual design
- Shareable HTML file

See [Web Dashboard](web-dashboard.md) for detailed guide.

---

## Cloudflare Infrastructure

### Why Cloudflare?

**speedtest-cli** uses Cloudflare's global network for testing:

**Advantages:**

1. **Global Coverage**: 300+ cities worldwide
2. **Low Latency**: Edge servers close to users
3. **High Capacity**: No bandwidth bottlenecks
4. **Reliability**: 99.99%+ uptime
5. **Privacy**: No account required, minimal data collection
6. **Speed**: Optimized infrastructure

### How It Works

```
Your Device → Your ISP → Internet → Cloudflare Edge → Speed Test
```

**Test Process:**

1. Your device connects to nearest Cloudflare edge server
2. Metadata retrieved (IP, location, ISP)
3. Speed tests executed using HTTP streaming
4. Results calculated locally
5. Optional dashboard generation

### Accuracy

**Factors Ensuring Accuracy:**

- Large test files to smooth out variance
- HTTP streaming for realistic measurements
- Multiple attempts support
- Cloudflare's uncongested network
- Direct measurement without middle servers

**Potential Variations:**

- Network congestion
- Wi-Fi interference
- Background applications
- Time of day
- Server load (rare with Cloudflare)

---

## Advanced Features

### Multiple Attempts

Run tests multiple times and get averaged results.

```bash
speedtest-cli --attempts 5
```

**Benefits:**

- Reduces impact of random variance
- More reliable measurements
- Identifies connection instability
- Better statistical confidence

**Use Case:**

When you need accurate measurements for reporting or diagnostics.

### Silent Mode

Run tests without visual output.

```bash
speedtest-cli --silent
```

**Features:**

- No progress bars
- No console output (except errors)
- Exit codes indicate success/failure
- Works with `--json-output`

**Use Cases:**

- Cron jobs
- Background monitoring
- Automated scripts
- Minimal logging

### Selective Testing

Test only specific aspects:

```bash
# Download only
speedtest-cli --download

# Upload only
speedtest-cli --upload

# Both (explicit)
speedtest-cli --download --upload
```

**Benefits:**

- Faster testing
- Focus on specific metrics
- Save bandwidth
- Targeted troubleshooting

### Configurable Test Sizes

Adjust data volume for your connection speed:

```bash
# Small files for slow connections
speedtest-cli -ds 10 -us 5

# Large files for fast connections
speedtest-cli -ds 100 -us 50
```

**Guidelines:**

| Connection Speed | Recommended Download Size | Recommended Upload Size |
|-----------------|--------------------------|------------------------|
| < 10 Mbps       | 10-25 MB                | 5-10 MB                |
| 10-50 Mbps      | 25-50 MB                | 10-25 MB               |
| 50-100 Mbps     | 50-100 MB               | 25-50 MB               |
| 100-500 Mbps    | 100-200 MB              | 50-100 MB              |
| > 500 Mbps      | 200+ MB                 | 100+ MB                |

### Adaptive Test Sizing

**NEW:** Automatically adjusts test sizes based on your connection speed.

**How It Works:**

1. Runs a quick 5MB probe test (takes 1-2 seconds)
2. Estimates your connection speed from probe results
3. Calculates optimal test size for ~7.5 second test duration
4. Applies min/max boundaries (1MB - 200MB)
5. Runs main test with adaptive size

**Benefits:**

- **Fast for slow connections**: 1 Mbps connection uses 1MB test (not 30MB!)
- **Accurate for fast connections**: 500 Mbps connection uses 200MB test
- **Saves time**: No more waiting for large downloads on slow connections
- **Balanced accuracy**: Tests run long enough for accurate measurements

**Enabled by Default:**

```bash
# Adaptive mode is enabled automatically
speedtest-cli

# Example output:
# Running probe test to detect connection speed...
# ✓ Detected speed: ~56.1 Mbps
# Adaptive mode: Using 53MB for download test
```

**Disable Adaptive Mode:**

```bash
# Use fixed 30MB size (legacy behavior)
speedtest-cli --no-adaptive

# Manual sizes always disable adaptive
speedtest-cli --download_size 50  # Uses exactly 50MB
```

**Example Scenarios:**

| Connection Speed | Probe Detects | Adaptive Size | Test Duration |
|-----------------|---------------|---------------|---------------|
| 1 Mbps          | ~1 Mbps       | 1 MB          | ~8 seconds    |
| 10 Mbps         | ~10 Mbps      | 9 MB          | ~7 seconds    |
| 50 Mbps         | ~50 Mbps      | 47 MB         | ~7.5 seconds  |
| 100 Mbps        | ~100 Mbps     | 94 MB         | ~7.5 seconds  |
| 500 Mbps        | ~480 Mbps     | 200 MB (max)  | ~3.2 seconds  |
| 1000 Mbps       | ~950 Mbps     | 200 MB (max)  | ~1.6 seconds  |

**When to Disable:**

- Comparing results with specific test sizes
- Meeting exact test requirements for diagnostics
- Using scripts that expect specific data volumes
- Benchmarking with consistent parameters

---

## IPv6 Support

Full support for IPv6 connections.

**Features:**

- Automatic IPv6 detection
- IPv4 and IPv6 dual-stack support
- Displays both addresses when available
- Tests over IPv6 when preferred

**Example:**

```
IPv4: 203.0.113.45
IPv6: 2001:0db8:85a3::8a2e:0370:7334
```

**Benefits:**

- Future-proof testing
- Proper IPv6 performance measurement
- Dual-stack validation

---

## Privacy and Security

### Data Collection

**What speedtest-cli Collects:**

- Your public IP address (temporary, for testing)
- ISP information (from Cloudflare)
- Geolocation (from Cloudflare)

**What It Doesn't Collect:**

- Personal information
- Browsing history
- Device details
- Persistent identifiers

### Local Processing

- All calculations done locally
- Results stored only if you use `--json-output`
- No telemetry sent to developers
- No analytics or tracking

### Open Source

- Full source code available on GitHub
- Auditable security
- Community reviewed
- Transparent operation

---

## Performance Optimization

### Tips for Accurate Results

1. **Use Wired Connection**: Ethernet is more stable than Wi-Fi
2. **Close Background Apps**: Stop downloads, updates, streaming
3. **Test Multiple Times**: Use `--attempts 3` or more
4. **Avoid Peak Hours**: Test during off-peak times
5. **Direct Connection**: Connect directly to modem when possible

### System Requirements

**Minimum:**

- Python 3.9+
- 50 MB free RAM
- Internet connection

**Recommended:**

- Python 3.12+
- 100 MB free RAM
- Wired Ethernet connection
- ICMP ping permissions

---

## Integration Capabilities

### Command-Line Scripts

Easily integrate into shell scripts:

```bash
#!/bin/bash
SPEED=$(speedtest-cli --json | jq -r '.download')
echo "Current speed: $SPEED Mbps"
```

### Python Programs

Use as a library (see [API Reference](api-reference.md)):

```python
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

test = SpeedTest()
results = test.run()
print(f"Download: {results.download} Mbps")
```

### Monitoring Systems

- Prometheus exporters
- Grafana dashboards
- Custom alerting
- Historical tracking

### CI/CD Pipelines

Monitor deployment environment network:

```yaml
- name: Test Network Speed
  run: speedtest-cli --json-output network-test.json
```

---

## Comparison with Other Tools

### vs. Ookla Speedtest

| Feature | speedtest-cli | Ookla Speedtest |
|---------|---------------|-----------------|
| Backend | Cloudflare | Ookla servers |
| Open Source | Yes | No |
| CLI Only | Yes | No (GUI available) |
| JSON Output | Yes | Limited |
| Privacy | High | Medium |
| Accounts | Not required | Optional |

### vs. Fast.com

| Feature | speedtest-cli | Fast.com |
|---------|---------------|----------|
| Backend | Cloudflare | Netflix CDN |
| CLI | Yes | Web only |
| Upload Test | Yes | Yes |
| Detailed Metrics | Yes | Basic |
| Automation | Easy | Difficult |

### vs. LibreSpeed

| Feature | speedtest-cli | LibreSpeed |
|---------|---------------|------------|
| Backend | Cloudflare | Self-hosted |
| Installation | Simple | Complex |
| Global Servers | Yes | Depends |
| Maintenance | None | Self-managed |

---

## Limitations

### Known Limitations

1. **Network Access Required**: Cannot test without internet
2. **ICMP Permissions**: May need elevated privileges for ping on some systems
3. **Cloudflare Only**: Tests only to Cloudflare servers, not other endpoints
4. **No Server Selection**: Automatically uses nearest Cloudflare edge
5. **Single Connection**: Doesn't test multi-connection scenarios

### Not Suitable For

- Testing local network speeds (use iperf instead)
- Measuring Wi-Fi range
- Testing specific server endpoints
- Multi-threaded download scenarios

---

## Next Steps

- **[Usage Guide](usage.md)** - Learn all CLI options
- **[Web Dashboard](web-dashboard.md)** - Explore the interactive dashboard
- **[Docker](docker.md)** - Run in containers
- **[API Reference](api-reference.md)** - Use as a Python library
- **[FAQ](faq.md)** - Common questions and troubleshooting
