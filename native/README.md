# Native prototype

Status: first native component only; no printer driver, service or installer yet.
The C++17 ticket checker validates settings and emits normalized JSON for development. It does not open a document, contact a service or write to USB. Runtime uses system C++ libraries only; Python is used only for development tests. Missing options use A4/colour/Normal. Explicit unsupported values, repeated options and malformed requests fail with exit 2 and no success output. IPP High maps to Fine; input dpi is intentionally unspecified. The JSON is a diagnostic CLI format, not an IPP implementation.

Build and test from repository root (generated executable stays outside Git):

```sh
xcrun clang++ -std=c++17 -arch arm64 -Wall -Wextra -Werror -pedantic native/ticket_check.cpp -o /private/tmp/brother-ticket-check
python3 native/test_ticket.py /private/tmp/brother-ticket-check
```

Future IPP callbacks construct a validated per-job ticket and hand it unchanged to the raster pipeline. `auto` is intentionally rejected until its semantics are implemented; this is separate from the existing Docker fallback, which supports it. No prototype capabilities are advertised to macOS yet.

Next: synthetic raster fixture source, conversion-only decoder research after provenance checks, native file-sink service, then encoder/USB integration and physical acceptance. A pkg must wait for a functional native path; wrapping this checker in an installer would not create printer support.
