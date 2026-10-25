# SPDX-License-Identifier: Apache-2.0
"""Owned deterministic RGB sample fixtures; no printer/proprietary dependencies."""
import argparse
import hashlib
import json
from pathlib import Path

PALETTE = [(255,255,255), (0,0,0), (255,0,0), (0,255,0),
           (0,0,255), (0,255,255), (255,0,255), (255,255,0)]
PATTERNS = ("white", "black", "patches", "ramp", "alternating", "row-marker")

def row(pattern, width, y):
    if pattern == "white": return bytes([255,255,255]) * width
    if pattern == "black": return bytes(width * 3)
    if pattern == "patches":
        return bytes(c for x in range(width) for c in PALETTE[min(7, x * 8 // width)])
    if pattern == "ramp":
        return bytes(c for x in range(width) for c in [x * 255 // max(1,width-1)] * 3)
    if pattern == "alternating":
        return bytes(c for x in range(width) for c in [(x+y) % 2 * 255] * 3)
    if pattern == "row-marker": return bytes([y % 256, (y // 256) % 256, 255]) * width
    raise ValueError("Unknown pattern")

def generate(path, width, height, pattern):
    if not (1 <= width <= 10000 and 1 <= height <= 10000): raise ValueError("Invalid dimensions")
    if width * height * 3 > 128 * 1024 * 1024: raise ValueError("Raster too large")
    if pattern not in PATTERNS: raise ValueError("Unknown pattern")
    digest = hashlib.sha256()
    # Exclusive creation prevents overwriting an existing reference.
    with Path(path).open("xb") as output:
        header = f"P6\n{width} {height}\n255\n".encode("ascii")
        output.write(header); digest.update(header)
        for y in range(height):
            data = row(pattern, width, y)
            output.write(data); digest.update(data)
    return dict(schema_version=1, generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                pattern=pattern, width=width, height=height, channels="RGB", bits_per_channel=8,
                color_encoding="synthetic sample values; no ICC profile or colourimetric claim",
                dpi=None, sha256=digest.hexdigest())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output")
    parser.add_argument("--width", type=int, default=257)
    parser.add_argument("--height", type=int, default=259)
    parser.add_argument("--pattern", choices=PATTERNS, default="patches")
    args = parser.parse_args()
    print(json.dumps(generate(args.output, args.width, args.height, args.pattern), sort_keys=True))
