# Native development candidate status — 2026-10-25

Artifact: native/dist/Brother-T220-Native-0.1.0-development.pkg. Development only; not a finished release.

| Check | Evidence / status |
|---|---|
| Official package provenance/current terms | Retrieved official source, matched both archives; scoped black-box experiment decision documented |
| Native converter | C++17 arm64, 300 dpi sRGB/sGray, PJL + standard PWG Raster using system libcups |
| Reference conversion | 12 full-page media/colour/quality cases: decoded pixel byte arrays match exactly; compression/header defaults differ |
| PDF integration | 26 offline pipeline jobs passed under AddressSanitizer/UndefinedBehaviorSanitizer, including 12 two-page combinations, copies and rejection paths |
| Host geometry | White full-page reconstruction from macOS imageable bounds; A4 final-edge one-row rounding handled without scaling |
| Native ticket / restricted raster tests | 29 / 27 checks passed; existing seven mocked fallback tests passed |
| Setup safety | 17 mocked scenarios passed, including absent/ambiguous USB, pending jobs, queue ownership, rollback and remove |
| Package inspection | Expanded without installation; scripts/source match, PPD semantics pass, arm64 binaries and system-only linkage verified, code integrity signatures verified |
| Installed permissions | BOM records root:wheel and 0755 executable; extracted temp files are user-owned, so PPD tool's filter-ownership warning is expected in the temp validation root |
| Resource sample | Two-page native conversion: 0.02 s wall time, 6,094,848 bytes maximum RSS on this development Mac; excludes PDF rendering and USB, not an M1/8GB or endurance benchmark |
| Startup | Uses OS CUPS on demand; no custom persistent process. Reboot/startup acceptance not run |
| Package trust | Package unsigned; app/filter ad-hoc signed only. No account/identities for Developer ID/notarization |
| Actual installation | User screenshot reports installer success; installed 0.1.0 receipt and root-owned native filter verified on 2026-10-25. Native queue absent afterward; configuration pending |
| Upgrade/uninstall | Installed-system upgrade/full uninstall not run; script syntax, package inspection and mocked helper tests only |
| Setup GUI / Cmd+P preview | App compiled; visual validation unavailable because Computer Use permission is not granted |
| USB/physical colour/quality/pages | Not run, explicitly held by user request to build/test without printing |
| Long-term driverless application | PAPPL/IPP integration remains deferred; interim legacy CUPS design recorded in ADR 002 |

The final verified package includes Apple metadata sidecars created by pkgbuild, not proprietary artifacts or user documents. pkgbuild emitted metadata-write warnings but exited successfully; package expansion, payload/code-signature verification and BOM ownership checks passed. These warnings do not establish installation success and should be investigated if reproducing outside this development environment.

All private reference outputs, generated PDFs/raster/PRN, build executables, package and logs remain outside version control. The user subsequently installed the package; receipt and installed filter were checked read-only. The agent did not install it, modify queues or submit a print job. The native queue is still absent at the latest 2026-10-25 check. Physical printing is not authorized in the current session. Signed distribution is blocked by unavailable Developer ID credentials, not by a claim that the native path has passed release acceptance.

## Installation follow-up — 2026-10-25

Installer success and installed files are confirmed, while queue configuration remains a separate pending step. The documentation now puts this distinction before first-print instructions and explains intended startup/restart behavior. No new physical, preview, reboot or upgrade acceptance is implied. Start with [native installation](NATIVE_INSTALLATION.md); diagnostic paths are covered in [troubleshooting](TROUBLESHOOTING.md).
