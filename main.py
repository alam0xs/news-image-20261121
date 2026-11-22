"""Assemble the entry image from three base64 chunks.

The PNG image is stored split across three sibling modules
(img_part1, img_part2, img_part3), each exposing a string constant
DATA holding a consecutive chunk of one base64-encoded PNG file.
This program concatenates the chunks in order, decodes them, and
writes the resulting bytes to the output file.
"""

import base64
import os
import sys

# The -P flag (and running from another directory) keeps this script's
# own directory off sys.path, so make the sibling modules importable.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from img_part1 import DATA as DATA1
from img_part2 import DATA as DATA2
from img_part3 import DATA as DATA3


def main() -> int:
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    elif os.environ.get("MAKEFUN_OUTPUT_DIR"):
        output_path = os.path.join(os.environ["MAKEFUN_OUTPUT_DIR"], "entry.png")
    else:
        output_path = "/output/entry.png"

    try:
        encoded = DATA1 + DATA2 + DATA3
        image_bytes = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        print(f"error: failed to decode image data: {exc}", file=sys.stderr)
        return 1

    try:
        parent = os.path.dirname(os.path.abspath(output_path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(output_path, "wb") as fh:
            fh.write(image_bytes)
    except OSError as exc:
        print(f"error: failed to write {output_path}: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {output_path} ({len(image_bytes)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
