#!/bin/bash
set -euo pipefail

if [ "$#" -lt 2 ] || [ "$#" -gt 4 ]; then
    echo "Usage: $0 input.pdf output.prn [auto|color|monochrome] [draft|normal|high]"
    exit 1
fi

case "${3:-color}" in
    auto|color) BROTHER_COLOR=FullColor ;;
    monochrome) BROTHER_COLOR=Mono ;;
    *) echo "Error: Unsupported color mode" >&2; exit 1 ;;
esac

case "${4:-normal}" in
    draft|3) BROTHER_QUALITY=Draft ;;
    normal|4) BROTHER_QUALITY=Normal ;;
    high|5) BROTHER_QUALITY=Fine ;;
    *) echo "Error: Unsupported quality" >&2; exit 1 ;;
esac

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INPUT="$(realpath "$1")"
OUTPUT_DIR="$(cd "$(dirname "$2")" && pwd)"
OUTPUT="$OUTPUT_DIR/$(basename "$2")"

if [ ! -f "$INPUT" ]; then
    echo "Error: Input file not found"
    exit 1
fi

DRIVER="$SCRIPT_DIR/extracted/opt/brother/Printers/dcpt220"
RCFILE="$DRIVER/inf/brdcpt220rc"

if [ ! -x "$DRIVER/lpd/x86_64/brdcpt220filter" ] || [ ! -f "$RCFILE" ]; then
    echo "Error: Brother's extracted DCP-T220 Linux driver was not found under:" >&2
    echo "  $DRIVER" >&2
    echo "See README.md for setup instructions." >&2
    exit 1
fi

TMPDIR_JOB="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_JOB"' EXIT

cp "$INPUT" "$TMPDIR_JOB/document"
# Keep Brother's original configuration untouched. The bridge currently
# targets A4; quality and colour mode are isolated to this job.
sed \
    -e 's/^PageSize=.*/PageSize=A4/' \
    -e "s/^BRResolution=.*/BRResolution=$BROTHER_QUALITY/" \
    -e "s/^BRMonoColor=.*/BRMonoColor=$BROTHER_COLOR/" \
    "$RCFILE" > "$TMPDIR_JOB/printer.rc"

docker run --rm \
    --platform linux/amd64 \
    --network none \
    -v "$DRIVER:/opt/brother/Printers/dcpt220:ro" \
    -v "$TMPDIR_JOB:/work" \
    brother-t220-converter:1.0 \
    /bin/sh -c '
      set -e

      gs -q -dNOPAUSE -dBATCH -dSAFER \
        -sDEVICE=ppmraw \
        -r300 \
        -g2480x3507 \
        -sOutputFile=/work/page-%03d.ppm \
        /work/document

      for page in /work/page-*.ppm; do
        /opt/brother/Printers/dcpt220/lpd/x86_64/brdcpt220filter \
          -pi /opt/brother/Printers/dcpt220/inf/paperinfij2 \
          -rc /work/printer.rc \
          < "$page"
      done > /work/output.prn
    '

cp "$TMPDIR_JOB/output.prn" "$OUTPUT"

echo "Brother printer file created: $OUTPUT"
