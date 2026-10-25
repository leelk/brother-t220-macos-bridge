# Experimental native installer — 0.1.0

## Current output

Local development artifact: `native/dist/Brother-T220-Native-0.1.0-development.pkg` (ignored by Git). SHA-256 for the verified build: `08ce61f2486902986e94eefc2cdf56ac6a69301eefedaa16f6be48a80cb0634b`.

This is an installable-format development candidate, **not a signed/notarized or physically validated release**. It has not been installed on the user's Mac. The filter/app have ad-hoc integrity signatures, not Developer ID trust. No Apple Developer account is currently available. If macOS blocks installation, stop; do not disable Gatekeeper or remove quarantine as part of these instructions.

## What the package is designed to do

Install Brother T220 Native Setup.app into Applications, a native arm64 converter under `/Library/Printers/leelk/BrotherT220/versions/0.1.0/`, a model PPD under `/Library/Printers/PPDs/Contents/Resources/`, and a narrowly scoped setup helper. System-owned paths are recorded root:wheel in the package with executable permissions; no system CUPS executable is replaced.

The preflight requires Apple Silicon, macOS 14+, the running system volume, and no pending jobs in this project's Brother queues. Only macOS 27.0.1 has been tested offline. A connected USB printer can be configured automatically by postinstall; otherwise open the setup app after connecting it and choose Add or Refresh Native Printer. Postinstall reports pending setup rather than claiming that an unavailable/busy queue was configured. Setup never submits a print job.

The queue is named **Brother_T220_Native**. This candidate prints through macOS's existing print service and USB backend; Docker, Homebrew, Python and the Brother Linux driver are not runtime dependencies. Close the setup app after configuration. CUPS starts the native filter when a job arrives; no custom launch agent, daemon or GUI must remain running.

## Intended first validation (not performed)

1. Keep the working Docker setup intact. Resolve pending jobs first and avoid concurrent native/fallback submissions to one USB printer.
2. Install the locally built package only when ready to test this experimental candidate. Complete normal macOS administrator prompts; installation and security acceptance have not been tested here.
3. Connect one powered-on DCP-T220 by USB. If needed, open Brother T220 Native Setup and add the printer. If no printer is found, queue creation fails clearly; file installation alone is not successful printer setup.
4. With a synthetic coloured PDF, open Cmd+P and choose Brother_T220_Native. Verify colour preview, A4/Letter and Draft/Normal/Fine choices, then cancel. Actual UI validation remains pending because computer-control permission is unavailable.
5. Do not print until the user authorizes hardware tests. Then begin with a labelled A4 Normal colour page and check page scale/margins/colour before expanding to the physical matrix.

Input resolution is 300 dpi for all qualities; Fine maps to the device's HIGH mode. Plain paper and one-sided printing only. The host handles requested copies with bounded staged output; physical copy/ordering behavior is unverified. Page selection/rotation is delegated to macOS. Mixed-paper PDFs follow the selected macOS media; automatic mixed-tray handling is not claimed.

## Removal and rollback

Open the setup app and choose Remove Native Queue to remove only Brother_T220_Native, retaining installed files and existing fallback queues. The helper refuses changes while this project's queues have pending jobs and refuses to modify a same-named queue belonging to another driver. Restore Previous Native Queue uses a saved prior native PPD/device URI when available. Fresh installation has no previous native version, so use queue removal to return to the unchanged fallback. Older version binaries must still exist for a saved PPD to work; cross-version rollback has not been tested.

This is reversible queue removal, not a complete file-uninstaller. Package files/receipts remain; a full verified uninstall and transactional update/rollback remain release tasks. No fallback scripts, image, proprietary files or USB queues are removed. Existing Docker fallback can be started with its original instructions when native testing is over; installing the native package does not disable it.

## Build and offline verification

From the repository root:

```sh
native/packaging/build-pkg.sh
PYTHONDONTWRITEBYTECODE=1 python3 native/test_package.py native/dist/Brother-T220-Native-0.1.0-development.pkg
```

A source build requires Xcode tools; users of a future verified installer should not need them. All build/test fixtures and packages are excluded from Git. `BROTHER_APP_SIGN_IDENTITY` and `BROTHER_INSTALLER_SIGN_IDENTITY` allow configured Developer ID identities; credentials must remain outside the repository. Timestamping, notarization, stapling and clean-machine Gatekeeper verification are not automated by this first development build and remain release requirements.
