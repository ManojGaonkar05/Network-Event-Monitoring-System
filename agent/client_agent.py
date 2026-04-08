"""Client agent for the UDP Network Event Monitoring System."""

from __future__ import annotations

import os
import socket
import sys
import time
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agent.node_status import build_node_status
from agent.network_probe import NetworkProbe
from agent.system_metrics import SystemMetrics
from common.config import MONITOR_INTERVAL_SECONDS, SERVER_PORT, SERVER_HOST
from common.packet_format import Packet


class ClientAgent:
    def __init__(self, server_host: str = SERVER_HOST, node_id: str | None = None) -> None:
        self.server_address = (server_host, SERVER_PORT)
        self.node_id = node_id or f"node-{uuid.uuid4().hex[:8]}"
        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.metrics = SystemMetrics()
        self.probe = NetworkProbe(self.socket_connection, self.node_id)
        self.packets_sent = 0
        self.started_at = time.time()

    def _send_packet(self, packet: Packet) -> None:
        self.socket_connection.sendto(packet.encode(), self.server_address)
        self.packets_sent += 1

    def _send_metrics(self) -> None:
        for metric_type, metric_value in self.metrics.collect().items():
            self._send_packet(
                Packet(
                    node_id=self.node_id,
                    packet_type=metric_type,
                    value=metric_value,
                    timestamp=time.time(),
                )
            )

    def _display_metrics(self, latency_ms: float | None, packet_loss: float) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        elapsed_time = max(time.time() - self.started_at, 1e-6)
        packet_rate = self.packets_sent / elapsed_time
        print(f"[CLIENT {self.node_id}]")
        if latency_ms is None:
            print("Latency: TIMEOUT")
        else:
            print(f"Latency: {latency_ms:.2f} ms")
        print(f"Packet Loss: {packet_loss:.2f}%")
        print(f"Packets Sent: {self.packets_sent}")
        print(f"Packet Rate: {packet_rate:.2f} packets/sec")

    def run(self) -> None:
        print(
            f"Client agent started for {self.node_id}. "
            f"Sending UDP monitoring packets to {self.server_address[0]}:{self.server_address[1]}"
        )
        while True:
            self._send_packet(build_node_status(self.node_id))
            latency_ms = self.probe.send_probe(self.server_address)
            if latency_ms is not None:
                self._send_packet(
                    Packet(
                        node_id=self.node_id,
                        packet_type="LATENCY",
                        value=f"{latency_ms:.2f}",
                        timestamp=time.time(),
                    )
                )

            packet_loss = self.probe.packet_loss_percent()
            self._send_packet(
                Packet(
                    node_id=self.node_id,
                    packet_type="PACKET_LOSS",
                    value=f"{packet_loss:.2f}",
                    timestamp=time.time(),
                )
            )

            self._send_metrics()
            self._display_metrics(latency_ms, packet_loss)
            time.sleep(MONITOR_INTERVAL_SECONDS)


def main() -> None:
    server_host = sys.argv[1] if len(sys.argv) > 1 else SERVER_HOST
    node_id = sys.argv[2] if len(sys.argv) > 2 else None

    ClientAgent(server_host=server_host, node_id=node_id).run()


if __name__ == "__main__":
    main()
