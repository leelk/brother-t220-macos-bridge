# Reference fixtures and test matrix

## Reproducible fixtures

Future fixture generators must be project-owned source with fixed seeds, explicit fonts/licenses and source hashes. Commit generator code and small human-readable expected metadata, not generated PDFs, raster pages, printer streams, captures or logs. Use temporary ignored output directories. Never use customer documents.

| Fixture ID | Contents / purpose |
|---|---|
| F01 | Blank, black/white, RGB/CMY patches; framing and channel order |
| F02 | Neutral ramps, gradients, fine colour lines; colour and dithering |
| F03 | 6–24 pt embedded licensed text and hairlines; quality |
| F04 | A4 and Letter rulers, edge boxes, corners, crop/rotation; geometry |
| F05 | 1/2/10/100 numbered pages with unique markers, plus mixed orientation/media |
| F06 | Alternating pixels/rows, odd widths, partial final bands; packing/compression |
| F07 | Malformed/truncated/oversized/encrypted PDFs and raster lengths; rejection |
| F08 | Two overlapping jobs with opposite modes; serialization/isolation |

Each run manifest records generator commit, seed, fixture hash, input profile, ticket, renderer/encoder version, expected page count/geometry, observer and date. Keep vendor oracle outputs private; publish only reviewed derived facts and independently authored expectations. Hash equality checks reproducibility, decoded comparisons check meaning, physical output checks compatibility.

## Required coverage and evidence

| Layer | Matrix / acceptance |
|---|---|
| Pure converter | A4/Letter × colour/mono × Draft/Normal/Fine = 12 combinations; decode, dimensions, framing, deterministic rules and mode isolation |
| PDF/raster | Tagged/untagged RGB, alpha, gray, rotated/cropped PDF, PWG/Apple raster as advertised; correct orientation and margins |
| Multipage | 1,2,10 physical pages once in order; 100-page synthetic endurance; mixed-size policy explicit; >999-page ordering via mocked sink |
| Cmd+P | Preview + second app, oldest/latest supported OS, fresh/cached queues; preview colour/media and all supported options |
| USB physical | All 12 combinations at least one page; small text, gradients, rulers; compare Normal/Fine; no invented dpi or black-ink-only claims |
| Failures | Unplug before/during/after transfer, partial write, renderer/encoder crash, disk full, cancel queued/active, malformed options, port conflict |
| Lifecycle | Reboot, login/logout, sleep/wake, reconnect, two users, service crash/restart; no duplicate or interleaved prints |
| Distribution | Clean quarantined signed pkg on oldest/latest target; reinstall/update/failed update/uninstall and fallback rollback |
| Resources | NATIVE_PERFORMANCE.md gates for every supported mode; bounded memory and cleanup |
| Security | Loopback binding, private spool, restricted account, dependency/license audit, sanitizers/fuzzing, no document logging |

Required physical geometry tolerance: propose ±1 mm against measured reference after accounting for feed variability; investigate repeated systematic errors. Colour acceptance initially includes correct channels, neutral balance and no clipping/banding in controlled comparison. A colourimetric accuracy claim requires a measured profile, instrument and agreed ΔE criterion; not covered by visual preview alone.

Record pass/fail/not-run with environment, commands, evidence IDs and limitations. Automated CI must use only synthetic inputs/mocks, never vendor binaries, credentials, USB or real print submission. Manual physical results need explicit observer confirmation. Existing seven fallback mocked tests remain regression gates, not native acceptance.
