# Brother DCP-T220 macOS bridge

This experimental bridge enables normal macOS **Cmd + P** PDF printing to a USB-connected Brother DCP-T220. It combines a local IPP printer, Docker, Brother's official Linux conversion filter, and a CUPS USB pass-through queue.

## How it works

```text
macOS application -> local IPP printer -> Python bridge
-> Docker/Ghostscript -> Brother Linux filter -> CUPS USB queue -> printer
```

The current configuration produces A4 output with selectable Draft, Normal or High quality, full colour by default, and per-job grayscale support. Colour printing has been physically tested. The virtual printer advertises colour support when launched with the provided script. A previously running monochrome instance and cached Gray-only macOS queue were corrected; the user subsequently confirmed a colour print-dialog preview in Preview with the virtual printer and Default Settings selected. See [colour preview checks and limitations](docs/COLOR_PREVIEW.md).

## Requirements

- macOS with CUPS and `ippeveprinter`
- Docker Desktop running
- Brother DCP-T220 connected over USB
- Brother's official **Linux printer driver (deb package)** for the DCP-T220

Brother's driver package and extracted files are deliberately excluded from this repository. Download them directly from Brother and review their license before use.

## Setup

Clone the repository into any folder, then place the official `.deb` package in that folder and extract it without installing it:

```bash
ar -x dcpt220pdrv-3.5.0-1.i386.deb
mkdir -p extracted
tar -xzf data.tar.gz -C extracted
```

The bridge expects this executable to exist afterward:

```text
extracted/opt/brother/Printers/dcpt220/lpd/x86_64/brdcpt220filter
```

Build the AMD64 conversion image (Apple Silicon uses Docker emulation):

```bash
docker build --platform linux/amd64 \
  -f Dockerfile.brother \
  -t brother-t220-converter:1.0 .
```

Make the scripts executable:

```bash
chmod +x convert-brother.sh start-brother-service.sh ipp-test/*.sh
```

### Create the physical USB pass-through queue

Find the printer URI:

```bash
lpinfo -v | grep -i brother
```

Substitute that URI below:

```bash
sudo lpadmin \
  -p Brother_T220_Test \
  -E \
  -v 'usb://Brother/DCP-T220?serial=YOUR_SERIAL' \
  -P "$PWD/config/Brother_T220_Test.ppd"
```

macOS may warn that PPD drivers are deprecated. This queue only carries printer-ready data produced by Brother's filter.

### Start and register the local IPP printer

Start the service and leave it running:

```bash
./start-brother-service.sh
```

In another terminal, register it with macOS:

```bash
sudo lpadmin \
  -p Brother_T220_Virtual \
  -E \
  -v ipp://localhost:8631/ipp/print \
  -m everywhere
```

Select **Brother_T220_Virtual** from an application's print dialog.

## Direct tests

Convert a PDF without printing:

```bash
./convert-brother.sh document.pdf document.prn
```

Convert and submit a PDF to the USB queue:

```bash
python3 brother-bridge.py document.pdf
```

## Grayscale printing

In Cmd+P, select the virtual printer, scroll to **Printer Options** and look
for **Color Mode**, **Output Mode**, or **Print in Color** (wording varies by
application). Select **Grayscale** or turn off **Print in Color** for this job.
The queue exposes RGB and Gray; some applications hide this under a collapsed
printer-options section. Leave colour enabled for full-colour output.

The bridge forwards IPP `print-color-mode=monochrome` to Brother's `Mono`
configuration in a temporary per-job file. `color`, `auto`, and missing options
preserve FullColor. No service restart is required for these script changes.

You can also explicitly submit a grayscale PDF from Terminal (this prints):

```sh
lp -d Brother_T220_Virtual -o print-color-mode=monochrome document.pdf
# Or bypass the virtual queue:
python3 brother-bridge.py document.pdf --color-mode monochrome
```

Convert without printing:

```sh
./convert-brother.sh document.pdf document.prn monochrome
```

Validation without printing:

```sh
python3 -m unittest discover -s tests -v
ipptool -tv ipp://localhost:8631/ipp/print ipp-test/grayscale-job.test
```

Tests cover option forwarding and per-job configuration with mocked Docker
and printing. Actual grayscale output and the application's grayscale control
still require verification: print a coloured document in grayscale, then in
colour and confirm the second job stays coloured. No physical grayscale test
has been performed. No claim is made about exclusive black-ink use.

## Print quality

Cmd+P **High** now selects Brother **Fine** mode. Previously every selection
was forced to Normal. Draft selects Draft; Normal and missing selections
select Normal. Numeric IPP values 3/4/5 and keyword values are handled, with
per-job configuration isolation. Colour/grayscale selection is independent.
No service restart or queue re-registration is required for this change.

```sh
# These commands print:
lp -d Brother_T220_Virtual -o print-quality=5 document.pdf
python3 brother-bridge.py document.pdf --quality high
# Convert without printing:
./convert-brother.sh document.pdf document.prn color high
# Validate advertised choices and High requests without printing:
ipptool -tv ipp://localhost:8631/ipp/print ipp-test/quality-job.test
```

Seven automated tests cover defaults, keyword/numeric quality modes,
colour/grayscale combinations, invalid values and unchanged vendor settings.
Local conversion-only checks using the real Docker/Brother filter produced
nonempty, distinct Draft/Normal/Fine output streams from the same one-page
test PDF; no jobs were submitted. Original vendor configuration checksums
matched before and after. This confirms selection reaches the converter,
not that physical quality has been visually verified.

The existing 300 dpi RGB raster and page geometry are preserved, consistent
with the installed vendor wrapper's input resolution. Fine is a vendor print
mode, not a promise of increased input dpi. The generic virtual service still
advertises 600 dpi, which is not the bridge's actual PDF raster resolution.
Changing that profile or raster geometry requires separate scale/detail tests.
Paper/media mapping is also not implemented; the generic photo-media choices
must not be treated as validated photo-paper support.

To finish verification, print the same document with fine text, linework and
colour detail at Normal and High on suitable paper, then check detail, margins
and scale. Repeat High in grayscale and switch back to Normal/colour. Physical
improvement remains unverified until this comparison is performed.

## Current limitations

- Docker Desktop and the local IPP service must be running.
- A4 is currently fixed in the converter. Quality and colour/grayscale can be selected per job.
- Duplex and print-dialog option mapping are not implemented.
- Multipage output is implemented page-by-page but needs broader physical testing.
- This is an independent experimental project, not an official Brother product.

## Repository policy

Do not commit Brother's `.deb`, extracted driver files or binaries, generated `.prn`/`.ppm` files, spool documents, logs, credentials, keys, or local environment files. The included `.gitignore` excludes them.

## License

Original project code and documentation are licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE). This does not license Brother software or other third-party components; those retain their own terms. Brother packages and extracted files are excluded from this repository and the planned native distribution.
