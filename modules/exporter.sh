#!/bin/bash
# exporter.sh - Exports monitoring data to CSV

OUTPUT="../logs/monitoring_$(date +%F_%H-%M-%S).csv"
echo "script_name,pid,cpu,mem,elapsed_time,command" > "$OUTPUT"
../modules/monitor.sh | awk '{print $1","$2","$3","$4","$5","$6}' >> "$OUTPUT"
echo "Exported to $OUTPUT"
