# M0: initial read-only research findings

Date: 2026-10-25 (Asia/Colombo). Planning commit: `2948482`. Inspected baseline: `958606860eb9e9d08cccdbbbd64a1a60a53161ca`. Native support is not implemented or proven feasible.

## Repository and environment

Actual project is `/Users/leel/brother-driver-research`, distinct from the chat workspace. Initial working tree was clean on main; origin points to https://github.com/leelk/brother-t220-macos-bridge.git . Remote main matched the full baseline SHA before changes. No applicable AGENTS.md was found at the project or directly checked parent locations. Host reports arm64, macOS 27.0.1 (26A434).

Tracked source was inspected: README, Dockerfile.brother, brother-bridge.py, convert-brother.sh, start-brother-service.sh, callback, existing plans and mocked tests. No project LICENSE file is tracked. Existing proprietary archives/extracted files and generated test/log artifacts are local ignored material and were not staged.

## Observed implementation

The callback reads IPP colour/quality environment values, normalizes quality 3/4/5 and invokes Python. Python converts to one temporary printer stream, checks nonempty output and submits through lp raw to Brother_T220_Test. Successful submission establishes queue acceptance only.

The shell converter uses a per-job copy of vendor configuration and maps colour/auto to FullColor, monochrome to Mono, and draft/normal/high to Draft/Normal/Fine. It fixes A4 and invokes Ghostscript in a network-disabled linux/amd64 Docker container at 300 dpi, 2480×3507 RGB. It invokes the vendor converter per raster page and concatenates results into one stream. All raster pages are generated before conversion, creating document-sized temporary storage; lexical page glob ordering can become incorrect after page 999. No native code or native installer exists.

The startup script starts system ippeveprinter manually on 8631 with PDF input and colour speed enabled. No launchd installation is tracked. Existing README reports generic 600 dpi advertisement despite actual 300 dpi conversion and no media mapping. Existing callback logs input paths; future native diagnostics must avoid this privacy issue. No fallback runtime files were changed.

## Binary metadata only

`file` identifies the i686 converter as a dynamically linked 32-bit Intel Linux ELF and the x86_64 converter as a dynamically linked 64-bit Intel Linux ELF, not stripped. The latter uses the Linux loader `/lib64/ld-linux-x86-64.so.2`; these are not native arm64 Mach-O executables. This establishes incompatibility with direct native execution, not protocol complexity or reverse-engineering permission.

Local x86_64 converter SHA-256: `68e0f0aa275e0a98ba885a0c221f4c13bccdaba2a179e996ed8c138b47b6008a`. This identifies the observed local file, not an authenticated vendor download. Package provenance/license must be established at M1. No binary bytes, symbols, strings, disassembly or vendor configuration contents are included here. No vendor executable was run.

## Validation performed

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`: **7 tests passed**, 10.092 seconds. Tests use temporary copies and fake Docker/lp commands; no real printing or converter execution. They cover default/explicit colour and quality, invalid values, direct converter default and per-job configuration isolation. They do not validate native conversion, actual IPP UI, USB, colour fidelity or physical quality.

Read-only source/metadata checks and mocked tests made no queue, printer, service, Docker image or proprietary-file modifications. No captures, installation, firmware operations, print submissions or live service restarts were performed. Initial inventory is complete; deeper protocol research is pending.

## Evidence limits and next step

Existing README/COLOR_PREVIEW.md report prior physical colour and a user-confirmed Preview colour thumbnail. These are historical reports, not repeated physical/UI verification today. Monochrome, Fine improvement, Letter and broader multipage physical acceptance remain open.

Next is M1/T10–T13 in NATIVE_BACKLOG.md: exact package/license provenance, project/dependency licensing, exact-model public protocol/open-driver research and a reviewed experiment plan. No proprietary oracle execution or native implementation should be inferred from M0. Signing credentials, clean-machine coverage and real hardware acceptance are future gates.
