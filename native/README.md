# Native prototype

Status: experimental native CUPS filter and local development pkg now exist; see [installation/status](../docs/NATIVE_INSTALLATION.md). No hardware or installed-system acceptance yet. The settings/raster tools below remain development components.
The C++17 ticket checker validates settings and emits normalized JSON for development. It does not open a document, contact a service or write to USB. Runtime uses system C++ libraries only; Python is used only for development tests. Missing options use A4/colour/Normal. Explicit unsupported values, repeated options and malformed requests fail with exit 2 and no success output. IPP High maps to Fine; input dpi is intentionally unspecified. The JSON is a diagnostic CLI format, not an IPP implementation.

Build and test from repository root (generated executable stays outside Git):

```sh
xcrun clang++ -std=c++17 -arch arm64 -Wall -Wextra -Werror -pedantic native/ticket_check.cpp -o /private/tmp/brother-ticket-check
python3 native/test_ticket.py /private/tmp/brother-ticket-check
```

Future IPP callbacks construct a validated per-job ticket and hand it unchanged to the raster pipeline. `auto` is intentionally rejected until its semantics are implemented; this is separate from the existing Docker fallback, which supports it. No prototype capabilities are advertised to macOS yet.

Next: synthetic raster fixture source, conversion-only decoder research after provenance checks, native file-sink service, then encoder/USB integration and physical acceptance. A pkg must wait for a functional native path; wrapping this checker in an installer would not create printer support.

## Bounded raster-input prototype

`ppm_reader.hpp` reads one deliberately restricted P6 test image: LF-only three-line header, one space between decimal width/height, maxval 255 and exactly width × height × 3 payload bytes. It rejects comments, other PPM variants, concatenated pages and trailing data. This is a private test interchange contract, not a general PPM decoder or Brother stream decoder. Header lines are limited to 63 bytes, dimensions to 10,000 each, and payload to 128 MiB. The 64-bit size calculation precedes allocation. Raster storage is at most 128 RGB rows (3,840,000 bytes at maximum width); this is not a measurement of whole-process RSS.

The consumer receives page dimensions, starting row, row count and bytes synchronously; the buffer is reused after return. Exceptions propagate. Earlier bands can be consumed before truncation/trailing-data errors are found: use a discard/transactional file sink for research, never connect this unchecked stream directly to USB. There is no cancellation, timeout, document-level transaction or production transport yet.

Build and exercise with memory/undefined-behaviour sanitizers:

```sh
xcrun clang++ -std=c++17 -arch arm64 -Wall -Wextra -Werror -pedantic -fsanitize=address,undefined -fno-omit-frame-pointer native/raster_check.cpp -o /private/tmp/brother-raster-check
PYTHONDONTWRITEBYTECODE=1 python3 native/test_raster.py /private/tmp/brother-raster-check
```

`raster-check` emits dimensions, byte/band counts and FNV-1a-64 of payload bytes only after the entire input passes. FNV is a test diagnostic, not a security checksum. Fixture manifests use SHA-256 of the complete file and generator source.

`generate_raster.py` generates white, black, eight colour patches, neutral ramp, alternating-pixel and row-marker patterns using only Python's standard library. Defaults deliberately use odd dimensions and a partial final band. Samples have no embedded profile/dpi; manifest explicitly avoids a colourimetric interpretation. They do not yet cover PDF text, calibrated colour, media margins or multipage documents. Source-only generators are committed; output remains outside Git.

Example (use a new filename; generator refuses to overwrite):

```sh
python3 native/generate_raster.py /private/tmp/brother-patches.ppm --pattern patches --width 257 --height 259
/private/tmp/brother-raster-check /private/tmp/brother-patches.ppm
```

Reference for the restricted fixture container: [Netpbm PPM specification](https://netpbm.sourceforge.net/doc/ppm.html), reviewed 2026-10-25. Full PPM supports variants this prototype deliberately rejects.

## Native CUPS filter and installer

`cups_filter.cpp` accepts CUPS raster from macOS cgpdftoraster, validates media/colour/quality/geometry, restores the imageable rectangle on a white full-page raster and emits observed PJL framing plus standard PWG Raster. It uses one row of input/output buffers and a private anonymous disk staging file capped at 512 MiB, validating the job before any backend output. Maximum 1000 input pages and 99 copies, with aggregate output bounded to 512 MiB. Cancellation is checked while converting/copying; transport outcomes after partial output remain uncertain and the setup queue uses abort-job rather than automatic retries. Error messages exclude user titles/paths. No calibrated colour or black-ink-only claim.

The PPD exposes plain, one-sided A4/Letter, colour/monochrome and Draft/Normal/Fine at 300 dpi. Setup uses a separate native queue and never prints automatically. Legacy PPD integration is an interim choice, not PAPPL/IPP completion. See ADR 002.

```sh
xcrun clang++ -std=c++17 -arch arm64 -mmacosx-version-min=14.0 -Wall -Wextra -Werror -pedantic -fsanitize=address,undefined -fno-omit-frame-pointer native/cups_filter.cpp -lcups -o /private/tmp/brother-t220-native-asan
xcrun clang++ -std=c++17 -arch arm64 -O2 -Wall -Wextra -Werror -pedantic native/inspect_test_prn.cpp -lcups -o /private/tmp/brother-inspect-test-prn
PYTHONDONTWRITEBYTECODE=1 python3 native/test_cups_pipeline.py /private/tmp/brother-t220-native-asan /private/tmp/brother-inspect-test-prn
PYTHONDONTWRITEBYTECODE=1 python3 native/test_setup_helper.py
native/packaging/build-pkg.sh
PYTHONDONTWRITEBYTECODE=1 python3 native/test_package.py native/dist/Brother-T220-Native-0.1.0-development.pkg
```

`generate_pdf.py` is an owned two-page vector PDF fixture generator. `ppm_to_test_raster.cpp` bridges owned PPM fixtures into CUPS raster for development comparisons. `inspect_test_prn.cpp` is only a synthetic-fixture decoder/inspector, not a general security parser and not shipped. Tests never call lp, create a real queue or print. The installed runtime has no Python, Docker, Homebrew or vendor-binary dependency.
