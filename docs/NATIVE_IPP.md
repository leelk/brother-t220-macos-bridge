# IPP/PAPPL and macOS integration

## M3 spike

Pin PAPPL plus transitive dependency versions and build native arm64 on the oldest target SDK. Confirm actual raster/PDF input paths and USB backend support on macOS. PAPPL overview lists raster/image/raw formats; PDF rendering must be provided or delegated deliberately. Prove a synthetic job reaches a nonprinting file sink before connecting transport. No shipping path may depend on Homebrew tools or system ippeveprinter availability.

## Truthful capabilities

| IPP field | Required behavior |
|---|---|
| color-supported | true only with functioning colour path |
| print-color-mode-supported/default | color, monochrome; default color; auto only if semantics tested |
| print-quality-supported/default | 3/4/5, default 4; high maps to Fine |
| media-supported/media-col-database | iso_a4_210x297mm, na_letter_8.5x11in with measured margins |
| printer-resolution | only validated input modes; remove existing generic 600 dpi mismatch |
| document-format-supported | only tested decoders/renderers |
| sides-supported | one-sided |
| printer-state/reasons | truthful offline, processing, error and readiness states |

Validate job options consistently with IPP fidelity/unsupported-attribute rules, including malformed media and mode combinations. Implement Get-Printer-Attributes, Validate-Job, Print-Job, Get-Jobs/Get-Job-Attributes and Cancel-Job; investigate Create-Job/Send-Document requirements before advertising them. A multipage PDF is distinct from a multi-document IPP job.

Bind to loopback only by default; choose a stable configurable port without colliding with fallback 8631. Disable LAN advertisement unless intentionally designed. Verify driverless explicit URI registration and any local discovery behavior. Persist queue identity across updates; capability changes trigger a controlled refresh after saving user defaults, never deletion of the physical fallback queue.

## UI and transport acceptance

Use fresh/default presets in Preview and a second Cmd+P app. Colour source must retain colours when colour is selected; monochrome and media previews must reflect selection where macOS supports it. Document application-specific behavior; no promise of calibrated paper matching. Capture sanitized screenshots only with synthetic content.

Compare PAPPL/libusb transport against a CUPS USB pass-through bridge on macOS. Choose one owner of the USB interface; never have fallback and native jobs writing simultaneously. Handle partial writes, bounded timeouts, unplug/replug, sleep/wake and cancellation between bands. Map conversion failure to failed IPP job. If bytes may already have reached the printer, report uncertain outcome and require explicit user retry to avoid duplicates. Distinguish transfer complete from device-confirmed print complete. Do not fabricate ink/status telemetry.
