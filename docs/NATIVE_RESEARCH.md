# Protocol research and legal precautions

## Authorization boundary

M0 permits source review, file metadata/hash inventory and mocked tests only. No vendor execution, disassembly, stream capture, USB writes, queue changes or software installation. Subsequent milestones require completion of their license and safety gates. Locally possessing an executable is not redistribution permission.

## M1: rights and feasibility

1. Locate the original Brother download page, package version, accompanying license and jurisdiction-specific restrictions. Record URLs, retrieval date, package hash and a prose summary in a sanitized ledger; do not copy proprietary text or binaries into Git.
2. Review reverse-engineering/interoperability permissions and any restrictions before execution, tracing or disassembly. Obtain qualified advice where rights are uncertain. Stop restricted techniques while reviewing public specifications/open drivers and the project’s own code. This plan is not legal clearance.
3. Audit repository licensing: no project license is currently tracked. Select a license with the owner before importing implementation code. Record SPDX identifiers, dependency versions, linkage obligations, notices and source-offer requirements. Check PAPPL and all transitive libraries; Ghostscript reuse needs a separate license decision.
4. Search primary Brother documentation and open driver source for exact device/protocol support. Similar model names are hypotheses only. Publish original behavioral specifications, not copied proprietary code or reverse-engineered confidential material.
5. If permissible, use an isolated local oracle running the separately acquired converter, with no network and no printer transport. Never bundle it with the native app or CI. Any disassembly requires an explicit rights decision recorded first. Separate observation notes/specification from independently written implementation where practical; record provenance of every finding.

## M2: controlled experiment plan

Generate synthetic references from source (NATIVE_TEST_MATRIX.md). Vary one factor at a time: blank/solid/single-channel/alternating rows, dimensions, page count, media, colour and quality. Hold renderer/config/version constant. Repeat identical conversions to detect timestamps/non-determinism before comparing bytes.

Keep outputs private and ignored; record hashes, sizes, offsets and original descriptions only when publishable. Infer job/page headers and trailers, byte order, lengths, compression, planes/channel order, row stride, colour transforms, dithering and quality-specific behavior. Build a decoder/validator from observed structure before an encoder. Use local oracle output to verify independent decoding, then compare decoded raster semantics; byte equality alone is neither required nor sufficient.

Every protocol rule must cite experiment IDs, confidence (observed/inferred/unresolved), counterexamples and supported modes. Maintain a coverage table for A4/Letter × two colours × three qualities. Do not guess USB control/status commands. Start physical testing only with reviewed framing, bounded writes, cancellation and a recovery plan; exclude firmware, maintenance and EEPROM commands.

## Primary references reviewed 2026-10-25

- PAPPL overview and dependency/license claims: https://www.msweet.org/pappl/ ; pin and verify the actual source release later.
- IPP semantics and quality enums: https://www.rfc-editor.org/rfc/rfc8011.html
- Apple notarization workflow: https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution

These references establish architecture context, not Brother protocol compatibility or legal permission. Record future Brother source URLs only after locating the exact package/license; do not invent them.
