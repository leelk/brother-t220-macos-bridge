# SPDX-License-Identifier: Apache-2.0
"""Inspect a generated package without installing it or running installer scripts."""
import json
from pathlib import Path
import plistlib
import re
import subprocess
import sys
import tempfile

package=Path(sys.argv[1]).resolve()
with tempfile.TemporaryDirectory() as directory:
    expanded=Path(directory)/"expanded"
    subprocess.run(["/usr/sbin/pkgutil","--expand-full",str(package),str(expanded)],check=True)
    root=expanded/"Payload"
    base=root/"Library/Printers/leelk/BrotherT220"
    binary=base/"versions/0.1.0/brother-t220-native"
    app=root/"Applications/Brother T220 Native Setup.app"
    ppd=root/"Library/Printers/PPDs/Contents/Resources/Brother_DCP_T220_Native.ppd"
    assert binary.is_file() and ppd.is_file() and (base/"LICENSE").is_file()
    info=plistlib.loads((app/"Contents/Info.plist").read_bytes())
    assert info["CFBundleIdentifier"]=="com.leelk.brother-t220-native.setup"
    for target in [binary,app/"Contents/MacOS/BrotherT220Setup"]:
        text=subprocess.check_output(["/usr/bin/file",str(target)],text=True)
        assert 'arm64' in text,text
        deps=subprocess.check_output(["/usr/bin/otool","-L",str(target)],text=True).splitlines()[1:]
        assert all(line.strip().startswith(("/usr/lib/","/System/Library/")) for line in deps),deps
    for target in [binary,app]:subprocess.run(["/usr/bin/codesign","--verify","--strict",str(target)],check=True)
    subprocess.run(["/usr/bin/cupstestppd","-W","filters","-R",str(root),str(ppd)],check=True)
    bom=subprocess.check_output(["/usr/bin/lsbom","-p","fMUG",str(expanded/"Bom")],text=True)
    line=next(line for line in bom.splitlines() if line.split('\t')[0].endswith('/0.1.0/brother-t220-native'))
    assert 'root' in line and 'wheel' in line and '-rwxr-xr-x' in line,line
    for path in root.rglob('*'):
        if path.is_file() and not path.name.startswith('._'):
            assert path.suffix not in ['.deb','.prn','.ppm','.ras','.raw','.log'],path
            assert path.name not in ['brdcpt220filter','brprintconf_dcpt220'],path
    source=Path(__file__).resolve().parent/"packaging"
    for name in ['preinstall','postinstall']:
        assert (expanded/"Scripts"/name).read_bytes()==(source/name).read_bytes()
        subprocess.run(["/bin/sh","-n",str(expanded/"Scripts"/name)],check=True)
    assert (base/"manage-driver.sh").read_bytes()==(source/"manage-driver.sh").read_bytes()
print('PASS: package contents, native architectures, system-only linkage, signatures, ownership, PPD and scripts; no installation or printing')
