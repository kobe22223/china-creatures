#!/bin/bash
# finish a batch: merged FBX + contact sheet + CreatureData.rbxmx.  usage: ./finish.sh China02_Z1G2
cd "$(dirname "$0")"
ids=$(python3 -c "
src=open('batch_fbx.py').read(); B=eval(src[src.index('BATCHES = {')+10:src.index('}\nonly')+1]); print(' '.join(B['$1']))")
python3 batch_fbx.py "$1" 2>&1 | grep -E "^BATCH|^SKIP|Error"
python3 sheet.py "out/sheets/$1_contact.png" $ids
python3 gen_rbxmx.py 2>&1 | grep -E "TOTAL|Error|Traceback"
