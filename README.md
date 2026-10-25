# Brother DCP-T220 for macOS

Experimental native printing support for a USB-connected **Brother DCP-T220** on **Apple Silicon**. The native driver integrates with the macOS print service so applications can print through **Cmd+P**, without Docker or an application running in the background.

**Current version: 0.1.0 development.** The package has been installed successfully on the development Mac, but printer setup is incomplete and physical output is not yet verified. The installer is unsigned and not notarized. This is an independent project, not an official Brother driver.

[Install and configure](docs/NATIVE_INSTALLATION.md) · [Troubleshooting](docs/TROUBLESHOOTING.md) · [Validation status](docs/NATIVE_RELEASE_STATUS.md) · [Docker fallback](docs/DOCKER_FALLBACK.md)

## Quick start

1. Obtain the locally built `Brother-T220-Native-0.1.0-development.pkg` and complete the macOS Installer steps.
2. Connect **one** DCP-T220 by USB and turn it on.
3. Open **Applications → Brother T220 Native Setup**.
4. Choose **Add or Refresh Native Printer** and complete the administrator prompt.
5. Open a document, press **Cmd+P**, and select **Brother_T220_Native**. Review the preview and settings before choosing Print.

**An “installation successful” message confirms the software files were installed; it does not guarantee the printer queue was added.** If the printer was unavailable during installation, complete steps 2–4. Setup does not print a test page automatically.

The generated installer is located at `native/dist/Brother-T220-Native-0.1.0-development.pkg` on the build Mac. It is excluded from Git and is not included in a source clone. No public binary release is published by these instructions. To create your own package, see [Building from source](#building-from-source).

## Requirements

| Requirement | Native development driver |
|---|---|
| Mac | Apple Silicon (`arm64`) |
| macOS | Installer requires macOS 14 or newer; current testing is on macOS 27.0.1 only |
| Printer | Brother DCP-T220, connected directly by USB |
| Setup access | Administrator authorization for installation and queue changes |
| Runtime dependencies | Built-in macOS print service and system libraries |
| Package trust | Unsigned/unnotarized development package; no Developer ID release yet |

Docker, Homebrew, Python, Ghostscript and the Brother Linux driver are **not required by the installed native path**. Source builds and development tests have separate requirements. If macOS blocks an untrusted package or application, stop and follow the project's signing/release process; these instructions do not disable system security protections.

## Features and validation

| Feature | Current implementation | Validation |
|---|---|---|
| Normal Cmd+P integration | Native CUPS filter and model PPD | Offline PDF pipeline passes; live print-dialog verification pending |
| Colour / monochrome | Per-job RGB / single-channel grayscale | Reference conversion and offline tests pass; physical checks pending |
| Draft / Normal / Fine | Per-job device quality mapping | All three mappings tested; printed quality differences pending |
| A4 / US Letter | 300 dpi input, media-specific geometry | Both sizes tested offline; physical scale/margins pending |
| Multipage documents | Ordered page conversion and staged output | Two-page combinations tested; physical/endurance checks pending |
| USB | Uses the macOS USB print backend | Native hardware delivery pending |
| Automatic startup | macOS launches the filter on demand | No custom startup process needed; reboot validation pending |
| Installation | `.pkg` plus a setup app | User installation and installed receipt confirmed; native queue not yet created |
| Rollback / removal | Saved prior native queue or remove native queue | Mocked scenarios pass; live upgrade/rollback pending |

All quality settings use **300 dpi input**. Fine maps to the printer's HIGH mode; it does not change input resolution. The current candidate supports plain-paper, one-sided printing. Scanning, automatic duplex, borderless/photo-media modes, Intel Macs and network printing are outside this candidate's scope. Preview fidelity and calibrated screen-to-paper colour matching are not verified.

## After restarting your Mac

Once **Brother_T220_Native** has been configured, its registration is intended to persist. macOS starts the filter when a job arrives; you do not need Docker, a terminal command, the setup app, or a custom login item. Connect and power on the USB printer before printing.

Restarting does **not** add a missing printer queue. Reboot behavior still needs an observed end-to-end test. See [restart and first-print checks](docs/NATIVE_INSTALLATION.md#after-restarting).

## Native driver and Docker fallback

| Path | Printer to select | Docker required? | Startup |
|---|---|---|---|
| Native development driver | `Brother_T220_Native` | No | macOS starts the filter per job |
| Existing fallback | `Brother_T220_Virtual` | Yes | Start Docker and the bridge service |
| Fallback USB pass-through | `Brother_T220_Test` | Part of fallback | Internal transport queue; not the normal document-printing choice |

Keep the existing fallback available while testing native output. Avoid simultaneous submissions from both paths to the same USB device. The native installer does not remove or reconfigure the fallback. Complete fallback setup, option mapping and historical colour-preview evidence are retained in the [Docker fallback guide](docs/DOCKER_FALLBACK.md).

## Building from source

On an Apple Silicon development Mac with Xcode and its command-line tools:

```sh
git clone https://github.com/leelk/brother-t220-macos-bridge.git
cd brother-t220-macos-bridge
native/packaging/build-pkg.sh
```

Output:

```text
native/dist/Brother-T220-Native-0.1.0-development.pkg
```

The build creates a development package without installing it or printing. It contains project-owned code and uses system libraries; no Brother binaries are bundled. To inspect the generated package without installation:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 native/test_package.py native/dist/Brother-T220-Native-0.1.0-development.pkg
```

Python is required for development tests only. See [native development instructions](native/README.md) for compiler commands, offline PDF/raster tests and packaging checks. The builder supports configured signing identities but does not implement the complete notarization/stapling workflow.

## Documentation

| Guide | Purpose |
|---|---|
| [Native installation](docs/NATIVE_INSTALLATION.md) | Package location, setup, printing, restart, removal and rollback |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Missing queue, USB detection, stalled jobs and safe diagnostics |
| [Release status](docs/NATIVE_RELEASE_STATUS.md) | Evidence, test results and outstanding acceptance gates |
| [Docker fallback](docs/DOCKER_FALLBACK.md) | Existing working bridge and its requirements |
| [Native development](native/README.md) | Build and test commands, interfaces and bounds |
| [Planning index](docs/NATIVE_PLAN.md) | Architecture, research, milestones and task backlog |
| [Current architecture decision](docs/NATIVE_ADR_002.md) | Why the first candidate uses CUPS; long-term IPP/PAPPL work |
| [Protocol findings](docs/NATIVE_PROTOCOL_FINDINGS.md) | Reference provenance and independently observed format behavior |

The native driver currently uses legacy CUPS PPD/filter integration. It is an interim implementation, not the planned driverless IPP/PAPPL application; future macOS compatibility remains a release risk.

## Reporting a problem

Check [Troubleshooting](docs/TROUBLESHOOTING.md) first. When reporting an issue, include the driver version, macOS version, Mac architecture, selected queue, media/colour/quality settings, and exact error message. Use synthetic documents where possible and distinguish a preview issue, conversion failure, queue submission, and actual printed output.

Do not publish document contents, printer serial numbers or USB URIs, account information, full spool/log dumps, or signing credentials.

## Repository policy and license

Only source, tests and sanitized documentation belong in Git. Do not commit Brother packages or extracted files, generated installers/PDFs/raster/print streams, spool documents, logs, environment files, credentials or private keys. See [.gitignore](.gitignore).

Original project code and documentation are licensed under [Apache License 2.0](LICENSE). Brother software and other third-party components retain their own terms. Brother artifacts are excluded from this repository and the native package.
