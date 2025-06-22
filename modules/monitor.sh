#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$PROJECT_ROOT/config/scripts.conf"

while IFS= read -r script_path; do
  script_name=$(basename "$script_path")
  pids=$(pgrep -f "$script_name")
  for pid in $pids; do
    # On récupère les stats du process
    stats=$(ps -p "$pid" -o pid=,pcpu=,pmem=,etime=,cmd= --no-headers)
    if [[ -n "$stats" ]]; then
      # On découpe les champs pour un affichage propre
      pid=$(echo "$stats" | awk '{print $1}')
      cpu=$(echo "$stats" | awk '{print $2}')
      mem=$(echo "$stats" | awk '{print $3}')
      etime=$(echo "$stats" | awk '{print $4}')
      # On reconstitue la commande (qui peut contenir des espaces)
      cmd=$(echo "$stats" | cut -d' ' -f5-)
      printf "%-15s | %-6s | %-7s | %-7s | %-12s | %s\n" "$script_name" "$pid" "$cpu" "$mem" "$etime" "$cmd"
    fi
  done
done < "$CONFIG_FILE"
