# Candidate dependency and license ledger

Reviewed 2026-10-25. Preliminary screening, not a release SBOM. No dependency was downloaded, vendored, linked or installed. Versions below are candidate facts, not locked build inputs. Record exact release hash, build flags, transitive components and license texts before adoption.

| Component | Candidate / evidence | License and action |
|---|---|---|
| Project-owned native code | Not yet written | Owner selected Apache-2.0 on 2026-10-25; root LICENSE applies to original project code/documentation. Vendor/dependency code retains its own terms. |
| PAPPL | 1.4.12 appears on official release page; source master reviewed only | Apache-2.0 plus exceptions in NOTICE. Preserve LICENSE/NOTICE, changes and attribution; verify exact pinned release. |
| libcups | Choice of system vs bundled unresolved | OpenPrinting master LICENSE is Apache-2.0; inspect its NOTICE and actual chosen version. Do not apply that result automatically to Apple's system CUPS or older CUPS. |
| zlib | Release/site version 1.3.2 | Zlib license: retain source notices and mark alterations; include notice in packaged license inventory. |
| TLS | OpenSSL candidate; not selected | OpenSSL master LICENSE is Apache-2.0. Pin release and audit bundled components; alternatives need their own review. |
| USB | PAPPL backend/libusb candidate; not selected | License/build/linkage review pending; macOS service permissions unproven. |
| Discovery | System mDNSResponder candidate | Verify SDK/system framework use and whether any source is bundled; do not assume redistribution rights from system availability. |
| PDF and colour | CoreGraphics/ColorSync candidate | System framework/SDK deployment and service-context validation pending; no third-party renderer selected. |
| Optional image codecs | JPEG/PNG not selected | Avoid enabling unnecessary formats; audit licenses/transitive components if enabled. |
| Ghostscript | Existing Docker fallback only | Artifex licensing review required if adopted in native product. Prefer native renderer evaluation; do not silently link/copy fallback dependencies. |
| Brother filter | Local oracle candidate only | Custom Brother terms; never part of native runtime or Git under current policy. |
| Brother CUPS wrapper | No reuse planned | Local agreement identifies GPLv2 coverage; avoid copying into independently authored native code. |

Sources reviewed:

- [PAPPL overview](https://www.msweet.org/pappl/), [LICENSE](https://raw.githubusercontent.com/michaelrsweet/pappl/master/LICENSE), [NOTICE with exceptions](https://raw.githubusercontent.com/michaelrsweet/pappl/master/NOTICE).
- [OpenPrinting CUPS LICENSE](https://raw.githubusercontent.com/OpenPrinting/cups/master/LICENSE).
- [zlib license](https://www.zlib.net/zlib_license.html).
- [OpenSSL LICENSE](https://raw.githubusercontent.com/openssl/openssl/master/LICENSE.txt).
- [Artifex licensing](https://artifex.com/licensing).

A release lock must replace master URLs with immutable tag/commit sources and include actual license/notice files. Source-distribution or source-offer duties depend on exact adopted licenses, linkage and distribution; this screening makes no blanket compatibility claim. No native dependency audit is complete until the real build graph exists.
