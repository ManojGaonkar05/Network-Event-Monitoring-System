"""UDP monitoring server for the Network Event Monitoring System."""

from __future__ import annotations

import socket
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.config import BUFFER_SIZE, SERVER_HOST, SERVER_PORT
from common.packet_format import Packet
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


def main() -> None:
    MonitoringServer().start()


if __name__ == "__main__":
    main()
