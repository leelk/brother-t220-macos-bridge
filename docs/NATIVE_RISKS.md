# Risks, decisions and stop conditions

| Risk | Response / owner milestone / gate |
|---|---|
| Unknown or model-specific protocol | M1/M2 prove decoding/framing and all mode coverage before USB; stop native encoder route if infeasible |
| Brother license restrictions | M1 rights ledger and qualified review where needed; no redistribution or restricted analysis without clearance |
| No repository license | Owner decision before importing implementation; dependency audit before distribution |
| PAPPL macOS/USB or PDF gaps | M3 arm64 file-sink and USB spike; compare alternatives in NATIVE_ARCHITECTURE.md |
| Colour/quality differs from vendor | M2/M4 controlled patches, measured geometry and physical quality gates; no unsupported accuracy claims |
| Generic IPP capabilities mislead UI | M3 truthful capabilities + app matrix; reject unsupported requests |
| CPU/RAM exceed goals | M4 bounded bands, backpressure and measured budgets; avoid persistent renderer/GUI |
| USB ownership conflicts | M3 one transport owner; preserve fallback, never parallel writes |
| Disconnect or crash duplicates output | M3 persist job state, uncertain outcome visible, no automatic replay |
| launchd permissions/sandbox issues | M5 prove dedicated-account access and service-context renderer on clean machine |
| Signing credentials unavailable | M5 development artifacts only; signed/notarized release remains blocked |
| Deprecated macOS printing interfaces | M3 prefer driverless IPP; verify oldest/latest OS before support claims |
| Secrets/documents leak | Explicit staging, private spool, redaction and ignore rules; review tree/diff before every push |

## Decision log

2026-10-25: retain working Docker fallback unchanged. Prefer PAPPL plus independent arm64 encoder conditionally, not as an established implementation decision. No native converter, pkg, protocol specification or USB backend is verified. No scanner/duplex/photo-media promises. M0 is the only research performed in this change.

At each gate record decision, evidence, alternatives, owner and date. Unknown rights, unsafe framing, destructive commands, unexplained mode differences or unbounded memory prevent advancement to the affected stage. Continue independent documentation/public-source work when a gate is blocked. See NATIVE_BACKLOG.md for dependencies.
