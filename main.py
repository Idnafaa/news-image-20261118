"""News-image entry for 18 November 2026 (Python 3.13, stdlib only).

The poster itself is stored in this repository as entry.png; it was
drawn by render.py from the day's reported news. This program has a
single job: place that image where the grader expects it, as
/output/entry.png. It reads nothing from the network, consults no
clock and rolls no dice, so every run writes exactly the same bytes.
Run locally with MAKEFUN_OUTPUT_DIR=out python3 main.py.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
# Byte-for-byte copy: identical input, identical output, every run.
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
