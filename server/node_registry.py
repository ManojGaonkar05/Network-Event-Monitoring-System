"""In-memory registry of nodes and their most recent metrics."""

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

    @property
    def status(self) -> str:
        return "ACTIVE" if self.is_active else "INACTIVE"

    def refresh_status(self) -> None:
        self.metrics["NODE_STATUS"] = self.status


class NodeRegistry:
    def __init__(self) -> None:
        self._nodes: dict[str, NodeState] = {}

    @staticmethod
    def _current_time() -> float:
        return time.time()

    def _refresh_node(self, node_state: NodeState) -> NodeState:
        node_state.refresh_status()
        return node_state

    def _refresh_all_nodes(self) -> list[NodeState]:
        return [self._refresh_node(node_state) for node_state in self._nodes.values()]

    def update(
        self,
        node_id: str,
        client_address: tuple[str, int],
        packet_type: str,
        value: str,
        received_at: float | None = None,
    ) -> None:
        current_time = received_at if received_at is not None else self._current_time()
        node_state = self._nodes.get(node_id)
        if node_state is None:
            node_state = NodeState(
                node_id=node_id,
                address=client_address,
                last_seen=current_time,
            )
            self._nodes[node_id] = node_state
        node_state.address = client_address
        # Refresh last_seen on every packet, regardless of packet type.
        node_state.last_seen = current_time
        node_state.timeout_reported = False
        node_state.metrics[packet_type] = value
        node_state.refresh_status()

    def active_nodes(self) -> list[NodeState]:
        return [node_state for node_state in self._refresh_all_nodes() if node_state.is_active]

    def timed_out_nodes(self) -> list[NodeState]:
        timed_out_nodes: list[NodeState] = []
        for node_state in self._refresh_all_nodes():
            if node_state.is_active or node_state.timeout_reported:
                continue
            node_state.timeout_reported = True
            timed_out_nodes.append(node_state)
        return timed_out_nodes

    def snapshot(self) -> list[NodeState]:
        return sorted(self._refresh_all_nodes(), key=lambda node_state: node_state.node_id)
