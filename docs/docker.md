# Docker & Container Deployment

Run **speedtest-cli** in a container using Docker or Podman for isolated, reproducible speed tests.

## Quick Start

### Using Docker

```bash
docker run --rm -it ghcr.io/takitsu21/speedtest:latest
```

### Using Podman

```bash
podman run --rm -it ghcr.io/takitsu21/speedtest:latest
```

Both commands will:
1. Pull the latest speedtest-cli image (if not already cached)
2. Run a complete speed test
3. Display results in your terminal
4. Remove the container after completion

## Container Image Details

### Image Information

- **Registry**: GitHub Container Registry (ghcr.io)
- **Repository**: `ghcr.io/takitsu21/speedtest`
- **Tags**: `latest`, version-specific tags (e.g., `1.2.3`)
- **Base Image**: Python 3.13-slim
- **Size**: ~200 MB (optimized)

### Supported Platforms

- **linux/amd64** (x86_64)
- **linux/arm64** (ARM64/Apple Silicon)
- **linux/arm/v7** (ARM 32-bit)

Multi-architecture support ensures the image works on:
- Intel/AMD servers and desktops
- Apple Silicon Macs (M1/M2/M3)
- Raspberry Pi and ARM devices
- Cloud platforms (AWS, GCP, Azure)

## Basic Usage

### Run Default Speed Test

```bash
docker run --rm -it ghcr.io/takitsu21/speedtest:latest
```

**Flags Explained:**
- `--rm`: Remove container after it exits
- `-it`: Interactive terminal (for colored output)
- `ghcr.io/takitsu21/speedtest:latest`: Image name

### Run with CLI Options

Pass any speedtest-cli option to the container:

```bash
# Download only
docker run --rm -it ghcr.io/takitsu21/speedtest:latest --download

# Custom size
docker run --rm -it ghcr.io/takitsu21/speedtest:latest -ds 50 -us 25

# Multiple attempts
docker run --rm -it ghcr.io/takitsu21/speedtest:latest --attempts 3

# JSON output
docker run --rm -it ghcr.io/takitsu21/speedtest:latest --json
```

## Advanced Usage

### Save JSON Results to Host

Mount a volume to save results to your host machine:

```bash
# Create output directory
mkdir -p ~/speedtest-results

# Run and save JSON output
docker run --rm -it \
  -v ~/speedtest-results:/output \
  ghcr.io/takitsu21/speedtest:latest \
  --json-output /output/results.json
```

**Result:** JSON file saved to `~/speedtest-results/results.json` on your host.

### Silent Mode for Automation

Run without interactive terminal:

```bash
docker run --rm ghcr.io/takitsu21/speedtest:latest --silent --json
```

### Specific Version

Use a specific version instead of `latest`:

```bash
docker run --rm -it ghcr.io/takitsu21/speedtest:1.2.3
```

**Benefits:**
- Reproducible builds
- Version pinning for CI/CD
- Rollback capability

### Custom Network Configuration

Run with host networking for accurate results:

```bash
# Docker
docker run --rm -it --network host ghcr.io/takitsu21/speedtest:latest

# Podman
podman run --rm -it --network host ghcr.io/takitsu21/speedtest:latest
```

**When to Use:**
- Container networking adds latency
- Host network gives most accurate results
- Required for some network configurations

!!! warning "Security Note"
    `--network host` gives container access to host network stack. Only use if you trust the image.

## Building Custom Image

### Clone Repository

```bash
git clone https://github.com/takitsu21/speedtest.git
cd speedtest
```

### Build Image

```bash
# Using Docker
docker build -t speedtest-custom .

# Using Podman
podman build -t speedtest-custom .
```

### Build with BuildKit (Faster)

```bash
# Docker with BuildKit
DOCKER_BUILDKIT=1 docker build -t speedtest-custom .

# Podman (BuildKit enabled by default)
podman build -t speedtest-custom .
```

### Multi-Platform Build

Build for multiple architectures:

```bash
docker buildx create --use
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t speedtest-custom \
  --push .
```

### Run Custom Image

```bash
docker run --rm -it speedtest-custom
```

## Docker Compose

Create `docker-compose.yml` for easier management:

```yaml
version: '3.8'

services:
  speedtest:
    image: ghcr.io/takitsu21/speedtest:latest
    stdin_open: true
    tty: true
    volumes:
      - ./results:/output
    command: --json-output /output/speedtest.json
```

**Run:**

```bash
docker-compose run --rm speedtest
```

**Custom Options:**

```bash
docker-compose run --rm speedtest --download --attempts 3
```

## Scheduled Testing with Cron

### Using Docker

Create a script `~/speedtest.sh`:

```bash
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker run --rm \
  -v ~/speedtest-logs:/output \
  ghcr.io/takitsu21/speedtest:latest \
  --silent --json-output /output/speedtest_$TIMESTAMP.json
```

Make it executable:

```bash
chmod +x ~/speedtest.sh
```

Add to crontab:

```bash
# Run every day at 2 AM
0 2 * * * /home/username/speedtest.sh
```

### Using systemd Timer (Linux)

Create `~/.config/systemd/user/speedtest.service`:

```ini
[Unit]
Description=Speed Test

[Service]
Type=oneshot
ExecStart=/usr/bin/docker run --rm \
  -v %h/speedtest-logs:/output \
  ghcr.io/takitsu21/speedtest:latest \
  --silent --json-output /output/speedtest_$(date +\%Y\%m\%d_\%H\%M\%S).json
```

Create `~/.config/systemd/user/speedtest.timer`:

```ini
[Unit]
Description=Run Speed Test Daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:

```bash
systemctl --user enable --now speedtest.timer
systemctl --user status speedtest.timer
```

## Kubernetes Deployment

### CronJob for Scheduled Testing

Create `speedtest-cronjob.yaml`:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: speedtest
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: speedtest
            image: ghcr.io/takitsu21/speedtest:latest
            args: ["--silent", "--json-output", "/output/results.json"]
            volumeMounts:
            - name: results
              mountPath: /output
          volumes:
          - name: results
            persistentVolumeClaim:
              claimName: speedtest-results
          restartPolicy: OnFailure
```

Apply:

```bash
kubectl apply -f speedtest-cronjob.yaml
```

### One-Time Job

Create `speedtest-job.yaml`:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: speedtest-once
spec:
  template:
    spec:
      containers:
      - name: speedtest
        image: ghcr.io/takitsu21/speedtest:latest
        args: ["--json"]
      restartPolicy: Never
  backoffLimit: 3
```

Run:

```bash
kubectl apply -f speedtest-job.yaml
kubectl logs job/speedtest-once
```

## CI/CD Integration

### GitHub Actions

Add to `.github/workflows/speedtest.yml`:

```yaml
name: Network Speed Test

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  speedtest:
    runs-on: ubuntu-latest
    steps:
      - name: Run Speed Test
        run: |
          docker run --rm ghcr.io/takitsu21/speedtest:latest --json > results.json
      
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: speedtest-results
          path: results.json
```

### GitLab CI

Add to `.gitlab-ci.yml`:

```yaml
speedtest:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker run --rm ghcr.io/takitsu21/speedtest:latest --json > results.json
  artifacts:
    paths:
      - results.json
    expire_in: 1 week
  only:
    - schedules
```

### Jenkins

```groovy
pipeline {
    agent any
    triggers {
        cron('0 */6 * * *')
    }
    stages {
        stage('Speed Test') {
            steps {
                sh '''
                    docker run --rm ghcr.io/takitsu21/speedtest:latest \
                        --json-output results.json
                '''
                archiveArtifacts artifacts: 'results.json'
            }
        }
    }
}
```

## Monitoring Integration

### Prometheus Exporter

Create a simple exporter script:

```bash
#!/bin/bash

# Run speedtest and convert to Prometheus metrics
RESULTS=$(docker run --rm ghcr.io/takitsu21/speedtest:latest --json)

echo "# HELP speedtest_download_mbps Download speed in Mbps"
echo "# TYPE speedtest_download_mbps gauge"
echo "speedtest_download_mbps $(echo $RESULTS | jq -r '.download')"

echo "# HELP speedtest_upload_mbps Upload speed in Mbps"
echo "# TYPE speedtest_upload_mbps gauge"
echo "speedtest_upload_mbps $(echo $RESULTS | jq -r '.upload')"

echo "# HELP speedtest_ping_ms Ping latency in milliseconds"
echo "# TYPE speedtest_ping_ms gauge"
echo "speedtest_ping_ms $(echo $RESULTS | jq -r '.ping')"
```

### InfluxDB Integration

```python
import subprocess
import json
from influxdb import InfluxDBClient

# Run speedtest
result = subprocess.run(
    ['docker', 'run', '--rm', 'ghcr.io/takitsu21/speedtest:latest', '--json'],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)

# Write to InfluxDB
client = InfluxDBClient(host='localhost', port=8086, database='speedtest')
point = {
    "measurement": "speed",
    "fields": {
        "download": data['download'],
        "upload": data['upload'],
        "ping": data['ping'],
        "jitter": data['jitter']
    }
}
client.write_points([point])
```

## Troubleshooting

### Image Pull Issues

**Problem:** Cannot pull image

**Solutions:**

```bash
# Try with explicit registry
docker pull ghcr.io/takitsu21/speedtest:latest

# Check network connectivity
ping ghcr.io

# Login if private (not needed for this public image)
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

### Permission Denied

**Problem:** Docker permission errors on Linux

**Solution:**

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again, or:
newgrp docker

# Or use Podman (rootless by default)
podman run --rm -it ghcr.io/takitsu21/speedtest:latest
```

### Slow Test Execution

**Problem:** Tests take too long in container

**Possible Causes:**
- Container networking overhead
- Resource limits
- Network configuration

**Solutions:**

```bash
# Use host networking
docker run --rm -it --network host ghcr.io/takitsu21/speedtest:latest

# Increase container resources
docker run --rm -it --memory 512m --cpus 2 ghcr.io/takitsu21/speedtest:latest

# Use smaller test sizes
docker run --rm -it ghcr.io/takitsu21/speedtest:latest -ds 25 -us 10
```

### No Output

**Problem:** Container runs but shows no output

**Solutions:**

```bash
# Ensure -it flags are used
docker run --rm -it ghcr.io/takitsu21/speedtest:latest

# Check container logs
docker ps -a
docker logs <container-id>

# Run with explicit shell
docker run --rm -it ghcr.io/takitsu21/speedtest:latest sh -c "speedtest-cli"
```

## Best Practices

### 1. Use Specific Tags

```bash
# ✅ Good - version pinning
docker run --rm -it ghcr.io/takitsu21/speedtest:1.2.3

# ⚠️ Acceptable - latest
docker run --rm -it ghcr.io/takitsu21/speedtest:latest
```

### 2. Resource Limits

```bash
docker run --rm -it \
  --memory 256m \
  --cpus 0.5 \
  ghcr.io/takitsu21/speedtest:latest
```

### 3. Cleanup Old Images

```bash
# Remove unused images
docker image prune -a

# Remove specific version
docker rmi ghcr.io/takitsu21/speedtest:old-version
```

### 4. Security

```bash
# Run as non-root (image already does this)
# Use read-only filesystem when possible
docker run --rm -it --read-only ghcr.io/takitsu21/speedtest:latest

# Drop capabilities
docker run --rm -it --cap-drop=ALL ghcr.io/takitsu21/speedtest:latest
```

## Comparison: Container vs. Native

| Aspect | Container | Native Installation |
|--------|-----------|---------------------|
| **Setup** | Pull image only | Install Python + packages |
| **Isolation** | Fully isolated | System packages |
| **Updates** | Pull new image | Package upgrade |
| **Portability** | Highly portable | Python dependency |
| **Performance** | Slight overhead | Native speed |
| **Networking** | May affect latency | Direct access |
| **Disk Space** | ~200 MB | ~50 MB |

**Use Containers When:**
- CI/CD pipelines
- Consistent environments needed
- Multiple versions required
- Easy cleanup desired
- Kubernetes/cloud deployments

**Use Native When:**
- Development
- Frequent testing
- Minimal overhead required
- Direct system access needed

## Next Steps

- **[Usage Guide](usage.md)** - Learn all CLI options
- **[Features](features.md)** - Explore capabilities
- **[API Reference](api-reference.md)** - Programmatic usage
- **[Contributing](contributing.md)** - Build from source
- **[FAQ](faq.md)** - Common questions
