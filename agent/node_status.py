"""Node status packet helpers for the monitoring agent."""

from __future__ import annotations

import time

from common.packet_format import Packet


def build_node_status(node_id: str) -> Packet:
    return Packet(
        node_id=node_id,
        packet_type="NODE_STATUS",
        value="ALIVE",
        timestamp=time.time(),
    )


def build_heartbeat(node_id: str) -> Packet:
    return build_node_status(node_id)
