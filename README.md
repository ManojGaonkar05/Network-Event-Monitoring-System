# 🚀 Network Event Monitoring System (NEMS)

## 📌 Overview

The **Network Event Monitoring System (NEMS)** is a distributed monitoring solution designed to track network and system performance across multiple client nodes.

Each client (agent) collects real-time data such as latency, packet loss, and system metrics, and transmits it to a centralized server using UDP. The server processes incoming data, detects abnormal conditions, and maintains logs for monitoring and analysis.

---

## 🎯 Objectives

* Monitor network performance in real time
* Detect high latency and packet loss
* Track node availability and health
* Collect system metrics (CPU, Memory)
* Provide centralized logging and monitoring

---

## 🏗️ System Architecture

```
Client Nodes (Agents)  →  UDP Communication  →  Monitoring Server
```

---

## ⚙️ Features

* Real-time distributed monitoring
* UDP-based lightweight communication
* Latency measurement
* Packet loss detection
* Node status tracking
* System metrics collection
* Threshold-based event detection
* Logging and database storage

---

## 📁 Project Structure

```
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

```
NODE_ID | TYPE | VALUE | TIMESTAMP
```

### Example:

```
node-123 | NODE_STATUS | ACTIVE | 17123231
node-123 | LATENCY | 35.5 | 17123231
node-123 | PACKET_LOSS | 2.0 | 17123231
```

---

## 🚀 How to Run

### 🖥️ 1. Run the Server

#### Step 1: Navigate to project folder

```bash
cd Network-Event-Monitoring-System
```

#### Step 2: Start server

**Windows:**

```bash
python server/monitoring_server.py
```

**Linux / Mac:**

```bash
python3 server/monitoring_server.py
```

#### Step 3: Expected output

```
Monitoring server listening on UDP 0.0.0.0:9999
```

#### Step 4: Find server IP address

**Windows:**

```bash
ipconfig
```

**Linux:**

```bash
ip addr
```

or

```bash
hostname -I
```

**Example:**

```
10.30.202.120
```

---

### 💻 2. Run the Client

#### Step 1: Open another terminal

```bash
cd Network-Event-Monitoring-System
```

#### Step 2: Run client

**Windows:**

```bash
python agent/client_agent.py <SERVER_IP>
```

**Linux / Mac:**

```bash
python3 agent/client_agent.py <SERVER_IP>
```

#### Example:

```bash
python3 agent/client_agent.py 10.30.202.120
```

#### Expected output:

```
Client agent started for node-xxxx
Sending UDP monitoring packets to 10.30.202.120:9999
```

---

### 🔁 Expected Server Output

```
Received from 10.30.202.233
node-xxxx | NODE_STATUS | ACTIVE
node-xxxx | LATENCY | 32 ms
node-xxxx | PACKET_LOSS | 0%
```

---

### 🧪 Local Testing (Same System)

```bash
python agent/client_agent.py 127.0.0.1
```

or

```bash
python3 agent/client_agent.py 127.0.0.1
```

---

## 🌐 Requirements

* Python 3.x
* Devices connected to same network

### Optional dependency:

```bash
pip install psutil
```

Linux:

```bash
pip3 install psutil
```

---

## 🗄️ Logging and Storage

* Logs: `logs/event_log.txt`
* Database: `network_logs.db`

---

## ⚠️ Limitations

* UDP does not guarantee packet delivery
* No encryption (basic implementation)
* Best suited for local/private networks

---

## 🔮 Future Enhancements

* Web-based dashboard
* Graph visualization
* Alert/notification system
* Secure communication (TLS)
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
* Distributed Systems
* Network Monitoring

---

## 📌 Summary

> A distributed UDP-based monitoring system that collects, processes, and analyzes network and system performance in real time.
