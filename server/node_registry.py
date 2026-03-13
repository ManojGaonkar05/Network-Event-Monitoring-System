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

    @property
    def is_active(self) -> bool:
        return (time.time() - self.last_seen) <= NODE_TIMEOUT_SECONDS


class NodeRegistry:
    def __init__(self) -> None:
        self._nodes: dict[str, NodeState] = {}

    def update(self, node_id: str, address: tuple[str, int], packet_type: str, value: str) -> None:
        node = self._nodes.get(node_id)
        if node is None:
            node = NodeState(node_id=node_id, address=address, last_seen=time.time())
            self._nodes[node_id] = node
        node.address = address
        node.last_seen = time.time()
        node.metrics[packet_type] = value

    def active_nodes(self) -> list[NodeState]:
        return [node for node in self._nodes.values() if node.is_active]

    def snapshot(self) -> list[NodeState]:
        return sorted(self.active_nodes(), key=lambda node: node.node_id)
