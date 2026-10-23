#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

exec /usr/bin/ippeveprinter \
    -p 8631 \
    -M Brother \
    -m DCP-T220 \
    -s 10,5 \
    -f application/pdf \
    -c "$SCRIPT_DIR/ipp-test/print-job.sh" \
    -v \
    "Brother DCP-T220 Virtual"
