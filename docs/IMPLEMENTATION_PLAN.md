# Brother DCP-T220 bridge: implementation roadmap

> Historical Docker roadmap (2026-10-24): baseline assertions below predate colour/quality changes. See [native plan](NATIVE_PLAN.md) for current native work and README for fallback behavior.

Status: proposed implementation; no runtime changes in this document.
Date: 2026-10-24. Baseline: `17e6423`.

## Goals and known baseline

Preserve confirmed physical full-color printing while fixing monochrome macOS print previews, exposing per-job Draft/Normal/Fine quality in Cmd+P, and starting the bridge reliably at user login.

Current path: macOS driverless IPP queue → `start-brother-service.sh` / `ippeveprinter` → `ipp-test/print-job.sh` → `brother-bridge.py` → `convert-brother.sh` → Docker/Ghostscript/Brother filter → raw `Brother_T220_Test` USB queue.

- `start-brother-service.sh` uses port 8631, PDF input and `-s 10,5`; this already requests color capability through a nonzero color speed. Do not assume color is wholly unadvertised.
- `convert-brother.sh` fixes A4, `BRResolution=Normal`, and `BRMonoColor=FullColor` in a temporary copy of the vendor configuration. Ghostscript uses color `ppmraw`, 300 dpi, and a fixed 2480×3507 raster.
- The wrapper and Python bridge currently forward only the PDF path; no job-option mapping exists.
- Multipage conversion invokes the filter once per page and concatenates its output; correct physical page boundaries and ordering still need verification.
- `config/Brother_T220_Test.ppd` belongs to the raw physical transport queue, not the driverless virtual printer. Editing it alone is not a preview fix.
- Launch is manual; Docker and the conversion image must already be ready. Existing diagnostic scripts can retain documents and logs locally.

## 1. Establish a reproducible baseline

Record locally the macOS, CUPS/ippeveprinter and Docker versions, queue configuration and defaults, image identity, and current commit. Use a synthetic A4 PDF with RGB swatches, grayscale, small text, gradients and numbered pages. Reproduce monochrome preview in Preview and at least one other Cmd+P application; distinguish the print-dialog preview from the source PDF view. Record physical color as already confirmed, then repeat a controlled baseline before runtime edits.

Inspect installed `ippeveprinter` help/manual and its actual callback behavior before choosing configuration flags or environment handling. Upstream features may differ from Apple's installed build. Save queue settings privately for rollback; do not publish machine identifiers or spool content.

## 2. Fix and verify virtual-printer color capabilities

Use `ipptool` Get-Printer-Attributes against `ipp://localhost:8631/ipp/print`, then inspect the registered macOS queue with `lpoptions -p Brother_T220_Virtual -l` and its defaults. Check Bonjour/DNS-SD metadata if discovery is used. Investigate contradictory defaults, cached capability data, application presets and grayscale selections before changing rendering.

Target truthful, consistent attributes:

| Attribute | Required behavior |
| --- | --- |
| `color-supported` | Boolean true |
| `print-color-mode-supported` | Includes `color`; advertise other modes only when implemented |
| `print-color-mode-default` | `color` |
| `document-format-supported` | Includes the actually accepted `application/pdf` |
| `print-quality-supported/default` | Supported values match implemented mapping; normal default |
| `printer-resolution-supported/default` | Match verified raster/rendering capabilities; no invented hardware resolutions |
| `job-creation-attributes-supported` | Includes implemented job options, consistent with server behavior |

Prefer supported `ippeveprinter` attribute configuration on the installed version. If it cannot express the required capabilities, document and test a compatible upgrade or a small server change before selecting an alternative. Do not publish unsupported modes merely to influence the UI.

Restart the service after changing capabilities. Recreate only the virtual queue with `-m everywhere` if capability caching persists, after saving its settings; do not delete the physical queue. Reopen applications and test a fresh preset. Verify both IPP responses and color previews in the application matrix. Keep `ppmraw` and `BRMonoColor=FullColor` throughout. If one application remains monochrome, isolate that behavior and leave its acceptance item open rather than declaring success from a color print alone.

## 3. Implement per-job quality end to end

Proposed contract (vendor tokens must be checked against the locally obtained driver configuration and verified physically):

| Cmd+P intent | IPP `print-quality` | Callback value to normalize | Brother `BRResolution` candidate |
| --- | --- | --- | --- |
| Draft | 3 (`draft`) | `draft` or `3` | `Draft` |
| Normal, default | 4 (`normal`) | `normal` or `4` | `Normal` (existing baseline) |
| Fine | 5 (`high`) | `high` or `5` | `Fine` |

IPP calls its highest standard quality `high`; macOS may label it High or Best rather than Fine. Verify actual Cmd+P labels and document Fine's mapping. If an exact Fine label requires a supported UI extension, assess that separately without replacing interoperable standard quality values.

Implementation sequence:

1. Advertise only quality values whose vendor tokens and rendering settings have been confirmed. Do not infer token validity from the desired UI name.
2. Capture allowlisted callback metadata locally to confirm `IPP_PRINT_QUALITY` representation and `IPP_PRINT_COLOR_MODE` propagation. Upstream ippeveprinter converts standard quality enums to keywords; test the installed version.
3. In `ipp-test/print-job.sh`, forward normalized quality through an explicit argument to `brother-bridge.py`; add an optional quality argument to Python and `convert-brother.sh` while preserving existing direct invocation and Normal default.
4. Use a closed mapping, quoted arguments and subprocess argument arrays; never interpolate arbitrary job values into a shell or vendor configuration. Reject unsupported explicit values clearly; missing quality selects Normal.
5. Keep a separate temporary directory and rc file per job. Never edit the extracted driver configuration or global printer defaults to select quality. Retain `BRMonoColor=FullColor` for all three modes. Until monochrome is implemented, do not advertise or silently accept it as if honored.
6. Validate how each vendor quality interacts with Ghostscript resolution and page geometry. Do not equate quality enums with dpi. If changing dpi, derive pixel dimensions from A4 consistently and verify scale, margins and clipping. Gate rollout on physical results.
7. Confirm separate jobs can alternate quality without restarting the service, changing queue defaults, or affecting later jobs.

## 4. Make job handling reliable

Keep each document's ordered page streams in one submission to the physical queue. Verify that concatenated Brother streams produce exactly the expected pages, without extra blanks or lost final pages. Check numeric page ordering beyond 999 pages with mocked conversion if physical testing at that size is impractical; lexical filename ordering must not reorder pages.

Inspect whether ippeveprinter serializes callbacks; implement explicit serialization if the conversion/transport path requires it. Concurrent jobs must have isolated files and intact document boundaries. Propagate conversion and `lp` failures to a failed IPP job using the installed server's documented callback/status interface. A successful `lp` submission proves queue acceptance, not physical completion. Do not retry an ambiguously submitted job automatically, which can print duplicates.

## 5. User launchd and Docker readiness

Add a documented LaunchAgent template and install/uninstall helper for a stable label such as `com.leelk.brother-t220-bridge`. Install under `~/Library/LaunchAgents` for the logged-in user; use explicit absolute paths, working directory and a minimal PATH. Do not require a root LaunchDaemon or assume shell startup files load.

- Use RunAtLoad plus controlled restart/backoff; prevent duplicate manual/launchd instances and handle port 8631 conflicts with an actionable error.
- Check Docker CLI availability, `docker info`, the local `brother-t220-converter:1.0` image, driver files, and the physical queue. Bound waits and provide useful failure states. Recheck Docker at job time because readiness can change after login.
- Document Docker Desktop's user-login startup setting. If offering to open Docker Desktop automatically, make it an explicit installation option; do not build images or download drivers during login.
- Choose and test whether IPP starts only after readiness or remains visible while reporting a not-ready state. Never acknowledge a job as successfully printed while dependencies are unavailable.
- Use private user log/spool locations, bounded logs and cleanup. Avoid storing document paths, payloads or environment dumps by default. Handle logout, sleep/wake, Docker restarts and USB reconnects.
- Document `launchctl bootstrap gui/$(id -u)`, `kickstart`, `print` and `bootout` using the installed plist path and label. Installation must be idempotent and reversible, and stop the old instance before starting another.

## 6. Verification and acceptance gates

Automated tests use synthetic inputs and mocked Docker/filter/`lp` commands; they must not require proprietary artifacts or print during CI.

| Area | Tests and release acceptance |
| --- | --- |
| Mapping | All keyword/numeric quality values, missing Normal default, invalid values, quoted paths; intended rc field and FullColor asserted for each mode |
| Isolation | Two overlapping jobs use distinct rc/output files; original rc remains unchanged; cleanup on success and failure |
| Failures | Missing driver/image, Docker unavailable, invalid PDF, filter failure, empty output and `lp` failure yield actionable failure with no false success |
| IPP | Checked-in `ipptool` tests assert color/quality defaults, supported values and option submission; malformed/unsupported requests receive truthful responses |
| Preview | Synthetic swatches stay colored in Cmd+P in Preview and a second application after fresh capability discovery |
| Physical quality | Each Draft/Normal/Fine job prints in color; verify small text, coverage, page scale and vendor mode selection, with differences documented |
| Multipage | 1-, 2-, and 10-page PDFs with unique numbers/color markers print once, in order, without blank/extra/missing pages; mixed portrait/landscape has documented correct behavior |
| Multiple jobs | Alternate Draft → Fine → Normal; repeat and overlap submissions; no option leakage, interleaving or duplicate pages |
| Lifecycle | Login starts exactly one service; delayed Docker, absent image, Docker restart, sleep/wake and USB reconnect recover or fail visibly within documented timeouts |
| Rollback | Disable LaunchAgent, restore prior runtime and virtual queue settings, and reproduce baseline full-color Normal printing |

Commit only a sanitized results summary with versions, pass/fail counts and limitations. Do not claim physical or UI tests passed until actually performed. Update README with quality selection, startup management, troubleshooting and remaining limitations only after the corresponding gates pass.

## 7. Delivery order and rollback

Deliver small reviewable commits: baseline/tests → capability and preview fix → quality mapping → multipage/job robustness → LaunchAgent/readiness → setup documentation and acceptance results. Record a known-good revision and private queue backup before each runtime stage. Keep manual startup available throughout.

Rollback procedure:

1. Stop accepting new jobs and inspect both queues; do not blindly replay or purge jobs. Resolve any uncertain submissions to avoid duplicates.
2. Boot out the user LaunchAgent, remove only its installed plist, and stop only the bridge-owned manual instance. Keep Docker's existing user settings intact unless explicitly changed during installation.
3. Revert the implementation commits on a clean branch (preserve unrelated work); avoid destructive reset/clean operations. Restore the previous local image tag if changed.
4. Restore saved virtual-queue defaults/capabilities, recreating only that queue if required, and restart `start-brother-service.sh` manually. Retain the physical USB queue and locally acquired driver.
5. Verify a baseline A4 Normal full-color print and preview status. Record unresolved preview limitations separately from physical color behavior.

## Repository hygiene and references

Do not commit Brother packages, archives, extracted configuration/binaries, printer-ready streams, raster pages, spool documents, logs, credentials or local machine identifiers. Reference vendor token findings in original prose rather than copying proprietary files. Use explicit staging of intended source/docs/tests, inspect the staged diff and tracked paths, and keep `.gitignore` protections. Driver-required integration tests run only locally with separately acquired files.

Primary technical references (confirm against installed versions):

- [OpenPrinting ippeveprinter manual](https://openprinting.github.io/cups/doc/man-ippeveprinter.html): color-speed option, attribute configuration and callback environment.
- [Apple CUPS ippeveprinter source](https://github.com/apple/cups/blob/master/tools/ippeveprinter.c): investigate platform capability construction and job handling; installed source/version takes precedence.
- [RFC 8011, section 5.2.13](https://www.rfc-editor.org/rfc/rfc8011.html#section-5.2.13): standard print-quality values 3/4/5.
