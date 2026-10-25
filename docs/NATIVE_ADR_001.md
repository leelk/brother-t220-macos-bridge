# ADR 001 — conditional independent converter route

Date: 2026-10-25. Status: provisional, not a completed feasibility decision.

## Decision

Continue read-only official-driver verification first. If no supported native Cmd+P solution satisfies requirements, evaluate PAPPL plus an independently authored arm64 encoder, using a locally acquired, provenance-checked Linux converter solely as a conversion-only reference where terms permit. Maintain separate protocol observations and implementation; no binary redistribution or copying wrapper source.

## Evidence and alternatives

Local converter is Intel Linux ELF, so direct native execution does not meet the requirement. Local agreement has affirmative modification permissions, but download provenance/current terms remain unresolved. No exact DCP-T220 support was found in the reviewed Gutenprint list. PAPPL supplies an IPP framework, not the missing model-specific raster encoder; native PDF rendering and USB must still be proven. See NATIVE_M1_FINDINGS.md and NATIVE_DEPENDENCIES.md for primary sources and limitations.

Official Mac software is a serious alternative to check: regional listings are insufficient to establish system print-dialog support. Inspect exact model/architecture/package components and supported workflow without installing or accepting new terms automatically. If a vendor native driver meets Cmd+P, quality, media, resource and distribution goals, document the simpler path and reconsider replacement work. Do not infer that iPrint&Scan alone supplies a driver.

Custom IPP, legacy PPD and emulated Linux remain alternatives in NATIVE_ARCHITECTURE.md. None is selected for shipping. Preserve the working Docker baseline independently.

## Revisit / acceptance

Finalize only after exact vendor download provenance/current terms, project license choice, official Mac alternative review and a successful arm64 PAPPL file-sink spike. Protocol feasibility requires independent decoding and all-mode evidence, followed by physical gates. A provisional architecture does not authorize disassembly or USB experiments. This ADR permits no release or native-completion claim.
