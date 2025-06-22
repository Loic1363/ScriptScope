#!/bin/bash
# ui.sh - Displays monitored scripts in a table

echo "Script Name | PID | CPU (%) | MEM (%) | Elapsed Time | Command"
echo "---------------------------------------------------------------"
../modules/monitor.sh
