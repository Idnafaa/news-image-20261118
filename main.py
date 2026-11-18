"""Hand the finished v4 front page to the grader.

The poster for Wednesday 18 November 2026 lives next to this script as
entry.png. The grader runs this file and expects the picture at
/output/entry.png, so all this does is copy it there.
"""

import os
import shutil


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    target_dir = "/output"
    os.makedirs(target_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(target_dir, "entry.png"))


if __name__ == "__main__":
    run()
