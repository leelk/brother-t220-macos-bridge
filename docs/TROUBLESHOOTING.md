# Troubleshooting native printing

Applies to **0.1.0 development**. This guide distinguishes software installation, queue setup, conversion, USB delivery and physical output. Passing one stage does not establish that the later stages work.

## Installer succeeded, but the native printer is missing

**Likely state:** files were installed, but the USB printer was unavailable or queue setup was deferred. This condition was observed on the development Mac after a successful package installation.

Connect and power on one DCP-T220 by USB. Open **Applications → Brother T220 Native Setup → Add or Refresh Native Printer**, complete the administrator prompt and read the result. Then check Printers & Scanners or reopen Cmd+P. A restart alone does not create the queue.

Optional read-only checks:

```sh
pkgutil --pkg-info com.leelk.brother-t220-native
lpstat -p Brother_T220_Native
```

If the receipt exists but lpstat reports an invalid destination, installation is recorded but that queue is absent.

## Setup cannot find the USB printer

Check that the printer is powered on, connected by a working USB cable/adapter, and directly accessible to the Mac. Connect only one matching model during setup. Reconnect the cable and retry the setup app. Do not create a queue with a guessed device URI or borrow another model's driver.

If the device is still unavailable, record the exact setup error and macOS version. Detailed USB enumeration can expose the printer serial number; redact it before sharing diagnostic output.

## Setup reports unfinished jobs

Open the affected queue in the macOS print interface and inspect the pending jobs. Let intended jobs finish, or cancel them only after checking which documents they are. Do not automatically purge queues or replay uncertain jobs. Setup, removal and rollback intentionally refuse to proceed while this project's queues have unfinished jobs.

## Which printer should I choose?

| Selection | Behavior |
|---|---|
| `Brother_T220_Native` | Uses the new native filter; Docker is not required |
| `Brother_T220_Virtual` | Uses the existing Docker bridge; Docker and the bridge must be running |
| `Brother_T220_Test` | Fallback transport for printer-ready data; not the normal PDF printing selection |

Make sure the application selected the intended printer rather than a saved fallback preset. Avoid simultaneous jobs from the native and fallback paths to one USB device.

## Printing after a restart

A configured native queue is intended to persist. macOS launches the filter for a print job, so no custom startup app, login item, terminal process or Docker service is needed. Power on and connect the printer before printing.

If the queue is missing, configure it through the setup app. If it exists but cannot print, inspect its status and any error message. Reboot/startup behavior has not yet passed a physical end-to-end test; do not repeatedly restart as a substitute for diagnosing a missing queue.

## The preview is monochrome or expected options are missing

Select `Brother_T220_Native`, use a fresh/default preset, select colour and check A4/Letter and quality settings. Expand Printer Options; labels and placement can vary by application. Close and reopen the print dialog after changing printers or refreshing the queue.

The PPD declares a colour device with RGB/Gray and Draft/Normal/Fine options. Offline raster tests pass, but live print-dialog appearance and native physical colour are still unverified. The historical preview repair in [COLOR_PREVIEW.md](COLOR_PREVIEW.md) applies to the Docker virtual queue, not proof of native preview acceptance.

Do not change media, profiles or resolution blindly to force the preview. Capture only synthetic content if reporting a screenshot.

## A job fails or stops

Check the queue's exact error message and whether bytes may already have reached the device. The setup helper configures an abort-job policy to avoid automatic retries of uncertain partial output. Inspect the paper before manually resubmitting; a host error does not prove no page printed.

The native filter accepts the tested 300 dpi sRGB/sGray raster path and A4/Letter geometry. Unsupported settings, malformed/truncated raster, excessive copy/page/output limits, or write failures can reject a job. Do not edit the PPD or use raw submission as a general workaround. Report the selected settings and the error, using a synthetic document when possible.

Physical USB behavior and recovery remain acceptance tasks. This project's own messages distinguish conversion completion from physical printing completion.

## macOS blocks the package or setup app

The development package is unsigned and not notarized; ad-hoc app/filter signatures are integrity checks, not Developer ID trust. Trusted distribution requires a signed/notarized release. Do not disable Gatekeeper, alter security settings, strip quarantine or run downloaded scripts as a troubleshooting shortcut in this guide.

Record the exact message. Package installation has succeeded on the current development Mac, but that does not establish clean-Mac security acceptance elsewhere.

## Restore Previous Native Queue says no backup exists

A first installation has no previous native configuration. Use **Remove Native Queue** to disable native printing and return to the unchanged Docker fallback. Saved prior-queue restoration is intended for earlier-version upgrades and requires the old filter files to remain available. Live upgrade/rollback is not yet validated.

## Remove the driver without disturbing other printers

Use **Remove Native Queue** in the setup app. It removes only the project-owned native queue and retains software files and receipts for repair/reconfiguration. It does not perform complete file uninstallation. Do not delete system CUPS folders, other printer queues, or the fallback's driver files.

## Useful read-only checks

These commands do not print, install software or modify queues:

```sh
pkgutil --pkg-info com.leelk.brother-t220-native
lpstat -p Brother_T220_Native
lpoptions -p Brother_T220_Native -l
lpstat -W not-completed -o Brother_T220_Native
```

Job listings can contain document/user names; review and redact output before publishing it. Avoid public full logs, spool files, USB URIs/serial numbers or customer documents.

## Report a reproducible issue

Include driver/package version, macOS version, Apple Silicon model, selected queue, paper/colour/quality choices, a short sequence of actions, and the exact error. State whether you observed a preview problem, conversion failure, queued job, USB delivery issue or printed-page defect. Include only source-generated/synthetic examples with permission to share them.

See [release status](NATIVE_RELEASE_STATUS.md) for verified checks and open limitations, and [installation](NATIVE_INSTALLATION.md) for normal setup/removal.
