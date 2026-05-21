#!/bin/bash

PHONE_IP="10.79.210.67"
API="http://localhost:8000/alerts"

echo "=============================="
echo " SENTINELX VIVA DEMO"
echo "=============================="

echo ""
echo "[1] Port Scan from phone..."
curl -s -X POST "$API?src_ip=$PHONE_IP&attack_type=Port%20Scan&severity=HIGH&ai_score=87&blocked=true" > /dev/null
echo "✅ Port Scan alert added!"
sleep 2

echo ""
echo "[2] ICMP Flood..."
curl -s -X POST "$API?src_ip=$PHONE_IP&attack_type=ICMP%20Flood&severity=CRITICAL&ai_score=92&blocked=true" > /dev/null
echo "✅ ICMP Flood alert added!"
sleep 2

echo ""
echo "[3] SSH Brute Force..."
curl -s -X POST "$API?src_ip=$PHONE_IP&attack_type=SSH%20Brute%20Force&severity=HIGH&ai_score=89&blocked=true" > /dev/null
echo "✅ SSH Brute Force alert added!"
sleep 2

echo ""
echo "[4] SYN Flood..."
curl -s -X POST "$API?src_ip=$PHONE_IP&attack_type=SYN%20Flood&severity=CRITICAL&ai_score=95&blocked=true" > /dev/null
echo "✅ SYN Flood alert added!"
sleep 2

echo ""
echo "[5] HTTP Flood..."
curl -s -X POST "$API?src_ip=$PHONE_IP&attack_type=HTTP%20Flood&severity=HIGH&ai_score=85&blocked=true" > /dev/null
echo "✅ HTTP Flood alert added!"

echo ""
echo "=============================="
echo " ALL ATTACKS SHOWN IN DASHBOARD"
echo " Open: http://localhost:3000"
echo "=============================="
