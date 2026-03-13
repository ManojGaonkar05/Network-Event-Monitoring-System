# Network Event Monitoring System (NEMS)

## Overview

The **Network Event Monitoring System (NEMS)** is a distributed monitoring system designed to detect and report network events such as latency, packet loss, and node availability. Multiple client nodes monitor their network conditions and periodically send reports to a centralized monitoring server using **UDP communication**.

The monitoring server collects these reports, analyzes the data, detects abnormal network conditions, and displays the current network status.

This project demonstrates important **Computer Network concepts**, including socket programming, UDP communication, distributed monitoring, and event detection.

---

## Features

* UDP-based communication between nodes and server
* Real-time monitoring of multiple client nodes
* Detection of network events such as:

  * High latency
  * Packet loss
  * Client offline
* Heartbeat system to track active clients
* Monitoring dashboard displayed in the terminal
* Logging of events for analysis

---

## System Architecture

```
                Monitoring Server
                   (Server Node)

                        │
        ┌───────────────┼───────────────┐
        │               │               │
     Client A        Client B        Client C
    (Agent Node)    (Agent Node)    (Agent Node)
```

Each client runs a **monitoring agent** that measures network conditions and sends monitoring packets to the server.

---

## Project Structure

```
network-event-monitor/

server/
│
├── monitoring_server.py
├── event_processor.py
├── node_registry.py
└── dashboard.py

agent/
│
├── client_agent.py
├── network_probe.py
├── system_metrics.py
└── heartbeat.py

common/
│
├── packet_format.py
└── config.py

logs/
│
└── event_log.txt

README.md
```

### Server Components

* **monitoring_server.py** – UDP server that receives monitoring packets
* **event_processor.py** – Detects abnormal network conditions
* **node_registry.py** – Tracks connected nodes
* **dashboard.py** – Displays monitoring results

### Client Components

* **client_agent.py** – Main monitoring agent
* **network_probe.py** – Measures latency and packet loss
* **system_metrics.py** – Collects system resource information
* **heartbeat.py** – Sends periodic heartbeat signals

---

## Packet Format

Monitoring packets follow this structure:

```
NODE_ID | TYPE | VALUE | TIMESTAMP
```

Examples:

```
Laptop_A | HEARTBEAT | OK | 17123231
Laptop_B | LATENCY | 35ms | 17123231
Laptop_C | PACKET_LOSS | 5% | 17123231
```

---

## Event Detection

The server generates alerts when thresholds are exceeded.

| Condition             | Event            |
| --------------------- | ---------------- |
| Latency > 100 ms      | HIGH_LATENCY     |
| Packet loss > 10%     | HIGH_PACKET_LOSS |
| No heartbeat received | CLIENT_DOWN      |

Events are logged in:

```
logs/event_log.txt
```

---

## Requirements

* Python 3.8 or higher
* All devices connected to the same network (LAN/WiFi)

Optional library:

```
psutil
```

Install with:

```
pip install psutil
```

---

## Running the Project

### 1. Start the Monitoring Server

On the server machine:

```
python server/monitoring_server.py
```

---

### 2. Configure Server IP

Edit:

```
common/config.py
```

Example:

```
SERVER_IP = "192.168.1.10"
PORT = 9999
INTERVAL = 5
```

---

### 3. Start Client Agents

On each client laptop:

```
python agent/client_agent.py
```

---

### Example Output

```
----- Network Monitoring -----

Laptop_A latency 32ms
Laptop_B latency 41ms
Laptop_C packet_loss 3%

Active nodes: 3
```

---

## Applications

This system can be used for:

* Monitoring network performance in LAN environments
* Detecting network congestion or failures
* Monitoring distributed systems
* Learning socket programming and network monitoring concepts

Similar real-world tools include:

* Nagios
* Zabbix
* Prometheus
* Datadog

---

## Future Improvements

* Web-based monitoring dashboard
* Database storage for events
* Encryption and authentication for agents
* Automatic node discovery
* Graphical visualization of network metrics

---

## Author

Manoj Gaonkar
B.Tech CSE – Computer Networks Project
