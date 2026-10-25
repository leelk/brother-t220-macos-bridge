# Native driver installation and user guide

Version: **0.1.0 development** · Last updated: **2026-10-25**

## Before you begin

This candidate provides a native Apple Silicon print filter and a setup app for the USB Brother DCP-T220. It is unsigned/unnotarized and remains experimental. The user has completed package installation on the development Mac; physical printing and live Cmd+P preview have not been verified.

Requirements:

- Apple Silicon Mac; installer requires macOS 14 or newer. Only macOS 27.0.1 is currently tested.
- One powered-on Brother DCP-T220 connected by USB.
- Administrator authorization for installation and printer setup.
- The development `.pkg` built from this project.

The installed native path does not require Docker, Homebrew, Python, Ghostscript, the Brother Linux package, or a terminal service. Keep the existing Docker fallback intact until native output is verified.

## 1. Locate and verify the package

On the build Mac, the output is:

```text
native/dist/Brother-T220-Native-0.1.0-development.pkg
```

This file is deliberately ignored by Git. A source clone contains the builder, not a ready-made installer. See the [README build instructions](../README.md#building-from-source) if the package is missing.

The verified development artifact has this SHA-256:

```text
08ce61f2486902986e94eefc2cdf56ac6a69301eefedaa16f6be48a80cb0634b
```

Optional integrity check, from the repository root:

```sh
shasum -a 256 native/dist/Brother-T220-Native-0.1.0-development.pkg
```

This checksum identifies this specific build; rebuilding can produce a different package hash. It does not provide Developer ID trust. The filter/app use ad-hoc integrity signatures; the installer has no distribution signature. If macOS blocks the package or app, stop. Disabling Gatekeeper or stripping quarantine is not part of this guide.

## 2. Install the software

1. Resolve unfinished jobs in the project's Brother queues before installation.
2. Double-click the package in Finder.
3. Follow the macOS Installer steps and complete the administrator prompt.
4. Close Installer after it reports success.

The installer targets the running system volume. It installs the driver files and the **Brother T220 Native Setup** app. If exactly one suitable USB printer is available and setup succeeds, it can also add the native queue. Otherwise, software installation can finish with printer configuration still pending.

**Installer success means the software is installed. A printer is ready only after its queue has been added successfully.** The observed installation on 2026-10-25 completed successfully and its package receipt was verified, but `Brother_T220_Native` was absent afterward. Follow the next section in that situation.

Nothing prints automatically during installation or setup.

## 3. Add the native printer

1. Connect one DCP-T220 by USB and turn it on. Disconnect additional DCP-T220 printers during setup.
2. Open **Finder → Applications → Brother T220 Native Setup**.
3. Choose **Add or Refresh Native Printer**.
4. Complete the administrator prompt and read the result message.
5. Check **System Settings → Printers & Scanners** for **Brother_T220_Native**.

The setup helper refuses changes when this project's queues have unfinished jobs, when no suitable USB printer is detected, when multiple matching printers are connected, or when the intended queue name belongs to another driver. Resolve the reported condition and retry; do not delete unrelated queues.

After setup, close the app. macOS handles printing on demand.

## 4. Review settings and print

1. Open a small, known coloured PDF in Preview.
2. Press **Cmd+P** and select **Brother_T220_Native**.
3. Select A4 or US Letter to match the loaded plain paper.
4. Review the preview and available colour/quality options. Their placement can vary by application; expand Printer Options if needed.
5. Choose Print only when you are ready to use paper and ink. For a setup-only check, choose Cancel.

| Setting | Candidate behavior |
|---|---|
| Colour | RGB output; colour is the default |
| Monochrome | Single-channel grayscale; exclusive black-ink use is not established |
| Draft | Device DRAFT mode |
| Normal | Device NORMAL mode; default quality |
| Fine | Device HIGH mode; standard IPP High maps to Fine |
| Paper | A4 or US Letter, plain paper, one-sided |
| Input resolution | 300 dpi for every quality mode |

Native offline PDF tests cover both paper sizes, colour modes and three qualities with two numbered pages. Physical colour, scale/margins, quality differences and page ordering still need validation. Selected media applies to the macOS job; automatic mixed-paper/tray handling is not claimed. Scanning, duplex and borderless/photo-media printing are not implemented.

In the current project session, the user has requested building/testing without physical printing. No hardware acceptance print has been submitted by the agent. A future physical test must be explicitly agreed before the agent sends it.

## After restarting

Once configured, the native queue is intended to remain registered across restarts. Connect and power on the USB printer, then choose **Brother_T220_Native** in Cmd+P. You should not need to open the setup app, start Docker, run a terminal command, or install a custom launch/login service. macOS starts the filter for the job.

A restart does not add a missing queue. If the native printer is absent, complete [Add the native printer](#3-add-the-native-printer). Reboot behavior and end-to-end printing remain unverified; do not treat this intended lifecycle as a completed test.

## Printer names and the Docker fallback

| Queue | Purpose |
|---|---|
| `Brother_T220_Native` | Native development driver; no Docker runtime |
| `Brother_T220_Virtual` | Existing Docker-backed bridge |
| `Brother_T220_Test` | Existing fallback's printer-ready USB transport |

Choosing the virtual fallback still requires Docker and its bridge service. Choosing the native queue uses the native path. Avoid simultaneous submissions from the native and fallback paths to one USB device. Installing the native package does not disable, remove or reconfigure the fallback.

## Troubleshooting and diagnostics

Start with the [troubleshooting guide](TROUBLESHOOTING.md). These optional terminal checks are read-only and do not print:

```sh
pkgutil --pkg-info com.leelk.brother-t220-native
lpstat -p Brother_T220_Native
lpoptions -p Brother_T220_Native -l
lpstat -W not-completed -o Brother_T220_Native
```

An installed receipt with a missing destination means file installation and queue configuration are in different states; it does not by itself mean conversion is broken. Do not share USB device URIs or full job/log output publicly.

## Remove the native queue

1. Resolve unfinished jobs first.
2. Open **Brother T220 Native Setup**.
3. Choose **Remove Native Queue** and complete the administrator prompt.

This removes only `Brother_T220_Native`. It retains the installed app, filter, package receipt and saved settings so setup can be repeated. The Docker fallback remains available. Queue removal is **not a complete file uninstall**; a verified full-uninstall workflow is still pending. Do not manually remove shared macOS CUPS directories.

## Restore a previous native queue

Choose **Restore Previous Native Queue** in the setup app only if a previous native configuration was saved during an earlier-version upgrade. The helper uses that saved PPD and USB URI and checks for pending jobs first.

A first installation has no previous native version to restore. In that case, remove the native queue and use the unchanged [Docker fallback](DOCKER_FALLBACK.md). Older filter binaries must still exist for a saved PPD to work. Live cross-version rollback and transactional upgrade recovery are not yet validated; do not infer full rollback coverage from the mocked helper tests.

## Installed locations

| Item | Location |
|---|---|
| Setup app | `/Applications/Brother T220 Native Setup.app` |
| Native filter | `/Library/Printers/leelk/BrotherT220/versions/0.1.0/brother-t220-native` |
| Setup helper | `/Library/Printers/leelk/BrotherT220/manage-driver.sh` |
| Printer description | `/Library/Printers/PPDs/Contents/Resources/Brother_DCP_T220_Native.ppd` |
| Private rollback state | `/Library/Application Support/leelk/BrotherT220/` |
| Package identifier | `com.leelk.brother-t220-native` |

The package records root:wheel ownership and executable permissions. These paths are implementation details for diagnosis; normal setup uses the app. The package does not replace Apple's print-service executables, install a custom background daemon, or bundle proprietary Brother files.

## Development and release status

See [native development](../native/README.md) for build/test commands and [release status](NATIVE_RELEASE_STATUS.md) for observed evidence. A source build requires Xcode tools; installed native operation does not. The package builder can use configured `BROTHER_APP_SIGN_IDENTITY` and `BROTHER_INSTALLER_SIGN_IDENTITY`, but the complete timestamp/notarization/stapling workflow remains future work. Credentials and private keys must remain outside the repository.

This candidate uses legacy CUPS PPD/filter integration. Long-term driverless IPP/PAPPL support, clean-Mac/multiple-OS acceptance, physical output tests and trusted distribution remain open tasks.
