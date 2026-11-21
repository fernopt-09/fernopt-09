#!/usr/bin/env python3
"""Убирает заголовок «Contributions calendar» из SVG, который рисует metrics."""

from __future__ import annotations

import re
import sys
from pathlib import Path

HEADER_HEIGHT = 30


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "metrics.isocalendar.svg")
    svg = path.read_text(encoding="utf-8")

    without_header, removed = re.subn(
        r'<h2 class="field">\s*<svg[\s\S]*?</svg>\s*Contributions calendar\s*</h2>',
        "",
        svg,
        count=1,
    )
    if not removed:
        print("isocalendar header not found; nothing to do")
        return 0

    outer = re.search(r"<svg\b[^>]*>", without_header)
    if not outer:
        print("could not find the outer <svg> tag", file=sys.stderr)
        return 1

    tag = outer.group(0)
    new_tag, replaced = re.subn(
        r'height="(\d+)"',
        lambda m: f'height="{max(int(m.group(1)) - HEADER_HEIGHT, 1)}"',
        tag,
        count=1,
    )
    if not replaced:
        print("could not find the SVG height", file=sys.stderr)
        return 1

    result = without_header[: outer.start()] + new_tag + without_header[outer.end() :]
    path.write_text(result, encoding="utf-8")
    print(f"removed isocalendar header: {tag} -> {new_tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
