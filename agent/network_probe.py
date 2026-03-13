"""UDP probe logic used by agents to measure latency and packet loss."""

from __future__ import annotations

import socket
import time
from collections import deque

from common.config import BUFFER_SIZE, PROBE_TIMEOUT_SECONDS
from common.packet_format import Packet


class NetworkProbe:
    def __init__(self, sock: socket.socket, node_id: str) -> None:
        self.sock = sock
        self.node_id = node_id
        self._probe_sequence = 0
        self._results: deque[bool] = deque(maxlen=20)

    def send_probe(self, server_address: tuple[str, int]) -> float | None:
        self._probe_sequence += 1
        sequence = self._probe_sequence
        packet = Packet(
            node_id=self.node_id,
            packet_type="PROBE",
            value=str(sequence),
            timestamp=time.time(),
        )
        sent_at = time.time()
        self.sock.sendto(packet.encode(), server_address)
        self.sock.settimeout(PROBE_TIMEOUT_SECONDS)

        try:
            raw_data, _ = self.sock.recvfrom(BUFFER_SIZE)
            response = Packet.decode(raw_data)
            if response.packet_type != "PROBE_ACK" or response.value != str(sequence):
                self._results.append(False)
                return None
            latency_ms = (time.time() - sent_at) * 1000
            self._results.append(True)
            return round(latency_ms, 2)
        except socket.timeout:
            self._results.append(False)
            return None
        finally:
            self.sock.settimeout(None)

    def packet_loss_percent(self) -> float:
        if not self._results:
            return 0.0
        failures = sum(1 for was_successful in self._results if not was_successful)
        return round((failures / len(self._results)) * 100, 2)
