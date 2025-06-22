#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

while true; do
    clear
    echo "Script Name | PID | CPU (%) | MEM (%) | Elapsed Time | Command"
    echo "---------------------------------------------------------------"
    "$PROJECT_ROOT/modules/monitor.sh"
    sleep 1
done
