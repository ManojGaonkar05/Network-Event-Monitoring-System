"""UDP monitoring server for the Network Event Monitoring System."""

from __future__ import annotations

import socket
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.config import (
    BUFFER_SIZE,
    LATENCY_THRESHOLD_MS,
    PACKET_LOSS_THRESHOLD_PERCENT,
    SERVER_HOST,
    SERVER_PORT,
)
from common.packet_format import Packet
from server.database import init_db, insert_log
from server.dashboard import Dashboard
from server.event_processor import EventProcessor
from server.node_registry import NodeRegistry


class MonitoringServer:
    def __init__(self, host: str = SERVER_HOST, port: int = SERVER_PORT) -> None:
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.registry = NodeRegistry()
        self.processor = EventProcessor()
        self.dashboard = Dashboard()

    def start(self) -> None:
        init_db()
        self.sock.bind(self.server_address)
        print(f"Monitoring server listening on UDP {self.server_address[0]}:{self.server_address[1]}")

        while True:
            raw_data, address = self.sock.recvfrom(BUFFER_SIZE)
            try:
                packet = Packet.decode(raw_data)
            except ValueError as error:
                print(f"Discarded malformed packet from {address}: {error}")
                continue

            self.registry.update(packet.node_id, address, packet.packet_type, packet.value)
            self.processor.log_packet(packet)
            self._store_snapshot(packet.node_id)

            if packet.packet_type == "PROBE":
                ack = Packet(
                    node_id="server",
                    packet_type="PROBE_ACK",
                    value=packet.value,
                    timestamp=packet.timestamp,
                )
                self.sock.sendto(ack.encode(), address)

            events = self.processor.evaluate(packet)
            if events:
                self.processor.log_events(events)

            self.dashboard.render(self.registry.snapshot())

    def _store_snapshot(self, node_id: str) -> None:
        node = next((item for item in self.registry.snapshot() if item.node_id == node_id), None)
        if node is None:
            return

        latency = self._to_float(node.metrics.get("LATENCY"))
        packet_loss = self._to_float(node.metrics.get("PACKET_LOSS"))
        status = "ALERT" if self._has_threshold_breach(latency, packet_loss) else "ALIVE"
        insert_log(node_id, latency, packet_loss, status)

    @staticmethod
    def _to_float(value: str | None) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except ValueError:
            return None

    def _has_threshold_breach(
        self, latency: float | None, packet_loss: float | None
    ) -> bool:
        return bool(
            (latency is not None and latency > LATENCY_THRESHOLD_MS)
            or (packet_loss is not None and packet_loss > PACKET_LOSS_THRESHOLD_PERCENT)
        )


def main() -> None:
    MonitoringServer().start()


if __name__ == "__main__":
    main()
