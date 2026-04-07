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
from server.database import insert_event_log


class EventProcessor:
    def __init__(self) -> None:
        LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

    def evaluate(self, packet: Packet) -> list[tuple[str, str, str]]:
        detected_events: list[tuple[str, str, str]] = []
        try:
            metric_value = float(packet.value)
        except ValueError:
            metric_value = None

        if packet.packet_type == "LATENCY" and metric_value is not None:
            if metric_value > LATENCY_THRESHOLD_MS:
                detected_events.append(
                    (
                        "ALERT",
                        "HIGH_LATENCY",
                        f"latency_ms={metric_value:.2f}",
                    )
                )

        if packet.packet_type == "PACKET_LOSS" and metric_value is not None:
            if metric_value > PACKET_LOSS_THRESHOLD_PERCENT:
                detected_events.append(
                    (
                        "ALERT",
                        "HIGH_PACKET_LOSS",
                        f"packet_loss={metric_value:.2f}%",
                    )
                )

        return detected_events

    def log_packet(self, packet: Packet) -> None:
        self.log_event(
            level="INFO",
            event_type="PACKET_RECEIVED",
            node_id=packet.node_id,
            message=f"{packet.packet_type} | {packet.value}",
            timestamp=self._format_timestamp(packet.timestamp),
        )

    def log_events(self, node_id: str, detected_events: list[tuple[str, str, str]]) -> None:
        for level, event_type, message in detected_events:
            self.log_event(level=level, event_type=event_type, node_id=node_id, message=message)

    def log_event(
        self,
        level: str,
        event_type: str,
        node_id: str,
        message: str,
        timestamp: str | None = None,
    ) -> None:
        entry_time = timestamp or datetime.now().isoformat(sep=" ", timespec="seconds")
        formatted_message = (
            f"{entry_time} | {level} | {event_type} | node_id={node_id} | {message}"
        )
        with EVENT_LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(f"{formatted_message}\n")
        insert_event_log(entry_time, node_id, level, event_type, message)
        self._print_alert(level, event_type, node_id, message)

    @staticmethod
    def _format_timestamp(timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp).isoformat(sep=" ", timespec="seconds")

    @staticmethod
    def _print_alert(level: str, event_type: str, node_id: str, message: str) -> None:
        if level in {"ALERT", "ERROR"}:
            print(f"{level}: {event_type} | node_id={node_id} | {message}")
