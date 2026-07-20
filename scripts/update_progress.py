#!/usr/bin/env python3
"""Regenerate assets/progress.svg and the README badge from solution counts.

Solved = number of .cpp files in each solutions/ subfolder (+ EXTRA overrides).
Run after adding a solution: python3 scripts/update_progress.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATEGORIES = [
    ("01_arrays_hashing", "Arrays & Hashing", 9),
    ("02_two_pointers", "Two Pointers", 5),
    ("03_sliding_window", "Sliding Window", 6),
    ("04_stack", "Stack", 6),
    ("05_binary_search", "Binary Search", 7),
    ("06_linked_list", "Linked List", 11),
    ("07_trees", "Trees", 15),
    ("08_heap_priority_queue", "Heap / Priority Queue", 7),
    ("09_backtracking", "Backtracking", 10),
    ("10_tries", "Tries", 3),
    ("11_graphs", "Graphs", 13),
    ("12_advanced_graphs", "Advanced Graphs", 6),
    ("13_dp_1d", "1-D Dynamic Programming", 12),
    ("14_dp_2d", "2-D Dynamic Programming", 11),
    ("15_greedy", "Greedy", 8),
    ("16_intervals", "Intervals", 6),
    ("17_math_geometry", "Math & Geometry", 8),
    ("18_bit_manipulation", "Bit Manipulation", 7),
]

# Problems solved but not yet committed as .cpp files — remove entries once committed.
EXTRA = {"01_arrays_hashing": 1}

BG = "#0d1117"
CARD = "#161b22"
BORDER = "#30363d"
TRACK = "#21262d"
TEXT = "#e6edf3"
MUTED = "#8b949e"
FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"


def solved_count(folder: str) -> int:
    d = ROOT / "solutions" / folder
    n = len(list(d.glob("*.cpp"))) if d.is_dir() else 0
    return n + EXTRA.get(folder, 0)


def bar(x, y, w, h, frac, grad="url(#grad)"):
    fill_w = 0 if frac <= 0 else max(h, frac * w)
    fill_w = min(fill_w, w)
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{TRACK}"/>']
    if fill_w > 0:
        parts.append(f'<rect x="{x}" y="{y}" width="{fill_w:.1f}" height="{h}" rx="{h/2}" fill="{grad}"/>')
    return "".join(parts)


def build_svg() -> str:
    counts = {f: solved_count(f) for f, _, _ in CATEGORIES}
    total = sum(t for _, _, t in CATEGORIES)
    done = sum(counts.values())
    pct = 100 * done / total

    W, PAD = 880, 24
    COLS, GAP = 2, 12
    CARD_W = (W - 2 * PAD - GAP * (COLS - 1)) / COLS
    CARD_H = 64
    HEADER_H = 118
    rows = (len(CATEGORIES) + COLS - 1) // COLS
    H = HEADER_H + rows * CARD_H + (rows - 1) * GAP + PAD

    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<defs><linearGradient id="grad" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%" stop-color="#26a641"/><stop offset="100%" stop-color="#39d353"/>'
        "</linearGradient></defs>",
        f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>',
        # header
        f'<text x="{PAD}" y="{PAD + 18}" font-family="{FONT}" font-size="13" font-weight="600" '
        f'letter-spacing="3" fill="{MUTED}">NEETCODE 150</text>',
        f'<text x="{PAD}" y="{PAD + 52}" font-family="{FONT}" font-size="30" font-weight="700" '
        f'fill="{TEXT}">{done} <tspan fill="{MUTED}" font-size="20" font-weight="500">/ {total} solved</tspan></text>',
        f'<text x="{W - PAD}" y="{PAD + 52}" text-anchor="end" font-family="{MONO}" font-size="22" '
        f'font-weight="600" fill="#39d353">{pct:.1f}%</text>',
        bar(PAD, PAD + 68, W - 2 * PAD, 12, done / total),
    ]

    for i, (folder, label, cat_total) in enumerate(CATEGORIES):
        col, row = i % COLS, i // COLS
        x = PAD + col * (CARD_W + GAP)
        y = HEADER_H + row * (CARD_H + GAP)
        c = counts[folder]
        s += [
            f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="10" '
            f'fill="{CARD}" stroke="{BORDER}"/>',
            f'<text x="{x + 16}" y="{y + 26}" font-family="{FONT}" font-size="13.5" '
            f'font-weight="600" fill="{TEXT}">{label.replace("&", "&amp;")}</text>',
            f'<text x="{x + CARD_W - 16}" y="{y + 26}" text-anchor="end" font-family="{MONO}" '
            f'font-size="12.5" fill="{"#39d353" if c else MUTED}">{c} / {cat_total}</text>',
            bar(x + 16, y + 40, CARD_W - 32, 8, c / cat_total),
        ]

    s.append("</svg>")
    return "\n".join(s)


def main():
    total = sum(t for _, _, t in CATEGORIES)
    done = sum(solved_count(f) for f, _, _ in CATEGORIES)

    out = ROOT / "assets" / "progress.svg"
    out.parent.mkdir(exist_ok=True)
    out.write_text(build_svg())

    readme = ROOT / "README.md"
    txt = readme.read_text()
    txt = re.sub(r"NeetCode_150-\d+%20%2F%20\d+", f"NeetCode_150-{done}%20%2F%20{total}", txt)
    readme.write_text(txt)

    print(f"{done} / {total} solved — wrote {out.relative_to(ROOT)} and updated README badge")


if __name__ == "__main__":
    main()
