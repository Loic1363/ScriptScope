#!/bin/bash
# scriptscope.sh - Main entrypoint for ScriptScope

case "$1" in
  monitor)
    ../modules/monitor.sh
    ;;
  ui)
    ../modules/ui.sh
    ;;
  alert)
    ../modules/alert.sh
    ;;
  export)
    ../modules/exporter.sh
    ;;
  *)
    echo "Usage: $0 {monitor|ui|alert|export}"
    ;;
esac
