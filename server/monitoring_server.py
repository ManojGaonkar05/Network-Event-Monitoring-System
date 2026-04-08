"""UDP monitoring server for the Network Event Monitoring System."""

from __future__ import annotations

import socket
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.config import (
    BUFFER_SIZE,
    EVENT_LOG_FILE,
    LATENCY_THRESHOLD_MS,
    PACKET_LOSS_THRESHOLD_PERCENT,
    SERVER_BIND_HOST,
    SERVER_PORT,
)
from common.packet_format import Packet
from server.database import init_db, insert_log
from server.dashboard import Dashboard
from server.event_processor import EventProcessor
from server.node_registry import NodeRegistry

REFRESH_INTERVAL = 1


class MonitoringServer:
    def __init__(self, host: str = SERVER_BIND_HOST, port: int = SERVER_PORT) -> None:
        self.server_address = (host, port)
        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.registry = NodeRegistry()
        self.processor = EventProcessor()
        self.dashboard = Dashboard()
        self.packets_received = 0
        self.started_at = time.time()
        self.last_dashboard_refresh = 0.0

    def _packet_rate(self) -> float:
        elapsed_time = max(time.time() - self.started_at, 1e-6)
        return self.packets_received / elapsed_time

    def start(self) -> None:
        init_db()
        self.socket_connection.settimeout(1.0)
        self.socket_connection.bind(self.server_address)
        print(f"Monitoring server listening on UDP {self.server_address[0]}:{self.server_address[1]}")

        while True:
            try:
                received_data, client_address = self.socket_connection.recvfrom(BUFFER_SIZE)
                received_at = time.time()
                self.packets_received += 1
            except socket.timeout:
                self._log_timeouts()
                self._render_dashboard_if_due()
                continue
            try:
                packet = Packet.decode(received_data)
            except ValueError as error:
                self.processor.log_event(
                    level="ERROR",
                    event_type="MALFORMED_PACKET",
                    node_id="unknown",
                    message=f"address={client_address[0]}:{client_address[1]} | error={error}",
                )
                continue

            self.registry.update(
                packet.node_id,
                client_address,
                packet.packet_type,
                packet.value,
                received_at=received_at,
            )
            node_state = next(
                (registered_node for registered_node in self.registry.snapshot() if registered_node.node_id == packet.node_id),
                None,
            )
            latency = node_state.metrics.get("LATENCY", "-") if node_state is not None else "-"
            loss = node_state.metrics.get("PACKET_LOSS", "-") if node_state is not None else "-"
            log_entry = (
                f"[{datetime.now()}] {packet.node_id} | "
                f"{client_address[0]}:{client_address[1]} | {latency} ms | Loss: {loss}%"
            )
            with open("logs/event_log.txt", "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
            self.processor.log_packet(packet)
            self._store_snapshot(packet.node_id)

            if packet.packet_type == "PROBE":
                acknowledgement_packet = Packet(
                    node_id="server",
                    packet_type="PROBE_ACK",
                    value=packet.value,
                    timestamp=packet.timestamp,
                )
                self.socket_connection.sendto(acknowledgement_packet.encode(), client_address)

            detected_events = self.processor.evaluate(packet)
            if detected_events:
                self.processor.log_events(packet.node_id, detected_events)

            self._log_timeouts()
            self._render_dashboard_if_due()

    def _store_snapshot(self, node_id: str) -> None:
        node_state = next(
            (registered_node for registered_node in self.registry.snapshot() if registered_node.node_id == node_id),
            None,
        )
        if node_state is None:
            return

        latency = self._to_float(node_state.metrics.get("LATENCY"))
        packet_loss = self._to_float(node_state.metrics.get("PACKET_LOSS"))
        status = "ALERT" if self._has_threshold_breach(latency, packet_loss) else "ALIVE"
        insert_log(node_id, latency, packet_loss, status)

    def _render_dashboard_if_due(self) -> None:
        current_time = time.time()
        if (current_time - self.last_dashboard_refresh) < REFRESH_INTERVAL:
            return
        self.dashboard.render(
            self.registry.snapshot(),
            packets_received=self.packets_received,
            packet_rate=self._packet_rate(),
        )
        self.last_dashboard_refresh = current_time

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

    def _log_timeouts(self) -> None:
        for node_state in self.registry.timed_out_nodes():
            age_seconds = int(time.time() - node_state.last_seen)
            self.processor.log_event(
                level="ERROR",
                event_type="CLIENT_DOWN",
                node_id=node_state.node_id,
                message=(
                    f"last_seen={age_seconds}s_ago | "
                    f"address={node_state.address[0]}:{node_state.address[1]}"
                ),
            )


def main() -> None:
    MonitoringServer(host=SERVER_BIND_HOST, port=SERVER_PORT).start()


if __name__ == "__main__":
    main()
