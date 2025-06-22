#!/bin/bash
# Simulate disk I/O
dd if=/dev/zero of=./tempfile bs=1M count=500 oflag=dsync
rm -f ./tempfile
