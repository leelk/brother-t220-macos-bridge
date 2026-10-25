# Architecture and alternatives

Status: long-term proposal. The first experimental package uses native CUPS integration selected in NATIVE_ADR_002.md; PAPPL is not yet implemented. See NATIVE_PLAN.md for scope.

## Preferred data path

Cmd+P → macOS driverless queue → loopback IPP service → validated immutable job ticket → raster input or native PDF renderer → banded converter → serialized USB transport → DCP-T220.

A small Swift/AppKit setup/status application manages discovery, readiness and diagnostics. A C/C++ arm64 service hosts a pinned PAPPL version and converter. No persistent GUI is needed for printing. A restricted service account owns a private spool and USB transport; root is reserved for installation and explicitly scoped setup. Final USB permissions and service-account viability are M3/M5 gates.

Keep boundaries explicit: IPP job ID and immutable media/mode/quality ticket; bounded raster band interface with stride/format/dpi; encoder output sink supporting backpressure; transport with cancellation and partial-write accounting. One active USB job per physical device, isolated queued jobs, no byte interleaving. Do not report physical completion if only host transfer is known.

Prefer PWG/Apple Raster from macOS when it preserves required controls and colour. PDF support is a separate renderer integration, not assumed to exist in PAPPL. If needed, evaluate CoreGraphics PDF rendering in a short-lived restricted native worker; prove service-context font, colour and memory behavior. Package every non-system dependency with compatible licenses and arm64 slices.

## Alternatives and decision gates

| Option | Benefit | Cost / decision |
|---|---|---|
| PAPPL + independent encoder | Established IPP framework, native process | Preferred only after macOS arm64/USB/raster spike and license audit |
| ippeveprinter + native callback | Closest to fallback, smaller initial change | Research prototype; installed system version/callback limits must be tested; do not rely on a development utility as a stable shipping dependency |
| Custom IPP server | Full control | Reject initially: protocol/security/conformance burden |
| Legacy CUPS PPD/filter | Familiar USB path | Temporary transport research only; deprecated integration unsuitable as long-term design |
| Existing open driver/Gutenprint | Could avoid reverse engineering | Check exact DCP-T220 support, quality and license first; no assumption of compatibility |
| Vendor native redistribution | Could reduce protocol work | Only if supported arm64 code and explicit rights exist; currently unverified |
| Intel Linux converter under VM/emulation | Existing fallback works | Preserve Docker fallback; violates native runtime/resource goal |

Record ADRs after M1 and M3: chosen protocol route, raster formats, renderer, transport and startup scope, with versions, license evidence, rejected options and measured consequences. Do not couple setup UI to print lifecycle.
