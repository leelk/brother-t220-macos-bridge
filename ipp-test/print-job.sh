#!/bin/bash
set -euo pipefail

BASE="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$BASE/ipp-test/printing.log"

if [ "$#" -lt 1 ] || [ ! -f "$1" ]; then
    echo "ERROR: Missing PDF print job" >> "$LOG"
    exit 1
fi

# Explicit job selection wins; auto and missing selections preserve full colour.
COLOR_MODE="${IPP_PRINT_COLOR_MODE:-${IPP_PRINT_COLOR_MODE_DEFAULT:-color}}"
case "$COLOR_MODE" in
    auto|color|monochrome) ;;
    *) echo "ERROR: Unsupported print-color-mode" >&2; exit 1 ;;
esac

{
    echo "=== Print job: $(date) ==="
    echo "Input: $1"
    /usr/bin/python3 "$BASE/brother-bridge.py" "$1" --color-mode "$COLOR_MODE"
    echo "=== Job submitted ==="
} >> "$LOG" 2>&1
