#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$PROJECT_ROOT/config/scripts.conf"
OUTPUT_JSON="$PROJECT_ROOT/stats.json"

output_terminal=""
first=1

echo "[" > "$OUTPUT_JSON"

while IFS= read -r script_path; do
  [[ -z "$script_path" ]] && continue
  script_name=$(basename "$script_path")
  pids=$(pgrep -f "$script_name")
  found=0
  for pid in $pids; do
    found=1
    stats=$(ps -p "$pid" -o pid=,pcpu=,pmem=,etime=,cmd= --no-headers)
    if [[ -n "$stats" ]]; then
      pid_val=$(echo "$stats" | awk '{print $1}')
      cpu=$(echo "$stats" | awk '{print $2}')
      mem=$(echo "$stats" | awk '{print $3}')
      etime=$(echo "$stats" | awk '{print $4}')
      cmd=$(echo "$stats" | awk '{$1=""; $2=""; $3=""; $4=""; sub(/^ +/, ""); print}')
      output_terminal+=$(printf "%-15s | %-8s | %-8s | %-8s | %-14s | %s\n" \
        "$script_name" "$pid_val" "$cpu" "$mem" "$etime" "$cmd")
      cmd_json=$(echo "$cmd" | sed 's/"/\\"/g')
      if [ $first -eq 0 ]; then
        echo "," >> "$OUTPUT_JSON"
      fi
      first=0
      echo "  { \"script_name\": \"$script_name\", \"pid\": \"$pid_val\", \"cpu\": \"$cpu\", \"mem\": \"$mem\", \"etime\": \"$etime\", \"cmd\": \"$cmd_json\" }" >> "$OUTPUT_JSON"
    fi
  done
  if [[ $found -eq 0 ]]; then
    output_terminal+=$(printf "%-15s | %-8s | %-8s | %-8s | %-14s | %s\n" \
      "$script_name" "-" "-" "-" "-" "(not running)")
    if [ $first -eq 0 ]; then
      echo "," >> "$OUTPUT_JSON"
    fi
    first=0
    echo "  { \"script_name\": \"$script_name\", \"pid\": \"-\", \"cpu\": \"-\", \"mem\": \"-\", \"etime\": \"-\", \"cmd\": \"(not running)\" }" >> "$OUTPUT_JSON"
  fi
done < "$CONFIG_FILE"

echo "]" >> "$OUTPUT_JSON"

if [ -t 1 ]; then
  printf "%s" "$output_terminal"
fi
