#!/bin/bash
# build + render + export several creatures (2 at a time), then their 3-view sheets.  usage: ./run.sh id1 id2 ...
cd "$(dirname "$0")"
one() { python3 make.py "$1" --render --two --walk --export > "out/log_$1.txt" 2>&1; grep -E "PROP|Error|Traceback|line [0-9]" "out/log_$1.txt" | sed "s/^/$1: /" | tail -6; }
export -f one
printf "%s\n" "$@" | xargs -P 2 -I{} bash -c 'one {}'
python3 views.py "$@" > /dev/null
