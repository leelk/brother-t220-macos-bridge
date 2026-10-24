"""Exercise wrapper -> Python -> converter with fake Docker and lp; no printing."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ColorModeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        (self.base / 'ipp-test').mkdir()
        for name in ('brother-bridge.py', 'convert-brother.sh', 'ipp-test/print-job.sh'):
            shutil.copy2(ROOT / name, self.base / name)
        driver = self.base / 'extracted/opt/brother/Printers/dcpt220'
        (driver / 'inf').mkdir(parents=True)
        (driver / 'lpd/x86_64').mkdir(parents=True)
        self.rc = driver / 'inf/brdcpt220rc'
        self.original = 'PageSize=A4\nBRResolution=Normal\nBRMonoColor=FullColor\n'
        self.rc.write_text(self.original)
        binary = driver / 'lpd/x86_64/brdcpt220filter'
        binary.touch()
        binary.chmod(0o755)
        bindir = self.base / 'bin'
        bindir.mkdir()
        docker = bindir / 'docker'
        docker.write_text('''#!/usr/bin/python3
import os, pathlib, sys
args = sys.argv[1:]
for i, arg in enumerate(args):
    if arg == '-v' and args[i+1].endswith(':/work'):
        work = pathlib.Path(args[i+1][:-6])
        with open(os.environ['CAPTURE'], 'a') as out:
            out.write((work / 'printer.rc').read_text())
        (work / 'output.prn').write_bytes(b'fake printer data')
''')
        docker.chmod(0o755)
        lp = bindir / 'lp'
        lp.write_text('#!/bin/sh\nprintf "submitted\\n" >> "$SUBMISSIONS"\n')
        lp.chmod(0o755)
        self.capture = self.base / 'capture'
        self.submissions = self.base / 'submissions'
        self.env = {k: v for k, v in os.environ.items() if not k.startswith('IPP_')}
        self.env.update(PATH=str(bindir) + ':' + os.environ['PATH'],
                        CAPTURE=str(self.capture), SUBMISSIONS=str(self.submissions))
        self.pdf = self.base / 'document with spaces.pdf'
        self.pdf.write_bytes(b'%PDF-1.4\nmock input; Docker is stubbed\n')

    def run_job(self, mode=None, default=None):
        env = self.env.copy()
        if mode is not None:
            env['IPP_PRINT_COLOR_MODE'] = mode
        if default is not None:
            env['IPP_PRINT_COLOR_MODE_DEFAULT'] = default
        return subprocess.run(['bash', str(self.base / 'ipp-test/print-job.sh'),
                               str(self.pdf)], env=env, capture_output=True)

    def test_job_modes_and_isolation(self):
        for mode, expected in [(None, 'FullColor'), ('monochrome', 'Mono'),
                               ('color', 'FullColor'), ('auto', 'FullColor')]:
            with self.subTest(mode=mode):
                self.capture.unlink(missing_ok=True)
                result = self.run_job(mode)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('BRMonoColor=' + expected + '\n', self.capture.read_text())
                self.assertEqual(self.rc.read_text(), self.original)
        self.assertEqual(len(self.submissions.read_text().splitlines()), 4)

    def test_default_and_explicit_override(self):
        self.assertEqual(self.run_job(default='monochrome').returncode, 0)
        self.assertIn('BRMonoColor=Mono', self.capture.read_text())
        self.capture.unlink()
        self.assertEqual(self.run_job('color', 'monochrome').returncode, 0)
        self.assertIn('BRMonoColor=FullColor', self.capture.read_text())

    def test_invalid_mode_does_not_submit(self):
        self.assertNotEqual(self.run_job('invalid').returncode, 0)
        self.assertFalse(self.capture.exists())
        self.assertFalse(self.submissions.exists())
        result = subprocess.run(['bash', str(self.base / 'convert-brother.sh'),
                                 str(self.pdf), str(self.base / 'out.prn'), 'invalid'],
                                env=self.env, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.submissions.exists())

    def test_direct_converter_keeps_color_default(self):
        result = subprocess.run(['bash', str(self.base / 'convert-brother.sh'),
                                 str(self.pdf), str(self.base / 'out.prn')],
                                env=self.env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('BRMonoColor=FullColor', self.capture.read_text())

if __name__ == '__main__':
    unittest.main()
