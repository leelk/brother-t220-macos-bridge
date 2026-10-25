# SPDX-License-Identifier: Apache-2.0
"""Offline PDF -> macOS raster -> native PJL/PWG tests. Never submits to a queue."""
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from generate_pdf import generate

binary, inspector = map(str,sys.argv[1:3])
ppd=Path(__file__).resolve().parent/"config/Brother_DCP_T220_Native.ppd"
checks=0

def convert(raster,output,options,copies="1",valid=True):
    global checks
    with output.open("wb") as target:
        result=subprocess.run([binary,"1","synthetic","test",copies,options,str(raster)],stdout=target,stderr=subprocess.PIPE)
    assert (result.returncode==0)==valid,(options,result.stderr.decode())
    checks+=1
    if not valid: assert output.stat().st_size==0,(options,output.stat().st_size)
    return result

def inspect(path):
    return json.loads(subprocess.check_output([inspector,str(path)]))

with tempfile.TemporaryDirectory() as directory:
    root=Path(directory)
    sample=None
    fingerprints={}
    for paper,color,quality in itertools.product(["A4","Letter"],["RGB","Gray"],["Draft","Normal","Fine"]):
        tag=f"{paper}-{color}-{quality}"
        pdf=root/(tag+".pdf");generate(pdf,[paper,paper])
        raster=root/(tag+".ras");output=root/(tag+".prn")
        opts=f"PageSize={paper} ColorModel={color} PrintQuality={quality}"
        with raster.open("wb") as target:
            result=subprocess.run(["/usr/sbin/cupsfilter","-i","application/pdf","-m","application/vnd.cups-raster","-p",str(ppd),
                "-o",f"PageSize={paper}","-o",f"ColorModel={color}","-o",f"PrintQuality={quality}",str(pdf)],stdout=target,stderr=subprocess.PIPE)
        assert result.returncode==0,result.stderr.decode()
        convert(raster,output,opts)
        b=output.read_bytes()
        for token in [f"PAPER={paper.upper()}",f"RENDERMODE={'COLOR' if color=='RGB' else 'GRAYSCALE'}",
                      "PRINTQUALITY="+{'Draft':'DRAFT','Normal':'NORMAL','Fine':'HIGH'}[quality]]:
            assert b.count(("@PJL SET "+token+"\n").encode())==2,token
        pages=inspect(output);assert len(pages)==2,pages
        width,height=(2480,3507) if paper=="A4" else (2550,3300)
        for page in pages:
            assert (page["width"],page["height"],page["channels"],page["dpi"])==(width,height,3 if color=="RGB" else 1,300),page
            assert page["chromatic"] == (color=="RGB") and page["white_edge"],page
        assert pages[0]["fnv1a64"]!=pages[1]["fnv1a64"],"Numbered pages lost identity"
        key=(paper,color)
        if key in fingerprints:assert fingerprints[key]==[p["fnv1a64"] for p in pages],"Quality unexpectedly changes host raster"
        else:fingerprints[key]=[p["fnv1a64"] for p in pages]
        if paper=="A4" and color=="RGB" and quality=="Normal":sample=raster
        print("PASS",tag,"two pages",flush=True)
    output=root/"failure.prn"
    for options in ["print-quality=9","print-color-mode=auto","ColorModel=bad","PrintQuality=bad","sides=two-sided-long-edge","PageSize=A3","media=iso_a3_297x420mm"]:
        convert(sample,output,options,valid=False)
    for copies in ["0","-1","100","oops"]:convert(sample,output,"",copies=copies,valid=False)
    convert(root/"missing.ras",output,"",valid=False)
    truncated=root/"truncated.ras";data=sample.read_bytes();truncated.write_bytes(data[:len(data)//2])
    convert(truncated,output,"",valid=False)
    convert(sample,output,"print-quality=3 print-color-mode=monochrome",copies="2")
    pages=inspect(output);assert len(pages)==4 and all(p["channels"]==1 for p in pages)
    assert [p["fnv1a64"] for p in pages[:2]]==[p["fnv1a64"] for p in pages[2:]]
print(f"PASS: {checks} native pipeline jobs; 12 two-page combinations; no printing")
