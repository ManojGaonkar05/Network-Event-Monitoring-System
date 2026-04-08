"""Standalone UDP client for a simple Network Event Monitoring System."""

from __future__ import annotations

import json
import random
import socket
import sys
import time
from dataclasses import dataclass
from datetime import datetime


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9999
SEND_INTERVAL_SECONDS = 2


@dataclass(slots=True)
class Packet:
    """Represents one monitoring sample sent to the server."""

    node_id: str
    latency: float
    packet_loss: float
    timestamp: str

    def to_bytes(self) -> bytes:
        """Encode the packet into JSON bytes for UDP transport."""
        payload = {
            "node_id": self.node_id,
            "latency": self.latency,
            "packet_loss": self.packet_loss,
            "timestamp": self.timestamp,
        }
        return json.dumps(payload).encode("utf-8")


class Client:
    """Sends simulated network metrics to the UDP monitoring server."""

    def __init__(
        self,
        node_id: str,
        server_host: str = SERVER_HOST,
        server_port: int = SERVER_PORT,
    ) -> None:
        self.node_id = node_id
        self.server_address = (server_host, server_port)
        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self) -> None:
        """Send one metrics packet every few seconds."""
        print(f"UDP NEMS client started for {self.node_id}")
        print(f"Sending packets to {self.server_address[0]}:{self.server_address[1]}")

        while True:
            packet = self._build_packet()
            self.socket_connection.sendto(packet.to_bytes(), self.server_address)
            print(
                f"[{packet.node_id}] Latency: {packet.latency:.2f}ms | "
                f"Loss: {packet.packet_loss:.2f}% | Timestamp: {packet.timestamp}"
            )
            time.sleep(SEND_INTERVAL_SECONDS)

    def _build_packet(self) -> Packet:
        """Create a sample packet with current timestamp and demo metrics."""
        return Packet(
            node_id=self.node_id,
            latency=random.uniform(10.0, 150.0),
            packet_loss=random.uniform(0.0, 10.0),
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )


def main() -> None:
    node_id = sys.argv[1] if len(sys.argv) > 1 else "Node 1"
    server_host = sys.argv[2] if len(sys.argv) > 2 else SERVER_HOST
    Client(node_id=node_id, server_host=server_host).run()


if __name__ == "__main__":
    main()
