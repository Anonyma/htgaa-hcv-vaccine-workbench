#!/usr/bin/env python3
"""Generate reviewer SVG plots from bundled or regenerated workbench outputs."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PACKAGE_ROOT / "notebook-output"


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    return paths[0]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_conservation_plot(path: Path, conservation_path: Path, windows_path: Path) -> None:
    cons_data = [
        {
            "pos": int(row["alignment_position"]),
            "cons": float(row["conservation"]),
            "residue": row["consensus_residue"],
        }
        for row in read_csv(conservation_path)
    ]
    windows = [
        {
            "start": int(row["start_alignment_position"]),
            "end": int(row["end_alignment_position"]),
            "mean_cons": float(row["mean_conservation"]),
        }
        for row in read_csv(windows_path)
    ]

    width, height = 1400, 280
    left, right, top, bottom = 60, 1380, 30, 240
    chart_width, chart_height = right - left, bottom - top
    mean_cons = sum(row["cons"] for row in cons_data) / len(cons_data)

    parts = [
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
    ]
    for y_value in [0.0, 0.25, 0.50, 0.75, 1.0]:
        y = bottom - y_value * chart_height
        parts.append(f'<line x1="{left}" y1="{y:.0f}" x2="{right}" y2="{y:.0f}" stroke="#d8e0dc" stroke-width="0.8"/>')
        parts.append(f'<text x="{left - 8}" y="{y + 4:.0f}" text-anchor="end" fill="#44524b" font-size="11">{y_value:.2f}</text>')

    bar_width = max(1.0, chart_width / len(cons_data))
    for row in cons_data:
        x = left + (row["pos"] - 1) / len(cons_data) * chart_width
        h = row["cons"] * chart_height
        y = bottom - h
        if row["cons"] >= 0.99:
            color = "#1f6b63"
        elif row["cons"] >= 0.95:
            color = "#2f72b7"
        elif row["cons"] >= 0.85:
            color = "#b48217"
        else:
            color = "#9f3d4a"
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{h:.1f}" fill="{color}" opacity="0.88"/>')

    for window in windows[:3]:
        x1 = left + (window["start"] - 1) / len(cons_data) * chart_width
        x2 = left + window["end"] / len(cons_data) * chart_width
        parts.append(f'<rect x="{x1:.1f}" y="{top}" width="{x2 - x1:.1f}" height="{chart_height}" fill="#1f6b63" opacity="0.09"/>')
        parts.append(f'<text x="{(x1 + x2) / 2:.0f}" y="{top + 11}" text-anchor="middle" fill="#1f6b63" font-size="9">{window["mean_cons"]:.3f}</text>')

    parts.extend(
        [
            f'<text x="{(left + right) // 2}" y="{height - 5}" text-anchor="middle" fill="#44524b" font-size="12">Alignment Position</text>',
            f'<text x="16" y="{(top + bottom) // 2}" text-anchor="middle" fill="#44524b" font-size="12" transform="rotate(-90,16,{(top + bottom) // 2})">Conservation</text>',
            f'<text x="{left}" y="18" fill="#1f2723" font-size="14" font-weight="600">E2 Conservation ({len(cons_data)} columns, {mean_cons:.1%} mean)</text>',
            "</svg>",
        ]
    )
    path.write_text("\n".join(parts))


def write_construct_architecture(path: Path) -> None:
    components = [
        ("Consensus E2", 434, "#2f72b7"),
        ("G4S", 5, "#b48217"),
        ("SpyTag", 13, "#1f6b63"),
        ("G4S", 5, "#b48217"),
        ("SpyCatcher", 12, "#1f6b63"),
        ("G4S", 5, "#b48217"),
        ("Ferritin", 166, "#7556a8"),
    ]
    total_len = sum(item[1] for item in components)
    parts = [
        '<svg viewBox="0 0 900 200" xmlns="http://www.w3.org/2000/svg">',
        '<rect width="900" height="200" fill="#ffffff"/>',
        '<text x="20" y="25" fill="#1f2723" font-size="14" font-weight="600">Design C: E2-Ferritin Nanoparticle</text>',
    ]
    x = 20.0
    for name, length, color in components:
        width = (length / total_len) * 860
        parts.append(f'<rect x="{x:.0f}" y="60" width="{width:.0f}" height="50" fill="{color}" rx="3"/>')
        if width > 20:
            font_size = 13 if length > 50 else 10
            parts.append(f'<text x="{x + width / 2:.0f}" y="91" text-anchor="middle" fill="#ffffff" font-size="{font_size}" font-weight="600">{name}</text>')
        x += width
    parts.extend(
        [
            '<text x="20" y="132" fill="#44524b" font-size="10">1</text>',
            f'<text x="880" y="132" text-anchor="end" fill="#44524b" font-size="10">{total_len}</text>',
            '<text x="20" y="178" fill="#44524b" font-size="11">Computational antigen-only construct map; not a validated expression or efficacy result.</text>',
            "</svg>",
        ]
    )
    path.write_text("\n".join(parts))


def write_scorecard_plot(path: Path, scorecard_path: Path) -> None:
    with scorecard_path.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    width, height = 720, 340
    left, right, top = 210, 650, 52
    bar_height, bar_gap = 30, 16
    parts = [
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{width // 2}" y="28" text-anchor="middle" fill="#1f2723" font-size="16" font-weight="600">Design Scorecard (100 points)</text>',
    ]
    for idx, row in enumerate(rows):
        total = int(row["total_100"])
        y = top + idx * (bar_height + bar_gap)
        bar_width = (total / 100) * (right - left)
        parts.append(f'<text x="{left - 10}" y="{y + 20}" text-anchor="end" fill="#1f2723" font-size="12">{row["design_id"]}: {row["design_name"]}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{right - left}" height="{bar_height}" fill="#eef2ef" rx="4"/>')
        parts.append(f'<rect x="{left}" y="{y}" width="{bar_width:.0f}" height="{bar_height}" fill="#1f6b63" rx="4"/>')
        parts.append(f'<text x="{right + 10}" y="{y + 20}" fill="#1f2723" font-size="13" font-weight="700">{total}</text>')
    parts.extend(
        [
            f'<text x="{width // 2}" y="{height - 14}" text-anchor="middle" fill="#44524b" font-size="10">Data: final-submission data or notebook-output/data/design-scorecard.tsv</text>',
            "</svg>",
        ]
    )
    path.write_text("\n".join(parts))


def main() -> None:
    parser = argparse.ArgumentParser(description="Render reviewer SVG plots.")
    parser.add_argument(
        "--conservation",
        type=Path,
        default=first_existing(OUTPUT_ROOT / "data" / "e2-conservation.csv", PACKAGE_ROOT / "data" / "e2-conservation.csv"),
    )
    parser.add_argument(
        "--windows",
        type=Path,
        default=first_existing(OUTPUT_ROOT / "data" / "e2-conserved-windows.csv", PACKAGE_ROOT / "data" / "e2-conserved-windows.csv"),
    )
    parser.add_argument(
        "--scorecard",
        type=Path,
        default=first_existing(OUTPUT_ROOT / "data" / "design-scorecard.tsv", PACKAGE_ROOT / "data" / "design-scorecard.tsv"),
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=OUTPUT_ROOT / "figures",
        help="Directory for regenerated SVG figures.",
    )
    args = parser.parse_args()

    args.figures_dir.mkdir(parents=True, exist_ok=True)
    write_conservation_plot(args.figures_dir / "conservation-plot.svg", args.conservation, args.windows)
    write_construct_architecture(args.figures_dir / "construct-architecture.svg")
    write_scorecard_plot(args.figures_dir / "scorecard-bars.svg", args.scorecard)

    print(f"Wrote {args.figures_dir / 'conservation-plot.svg'}")
    print(f"Wrote {args.figures_dir / 'construct-architecture.svg'}")
    print(f"Wrote {args.figures_dir / 'scorecard-bars.svg'}")


if __name__ == "__main__":
    main()
