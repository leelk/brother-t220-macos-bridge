#!/bin/bash
set -euo pipefail

LOGDIR="$(cd "$(dirname "$0")" && pwd)"

{
  echo "Job received: $(date)"
  echo "Content type: ${CONTENT_TYPE:-unknown}"
  echo "Arguments: $*"
} >> "$LOGDIR/jobs.log"

if [ "$#" -gt 0 ] && [ -f "$1" ]; then
  cp "$1" "$LOGDIR/received-document"
else
  cat > "$LOGDIR/received-document"
fi

echo "Document received successfully" >> "$LOGDIR/jobs.log"
