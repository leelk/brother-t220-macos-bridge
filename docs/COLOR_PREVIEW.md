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

## Visual acceptance — Preview confirmed

On 2026-10-24, the user supplied a screenshot of Preview's Cmd+P dialog
showing a colour photograph in the print thumbnail, with Brother DCP-T220
Virtual selected and the Default Settings preset. This confirms the reported
monochrome preview issue is resolved in Preview for that image.
Computer-control permission was unavailable during the earlier agent check;
visual verification is based on the user's screenshot and confirmation.
A second application and a coloured PDF have not been checked visually.

For further checks, reopen an application, open a known coloured document,
press Cmd+P, choose Brother_T220_Virtual and use a fresh/default preset with
colour enabled. Check coloured areas in the print-dialog thumbnail, then
cancel to avoid printing. A physical regression test requires the USB printer
connected and powered on; physical colour was previously confirmed by the
user, but was not repeated after this repair.

## Limits

The installed ippeveprinter built-in colour profile uses default `auto`
and also advertises monochrome and generic quality/media options. The
converter remains fixed to A4 and Normal. Per-job monochrome selection is
now forwarded to the vendor Mono setting; colour/auto retain FullColor.
Physical grayscale output still requires verification. Other generic options
are not mapped.
The `-a` option loads a replacement attribute profile, rather than a small
additive override; no partial profile was introduced to risk losing existing
capabilities. Accurate mapping of other generic options remains future work. Capability and cache repair and the Preview image print-dialog preview are
verified. Other applications, PDF preview and physical regression acceptance
remain pending.

Reference: [Apple ippeveprinter source](https://github.com/apple/cups/blob/master/tools/ippeveprinter.c)
and the installed `man ippeveprinter` (`-s speed,color-speed`).
