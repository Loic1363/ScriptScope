#!/bin/bash
# monitor.sh - Monitors resource usage of configured scripts

CONFIG_FILE="../config/scripts.conf"

while IFS= read -r script_path; do
  script_name=$(basename "$script_path")
  # Find running processes for the script
  pids=$(pgrep -f "$script_path")
  for pid in $pids; do
    # Get CPU and memory usage
    stats=$(ps -p "$pid" -o pid=,pcpu=,pmem=,etime=,cmd=)
    echo "$script_name: $stats"
  done
done < "$CONFIG_FILE"
