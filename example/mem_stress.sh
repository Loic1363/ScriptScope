#!/bin/bash
#500Mo for 1m
end=$((SECONDS+60))
mem=$(python3 -c "print('a'*500*1024*1024)")
while [ $SECONDS -lt $end ]; do
    sleep 1
done
unset mem

