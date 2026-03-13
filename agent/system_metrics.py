"""Collect lightweight host metrics using the Python standard library."""

from __future__ import annotations

import os
import platform
import socket
import time


class SystemMetrics:
    def __init__(self) -> None:
        self._started_at = time.time()

    def get_hostname(self) -> str:
        return socket.gethostname()

    def get_platform(self) -> str:
        return platform.system()

    def get_uptime_seconds(self) -> int:
        return int(time.time() - self._started_at)

    def get_load_average(self) -> float:
        if hasattr(os, "getloadavg"):
            return round(os.getloadavg()[0], 2)
        return 0.0

    def collect(self) -> dict[str, str]:
        return {
            "HOSTNAME": self.get_hostname(),
            "PLATFORM": self.get_platform(),
            "UPTIME_SECONDS": str(self.get_uptime_seconds()),
            "LOAD_AVERAGE": f"{self.get_load_average():.2f}",
        }
