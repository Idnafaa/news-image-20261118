"""News-image entry, 18 November 2026 (Python 3.13, stdlib only).

The front page is stored in this repository as entry.png; render.py
drew it from news first reported on Wednesday 18 November 2026. This
program does one thing: put that image where the grader looks for it,
as /output/entry.png. No network, no clock, no randomness, so every
run writes exactly the same bytes. Local check:
MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
# A plain copy: same input in, same bytes out, on every run.
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
