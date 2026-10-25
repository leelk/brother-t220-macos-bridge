# Packaging, launchd and rollback

## Proposed installation

Ship a versioned setup/status app in /Applications and a bundled arm64 service/dependencies in a stable application-support location. Prefer a dedicated non-login account and a LaunchDaemon for printing before user login if USB permissions permit; otherwise choose a LaunchAgent and explicitly scope startup to login. Resolve this at M5 rather than claiming both work. launchd uses absolute paths, a minimal environment, one service instance and bounded restart backoff. No shell profile, VM, emulation, package manager or GUI process is required at print time.

Only the installer and scoped setup helper receive necessary privileges. Restrict spool directories to the service owner; design authorization for local job access and multiple users. Keep status/UI unprivileged. Use event-driven USB/readiness handling, no busy polling, bounded redacted logs and rotation. Handle port conflicts without killing unrelated processes. Crash loops stop with an actionable status. Never log PDF content, serial numbers, filenames or arbitrary environments by default.

## Build and signing checklist (future implementation)

1. Reproducibly build pinned arm64 components, SBOM and license notices; inspect linked libraries and deployment targets. Exclude proprietary artifacts and local fixtures.
2. Sign nested executables/libraries and app with Developer ID Application, hardened runtime and minimal justified entitlements; verify strict codesign checks. Keep signing credentials outside Git and build logs.
3. Build component/product packages with idempotent narrowly scoped scripts; sign final pkg with Developer ID Installer. Submit with notarytool, inspect result, staple supported artifacts and validate stapler, pkgutil signatures and Gatekeeper assessment.
4. Install the quarantined download on a clean supported Mac without developer tools/Docker/Brother packages. Verify app/service/queue, offline launch after install, USB print, resource budgets and restart behavior. Notarization requires appropriate Apple credentials; unsigned development builds are not release acceptance.

## Transaction and recovery

Preflight compatibility, disk space, existing version/service/port, queue ownership and active jobs. Save private defaults/config and previous signed version. Stage files first, validate, quiesce only owned service after active jobs resolve, switch version atomically where possible, start and health-check. On failure stop new service, restore previous files/config and owned queue attributes, restart and verify. Handle partial pkg script failures with a durable journal and a documented repair path; receipts alone do not guarantee rollback.

Do not overwrite the fallback scripts, image or physical USB queue. Native setup gets a distinct virtual queue/service label and transport ownership is exclusive. Native uninstall stops only its service, removes only owned queue/files/receipt as appropriate, and asks before deleting retained jobs or settings. Never purge ambiguous jobs or replay automatically.

Acceptance includes fresh install, same-version reinstall, upgrade, failed upgrade, downgrade with compatible config, uninstall, reboot before/after login, sleep/wake and restoration of fallback manual startup. Preserve documents and unrelated printer settings. Publish an exact version-specific rollback procedure after implementation; this document is not an executable installer.
