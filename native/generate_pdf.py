# SPDX-License-Identifier: Apache-2.0
"""Create synthetic vector PDF pages for offline/explicitly authorized print tests."""
import argparse
from pathlib import Path

SIZES = {"A4": (595.276, 841.890), "Letter": (612,792)}

def generate(path, papers):
    if not papers or any(p not in SIZES for p in papers): raise ValueError("Unsupported paper")
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>", b"", b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    children = []
    for number, paper in enumerate(papers,1):
        w,h = SIZES[paper]
        page_id = len(objects)+1; content_id=page_id+1; children.append(page_id)
        stream = (f"1 1 1 rg 0 0 {w} {h} re f\n"
                  f"0 0 0 rg BT /F1 18 Tf 36 {h-50} Td (Native DCP-T220 test - page {number} - {paper}) Tj ET\n"
                  f"0 0 0 RG 0.5 w 36 36 {w-72} {h-72} re S\n"
                  f"BT /F1 10 Tf 36 {h-70} Td (Synthetic content. No physical print unless explicitly authorized.) Tj ET\n")
        for i,(red,green,blue) in enumerate([(1,0,0),(0,1,0),(0,0,1),(0,1,1),(1,0,1),(1,1,0)]):
            stream += f"{red} {green} {blue} rg {36+i*75} {h-160} 60 60 re f\n"
        for i in range(16):
            gray=i/15
            stream += f"{gray:.6f} {gray:.6f} {gray:.6f} rg {36+i*28} {h-220} 28 25 re f\n"
        stream += f"0 0 0 RG 0.5 w 36 80 m {36+100*72/25.4:.6f} 80 l S\n"
        stream += "0 0 0 rg BT /F1 10 Tf 36 63 Td (100 mm scale reference - verify only on physical output) Tj ET\n"
        data=stream.encode("ascii")
        objects.extend([f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {w} {h}] /Resources << /Font << /F1 3 0 R >> >> /Contents {content_id} 0 R >>".encode(),
                        f"<< /Length {len(data)} >>\nstream\n".encode()+data+b"endstream"])
    objects[1]=f"<< /Type /Pages /Count {len(papers)} /Kids [{' '.join(f'{n} 0 R' for n in children)}] >>".encode()
    output=bytearray(b"%PDF-1.4\n% synthetic test document\n");offsets=[0]
    for n,data in enumerate(objects,1):
        offsets.append(len(output));output.extend(f"{n} 0 obj\n".encode()+data+b"\nendobj\n")
    start=len(output);output.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]: output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n".encode())
    with Path(path).open("xb") as target: target.write(output)

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output");parser.add_argument("--papers",nargs="+",choices=SIZES,default=["A4","A4"])
    args=parser.parse_args();generate(args.output,args.papers)
