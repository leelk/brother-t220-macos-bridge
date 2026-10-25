# ADR 002 — first installable candidate uses native CUPS integration

Date: 2026-10-25. Status: selected for the experimental 0.1.0 development candidate; long-term driverless IPP application remains pending.

The user prioritized reaching an installable native driver. Observed DCP-T220 output is standard PWG Raster with PJL framing. A small arm64 C++ filter can therefore use system libcups, while macOS cgpdftoraster renders PDF. This removes Docker, the Brother executable, Ghostscript, external Python and third-party runtime libraries from the installed path.

Candidate path: Cmd+P → macOS CUPS PDF renderer → native filter → system CUPS USB backend. A project-owned PPD exposes A4/Letter, RGB/Gray and Draft/Normal/Fine at a truthful 300 dpi input resolution. A Swift/AppKit setup app adds/refreshes or removes only Brother_T220_Native. Queue setup requires exactly one connected USB DCP-T220 and administrator authorization. No test print is automatic.

CUPS starts filters on demand, so the candidate needs no custom launchd service, login item or always-running helper. This meets the automatic-startup intent through the operating system's print service. There is zero additional idle service process when the setup app is closed; full system resource benchmarking is still pending.

Tradeoff: this is legacy PPD/filter integration, which is deprecated and is not the planned driverless IPP/PAPPL application. Only macOS 27.0.1 was tested offline; deployment target 14 is not a compatibility claim. The design deliberately favors a small independently testable installation candidate now. Revisit the PAPPL route before long-term support or when a supported macOS removes this integration. A PAPPL source release was inspected/downloaded temporarily but is neither linked nor shipped.

Installation, rollback, print-dialog preview and physical output are not accepted merely because the package builds. No signed/notarized release can be produced without suitable credentials. User corrected that no Apple Developer account is available; retain a development package and never disable Gatekeeper on their behalf. User explicitly requested no printing, so physical gates remain pending.
