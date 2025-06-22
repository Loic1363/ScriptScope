#!/bin/bash
# exporter.sh - Exports monitoring data to CSV

# Always resolve the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Ensure logs directory exists
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"

OUTPUT="$LOG_DIR/monitoring_$(date +%F_%H-%M-%S).csv"
echo "script_name,pid,cpu,mem,elapsed_time,command" > "$OUTPUT"
"$PROJECT_ROOT/modules/monitor.sh" | awk '{print $1","$2","$3","$4","$5","$6}' >> "$OUTPUT"
echo "Exported to $OUTPUT"
