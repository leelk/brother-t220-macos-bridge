#!/usr/bin/env python3

import argparse
import sys
import subprocess
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONVERTER = BASE_DIR / "convert-brother.sh"
PRINTER_QUEUE = "Brother_T220_Test"

def print_document(pdf_path, color_mode="color", quality="normal"):
    if color_mode not in ("auto", "color", "monochrome"):
        raise ValueError(f"Unsupported color mode: {color_mode}")
    if quality not in ("draft", "normal", "high"):
        raise ValueError(f"Unsupported quality: {quality}")
    pdf_path = Path(pdf_path).expanduser().resolve()

    if not pdf_path.is_file():
        raise FileNotFoundError(f"Document not found: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF documents are supported")

    with tempfile.TemporaryDirectory() as temp_dir:
        output = Path(temp_dir) / "document.prn"

        print("Converting document...")
        subprocess.run(
            [str(CONVERTER), str(pdf_path), str(output), color_mode, quality],
            check=True
        )

        if not output.is_file() or output.stat().st_size == 0:
            raise RuntimeError("Converter produced no printer data")

        print("Sending document to Brother printer...")
        subprocess.run(
            ["lp", "-d", PRINTER_QUEUE, "-o", "raw", str(output)],
            check=True
        )

        print("Print job submitted successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print a PDF through the Brother bridge")
    parser.add_argument("document")
    parser.add_argument("--color-mode", choices=("auto", "color", "monochrome"),
                        default="color")
    parser.add_argument("--quality", choices=("draft", "normal", "high"),
                        default="normal")
    args = parser.parse_args()
    try:
        print_document(args.document, args.color_mode, args.quality)
    except (OSError, ValueError, RuntimeError,
            subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
