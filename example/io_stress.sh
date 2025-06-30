#!/bin/bash

end=$((SECONDS+80))
while [ $SECONDS -lt $end ]; do
    dd if=/dev/zero of=tempfile bs=1M count=100 oflag=dsync 2>/dev/null
    rm -f tempfile
done
