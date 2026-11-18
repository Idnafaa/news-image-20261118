"""Put the v3 poster where the grader looks for it.

This entry for news-image-20261118 keeps its front page as entry.png in
the repo root. The grader reads /output/entry.png, so this script copies
the file there byte for byte. Standard library only, no network, no
clock: running it twice produces identical output. Check locally with:
MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(DST_DIR, exist_ok=True)
shutil.copyfile(SRC, os.path.join(DST_DIR, "entry.png"))
