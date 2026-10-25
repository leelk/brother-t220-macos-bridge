# Controlled conversion-only experiment specification

Date: 2026-10-25. Status: ready for review; not executed. Depends on M1 provenance/terms gate. This specification does not grant legal clearance.

## Preflight and containment

1. Obtain exact official DEB/source URL and applicable license legitimately; record version, complete package SHA-256 and date privately, then publish only sanitized provenance. Compare archive license and converter hashes with local material; unexplained differences stop experiments.
2. Confirm applicable terms permit planned execution/observation; record go/no-go and unresolved restrictions. No disassembly/tracing is required for this phase. Preserve vendor files read-only and avoid importing code into the native project.
3. Use the existing conversion environment only after verifying its image identity and tool versions. Network disabled, vendor mount read-only, private temporary workspace; no USB devices, printer backend, lp callback or privileged container. Never invoke brother-bridge.py or the printing callback for oracle runs.
4. Run explicitly bounded one-page conversions first with timeout, disk/output cap and separate job config. Retain diagnostics privately only as necessary. Stop on excessive memory/disk use, nondeterminism or unexplained executable behavior. Record no customer data.
5. Keep output outside tracked directories or in ignored test-output; never stage generated PDF/PPM/PRN, vendor data, logs or captures. Maintain a human-reviewed allowlist of published summaries.

## Experiment sequence

| ID | Input / controlled change | Question and expected evidence |
|---|---|---|
| E00 | Same tiny blank RGB raster, same mode, three runs | Reproducibility; size/hash differences and volatile-byte hypotheses |
| E01 | White vs black vs one RGB/CMY patch, identical geometry | Candidate colour-plane/framing differences; no assumed protocol |
| E02 | Single changed row/column, odd widths and last partial band | Stride, row/band boundaries and compression hypotheses |
| E03 | One option at a time: colour/mono, Draft/Normal/Fine | Distinct mode behavior; record all combinations without equating quality to dpi |
| E04 | A4 vs Letter at documented input dpi | Page geometry and mode-dependent framing; do not stretch input |
| E05 | Two distinct pages and reversed sequence | Job/page delimiters, trailers and ordering; no physical printing |
| E06 | Repeated rows vs alternating pixels, deterministic seed | Compression/packing hypotheses and counterexamples |

First validate accepted input geometry against the vendor wrapper/documentation where permitted. Tiny synthetic rasters may be rejected or padded by the oracle; a rejection is evidence, not permission to invent a geometry rule. Do not treat concatenation used by the fallback as proof of valid native multipage framing.

## Manifest and publication

Per run record experiment ID, input-generator commit/seed/hash, full ticket, raster width/height/stride/format/profile/dpi, oracle/package/image/tool hashes, exit status, duration, peak resources, output size/hash, and observation confidence. Store environment-specific paths and raw outputs privately. Publish an original concise summary, unresolved questions and independent decoder test criteria after provenance review; never publish proprietary tables or copied code as findings.

Acceptance before encoding: reproducible observations; independently checked job/page framing; channels/packing/compression explained with counterexamples; 12-mode media/colour/quality coverage. Begin with a file-sink decoder/validator. Physical writes require a separate bounded transport/recovery review after framing evidence. No output from this phase is sent to a printer.
