"""In-memory registry of active nodes and their most recent metrics."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from common.config import NODE_TIMEOUT_SECONDS


@dataclass(slots=True)
class NodeState:
    node_id: str
    address: tuple[str, int]
    last_seen: float
    metrics: dict[str, str] = field(default_factory=dict)
    timeout_reported: bool = False

    @property
    def is_active(self) -> bool:
        return (time.time() - self.last_seen) <= NODE_TIMEOUT_SECONDS


class NodeRegistry:
    def __init__(self) -> None:
        self._nodes: dict[str, NodeState] = {}

    def update(
        self,
        node_id: str,
        client_address: tuple[str, int],
        packet_type: str,
        value: str,
    ) -> None:
        node_state = self._nodes.get(node_id)
        if node_state is None:
            node_state = NodeState(node_id=node_id, address=client_address, last_seen=time.time())
            self._nodes[node_id] = node_state
        node_state.address = client_address
        node_state.last_seen = time.time()
        node_state.timeout_reported = False
        node_state.metrics[packet_type] = value

    def active_nodes(self) -> list[NodeState]:
        return [node_state for node_state in self._nodes.values() if node_state.is_active]

    def timed_out_nodes(self) -> list[NodeState]:
        timed_out_nodes: list[NodeState] = []
        for node_state in self._nodes.values():
            if node_state.is_active or node_state.timeout_reported:
                continue
            node_state.timeout_reported = True
            timed_out_nodes.append(node_state)
        return timed_out_nodes

    def snapshot(self) -> list[NodeState]:
        return sorted(self.active_nodes(), key=lambda node_state: node_state.node_id)
