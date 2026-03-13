"""Event detection and logging for monitoring packets."""

from __future__ import annotations

from datetime import datetime

from common.config import (
    EVENT_LOG_FILE,
    LATENCY_THRESHOLD_MS,
    LOG_DIRECTORY,
    PACKET_LOSS_THRESHOLD_PERCENT,
)
from common.packet_format import Packet


class EventProcessor:
    def __init__(self) -> None:
        LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

    def evaluate(self, packet: Packet) -> list[str]:
        events: list[str] = []
        try:
            numeric_value = float(packet.value)
        except ValueError:
            numeric_value = None

        if packet.packet_type == "LATENCY" and numeric_value is not None:
            if numeric_value > LATENCY_THRESHOLD_MS:
                events.append(
                    f"HIGH_LATENCY | node={packet.node_id} | latency_ms={numeric_value:.2f}"
                )

        if packet.packet_type == "PACKET_LOSS" and numeric_value is not None:
            if numeric_value > PACKET_LOSS_THRESHOLD_PERCENT:
                events.append(
                    f"HIGH_PACKET_LOSS | node={packet.node_id} | packet_loss={numeric_value:.2f}%"
                )

        return events

    def log_packet(self, packet: Packet) -> None:
        self._append_log(f"PACKET | {packet.as_log_line()}")

    def log_events(self, events: list[str]) -> None:
        for event in events:
            self._append_log(f"EVENT | {event}")

    def _append_log(self, message: str) -> None:
        timestamp = datetime.now().isoformat(sep=" ", timespec="seconds")
        with EVENT_LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(f"{timestamp} | {message}\n")
