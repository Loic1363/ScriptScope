#!/bin/bash
# Simulate RAM usage (100 MB for 60 seconds)
MEMORY_MB=100
timeout 60 bash -c "head -c $((MEMORY_MB*1024*1024)) </dev/zero | tail"
