"""Standalone UDP server for a simple Network Event Monitoring System."""

from __future__ import annotations

import json
import socket
import threading
from dataclasses import dataclass
from datetime import datetime


HOST = "0.0.0.0"
PORT = 9999
BUFFER_SIZE = 4096
LOG_FILE = "logs.txt"
LATENCY_ALERT_THRESHOLD_MS = 100.0
PACKET_LOSS_ALERT_THRESHOLD_PERCENT = 5.0


@dataclass(slots=True)
class Packet:
    """Represents one monitoring packet sent by a client node."""

    node_id: str
    latency: float
    packet_loss: float
    timestamp: str

    @classmethod
    def from_bytes(cls, payload: bytes) -> "Packet":
        """Decode a UDP payload into a Packet instance."""
        data = json.loads(payload.decode("utf-8"))
        return cls(
            node_id=str(data["node_id"]),
            latency=float(data["latency"]),
            packet_loss=float(data["packet_loss"]),
            timestamp=str(data["timestamp"]),
        )

    def format_line(self) -> str:
        """Build a readable terminal or log line."""
        return (
            f"[{self.node_id}] Latency: {self.latency:.2f}ms | "
            f"Loss: {self.packet_loss:.2f}% | Timestamp: {self.timestamp}"
        )


class Server:
    """Receives UDP monitoring packets from multiple clients."""

    def __init__(self, host: str = HOST, port: int = PORT) -> None:
        self.server_address = (host, port)
        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.log_lock = threading.Lock()

    def start(self) -> None:
        """Bind the UDP socket and process incoming packets forever."""
        self.socket_connection.bind(self.server_address)
        print(f"UDP NEMS server listening on {self.server_address[0]}:{self.server_address[1]}")

        while True:
            payload, client_address = self.socket_connection.recvfrom(BUFFER_SIZE)
            worker = threading.Thread(
                target=self._handle_packet,
                args=(payload, client_address),
                daemon=True,
            )
            worker.start()

    def _handle_packet(self, payload: bytes, client_address: tuple[str, int]) -> None:
        """Parse, display, alert, and log a received packet."""
        try:
            packet = Packet.from_bytes(payload)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print(f"[SERVER] Invalid packet from {client_address[0]}:{client_address[1]} | {error}")
            return

        print(packet.format_line())
        self._print_alerts(packet)
        self._log_packet(packet, client_address)

    def _print_alerts(self, packet: Packet) -> None:
        """Emit alert messages based on latency and packet loss thresholds."""
        high_latency = packet.latency > LATENCY_ALERT_THRESHOLD_MS
        high_packet_loss = packet.packet_loss > PACKET_LOSS_ALERT_THRESHOLD_PERCENT

        if high_latency and high_packet_loss:
            print("ALERT: High latency and packet loss detected")
        elif high_latency:
            print("ALERT: High Latency Alert")
        elif high_packet_loss:
            print("ALERT: Packet Loss Alert")

    def _log_packet(self, packet: Packet, client_address: tuple[str, int]) -> None:
        """Append the formatted packet data to a text log file."""
        log_line = (
            f"{packet.format_line()} | Source: {client_address[0]}:{client_address[1]}"
        )
        with self.log_lock:
            with open(LOG_FILE, "a", encoding="utf-8") as log_file:
                log_file.write(log_line + "\n")


def main() -> None:
    Server().start()


if __name__ == "__main__":
    main()
