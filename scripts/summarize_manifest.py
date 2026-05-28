#!/usr/bin/env python3
"""Summarize and sanity-check the public HCV sequence manifest.

This script is intentionally dependency-light. It helps the student turn the
download log into a defensible dataset summary before alignment and scoring.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


REQUIRED_COLUMNS = [
    "accession",
    "genotype",
    "subtype",
    "protein",
    "source_database",
    "source_url",
    "sequence_file",
    "length_aa",
    "include",
    "status_notes",
]

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PACKAGE_ROOT / "notebook-output"


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Manifest is missing required columns: {', '.join(missing)}")
        return [{key: (value or "").strip() for key, value in row.items()} for row in reader]


def validate_rows(rows: list[dict[str, str]]) -> list[str]:
    warnings: list[str] = []
    seen_accessions: set[str] = set()

    for index, row in enumerate(rows, start=2):
        accession = row["accession"]
        include = row["include"].lower()

        if not accession or accession == "ACCESSION_HERE":
            warnings.append(f"row {index}: missing accession")
        elif accession in seen_accessions:
            warnings.append(f"row {index}: duplicate accession {accession}")
        seen_accessions.add(accession)

        if include not in {"yes", "no", "needs-review"}:
            warnings.append(f"row {index}: include should be yes, no, or needs-review")
        if not row["subtype"]:
            warnings.append(f"row {index}: missing subtype")
        if not row["source_database"]:
            warnings.append(f"row {index}: missing source_database")
        if not row["source_url"]:
            warnings.append(f"row {index}: missing source_url or search URL")
        if not row["status_notes"]:
            warnings.append(f"row {index}: missing status_notes")

        length = row["length_aa"]
        if length:
            try:
                if int(length) <= 0:
                    warnings.append(f"row {index}: length_aa must be positive")
            except ValueError:
                warnings.append(f"row {index}: length_aa is not an integer")

    return warnings


def summarize(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for row in rows:
        key = (row["protein"] or "unknown", row["subtype"] or "unknown")
        grouped[key][row["include"].lower() or "blank"] += 1

    summary_rows: list[dict[str, object]] = []
    for (protein, subtype), counts in sorted(grouped.items()):
        summary_rows.append(
            {
                "protein": protein,
                "subtype": subtype,
                "included": counts["yes"],
                "excluded": counts["no"],
                "needs_review": counts["needs-review"],
                "blank_include": counts["blank"],
                "total": sum(counts.values()),
            }
        )
    return summary_rows


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, object]], warnings: list[str]) -> None:
    lines = [
        "# Sequence Manifest QA Summary",
        "",
        "This file summarizes the public sequence manifest before alignment.",
        "",
        "## Counts By Protein And Subtype",
        "",
        "| Protein | Subtype | Included | Excluded | Needs review | Total |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['protein']} | {row['subtype']} | {row['included']} | "
            f"{row['excluded']} | {row['needs_review']} | {row['total']} |"
        )

    lines.extend(["", "## QA Warnings", ""])
    if warnings:
        lines.extend(f"- {warning}" for warning in warnings)
    else:
        lines.append("- No manifest QA warnings.")

    lines.extend(
        [
            "",
            "## Final-Page Sentence Template",
            "",
            "I collected [N] public HCV E2 protein records across subtypes [list]. "
            "After manifest QA, [N] records were included, [N] were excluded, "
            "and [N] still needed review. Exclusion reasons were recorded before alignment.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize the HCV sequence manifest.")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=PACKAGE_ROOT / "data" / "sequence-manifest.tsv",
        help="Manifest TSV. Defaults to the bundled final-submission/data file.",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=OUTPUT_ROOT / "data",
        help="Directory for regenerated manifest summary outputs.",
    )
    args = parser.parse_args()

    rows = read_manifest(args.manifest)
    warnings = validate_rows(rows)
    summary_rows = summarize(rows)

    args.results_dir.mkdir(parents=True, exist_ok=True)
    write_tsv(args.results_dir / "sequence-manifest-summary.tsv", summary_rows)
    write_markdown(args.results_dir / "sequence-manifest-qa.md", summary_rows, warnings)

    included = sum(1 for row in rows if row["include"].lower() == "yes")
    needs_review = sum(1 for row in rows if row["include"].lower() == "needs-review")
    print(f"Loaded {len(rows)} manifest rows from {args.manifest}")
    print(f"Included rows: {included}")
    print(f"Rows needing review: {needs_review}")
    print(f"QA warnings: {len(warnings)}")
    print(f"Wrote {args.results_dir / 'sequence-manifest-summary.tsv'}")
    print(f"Wrote {args.results_dir / 'sequence-manifest-qa.md'}")


if __name__ == "__main__":
    main()
