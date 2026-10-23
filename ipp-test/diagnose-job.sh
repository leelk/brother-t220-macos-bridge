#!/bin/bash
set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG="$SCRIPT_DIR/diagnostic.log"

{
  echo "=== $(date) ==="
  echo "Arguments: $*"
  echo "Content type: ${CONTENT_TYPE:-unknown}"
  echo "Output format: ${OUTPUT_FORMAT:-unknown}"
  if [ "$#" -gt 0 ] && [ -f "$1" ]; then
    /usr/bin/file "$1"
  fi
} >> "$LOG" 2>&1

exit 0
