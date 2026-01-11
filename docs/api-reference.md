# API Reference

Use **speedtest-cli** as a Python library to integrate network speed testing into your own applications.

## Installation for Library Use

Install speedtest-cli in your Python project:

```bash
# Using pip
pip install speedtest-cloudflare-cli

# Using poetry
poetry add speedtest-cloudflare-cli

# Using uv
uv add speedtest-cloudflare-cli
```

## Quick Start

### Basic Usage

```python
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

# Create SpeedTest instance
test = SpeedTest()

# Run complete speed test
results = test.run()

# Access results
print(f"Download: {results.download} Mbps")
print(f"Upload: {results.upload} Mbps")
print(f"Ping: {results.ping} ms")
print(f"Jitter: {results.jitter} ms")
```

### Download Only

```python
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

test = SpeedTest(run_download=True, run_upload=False)
results = test.run()

print(f"Download: {results.download} Mbps")
```

### Upload Only

```python
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

test = SpeedTest(run_download=False, run_upload=True)
results = test.run()

print(f"Upload: {results.upload} Mbps")
```

### Custom Test Sizes

```python
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

test = SpeedTest(
    download_size=50,  # MB
    upload_size=25,    # MB
)
results = test.run()
```

### Silent Mode

```python
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

test = SpeedTest(silent=True)
results = test.run()
# No progress bars or output, just results
```

## Core Classes

### SpeedTest

::: speedtest_cloudflare_cli.core.speedtest.SpeedTest
    options:
      show_root_heading: true
      show_source: false
      heading_level: 4

## Data Models

### Result

::: speedtest_cloudflare_cli.models.result.Result
    options:
      show_root_heading: true
      show_source: false
      heading_level: 4

### Metadata

::: speedtest_cloudflare_cli.models.metadata.Metadata
    options:
      show_root_heading: true
      show_source: false
      heading_level: 4

## Advanced Examples

### Error Handling

```python
from speedtest_cloudflare_cli.core.speedtest import SpeedTest
import httpx

try:
    test = SpeedTest()
    results = test.run()
    print(f"Download: {results.download} Mbps")
except httpx.HTTPError as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Error running speed test: {e}")
```

### Multiple Attempts

```python
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

def run_multiple_tests(attempts=3):
    """Run multiple speed tests and return average results."""
    download_speeds = []
    upload_speeds = []
    
    for i in range(attempts):
        print(f"Attempt {i+1}/{attempts}")
        test = SpeedTest()
        results = test.run()
        
        download_speeds.append(results.download)
        upload_speeds.append(results.upload)
    
    avg_download = sum(download_speeds) / len(download_speeds)
    avg_upload = sum(upload_speeds) / len(upload_speeds)
    
    return {
        'download': avg_download,
        'upload': avg_upload,
        'download_speeds': download_speeds,
        'upload_speeds': upload_speeds,
    }

# Usage
averages = run_multiple_tests(attempts=5)
print(f"Average Download: {averages['download']:.2f} Mbps")
print(f"Average Upload: {averages['upload']:.2f} Mbps")
```

### Accessing Metadata

```python
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

test = SpeedTest()
results = test.run()

# Access metadata
metadata = results.metadata
if metadata:
    print(f"IP: {metadata.ip}")
    print(f"ISP: {metadata.isp}")
    print(f"Location: {metadata.city}, {metadata.region}, {metadata.country}")
    print(f"Coordinates: {metadata.loc}")
    print(f"Cloudflare Datacenter: {metadata.colo}")
```

### Export to JSON

```python
from speedtest_cloudflare_cli.core.speedtest import SpeedTest
import json

test = SpeedTest()
results = test.run()

# Convert to dict for JSON serialization
results_dict = {
    'download': results.download,
    'upload': results.upload,
    'ping': results.ping,
    'jitter': results.jitter,
    'http_latency': results.http_latency,
    'metadata': {
        'ip': results.metadata.ip if results.metadata else None,
        'isp': results.metadata.isp if results.metadata else None,
        'city': results.metadata.city if results.metadata else None,
        'region': results.metadata.region if results.metadata else None,
        'country': results.metadata.country if results.metadata else None,
        'loc': results.metadata.loc if results.metadata else None,
        'colo': results.metadata.colo if results.metadata else None,
    } if results.metadata else None
}

# Save to file
with open('speedtest_results.json', 'w') as f:
    json.dump(results_dict, f, indent=2)

print("Results saved to speedtest_results.json")
```

### Custom Progress Callback

```python
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

def progress_callback(progress: float, task: str):
    """Custom progress callback."""
    print(f"{task}: {progress:.1f}%")

# Note: This is conceptual - check actual API for progress hooks
test = SpeedTest()
results = test.run()
```

### Conditional Testing

```python
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

def smart_speed_test(min_download=50, min_upload=10):
    """
    Run speed test and alert if below thresholds.
    
    Args:
        min_download: Minimum acceptable download speed (Mbps)
        min_upload: Minimum acceptable upload speed (Mbps)
    
    Returns:
        dict: Results and status
    """
    test = SpeedTest()
    results = test.run()
    
    download_ok = results.download >= min_download
    upload_ok = results.upload >= min_upload
    
    status = {
        'download': results.download,
        'upload': results.upload,
        'download_ok': download_ok,
        'upload_ok': upload_ok,
        'overall_ok': download_ok and upload_ok,
    }
    
    if not status['overall_ok']:
        print("⚠️  Warning: Speed below threshold!")
        if not download_ok:
            print(f"  Download: {results.download:.1f} Mbps (min: {min_download})")
        if not upload_ok:
            print(f"  Upload: {results.upload:.1f} Mbps (min: {min_upload})")
    else:
        print("✓ Speed test passed!")
    
    return status

# Usage
status = smart_speed_test(min_download=100, min_upload=20)
```

### Integration with Web Framework

#### Flask Example

```python
from flask import Flask, jsonify
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

app = Flask(__name__)

@app.route('/api/speedtest', methods=['POST'])
def run_speedtest():
    """API endpoint to run speed test."""
    try:
        test = SpeedTest(silent=True)
        results = test.run()
        
        return jsonify({
            'success': True,
            'data': {
                'download': results.download,
                'upload': results.upload,
                'ping': results.ping,
                'jitter': results.jitter,
                'http_latency': results.http_latency,
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run()
```

#### FastAPI Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

app = FastAPI()

class SpeedTestResult(BaseModel):
    download: float
    upload: float
    ping: float
    jitter: float
    http_latency: float

@app.post('/api/speedtest', response_model=SpeedTestResult)
async def run_speedtest():
    """API endpoint to run speed test."""
    try:
        test = SpeedTest(silent=True)
        results = test.run()
        
        return SpeedTestResult(
            download=results.download,
            upload=results.upload,
            ping=results.ping,
            jitter=results.jitter,
            http_latency=results.http_latency,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Background Task

```python
import threading
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

def background_speedtest(callback):
    """Run speed test in background thread."""
    def run():
        test = SpeedTest(silent=True)
        results = test.run()
        callback(results)
    
    thread = threading.Thread(target=run)
    thread.start()
    return thread

# Usage
def on_complete(results):
    print(f"Test complete! Download: {results.download} Mbps")

thread = background_speedtest(on_complete)
print("Speed test running in background...")
thread.join()  # Wait for completion
```

### Scheduled Testing

```python
import schedule
import time
from speedtest_cloudflare_cli.core.speedtest import SpeedTest
import json
from datetime import datetime

def scheduled_speed_test():
    """Run speed test and log results."""
    test = SpeedTest(silent=True)
    results = test.run()
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'download': results.download,
        'upload': results.upload,
        'ping': results.ping,
    }
    
    # Append to log file
    with open('speedtest_log.jsonl', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    print(f"Logged: {log_entry}")

# Schedule tests
schedule.every().hour.do(scheduled_speed_test)
schedule.every().day.at("02:00").do(scheduled_speed_test)

print("Scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)
```

### Data Analysis

```python
import json
import pandas as pd
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

def analyze_speed_history(log_file='speedtest_log.jsonl'):
    """Analyze historical speed test data."""
    # Read log file
    data = []
    with open(log_file) as f:
        for line in f:
            data.append(json.loads(line))
    
    # Create DataFrame
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Calculate statistics
    stats = {
        'download': {
            'mean': df['download'].mean(),
            'min': df['download'].min(),
            'max': df['download'].max(),
            'std': df['download'].std(),
        },
        'upload': {
            'mean': df['upload'].mean(),
            'min': df['upload'].min(),
            'max': df['upload'].max(),
            'std': df['upload'].std(),
        },
        'ping': {
            'mean': df['ping'].mean(),
            'min': df['ping'].min(),
            'max': df['ping'].max(),
            'std': df['ping'].std(),
        }
    }
    
    return stats, df

# Usage
stats, df = analyze_speed_history()
print(f"Average Download: {stats['download']['mean']:.2f} Mbps")
print(f"Average Upload: {stats['upload']['mean']:.2f} Mbps")
print(f"Average Ping: {stats['ping']['mean']:.2f} ms")
```

## Type Hints

The library uses comprehensive type hints for better IDE support:

```python
from typing import Optional
from speedtest_cloudflare_cli.core.speedtest import SpeedTest
from speedtest_cloudflare_cli.models.result import Result

def run_test(silent: bool = False) -> Optional[Result]:
    """Run speed test with type hints."""
    test: SpeedTest = SpeedTest(silent=silent)
    results: Result = test.run()
    return results
```

## Best Practices

### 1. Use Silent Mode in Production

```python
# ✅ Good - no console output
test = SpeedTest(silent=True)

# ❌ Bad - progress bars in production logs
test = SpeedTest(silent=False)
```

### 2. Handle Exceptions

```python
# ✅ Good - proper error handling
try:
    test = SpeedTest()
    results = test.run()
except Exception as e:
    logger.error(f"Speed test failed: {e}")
    return None

# ❌ Bad - no error handling
test = SpeedTest()
results = test.run()  # May crash
```

### 3. Use Context Managers (if available)

```python
# Check if context manager is supported
# (Conceptual - verify in actual implementation)
with SpeedTest(silent=True) as test:
    results = test.run()
```

### 4. Don't Run Too Frequently

```python
# ✅ Good - reasonable intervals
schedule.every().hour.do(run_speedtest)

# ❌ Bad - too frequent, wastes bandwidth
schedule.every().minute.do(run_speedtest)
```

### 5. Cache Metadata

```python
# ✅ Good - reuse metadata when possible
metadata = get_metadata_once()
# Use cached metadata for multiple operations

# ❌ Bad - fetch metadata repeatedly
# (This depends on API design)
```

## Performance Considerations

### Memory Usage

- Silent mode uses less memory (no progress tracking)
- Smaller test sizes reduce memory footprint
- Single instance recommended per process

### Network Impact

- Each test consumes bandwidth
- Download test: ~10-200 MB
- Upload test: ~5-100 MB
- Consider test frequency in production

### Execution Time

Typical execution times:
- Complete test: 15-60 seconds
- Download only: 10-30 seconds
- Upload only: 10-30 seconds

Factors affecting speed:
- Test sizes
- Connection speed
- Network latency
- System load

## Troubleshooting

### Import Errors

```python
# If you get import errors, ensure package is installed
try:
    from speedtest_cloudflare_cli.core.speedtest import SpeedTest
except ImportError:
    print("Install: pip install speedtest-cloudflare-cli")
```

### Network Errors

```python
import httpx

try:
    test = SpeedTest()
    results = test.run()
except httpx.ConnectError:
    print("Cannot connect to Cloudflare servers")
except httpx.TimeoutError:
    print("Request timed out")
except httpx.HTTPError as e:
    print(f"HTTP error: {e}")
```

### Permission Errors

```python
# For ICMP ping, may need elevated privileges
# Library falls back to HTTP latency automatically
test = SpeedTest()
results = test.run()  # Works even without ICMP access
```

## Next Steps

- **[Usage Guide](usage.md)** - CLI usage patterns
- **[Features](features.md)** - Complete feature list
- **[Contributing](contributing.md)** - Contribute to development
- **[FAQ](faq.md)** - Common questions
