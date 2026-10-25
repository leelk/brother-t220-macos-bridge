# M1 public research and provenance findings

Date: 2026-10-25. Baseline: d00d58f. Status: partial M1; no native driver implementation or vendor experiment performed.

## Package identification

The local control archive identifies dcpt220pdrv 3.5.0-1, i386, maintained by Brother. Brother's [Linux DEB download list](https://support.brother.com/g/b/downloadlist.aspx?c=us_ot&lang=en&prod=dcpt220_all&os=128) lists that version, dated 2020-08-17. Its [package details link](https://support.brother.com/g/b/downloadend.aspx?c=us_ot&dlid=dlf105164_000&flang=4&lang=en&os=128&prod=dcpt220_all&type3=10283) returned 403/inaccessible during this research. The original DEB is absent locally. Consequently version correspondence is established but vendor-authenticated archive provenance and the current download agreement are not.

| Local artifact | SHA-256 |
|---|---|
| control.tar.gz | a5cd81ef4850ca2bab3edc8ed6c6a1b0951450d7cb72a0910139f0c52ea1f0d2 |
| data.tar.gz | 0b5bb7c71bc3e341d23e1904e4a1db8e3c15f9a9d1b0ff3d2b6158dbb672d07e |
| extracted LICENSE_ENG.txt | 46b2902ead35bd6d1a111740022133cb120bc7c32a2effdc8d381cc25a59dfa6 |
| x86_64 converter | 68e0f0aa275e0a98ba885a0c221f4c13bccdaba2a179e996ed8c138b47b6008a |

Read-only tar inspection confirms the English license and x86_64 converter inside data.tar.gz are byte-identical to their extracted counterparts. No archives or vendor files were extracted, executed, modified or committed in M1. The license was inspected locally; only this original summary is published.

## Local license findings

The English agreement retains Brother ownership and expressly grants nonexclusive reproduction/distribution and modification/derivative-work permissions. It disclaims warranties and any obligation to provide source. It separately identifies programs under cupswrapper and its subdirectories as governed by GPL version 2. Do not describe the entire package as GPL, or assume wrappers make the binary open source.

This is stronger permission evidence than M0 had, but it does not authenticate the download or establish all applicable terms. It does not resolve every jurisdiction's interoperability, patent or other legal question. The project still excludes all vendor artifacts from Git and the native distribution as an intentional design/policy choice, independently of these permissions. Disassembly is not necessary for the next proposed black-box experiments and remains deferred.

## Exact-model alternatives

The [Gutenprint supported-printer list](https://gimp-print.sourceforge.io/p_Supported_Printers.php) contains no DCP-T220 match when searched. The [OpenPrinting Gutenprint page](https://openprinting.github.io/foomatic/driver/gutenprint) likewise supplied no exact-model support evidence in this review. This is a bounded search result, not proof that no independent driver exists. Other Brother model support is not evidence of compatible inkjet framing.

Brother's [OS support page](https://support.brother.com/g/b/oslist.aspx?c=eu_ot&lang=en&prod=dcpt220_all) lists Mac versions, but an OS listing alone does not demonstrate Cmd+P driver availability. Regional [Brother product material](https://www.brother.co.th/th-th/printers/all-printers/dcp-t220) describes Mac use through iPrint&Scan and absence of a Mac driver. A different regional [download landing page](https://support.brother.com/g/b/downloadtop.aspx?c=us_ot&lang=en&prod=dcpt220_all) advertises a newer Mac software package; its contents, exact-model applicability and Cmd+P behavior remain unverified. Therefore a fresh official native-driver check remains ahead of expensive reverse engineering; no package was downloaded or installed here.

## Gate status

- T10 partial: local license/version/hash inventory complete; original DEB provenance and current click-through terms unresolved.
- T11 partial: dependency screening recorded in NATIVE_DEPENDENCIES.md; owner selected Apache-2.0 on 2026-10-25 and root LICENSE was added in a subsequent change; exact dependency build/license audit remains pending.
- T12 partial: public support search and provisional ADR recorded; current official Mac software needs inspection before choosing replacement-converter work conclusively.
- T13 complete as a specification: NATIVE_ORACLE_EXPERIMENTS.md; no oracle runs executed.

M1 is not accepted as complete. Continue read-only official package/source review and the exact dependency audit. Conversion-only research can follow once provenance/terms are matched and the experiment preflight passes. USB writes, disassembly and vendor redistribution remain outside this step. Docker fallback and all runtime files remain unchanged.

## Subsequent provenance resolution

Later on 2026-10-25, curl retrieval of Brother's details/how-to/current-agreement pages succeeded. The official DEB members match both local archives; scoped conversion-only experiments followed the reviewed grant. See NATIVE_PROTOCOL_FINDINGS.md for exact URL/hash and limits. The original unresolved-provenance statements above describe the earlier checkpoint. The selected project license is Apache-2.0; the current CUPS development candidate bundles no third-party libraries or vendor artifacts. The future PAPPL dependency/build audit remains separate.
