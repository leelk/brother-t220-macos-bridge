# Performance targets and benchmark protocol

All numbers below are provisional acceptance budgets, not measurements. Reference minimum machine: Apple Silicon M1 with 8 GB RAM, lowest supported macOS, USB-connected DCP-T220. Compare same fixtures and quality against local Docker fallback; report Docker VM separately from bridge processes.

| Metric | Proposed gate |
|---|---|
| Idle service RSS / total native processes | ≤30 MiB / ≤50 MiB with GUI closed |
| Idle CPU | <0.5% of one core averaged over 10 minutes after warmup |
| Idle activity | No conversion work, no busy polling; report wakeups and energy impact |
| Active aggregate peak RSS | ≤200 MiB for 100-page standard fixture; independent of document length within measurement noise |
| Converter speed | ≥1 A4 Normal colour page/s at validated 300 dpi on M1; report actual mode/input dpi |
| First-page host processing | ≤3 s warm, ≤5 s cold, excluding physical printer warmup/feed |
| Cancellation | Stop further host writes within 2 s, excluding bytes already buffered by device |
| Spool limit | Configurable 512 MiB total default, reject/hold safely before disk exhaustion |
| Retained artifacts | No raster/print payload after terminal job cleanup; bounded diagnostics ≤10 MiB |

Use Instruments/time/ps/vm measurements in a dedicated benchmark harness; no production sampling loop. Record hardware, RAM, macOS, build flags, commit, dependency versions, power mode and fixture seed/hash. Five cold and five warm runs per mode, median/p95/max and failures, plus 10-minute idle and 100-page endurance. Measure input render, conversion and transport independently and end-to-end wall time. Count service children and renderer memory, not just one process. Account for queued PDF spool growth separately from raster working set.

One uncompressed baseline RGB A4 page is 2480×3507×3 = 26,092,080 bytes; a 128-row RGB band is 952,320 bytes, before decoder/colour/codec state. Streaming reduces allocation only if upstream renderer and protocol allow it; measure both. Bound in-flight bands and queued jobs; backpressure rather than unbounded parallelism. If a gate fails, profile and revise design or document a justified revised budget before release; never relabel an unmeasured target as achieved.
