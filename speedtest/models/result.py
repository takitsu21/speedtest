from dataclasses import dataclass


@dataclass
class Result:
    speed: float
    jitter: float
    latency: float
    http_latency: float
