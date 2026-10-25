#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
PATH=/usr/bin:/bin:/usr/sbin:/sbin
export PATH
QUEUE=Brother_T220_Native
BASE=/Library/Printers/leelk/BrotherT220
PPD=/Library/Printers/PPDs/Contents/Resources/Brother_DCP_T220_Native.ppd
STATE='/Library/Application Support/leelk/BrotherT220'
CURRENT=/etc/cups/ppd/Brother_T220_Native.ppd
if [ "$(id -u)" != 0 ]; then echo 'Administrator access is required.' >&2; exit 1; fi
if [ "$#" != 1 ]; then echo 'Choose configure, configure-if-connected, rollback or remove.' >&2; exit 1; fi
busy() {
    # Changing/removing queues with pending jobs is never automatic.
    for queue in Brother_T220_Native Brother_T220_Test Brother_T220_Virtual; do
        jobs=$(lpstat -W not-completed -o "$queue" 2>/dev/null || true)
        if [ -n "$jobs" ]; then echo 'A Brother queue has unfinished jobs. Resolve them before changing the driver.' >&2; return 0; fi
    done
    return 1
}
# A matching queue name is not sufficient proof that this project owns it.
if lpstat -p "$QUEUE" >/dev/null 2>&1; then
    if [ ! -f "$CURRENT" ] || ! grep -q '/Library/Printers/leelk/BrotherT220/versions/' "$CURRENT"; then
        echo 'The native queue name belongs to a different driver; no changes were made.' >&2; exit 1
    fi
fi
case "$1" in
configure|configure-if-connected)
    if busy; then exit 1; fi
    if [ ! -f "$PPD" ] || [ ! -x "$BASE/versions/0.1.0/brother-t220-native" ]; then echo 'Driver files are missing. Reinstall the package.' >&2; exit 1; fi
    # Exact USB model, with CUPS-generated escaping. Never evaluate URI as shell code.
    devices=$(lpinfo -v | awk '$1 == "direct" && $2 ~ /^usb:\/\/Brother\/DCP-T220([?\/]|$)/ { print $2 }')
    count=$(printf '%s\n' "$devices" | awk 'NF { n++ } END { print n+0 }')
    if [ "$count" = 0 ]; then
        if [ "$1" = configure-if-connected ]; then echo 'Files installed. Connect USB and open Brother T220 Native Setup to add the printer.'; exit 0; fi
        echo 'Connect and power on one Brother DCP-T220 by USB, then try again.' >&2; exit 1
    fi
    if [ "$count" != 1 ]; then echo 'Connect only one DCP-T220 while setting up this experimental driver.' >&2; exit 1; fi
    lpadmin -p "$QUEUE" -E -v "$devices" -P "$PPD" -D 'Brother DCP-T220 Native Experimental' -o printer-error-policy=abort-job -o job-sheets-default=none,none
    echo 'Native experimental printer added. Select Brother_T220_Native in Cmd+P. No test was printed.'
    ;;
rollback)
    if busy; then exit 1; fi
    if [ ! -f "$STATE/previous.ppd" ] || [ ! -s "$STATE/previous-uri" ]; then
        echo 'No previous native queue was saved. Use Remove Native Queue; the Docker fallback is unchanged.' >&2; exit 1
    fi
    uri=$(cat "$STATE/previous-uri")
    case "$uri" in usb://Brother/DCP-T220*) ;; *) echo 'Invalid saved printer URI.' >&2; exit 1;; esac
    lpadmin -p "$QUEUE" -E -v "$uri" -P "$STATE/previous.ppd" -o printer-error-policy=abort-job
    echo 'Previous native queue restored. No print was submitted.'
    ;;
remove)
    if busy; then exit 1; fi
    # Keep package files/version history for reversible removal and future repair.
    # This removes only our virtual name, never the Docker or USB fallback queues.
    if lpstat -p "$QUEUE" >/dev/null 2>&1; then lpadmin -x "$QUEUE"; fi
    echo 'Native queue removed. Driver files remain for reinstall/rollback; fallback queues are unchanged.'
    ;;
*) echo 'Unknown operation.' >&2; exit 1;;
esac
