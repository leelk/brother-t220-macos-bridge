# SPDX-License-Identifier: Apache-2.0
"""Exercise queue setup decisions with fake commands in a temporary directory.
The production helper is not run against the real printer or administrator paths.
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile

source=Path(__file__).resolve().parent/"packaging/manage-driver.sh"
checks=0
with tempfile.TemporaryDirectory() as directory:
    root=Path(directory);binpath=root/"bin";binpath.mkdir()
    base=root/"driver"; (base/"versions/0.1.0").mkdir(parents=True)
    binary=base/"versions/0.1.0/brother-t220-native";binary.touch();binary.chmod(0o755)
    ppd=root/"test.ppd";ppd.touch();state=root/"state";state.mkdir()
    capture=root/"calls.jsonl"
    command=binpath/"fake-command"
    command.write_text(r"""#!/usr/bin/python3
import json,os,sys
from pathlib import Path
name=Path(sys.argv[0]).name
if name=='id': print(os.environ.get('FAKE_UID','0'))
elif name=='lpinfo': print(os.environ.get('FAKE_DEVICES',''))
elif name=='lpstat':
 if '-o' in sys.argv:
  if os.environ.get('FAKE_BUSY')=='1': print('pending-job 1')
 elif '-p' in sys.argv: sys.exit(0 if os.environ.get('FAKE_QUEUE')=='1' else 1)
elif name=='lpadmin':
 with open(os.environ['CAPTURE'],'a') as out: out.write(json.dumps(sys.argv[1:])+'\n')
 sys.exit(int(os.environ.get('FAKE_ADMIN_EXIT','0')))
else: sys.exit(99)
""")
    command.chmod(0o755)
    for name in ['id','lpinfo','lpstat','lpadmin']:(binpath/name).symlink_to(command)
    # Hardcoded production paths become only temporary paths in this test copy.
    text=source.read_text().replace('PATH=/usr/bin:/bin:/usr/sbin:/sbin',f'PATH={binpath}:/usr/bin:/bin')
    current=root/"current.ppd";current.write_text('/Library/Printers/leelk/BrotherT220/versions/0.1.0/')
    text=text.replace('CURRENT=/etc/cups/ppd/Brother_T220_Native.ppd',f'CURRENT={current}')
    text=text.replace('BASE=/Library/Printers/leelk/BrotherT220',f'BASE={base}')
    text=text.replace('PPD=/Library/Printers/PPDs/Contents/Resources/Brother_DCP_T220_Native.ppd',f'PPD={ppd}')
    text=text.replace("STATE='/Library/Application Support/leelk/BrotherT220'",f'STATE={state}')
    script=root/"helper.sh";script.write_text(text)
    def run(operation,ok,**values):
        global checks
        capture.unlink(missing_ok=True)
        env={k:v for k,v in os.environ.items() if not k.startswith('FAKE_')}
        env.update(CAPTURE=str(capture));env.update(values)
        result=subprocess.run(['/bin/sh',str(script),operation],env=env,capture_output=True,text=True)
        assert (result.returncode==0)==ok,(operation,result.stdout,result.stderr)
        checks+=1
        return [json.loads(line) for line in capture.read_text().splitlines()] if capture.exists() else []
    assert not run('configure',False,FAKE_UID='501')
    assert not run('configure',False)
    assert not run('configure-if-connected',True)
    assert not run('configure',False,FAKE_BUSY='1')
    device='direct usb://Brother/DCP-T220?serial=SYNTHETIC'
    calls=run('configure',True,FAKE_DEVICES=device)
    assert len(calls)==1 and calls[0][calls[0].index('-p')+1]=='Brother_T220_Native'
    assert calls[0][calls[0].index('-v')+1]=='usb://Brother/DCP-T220?serial=SYNTHETIC'
    assert 'printer-error-policy=abort-job' in calls[0]
    assert not run('configure',False,FAKE_DEVICES=device+'\n'+device)
    assert not run('configure',False,FAKE_DEVICES='direct usb://Brother/DCP-T2200?serial=OTHER')
    run('configure',False,FAKE_DEVICES=device,FAKE_ADMIN_EXIT='1')
    assert not run('remove',False,FAKE_BUSY='1',FAKE_QUEUE='1')
    assert not run('remove',True)
    assert run('remove',True,FAKE_QUEUE='1')==[['-x','Brother_T220_Native']]
    assert not run('rollback',False)
    (state/'previous.ppd').touch();(state/'previous-uri').write_text('usb://Brother/DCP-T220?serial=PREVIOUS')
    calls=run('rollback',True)
    assert len(calls)==1 and str(state/'previous.ppd') in calls[0]
    (state/'previous-uri').write_text('ipp://unrelated.invalid/printer')
    assert not run('rollback',False)
    assert not run('unknown',False)
    current.write_text('another driver')
    assert not run('remove',False,FAKE_QUEUE='1')
    assert not run('configure',False,FAKE_QUEUE='1',FAKE_DEVICES=device)
print(f'PASS: {checks} mocked setup/rollback/removal scenarios; no real queue changes')
