#!/bin/bash
# alert.sh - Alerts if resource usage exceeds thresholds

CPU_THRESHOLD=50
MEM_THRESHOLD=30

# Always resolve the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

"$PROJECT_ROOT/modules/monitor.sh" | while read -r line; do
  cpu=$(echo "$line" | awk '{print $3}')
  mem=$(echo "$line" | awk '{print $4}')
  if (( $(echo "$cpu > $CPU_THRESHOLD" | bc -l) )); then
    echo "ALERT: High CPU usage detected: $line"
  fi
  if (( $(echo "$mem > $MEM_THRESHOLD" | bc -l) )); then
    echo "ALERT: High MEM usage detected: $line"
  fi
done
