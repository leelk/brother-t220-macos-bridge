# Native implementation progress

2026-10-25: normal driver installation is now the delivery priority. No installable driver exists yet.

## Official Mac path check

Brother's exact-model [FAQ dated 2026-01-15](https://support.brother.com/g/b/faqend.aspx?c=ae&faqid=faq00100732_000&lang=en&pfs=1&prod=dcpt220_all) says DCP-T220 printing requires iPrint&Scan even after the Full Software Package is installed. The indexed [Mac download list](https://support.brother.com/g/b/downloadlist.aspx?c=us_ot&lang=en&os=10083&prod=dcpt220_all) directs users to iPrint&Scan and reports no AirPrint support. The list returned 403 on direct refetch; the exact-model FAQ was directly retrieved. These sources support pursuing our own Cmd+P integration; no current vendor installer was downloaded or inspected, so its component inventory/architectures remain unverified.

## First native component

Added native/job_ticket.hpp and a native arm64 ticket-check CLI, with native/test_ticket.py development contract checks. Validates A4/Letter, colour/monochrome and standard IPP quality 3/4/5 (High maps to Fine). Defaults and error paths are explicit; there is no transport or document processing. This begins the pure T31 normalization portion independently of PAPPL integration, without declaring M1 or M3 complete.

Validation: compiled with Apple clang++ as Mach-O arm64 using C++17 and strict warnings; 29 native CLI contract checks passed. Generated executable remains in /private/tmp, outside Git.

No vendor code copied/executed, no print submission, queue/service installation or fallback modification. Project-owned code uses Apache-2.0. Remaining provenance/terms, protocol, dependency and hardware gates still apply.

## Delivery order

Finish provenance/public research and generate owned fixtures → independent protocol decoder/encoder → native raster/file-sink IPP prototype → serialized USB and physical tests → launchd/package/rollback → signing/notarization and clean-Mac acceptance. Packaging is a delivery gate for a functioning native path, not a substitute for it.

## Raster-input and source fixture checkpoint — 2026-10-25

Added native/ppm_reader.hpp, raster_check.cpp, generate_raster.py and test_raster.py. This begins T20 (owned synthetic raster patterns) and the bounded raster-input interface portion of T40 without depending on vendor execution. It does not decode or encode Brother commands. See native/README.md for exact input restrictions and consumer safety boundaries.

Validation: arm64 C++17 build with strict warnings, AddressSanitizer and UndefinedBehaviorSanitizer passed 27 raster integration checks plus deterministic fixture regeneration and independent payload hash comparisons. Coverage includes six patterns, odd dimensions, a partial final band, initial payload whitespace/hash bytes, malformed/oversized/truncated input, trailing data, missing file and A4-sized input. The 2480×3507 fixture carries 26,092,080 RGB bytes in 28 bands, largest 952,320 bytes. This is observed buffer sizing, not total memory/CPU benchmarking. Existing 29 ticket checks and seven mocked fallback tests also passed.

No generated fixtures, executables or logs are committed. No printer, vendor binary, Docker process, service or queue was used or changed. M1 provenance/current terms, native protocol research, PDF/IPP integration, USB transport and signed package gates remain open. T20/T40 remain partial; fixtures do not yet cover the full planned matrix.

## Native development installer checkpoint — 2026-10-25

Official reference-package provenance/current agreement were resolved; 12 small plus 12 full-page black-box reference conversions performed with no hardware access. Full-sized swatch decoded pixel bytes match native output in all 12 settings. Added native CUPS filter, owned PDF fixtures, model PPD, Swift setup app, versioned development package builder and offline/package/helper checks. Runtime uses only macOS libraries/services. See NATIVE_PROTOCOL_FINDINGS.md, NATIVE_ADR_002.md, NATIVE_INSTALLATION.md and NATIVE_RELEASE_STATUS.md for evidence and exact limitations.

This supersedes earlier statements that only a settings/raster prototype exists. It does not mean the native driver is finished: physical printing is explicitly on hold, visual/installed-system validation was not possible here, and no Apple Developer account is available for signing/notarization. Generated package is local and ignored; source/tests/docs only are committed. Existing Docker fallback and system queues remain unchanged.

## Installation and documentation follow-up — 2026-10-25

The user installed 0.1.0 and supplied an Installer success screenshot. Read-only checks confirm the package receipt and installed native filter; Brother_T220_Native is absent, so setup is pending. This supersedes the checkpoint's earlier not-installed state without changing physical/visual/reboot acceptance. README is now native-first, full fallback instructions are preserved in DOCKER_FALLBACK.md, and NATIVE_INSTALLATION.md/TROUBLESHOOTING.md cover setup, restart behavior, settings, rollback/removal, trust and issue reporting. No runtime changes or print submissions were made for this documentation update.
