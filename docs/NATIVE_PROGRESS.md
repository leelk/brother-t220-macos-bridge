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
