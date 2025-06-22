#!/bin/bash
# monitor.sh - Monitors resource usage of configured scripts

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$PROJECT_ROOT/config/scripts.conf"

while IFS= read -r script_path; do
  [[ -z "$script_path" ]] && continue  # Ignore empty lines
  script_name=$(basename "$script_path")
  pids=$(pgrep -f "$script_name")
  for pid in $pids; do
    stats=$(ps -p "$pid" -o pid=,pcpu=,pmem=,etime=,cmd= --no-headers)
    if [[ -n "$stats" ]]; then
      # Extraction robuste des champs
      pid=$(echo "$stats" | awk '{print $1}')
      cpu=$(echo "$stats" | awk '{print $2}')
      mem=$(echo "$stats" | awk '{print $3}')
      etime=$(echo "$stats" | awk '{print $4}')
      # Récupère la commande complète (tous les champs à partir du 5e)
      cmd=$(echo "$stats" | awk '{$1=""; $2=""; $3=""; $4=""; sub(/^ +/, ""); print}')
      # Affichage aligné
      printf "%-15s | %-8s | %-8s | %-8s | %-14s | %s\n" \
        "$script_name" "$pid" "$cpu" "$mem" "$etime" "$cmd"
    fi
  done
done < "$CONFIG_FILE"
