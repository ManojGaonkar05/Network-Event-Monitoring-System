# Network Event Monitoring System (NEMS)

## 📌 Overview

The **Network Event Monitoring System (NEMS)** is a distributed monitoring solution designed to track network and system performance across multiple client nodes. Each client collects real-time data such as latency, packet loss, and system metrics, and transmits it to a centralized server using UDP.

The server processes incoming data, detects abnormal network conditions, and maintains logs for analysis and monitoring.

---

## 🎯 Objectives

* Monitor network performance in real time
* Detect issues such as high latency and packet loss
* Track node availability and status
* Collect system metrics from distributed nodes
* Provide centralized monitoring and logging

---

## 🏗️ System Architecture

```id="d7d2xh"
Client Nodes (Agents)  →  UDP Communication  →  Monitoring Server
```

* Multiple clients send monitoring data
* A central server receives, processes, and displays results

---

## ⚙️ Features

* Real-time distributed monitoring
* UDP-based communication (lightweight and fast)
* Latency measurement between client and server
* Packet loss calculation
* Node status tracking (active/inactive)
* System metrics collection (CPU and memory usage)
* Event detection based on configurable thresholds
* Logging of network events and system activity
* Database integration for persistent storage

---

## 📁 Project Structure

```id="x6n6d1"
NEMS/
│
├── agent/
│   ├── client_agent.py
│   ├── node_status.py
│   ├── network_probe.py
│   ├── system_metrics.py
│
├── server/
│   ├── monitoring_server.py
│   ├── event_processor.py
│   ├── node_registry.py
│   ├── database.py
│   ├── dashboard.py
│
├── common/
│   ├── config.py
│   ├── packet_format.py
│
├── logs/
│   └── event_log.txt
│
├── network_logs.db
├── README.md
```

---

## 📦 Data Format

All communication follows a structured packet format:

```id="m5z9z8"
NODE_ID | TYPE | VALUE | TIMESTAMP
```

### Example:

```id="f6s1f0"
node-123 | NODE_STATUS | ACTIVE | 17123231
node-123 | LATENCY | 35.5 | 17123231
node-123 | PACKET_LOSS | 2.0 | 17123231
```

---

## 🚀 Execution

### Run Server

```bash id="1xqg2x"
python server/monitoring_server.py
```

---

### Run Client

```bash id="7k8n5y"
python agent/client_agent.py <SERVER_IP>
```

Example:

```bash id="g2n7o9"
python agent/client_agent.py 192.168.1.240
```

---

## 🌐 Requirements

* Python 3.x
* Devices connected to the same network

Optional dependency:

```bash id="0m2r9y"
pip install psutil
```

---

## 📊 Output

The server displays real-time monitoring information such as:

```id="9t8h4y"
Node node-123 ACTIVE
Latency: 32 ms
Packet Loss: 1%
```

---

## 🗄️ Logging and Storage

* Event logs are stored in:

  ```
  logs/event_log.txt
  ```
* Persistent data is stored in:

  ```
  network_logs.db
  ```

---

## ⚠️ Limitations

* UDP does not guarantee packet delivery
* Basic implementation without encryption
* Designed for local network environments

---

## 🔮 Future Enhancements

* Web-based dashboard for visualization
* Graphical representation of metrics
* Alert and notification system
* Secure communication mechanisms
* Automatic node discovery

---

## 👨‍💻 Team Contribution

* Client Module: Data collection and transmission
* Server Module: Data processing and event detection
* Integration: Dashboard, database, and testing

---

## 🧠 Technologies Used

* Python
* UDP Socket Programming
* Distributed System Concepts
* Network Performance Analysis

---

## 📌 Summary

> A distributed UDP-based monitoring system that collects, processes, and analyzes network and system performance data in real time.
