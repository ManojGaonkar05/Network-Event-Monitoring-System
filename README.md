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

```
Client Nodes (Agents)  →  UDP Communication  →  Monitoring Server
```

---

## ⚙️ Features

* Real-time distributed monitoring
* UDP-based communication
* Latency measurement
* Packet loss detection
* Node status tracking
* System metrics collection (CPU, Memory)
* Event detection based on thresholds
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

Example:

```
node-123 | NODE_STATUS | ACTIVE | 17123231
node-123 | LATENCY | 35.5 | 17123231
node-123 | PACKET_LOSS | 2.0 | 17123231
```

---

## 🚀 How to Run

### 🖥️ Run the Server

1. Open terminal in the project folder:

```
cd Network-Event-Monitoring-System
```

2. Start the server:

```
python server/monitoring_server.py
```

3. You should see:

```
Monitoring server listening on UDP 0.0.0.0:9999
```

4. Find the server IP:

```
ipconfig
```

Example:

```
IPv4 Address: 10.30.202.120
```

---

### 💻 Run the Client

1. Open terminal in the project folder:

```
cd Network-Event-Monitoring-System
```

2. Run the client:

```
python agent/client_agent.py <SERVER_IP>
```

Example:

```
python agent/client_agent.py 10.30.202.120
```

3. Client output:

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

### 🧪 Local Testing (Optional)

Run both on same system:

```
python agent/client_agent.py 127.0.0.1
```

---

## 🌐 Requirements

* Python 3.x
* Devices connected to the same network

Optional:

```
pip install psutil
```

---

## 🗄️ Logging and Storage

* Logs: `logs/event_log.txt`
* Database: `network_logs.db`

---

## ⚠️ Limitations

* UDP does not guarantee delivery
* No encryption (basic implementation)
* Best suited for local networks

---

## 🔮 Future Enhancements

* Web dashboard
* Graph visualization
* Alert system
* Secure communication
* Auto node discovery

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
