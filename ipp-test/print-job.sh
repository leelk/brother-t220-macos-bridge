#!/bin/bash
set -euo pipefail

BASE="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$BASE/ipp-test/printing.log"

if [ "$#" -lt 1 ] || [ ! -f "$1" ]; then
    echo "ERROR: Missing PDF print job" >> "$LOG"
    exit 1
fi

{
    echo "=== Print job: $(date) ==="
    echo "Input: $1"
    /usr/bin/python3 "$BASE/brother-bridge.py" "$1"
    echo "=== Job submitted ==="
} >> "$LOG" 2>&1
