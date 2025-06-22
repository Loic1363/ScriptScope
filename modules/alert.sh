#!/bin/bash
# alert.sh - Alerts if resource usage exceeds thresholds

CPU_THRESHOLD=50
MEM_THRESHOLD=30

../modules/monitor.sh | while read -r line; do
  cpu=$(echo "$line" | awk '{print $3}')
  mem=$(echo "$line" | awk '{print $4}')
  if (( $(echo "$cpu > $CPU_THRESHOLD" | bc -l) )); then
    echo "ALERT: High CPU usage detected: $line"
  fi
  if (( $(echo "$mem > $MEM_THRESHOLD" | bc -l) )); then
    echo "ALERT: High MEM usage detected: $line"
  fi
done
