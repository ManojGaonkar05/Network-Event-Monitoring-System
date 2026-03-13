"""Shared configuration for the Network Event Monitoring System."""

from pathlib import Path

SERVER_HOST = "192.168.1.240"
SERVER_PORT = 9999
BUFFER_SIZE = 4096

MONITOR_INTERVAL_SECONDS = 5
NODE_TIMEOUT_SECONDS = 15
PROBE_TIMEOUT_SECONDS = 2

LATENCY_THRESHOLD_MS = 100.0
PACKET_LOSS_THRESHOLD_PERCENT = 10.0

LOG_DIRECTORY = Path(__file__).resolve().parents[1] / "logs"
EVENT_LOG_FILE = LOG_DIRECTORY / "event_log.txt"

PACKET_SEPARATOR = "|"