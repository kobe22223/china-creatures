#!/bin/bash
# build + render + export several creatures in parallel, then their 3-view sheets.  usage: ./run.sh id1 id2 ...
cd "$(dirname "$0")"
for id in "$@"; do
  ( python3 make.py "$id" --render --two --walk --export > "out/log_$id.txt" 2>&1; \
    grep -E "PROP|Error|Traceback|line [0-9]" "out/log_$id.txt" | sed "s/^/$id: /" | tail -6 ) &
done
wait
python3 views.py "$@" > /dev/null
