# Native DCP-T220 delivery plan

Date: 2026-10-25. Status: early native prototype; settings validation only, no driver/service/installer. Baseline: `958606860eb9e9d08cccdbbbd64a1a60a53161ca`.

## Scope and authority

Build an independent native arm64 macOS printer application installable on a new Apple Silicon Mac through a signed, notarized, stapled `.pkg`. Runtime must require neither Docker nor separately installed Python, Homebrew or Brother Linux software. Preserve all current fallback scripts, queues and local driver files. No native release is promised before protocol feasibility and physical acceptance.

This plan supersedes forward-looking guidance in IMPLEMENTATION_PLAN.md for native work. COLOR_PREVIEW.md remains historical evidence for the fallback. Existing README instructions continue to describe Docker only.

## Documents

1. [Architecture and alternatives](NATIVE_ARCHITECTURE.md)
2. [Protocol research and licensing gates](NATIVE_RESEARCH.md)
3. [Fixtures and acceptance matrix](NATIVE_TEST_MATRIX.md)
4. [Native raster converter](NATIVE_RASTER.md)
5. [IPP, PAPPL and macOS integration](NATIVE_IPP.md)
6. [Packaging, startup and rollback](NATIVE_PACKAGING.md)
7. [Resource budgets and benchmarks](NATIVE_PERFORMANCE.md)
8. [Risks and decisions](NATIVE_RISKS.md)
9. [Milestones and ordered issue backlog](NATIVE_BACKLOG.md)
10. [First read-only milestone findings](NATIVE_M0_FINDINGS.md)

11. [M1 provenance and public research findings](NATIVE_M1_FINDINGS.md)
12. [Candidate dependency/license ledger](NATIVE_DEPENDENCIES.md)
13. [Conditional architecture ADR](NATIVE_ADR_001.md)
14. [Controlled oracle experiment specification](NATIVE_ORACLE_EXPERIMENTS.md)

15. [Native implementation progress](NATIVE_PROGRESS.md)

## Required outcomes

Cmd+P from Preview and a second application; colour preview consistent with colour selection and supported capabilities; colour/monochrome; independent per-job Draft/Normal/Fine (standard IPP High maps to Fine); A4/Letter; ordered multipage PDF jobs; USB; automatic launchd startup; recoverable updates and uninstall/rollback. Accurate preview means correct source colours, geometry and selected mode within normal display limitations, not an unqualified screen-to-paper colourimetric guarantee. Physical colour accuracy needs separately measured profiling.

Initial compatibility target: macOS 14 and newer on arm64, subject to SDK/dependency verification; validate oldest supported and latest public release at shipment. Only macOS 27.0.1 is observed here. Do not advertise compatibility with versions not tested. Exclude scanning, duplex, borderless, photo media, remote network printing and vendor ink monitoring from v1 unless separately researched and accepted.

## Release rule

All milestone gates must have dated evidence. Mock tests do not establish printer compatibility, nonempty streams do not prove protocol correctness, queue submission does not prove physical completion, and notarization does not prove functional correctness. Never replace the working fallback on the strength of these plans.
