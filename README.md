# Brother DCP-T220 macOS bridge

This experimental bridge enables normal macOS **Cmd + P** PDF printing to a USB-connected Brother DCP-T220. It combines a local IPP printer, Docker, Brother's official Linux conversion filter, and a CUPS USB pass-through queue.

## How it works

```text
macOS application -> local IPP printer -> Python bridge
-> Docker/Ghostscript -> Brother Linux filter -> CUPS USB queue -> printer
```

The current configuration produces A4, normal-quality, full-colour output. Colour printing has been physically tested. The virtual printer advertises colour support, although some macOS applications may still show a monochrome preview.

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

## Current limitations

- Docker Desktop and the local IPP service must be running.
- A4, normal quality, and full colour are currently fixed in the converter.
- Duplex and print-dialog option mapping are not implemented.
- Multipage output is implemented page-by-page but needs broader physical testing.
- This is an independent experimental project, not an official Brother product.

## Repository policy

Do not commit Brother's `.deb`, extracted driver files or binaries, generated `.prn`/`.ppm` files, spool documents, logs, credentials, keys, or local environment files. The included `.gitignore` excludes them.
