# Colour preview investigation — 2026-10-24

## Verified cause and repair

On macOS 27.0.1 with Apple CUPS 2.3.4, the saved startup script already
contained `-s 10,5`, but the running process omitted it. Live IPP reported
`color-supported=false`, monochrome-only supported/default modes, and the
registered virtual queue offered only Gray.

Stopped only the idle bridge process, then launched the existing startup
script. Refreshed the existing virtual queue in place (no queue deletion):

```sh
lpadmin -p Brother_T220_Virtual -E -v ipp://localhost:8631/ipp/print -m everywhere
```

Post-restart Get-Printer-Attributes confirmed `color-supported=true`,
`pages-per-minute-color=5`, supported modes `auto,color,monochrome`, and
default `auto`. The regenerated macOS PPD reports `ColorDevice: True`,
`DefaultColorModel: RGB`, and offers RGB/Gray. No jobs were submitted.
The physical USB queue, converter, Docker image, and proprietary files were
not changed. Private queue backups are in `/private/tmp/brother-preview-backup`.
The service is running in a terminal session; automatic login startup is
not installed. If it stops, run `./start-brother-service.sh` and leave it open.

## Repeatable checks (no printer required)

```sh
ipptool -tv ipp://localhost:8631/ipp/print ipp-test/color-capabilities.test
lpoptions -p Brother_T220_Virtual -l
```

Expect PASS and `ColorModel/Output Mode: *RGB Gray`. If the service is still
monochrome, inspect its actual launch command and restart with the script.
Check outstanding jobs before restarting. Refresh the virtual queue with
the command above only after the IPP check passes; preserve custom queue
settings beforehand. Never delete or recreate the physical USB queue.

## Visual acceptance — still pending

Computer-control permission was unavailable, so no print-dialog preview was
observed. Reopen Preview, open a known coloured PDF, press Cmd+P, choose
Brother_T220_Virtual, and select a fresh/default preset with colour enabled.
Check red/green/blue areas in the print-dialog thumbnail. Repeat in another
application. Cancel to avoid printing. Report whether both remain coloured.
A final physical test requires the USB printer connected and powered on;
physical colour was previously confirmed by the user, not repeated here.

## Limits

The installed ippeveprinter built-in colour profile uses default `auto`
and also advertises monochrome and generic quality/media options. The
converter remains fixed to A4, Normal and FullColor and does not map these
options. Monochrome selection is therefore not implemented end to end.
The `-a` option loads a replacement attribute profile, rather than a small
additive override; no partial profile was introduced to risk losing existing
capabilities. Explicit colour-only advertisement and accurate option mapping
remain future work. Capability and cache repair is verified; visual preview
and physical regression acceptance remain pending.

Reference: [Apple ippeveprinter source](https://github.com/apple/cups/blob/master/tools/ippeveprinter.c)
and the installed `man ippeveprinter` (`-s speed,color-speed`).
