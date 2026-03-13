"""Helpers for serializing and parsing UDP monitoring packets."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from common.config import PACKET_SEPARATOR


@dataclass(slots=True)
class Packet:
    node_id: str
    packet_type: str
    value: str
    timestamp: float

    def encode(self) -> bytes:
        return PACKET_SEPARATOR.join(
            [
                self.node_id,
                self.packet_type,
                self.value,
                f"{self.timestamp:.6f}",
            ]
        ).encode("utf-8")

    @classmethod
    def decode(cls, raw_data: bytes) -> "Packet":
        decoded = raw_data.decode("utf-8").strip()
        parts = [part.strip() for part in decoded.split(PACKET_SEPARATOR)]
        if len(parts) != 4:
            raise ValueError(
                "Invalid packet format. Expected NODE_ID | TYPE | VALUE | TIMESTAMP."
            )
        node_id, packet_type, value, timestamp = parts
        return cls(
            node_id=node_id,
            packet_type=packet_type,
            value=value,
            timestamp=float(timestamp),
        )

    def as_log_line(self) -> str:
        readable_time = datetime.fromtimestamp(self.timestamp).isoformat(
            sep=" ", timespec="seconds"
        )
        return f"{readable_time} | {self.node_id} | {self.packet_type} | {self.value}"
