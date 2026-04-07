"""Terminal dashboard for displaying active node monitoring data."""

from __future__ import annotations

import os
from datetime import datetime

from server.node_registry import NodeState


class Dashboard:
    def render(self, nodes: list[NodeState]) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== Network Event Monitoring System ===")
        print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Active nodes: {len(nodes)}")
        print("-" * 88)
        print(
            f"{'Node ID':<16}{'Address':<24}{'Latency(ms)':<14}"
            f"{'Loss(%)':<10}{'Node Status':<12}{'Last Seen':<12}"
        )
        print("-" * 88)

        if not nodes:
            print("No active nodes detected.")
            return

        now = datetime.now().timestamp()
        for node_state in nodes:
            client_address = f"{node_state.address[0]}:{node_state.address[1]}"
            latency = node_state.metrics.get("LATENCY", "-")
            packet_loss = node_state.metrics.get("PACKET_LOSS", "-")
            node_status = node_state.metrics.get("NODE_STATUS", "-")
            age_seconds = int(now - node_state.last_seen)
            print(
                f"{node_state.node_id:<16}{client_address:<24}{latency:<14}"
                f"{packet_loss:<10}{node_status:<12}{age_seconds}s ago"
            )
