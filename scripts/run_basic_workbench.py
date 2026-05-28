#!/usr/bin/env python3
"""Run the first safe computational pass for the HCV workbench.

This script intentionally avoids specialized bioinformatics dependencies. It
expects that the student has already downloaded public E2 sequences and aligned
them with MAFFT, Clustal Omega, or another alignment tool.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PACKAGE_ROOT / "notebook-output"


def read_fasta(path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    name: str | None = None
    chunks: list[str] = []

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if name is not None:
                records.append((name, "".join(chunks).upper()))
            name = line[1:].strip()
            chunks = []
        else:
            chunks.append(line)

    if name is not None:
        records.append((name, "".join(chunks).upper()))

    return records


def write_fasta(path: Path, header: str, sequence: str) -> None:
    with path.open("w") as handle:
        handle.write(f">{header}\n")
        for start in range(0, len(sequence), 60):
            handle.write(sequence[start : start + 60] + "\n")


def compute_conservation(records: list[tuple[str, str]]) -> list[dict[str, object]]:
    if not records:
        raise ValueError("No FASTA records found.")

    lengths = {len(sequence) for _, sequence in records}
    if len(lengths) != 1:
        raise ValueError(f"Aligned sequences must have equal lengths; saw {sorted(lengths)}.")

    alignment_length = lengths.pop()
    rows: list[dict[str, object]] = []

    for idx in range(alignment_length):
        column = [sequence[idx] for _, sequence in records]
        non_gap = [aa for aa in column if aa != "-"]
        counts = Counter(non_gap)

        if counts:
            consensus, top_count = counts.most_common(1)[0]
            conservation = top_count / len(non_gap)
        else:
            consensus = "-"
            conservation = 0.0

        rows.append(
            {
                "alignment_position": idx + 1,
                "consensus_residue": consensus,
                "non_gap_count": len(non_gap),
                "conservation": round(conservation, 4),
            }
        )

    return rows


def conserved_windows(
    rows: list[dict[str, object]], sequence_count: int, window_size: int
) -> list[dict[str, object]]:
    windows: list[dict[str, object]] = []

    for start in range(0, len(rows) - window_size + 1):
        subset = rows[start : start + window_size]
        mean_conservation = sum(float(row["conservation"]) for row in subset) / window_size
        gap_fraction = (
            sum(1 for row in subset if int(row["non_gap_count"]) < sequence_count) / window_size
        )
        windows.append(
            {
                "start_alignment_position": start + 1,
                "end_alignment_position": start + window_size,
                "mean_conservation": round(mean_conservation, 4),
                "gap_fraction": round(gap_fraction, 4),
            }
        )

    return sorted(
        windows,
        key=lambda row: (float(row["mean_conservation"]), -float(row["gap_fraction"])),
        reverse=True,
    )


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path}.")

    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_conservation_svg(path: Path, rows: list[dict[str, object]]) -> None:
    """Write a simple dependency-free line plot for the final-page draft."""
    if not rows:
        raise ValueError("No conservation rows available for SVG plot.")

    width = 960
    height = 360
    left = 64
    right = 24
    top = 32
    bottom = 56
    plot_width = width - left - right
    plot_height = height - top - bottom
    max_position = max(int(row["alignment_position"]) for row in rows)

    def x_for(position: int) -> float:
        if max_position <= 1:
            return left
        return left + ((position - 1) / (max_position - 1)) * plot_width

    def y_for(value: float) -> float:
        return top + (1.0 - value) * plot_height

    points = " ".join(
        f'{x_for(int(row["alignment_position"])):.2f},{y_for(float(row["conservation"])):.2f}'
        for row in rows
    )
    threshold_y = y_for(0.8)

    x_ticks = []
    tick_count = 6
    for tick_idx in range(tick_count + 1):
        position = round(1 + tick_idx * (max_position - 1) / tick_count)
        x = x_for(position)
        x_ticks.append(
            f'<line x1="{x:.2f}" y1="{top + plot_height}" x2="{x:.2f}" y2="{top + plot_height + 6}" stroke="#44524b" />'
            f'<text x="{x:.2f}" y="{top + plot_height + 24}" text-anchor="middle" class="tick">{position}</text>'
        )

    y_ticks = []
    for value in [0.0, 0.25, 0.5, 0.75, 1.0]:
        y = y_for(value)
        y_ticks.append(
            f'<line x1="{left - 6}" y1="{y:.2f}" x2="{left}" y2="{y:.2f}" stroke="#44524b" />'
            f'<line x1="{left}" y1="{y:.2f}" x2="{left + plot_width}" y2="{y:.2f}" stroke="#d8e0dc" />'
            f'<text x="{left - 12}" y="{y + 4:.2f}" text-anchor="end" class="tick">{value:.2f}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">HCV E2 conservation across curated genotype panel</title>
  <desc id="desc">Line plot of per-column conservation scores from aligned E2 protein sequences.</desc>
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #1f2723; }}
    .tick {{ font-size: 12px; fill: #44524b; }}
    .label {{ font-size: 14px; font-weight: 600; }}
    .note {{ font-size: 12px; fill: #5f6a64; }}
  </style>
  <rect width="100%" height="100%" fill="#ffffff" />
  <text x="{left}" y="22" class="label">HCV E2 conservation across curated genotype panel</text>
  {''.join(y_ticks)}
  {''.join(x_ticks)}
  <line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" stroke="#1f2723" />
  <line x1="{left}" y1="{top + plot_height}" x2="{left + plot_width}" y2="{top + plot_height}" stroke="#1f2723" />
  <line x1="{left}" y1="{threshold_y:.2f}" x2="{left + plot_width}" y2="{threshold_y:.2f}" stroke="#8b3f4d" stroke-dasharray="6 5" />
  <text x="{left + plot_width - 2}" y="{threshold_y - 8:.2f}" text-anchor="end" class="note">0.80 reference line</text>
  <polyline fill="none" stroke="#1f6b63" stroke-width="2" points="{points}" />
  <text x="{left + plot_width / 2:.2f}" y="{height - 14}" text-anchor="middle" class="label">Aligned E2 position</text>
  <text x="18" y="{top + plot_height / 2:.2f}" transform="rotate(-90 18 {top + plot_height / 2:.2f})" text-anchor="middle" class="label">Conservation</text>
</svg>
'''
    path.write_text(svg)


def write_run_summary(
    path: Path,
    aligned_path: Path,
    records: list[tuple[str, str]],
    rows: list[dict[str, object]],
    windows: list[dict[str, object]],
    consensus: str,
) -> None:
    top_windows = windows[:5]
    mean_conservation = sum(float(row["conservation"]) for row in rows) / len(rows)
    lines = [
        "# HCV E2 Workbench Run Summary",
        "",
        "This summary is generated by `scripts/run_basic_workbench.py` after the student has curated and aligned public E2 protein sequences.",
        "",
        "## Inputs",
        "",
        f"- Aligned FASTA: `{aligned_path}`",
        f"- Sequence count: {len(records)}",
        f"- Alignment columns: {len(rows)}",
        "",
        "## Outputs",
        "",
        "- `notebook-output/data/e2-conservation.csv`",
        "- `notebook-output/data/e2-conserved-windows.csv`",
        "- `notebook-output/figures/e2-conservation.svg`",
        "- `notebook-output/data/workbench-run-summary.md`",
        "- `notebook-output/constructs/consensus-e2.protein.fasta`",
        "",
        "## First-Pass Metrics",
        "",
        f"- Mean per-column conservation: {mean_conservation:.4f}",
        f"- Consensus length after removing all-gap columns: {len(consensus)} aa",
        "",
        "## Top Conserved Windows",
        "",
        "| Start | End | Mean conservation | Gap fraction |",
        "|---:|---:|---:|---:|",
    ]
    for row in top_windows:
        lines.append(
            f'| {row["start_alignment_position"]} | {row["end_alignment_position"]} | {row["mean_conservation"]} | {row["gap_fraction"]} |'
        )
    lines.extend(
        [
            "",
            "## Safe Interpretation",
            "",
            "Use conserved windows as candidates for follow-up annotation, not as proof of antibody exposure, folding, immunogenicity, or protection. The project remains an antigen-only computational design workbench and does not include full HCV genomes or replication machinery.",
        ]
    )
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run basic HCV E2 conservation analysis.")
    parser.add_argument(
        "--aligned",
        type=Path,
        default=PACKAGE_ROOT / "data" / "e2_aligned.fasta",
        help="Aligned E2 FASTA file. Defaults to the bundled final-submission/data file.",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=OUTPUT_ROOT / "data",
        help="Directory for CSV result outputs.",
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=OUTPUT_ROOT / "figures",
        help="Directory for regenerated SVG figures.",
    )
    parser.add_argument(
        "--exports-dir",
        type=Path,
        default=OUTPUT_ROOT / "constructs",
        help="Directory for exported FASTA outputs.",
    )
    parser.add_argument("--window", type=int, default=15, help="Conserved window size.")
    args = parser.parse_args()

    records = read_fasta(args.aligned)
    rows = compute_conservation(records)
    windows = conserved_windows(rows, len(records), args.window)
    consensus = "".join(str(row["consensus_residue"]) for row in rows if row["consensus_residue"] != "-")

    args.results_dir.mkdir(parents=True, exist_ok=True)
    args.figures_dir.mkdir(parents=True, exist_ok=True)
    args.exports_dir.mkdir(parents=True, exist_ok=True)

    write_csv(args.results_dir / "e2-conservation.csv", rows)
    write_csv(args.results_dir / "e2-conserved-windows.csv", windows[:50])
    write_conservation_svg(args.figures_dir / "e2-conservation.svg", rows)
    write_fasta(args.exports_dir / "consensus-e2.protein.fasta", "consensus_E2_from_curated_HCV_panel", consensus)
    write_run_summary(
        args.results_dir / "workbench-run-summary.md",
        args.aligned,
        records,
        rows,
        windows,
        consensus,
    )

    print(f"Loaded {len(records)} aligned sequences from {args.aligned}")
    print(f"Wrote {args.results_dir / 'e2-conservation.csv'}")
    print(f"Wrote {args.results_dir / 'e2-conserved-windows.csv'}")
    print(f"Wrote {args.figures_dir / 'e2-conservation.svg'}")
    print(f"Wrote {args.results_dir / 'workbench-run-summary.md'}")
    print(f"Wrote {args.exports_dir / 'consensus-e2.protein.fasta'}")
    print(f"Consensus length: {len(consensus)} aa")
    print("Top conserved windows:")
    for row in windows[:5]:
        print(row)


if __name__ == "__main__":
    main()
