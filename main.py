#!/usr/bin/env python3
"""Copy the entry image to the output directory, verified.

The entry for make.fun competition news-image-20261118: one image summing
up the world's news of Wednesday 18 November 2026, drawn with PIL
(draw_infographic.py) and held in this repo as entry.png. This program
copies it unchanged to $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png),
then verifies the copy byte-for-byte.

Run locally:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

MAX_BYTES = 1048576
SOURCE = Path(__file__).resolve().parent / "entry.png"


def main():
    if not SOURCE.is_file():
        raise SystemExit("entry.png is missing beside main.py: %s" % SOURCE)
    if SOURCE.stat().st_size > MAX_BYTES:
        raise SystemExit("entry.png is larger than 1 MiB: %d bytes"
                         % SOURCE.stat().st_size)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)
    if dest.read_bytes() != SOURCE.read_bytes():
        raise SystemExit("verification failed: copied file differs from entry.png")
    print("copied %d bytes to %s (verified)" % (dest.stat().st_size, dest))


if __name__ == "__main__":
    main()
