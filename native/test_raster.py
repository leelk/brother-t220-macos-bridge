# SPDX-License-Identifier: Apache-2.0
"""Integration checks for independent generator and native band reader; no printing."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from generate_raster import generate, PATTERNS

binary = sys.argv[1]
checks = 0

def run(path, success):
    global checks
    result = subprocess.run([binary, str(path)], capture_output=True, text=True)
    assert result.returncode == (0 if success else 2), result.stderr
    checks += 1
    if not success:
        assert not result.stdout
        return None
    return json.loads(result.stdout)

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    for pattern in PATTERNS:
        path = root / (pattern + ".ppm")
        manifest = generate(path, 257, 259, pattern)
        data = path.read_bytes(); payload = data.split(b"\n",3)[3]
        assert manifest["sha256"] == hashlib.sha256(data).hexdigest()
        hash_value = 14695981039346656037
        for byte in payload:
            hash_value = ((hash_value ^ byte) * 1099511628211) & ((1 << 64)-1)
        result = run(path, True)
        assert result == dict(width=257,height=259,payload_bytes=257*259*3,
                              bands=3,max_band_bytes=257*128*3,fnv1a64=hash_value)
        twin = root / (pattern + "-again.ppm")
        assert generate(twin,257,259,pattern) == manifest
        assert twin.read_bytes() == data
    for index, first in enumerate([0, 9, 10, 13, 32, 35, 255]):
        path = root / f"byte-{index}.ppm"
        path.write_bytes(b"P6\n1 1\n255\n" + bytes([first,0,255]))
        run(path, True)  # Header parser must never eat initial payload whitespace/#.
    invalid = [b"", b"P3\n1 1\n255\nabc", b"P6\n0 1\n255\n",
        b"P6\n10001 1\n255\n", b"P6\n10000 10000\n255\n",
        b"P6\n-1 1\n255\n", b"P6\n1 1\n65535\nabc", b"P6\n1 1\n255\nab",
        b"P6\n1 1\n255\nabcEXTRA", b"P6\n1  1\n255\nabc",
        b"P6\n" + b"9"*100 + b" 1\n255\n", b"P6\n1 1\n255\nabcP6\n1 1\n255\nabc"]
    for index, data in enumerate(invalid):
        path = root / f"bad-{index}.ppm"; path.write_bytes(data); run(path,False)
    run(root / "missing.ppm", False)
    # Standard A4-sized sample is consumed in bounded bands, no full-page native buffer.
    large = root / "a4.ppm"; generate(large,2480,3507,"white")
    result = run(large,True)
    assert result["payload_bytes"] == 26092080
    assert result["bands"] == 28 and result["max_band_bytes"] == 952320
print(f"PASS: {checks} native raster checks plus fixture reproducibility/hash checks; no printing")
