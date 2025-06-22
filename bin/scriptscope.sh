#!/bin/bash

# Always resolve the project root, regardless of where the script is called from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

case "$1" in
  monitor)
    "$PROJECT_ROOT/modules/monitor.sh"
    ;;
  ui)
    "$PROJECT_ROOT/modules/ui.sh"
    ;;
  alert)
    "$PROJECT_ROOT/modules/alert.sh"
    ;;
  export)
    "$PROJECT_ROOT/modules/exporter.sh"
    ;;
  *)
    echo "Usage: $0 {monitor|ui|alert|export}"
    ;;
esac
