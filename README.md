# ⬡ SentinelX — AI-Powered IDS/IPS Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-green)
![Docker](https://img.shields.io/badge/Docker-blue)
![Snort](https://img.shields.io/badge/Snort-3.0-red)

## 🎯 Project Overview
AI-Powered Intrusion Detection and Prevention System
built during internship at Demmisto Technologies Pvt. Ltd.

**Intern:** Karan Vhanesa (220020107091)
**Institution:** Ahmedabad Institute of Technology
**Company:** Demmisto Technologies Pvt. Ltd.
**Period:** January 2026 – March 2026

## 🚀 Features
- Real-time network traffic monitoring
- AI threat detection (97% accuracy)
- Auto IP blocking via iptables
- Live SOC dashboard
- REST API with FastAPI
- Docker deployment
- n8n automation alerts

## 🤖 AI Models
- Isolation Forest (anomaly detection)
- Random Forest (attack classification)

## ⚙️ Tech Stack
| Component | Technology |
|-----------|-----------|
| Frontend | HTML5, Chart.js |
| Backend | Python, FastAPI |
| Database | PostgreSQL, Redis |
| IDS Tool | Snort 3 |
| AI/ML | scikit-learn |
| DevOps | Docker |
| Automation | n8n |
| OS | Kali Linux |

## 🔍 Detected Attacks
- Port Scanning
- SSH Brute Force
- SYN Flood
- ICMP Flood
- SQL Injection
- DNS Tunneling

## 🚀 Quick Start
```bash
git clone https://github.com/karanvhanesa/sentinelx-ids-ips.git
cd sentinelx-ids-ips
docker-compose up -d
```

Open: http://localhost:3000

## 📊 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /alerts | Get all alerts |
| POST | /alerts | Save new alert |
| GET | /dashboard/stats | Statistics |
| GET | /system/health | Health check |

