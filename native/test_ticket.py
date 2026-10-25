# SPDX-License-Identifier: Apache-2.0
"""Native CLI contract checks. Pass the compiled executable as the only argument."""
import itertools
import json
import subprocess
import sys

binary = sys.argv[1]
checks = 0

def run(args, expected=None):
    global checks
    result = subprocess.run([binary, *args], capture_output=True, text=True, check=False)
    if expected is None:
        assert result.returncode == 2 and not result.stdout, (args, result)
    else:
        assert result.returncode == 0, (args, result.stderr)
        assert json.loads(result.stdout) == expected, (args, result.stdout)
    checks += 1

def expected(media="iso_a4_210x297mm", color="color", quality=4):
    return dict(media=media, color_mode=color, print_quality=quality,
                device_quality={3:"Draft", 4:"Normal", 5:"Fine"}[quality])

run([], expected())
for media, color, quality in itertools.product(
        ["iso_a4_210x297mm", "na_letter_8.5x11in"],
        ["color", "monochrome"], [3, 4, 5]):
    run(["--media", media, "--color-mode", color, "--quality", str(quality)],
        expected(media, color, quality))
for keyword, quality in [("draft",3), ("normal",4), ("high",5)]:
    run(["--quality",keyword], expected(quality=quality))
for args in [["--quality","6"], ["--quality","Fine"], ["--quality",""],
             ["--color-mode","auto"], ["--color-mode","rgb"],
             ["--media","A3"], ["--media",""], ["--quality"],
             ["--unknown","value"], ["--quality","3","--quality","5"],
             ["--media","iso_a4_210x297mm","extra"],
             ["--media","na_letter_8.5x11in","--color-mode","monochrome","--quality","bad"]]:
    run(args)
# A new job must recover defaults after the preceding jobs/errors.
run([], expected())
print(f"PASS: {checks} native ticket contract checks; no printing")
