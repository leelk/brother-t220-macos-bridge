# Milestones and step-by-step issue backlog

Status 2026-10-25: M0 initial inspection performed; M1 provenance/terms resolved for scoped conversion experiments; native CUPS development candidate built. M2–M5 have partial offline evidence, not release acceptance. See NATIVE_RELEASE_STATUS.md and ADR 002; PAPPL integration and physical/signed-release gates remain pending. These are issue-ready task specifications, not GitHub issues already created. Owner defaults to project maintainer; license selection and release credentials require owner input when reached.

## M0 — read-only inventory (first safe milestone)

- T00: inspect Git status/remotes/history and tracked source; identify baseline and stale plans.
- T01: inspect executable metadata and hash only; inspect converter data path without running vendor code.
- T02: run existing tests with mocked Docker/lp and no print submissions; document sanitized results.
- T03: verify remote branch and publish findings after planning commit.

Acceptance: clean initial baseline identified, implementation limits stated, seven mocked tests reported accurately, no queue/process/USB/vendor-file changes. This is an initial inventory, not protocol reverse engineering or proof of native feasibility.

## M1 — legal/public research and feasibility (after M0)

- T10: scoped source/license/provenance inventory completed; official package matched, current terms reviewed. See NATIVE_PROTOCOL_FINDINGS.md.
- T11: select repository license with owner; audit candidate dependencies and notices.
- T12: inspect public protocol/open driver support for exact model; compare alternatives and record ADR.
- T13: write controlled oracle experiment specification with allowed techniques, fixtures and review gates.

Acceptance: rights/provenance ledger and dependency audit reviewed; explicit go/no-go for oracle experiments; evidence-backed architecture choice. If rights are unclear, keep restricted techniques blocked and use public-source alternatives.

## M2 — protocol characterization (after M1 gate)

- T20 (partial): six deterministic raster patterns and SHA-256 source/file manifests implemented; PDF/text/geometry/multipage fixtures and full manifest schema remain pending. See NATIVE_PROGRESS.md.
- T21 (partial): small and full-page 12-mode conversion-only experiments completed, private artifacts retained; broader pattern/repeatability corpus pending.
- T22: write original protocol observations with confidence and coverage; distinguish known from guessed fields.
- T23: build independent decoder/validator, establish page/job framing, channels, compression and each quality/media mode.

Acceptance: decoded semantics and 12-mode coverage explained, framing/trailers validated, no unexplained mandatory bytes; review before any printer writes. No claim of physical success yet.

## M3 — native integration spike (after M2 framing review; file-sink work may follow M1 independently)

- T30: build pinned PAPPL/dependencies arm64 with license notices; prove file-sink raster job.
- T31 (partial): native ticket normalization CLI implemented and 29 contract checks pass; IPP callback integration, immutable handoff and truthful capability tests remain pending. See NATIVE_PROGRESS.md.
- T32: compare renderer/input options and USB backends; record ADR with permissions and deployment target.
- T33: implement serialized transport, partial-write/cancel/disconnect handling; reviewed minimal physical test.
- T34: test loopback driverless queue and Preview/second-app option propagation.

Acceptance: native service receives Cmd+P jobs into file sink; correct 12-mode ticket mapping; selected USB transport safely sends reviewed stream and reports uncertainty without replay. Any physical evidence explicitly dated. No replacement of fallback.

## M4 — independent streaming encoder and fidelity (after M2/M3)

- T40 (partial): restricted P6 reader with checked dimensions/payload limits and synchronous 128-row interface implemented; media geometry, cancellation and production raster formats remain pending.
- T41 (partial): standard system PWG encoder plus independently authored observed PJL framing implemented; 12 full-page swatch decoded pixel comparisons pass. Physical acceptance and broader corpus pending; no custom proprietary compression needed.
- T42: add decoder round trips, fuzz/sanitizer/error/cancellation tests and per-job isolation.
- T43: execute 12-mode physical matrix, multipage/order/scale and UI preview tests.
- T44: benchmark cold/warm/idle/endurance and fix budget failures.

Acceptance: all converter, physical and performance gates in linked plans pass; Linux converter/Docker absent from native runtime; unresolved fidelity modes cannot be advertised.

## M5 — startup, installer and recovery (after M4; design/spike can begin after M3)

- T50: finalize service account/LaunchDaemon or scoped LaunchAgent ADR; prove USB and renderer access.
- T51: implement app/setup, private spool, bounded diagnostics, health and backoff.
- T52 (partial): development pkg, setup app, pending-job/ownership guards and saved prior-queue rollback implemented; 17 mocked helper scenarios pass. Full uninstall, transactional upgrade journal and installed-system recovery acceptance pending.
- T53: sign with Developer ID identities, notarize, staple, verify and archive reproducible release metadata privately.
- T54: test clean Mac install/reboot/update/failed update/uninstall/fallback recovery.

Acceptance: signed/notarized pkg works on supported clean Macs without developer dependencies; one service starts automatically in documented scope; rollback demonstrably restores prior version/fallback without duplicate jobs or unrelated changes.

## M6 — release readiness (after M5)

- T60: complete oldest/latest OS and multi-user matrix, final dependency/SBOM/license/security review.
- T61: publish user setup/troubleshooting/limitations and exact version rollback instructions.
- T62: stage a candidate artifact, verify signature/remote source tag and collect final physical acceptance evidence.

Acceptance: every required outcome in NATIVE_PLAN.md has dated pass evidence, reproducible build provenance and available signed package; no open critical safety/fidelity failures. Only then describe native support as complete.
