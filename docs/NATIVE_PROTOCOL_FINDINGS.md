# DCP-T220 reference-conversion findings

Date: 2026-10-25. Status: observed conversion behavior, not physical printer acceptance. No disassembly, firmware work or USB writes were performed.

## Provenance and permissions

The official [package details page](https://support.brother.com/g/b/downloadend.aspx?c=us_ot&dlid=dlf105164_000&flang=4&lang=en&os=128&prod=dcpt220_all&type3=10283) was retrieved with curl after the browser fetch had failed. Its agreement iframe points to Brother's [English agreement](https://support.brother.com/g/s/agreement/English_eula/agree.html); its [how-to page](https://support.brother.com/g/b/downloadhowto.aspx?c=us_ot&lang=en&prod=dcpt220_all&os=128&dlid=dlf105164_000&flang=4&type3=10283) supplies the [official DEB URL](https://download.brother.com/welcome/dlf105164/dcpt220pdrv-3.5.0-1.i386.deb).

Downloaded dcpt220pdrv 3.5.0-1 package SHA-256: `625f1d08bf1bb831cbc7c5f9230da9914184ffdce9cb9736fc78f006d55f348c`. Both control.tar.gz and data.tar.gz members match the existing local archives exactly; their hashes are in NATIVE_M1_FINDINGS.md. The English agreement retains the affirmative modification/distribution grant and the separate GPLv2 wrapper scope recorded there. The current online wording is not asserted byte-identical to the archived license. No vendor files are included in source or the installer.

Decision for this step: the matched source and reviewed terms support bounded conversion-only black-box observations of this already acquired driver. This is a narrow engineering decision for these experiments, not general legal clearance or redistribution approval. No proprietary implementation or wrapper code was copied into the native filter.

## Experiment containment and observations

Reference image ID: `sha256:055962a8bdeb0f793b79ba69353165c7339e923fb20374bcfdddcd2568010ca9`. Used only for development oracle runs: linux/amd64, network disabled, read-only root/vendor/input mounts, 256 MiB memory, one CPU, 64-process limit, 16 MiB temporary filesystem, bounded output and 45-second per-run timeout. No printer device or host printer command was passed into the container. An initial alternate vendor path failed because the binary expects its original configuration path; rerunning with the original read-only path succeeded.

First, 12 small synthetic swatch conversions identified mode choices. Then 12 full-page swatch conversions covered A4/Letter × colour/mono × Draft/Normal/Fine. Artifacts stay private in /private/tmp; source uses only owned generator patterns. Tiny inputs are unsuitable geometry references: the converter fixes page dimensions from media and can fill missing data unexpectedly, so the full-page runs are the comparison evidence.

The stream contains PJL job setup, a standard PWG Raster payload and two universal-exit markers. Functional mappings observed:

| Selection | Observed behavior |
|---|---|
| A4 | 2480×3507 at 300 dpi |
| Letter | 2550×3300 at 300 dpi |
| Colour | RGB, 8 bits/channel, three channels, standard sRGB identifier |
| Mono | 8-bit single-channel standard sGray identifier |
| Draft / Normal / Fine | PJL quality DRAFT / NORMAL / HIGH; same input dpi |
| Plain media | REGULAR, automatic tray, borderless and duplex disabled |
| Margins | PJL margin values 300 in each direction; physical interpretation remains unmeasured |

Our native encoder uses Apple's system libcups to write standard PWG Raster. Independently decoded pixel byte arrays from all 12 native/reference full-page swatch cases match exactly, and PJL setup text matches. Whole printer streams are not byte-identical: standard-library compression and at least the PWG alternate-primary default differ. This is valid-format evidence, not proof the device accepts every variation. The monochrome conversion used for RGB input reproduces these swatches with integer 30/59/11 weighting; this does not establish a calibrated transform or black-ink-only behavior.

Multipage native output uses one framed stream per page, concatenated in order, matching the existing fallback's approach. Two-page offline parsing passes; device page boundaries, physical quality differences and colour accuracy still require authorized printing. The test inspector is restricted to known synthetic fixtures; it is not a general hostile-stream parser.

Primary API reference: [CUPS raster API](https://www.cups.org/doc/api-raster.html). No independently authored Brother compression codec is needed for this candidate, because the payload is standard PWG Raster.
