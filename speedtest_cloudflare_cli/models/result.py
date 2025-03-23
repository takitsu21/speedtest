from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Result:
    speed: float | None
    jitter: float | None
    latency: float | str | None
    http_latency: float | None
