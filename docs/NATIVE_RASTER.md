# Native raster converter design

Status: design hypothesis; protocol and colour science unresolved.

## Interfaces and invariants

Normalize a ticket once: media A4/Letter, colour/color or monochrome, quality draft/normal/high, orientation, copies and page selection as actually supported. Reject unsupported combinations before transport; no silent A4 fallback. IPP high means vendor Fine, not a dpi claim. Initially one copy unless copy semantics are implemented and advertised.

Raster descriptor: width, height, resolution, colour space/profile, channel order, bits/channel, stride, band origin and media/imageable rectangle. Use checked integer arithmetic for width × channels × rows, upper bounds on dimensions/page count/bytes, and explicit endianness. A band consumer accepts bounded data and a sink, never a whole document allocation. Maintain required encoder state across bands; if compression needs a full page, benchmark bounded private disk staging and revise the design before claiming streaming.

Separate modules: ticket validation → geometry → colour conversion → halftone/plane packing → framing/compression → sink. Initially expose a conversion-only CLI without USB access. Cancellation and I/O errors unwind all state; temporary files have restrictive permissions and are deleted on success/failure. Malformed inputs cannot emit unchecked device commands.

## Geometry and colour

Existing fallback uses 300 dpi, 2480×3507 A4 RGB. Preserve this as a comparison case, not a correct specification. A4 is 210×297 mm; Letter is 8.5×11 in. Derive pixel dimensions with a documented rounding convention and confirmed imageable margins. Validate using rulers, edge boxes, rotation, crop boxes and mixed page sizes; do not stretch A4 to Letter. At 300 dpi Letter nominally has 2550×3300 pixels before margins.

Define tagged RGB input, ColorSync/profile handling, rendering intent and alpha compositing onto white. Convert monochrome explicitly; verify whether device Mono uses composite inks or black only before making ink claims. Preserve gradients and neutral grays; determine whether vendor output expects contone or halftoned planes experimentally. Do not apply both host and device colour corrections blindly. Draft/Normal/Fine may alter packing, halftoning or passes; implement from evidence independently for each mode.

## Verification sequence

First implement a safe independent decoder and protocol validator. Then blank page framing, single-colour patterns, channel/stride tests, page boundaries, mode parameters and compression. Test random/truncated input, extreme lengths, output failure and cancellation under sanitizers/fuzzing. Freeze reviewed public protocol facts and source-generated fixtures; vendor output stays local. Physical scale, colour, gradients, quality and multipage acceptance follow only after parser and framing gates. A release converter has no call or runtime dependency on the Linux binary.
