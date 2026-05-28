#!/usr/bin/env python3
"""Draft a conservative scorecard and final-page result snippet.

This helper does not decide that a candidate is a vaccine. It only gathers the
current workbench artifacts and turns them into a first-pass, editable summary
for the HTGAA page.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PACKAGE_ROOT / "notebook-output"
TARGET_SUBTYPES = {"1a", "1b", "2a", "3a"}
SCORE_FIELDS = [
    "genotype_coverage_25",
    "epitope_conservation_20",
    "hla_coverage_15",
    "developability_15",
    "mrna_dna_manufacturability_15",
    "interpretability_10",
]
BONUS_FIELDS = ["multivalency_bonus_15"]


def read_delimited(path: Path) -> list[dict[str, str]]:
    """Read a TSV or CSV file, auto-detecting delimiter from extension."""
    if not path.exists():
        return []
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    with path.open(newline="") as handle:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(handle, delimiter=delimiter)
        ]


def read_fasta_sequence(path: Path) -> str:
    if not path.exists():
        return ""
    chunks: list[str] = []
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if line and not line.startswith(">"):
            chunks.append(line)
    return "".join(chunks).replace("-", "").upper()


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def yes(value: str) -> bool:
    return value.strip().lower() in {"yes", "include", "included", "keep"}


def build_scorecard(args: argparse.Namespace) -> tuple[list[dict[str, object]], dict[str, object]]:
    manifest = read_delimited(args.manifest)
    candidate_regions = read_delimited(args.candidate_regions)
    windows = read_delimited(args.conserved_windows)
    consensus = read_fasta_sequence(args.consensus_protein)
    final_protein = read_fasta_sequence(args.final_protein)
    final_dna = read_fasta_sequence(args.final_dna)

    included = [row for row in manifest if row.get("include", "").lower() == "yes"]
    included_subtypes = {row.get("subtype", "") for row in included if row.get("protein", "").upper() == "E2"}
    has_target_dataset = bool(included_subtypes & TARGET_SUBTYPES)
    subtype_score = round(min(len(included_subtypes & TARGET_SUBTYPES), 4) / 4 * 25)

    e2_regions = [
        row for row in candidate_regions if row.get("protein", "").upper() == "E2" and yes(row.get("include_decision", ""))
    ]
    tcell_regions = [
        row
        for row in candidate_regions
        if row.get("protein", "").upper() in {"NS3", "NS5B"} and yes(row.get("include_decision", ""))
    ]
    hla_regions = [
        row
        for row in tcell_regions
        if row.get("hla_restriction", "").upper() not in {"", "TODO", "N/A", "NOT APPLICABLE"}
    ]

    top_window = windows[0] if windows else {}
    has_consensus = bool(consensus)
    has_final_export = bool(final_protein and final_dna)

    consensus_developability = 12 if has_consensus else 0
    if has_consensus and (len(consensus) < 150 or len(consensus) > 900):
        consensus_developability = 8

    rows: list[dict[str, object]] = [
        {
            "design_id": "A",
            "design_name": "Natural E2 baseline",
            "genotype_coverage_25": min(10, subtype_score) if has_target_dataset else 0,
            "epitope_conservation_20": 5 if e2_regions and has_target_dataset else 0,
            "hla_coverage_15": 0,
            "developability_15": 10 if has_target_dataset else 0,
            "mrna_dna_manufacturability_15": 10 if has_target_dataset else 0,
            "interpretability_10": 10 if has_target_dataset else 0,
            "multivalency_bonus_15": 0,
            "decision_notes": (
                "Baseline control: easiest to explain, but expected to represent one subtype best."
                if has_target_dataset
                else "Waiting on a real included E2 dataset; placeholder rows should not be scored."
            ),
        },
        {
            "design_id": "B",
            "design_name": "Consensus E2",
            "genotype_coverage_25": subtype_score,
            "epitope_conservation_20": 15 if e2_regions else (10 if top_window else 0),
            "hla_coverage_15": 0,
            "developability_15": consensus_developability,
            "mrna_dna_manufacturability_15": 12 if has_final_export else (8 if has_consensus else 0),
            "interpretability_10": 8 if has_consensus else 0,
            "multivalency_bonus_15": 0,
            "decision_notes": (
                "Draft score from alignment breadth and export readiness; review folding and epitope caveats manually."
                if has_consensus
                else "Waiting on consensus E2 FASTA from the aligned dataset."
            ),
        },
        {
            "design_id": "C",
            "design_name": "E2-ferritin nanoparticle",
            "genotype_coverage_25": subtype_score,
            "epitope_conservation_20": 15 if e2_regions else (10 if top_window else 0),
            "hla_coverage_15": 0,
            "developability_15": 5 if has_consensus else 0,
            "mrna_dna_manufacturability_15": 5 if has_consensus else 0,
            "interpretability_10": 9 if has_consensus else 0,
            "multivalency_bonus_15": 15 if has_consensus else 0,
            "decision_notes": (
                "Consensus E2 on a ferritin scaffold; multivalency bonus is offset by added construct complexity."
                if has_consensus
                else "Waiting on consensus E2 before ferritin scaffold review."
            ),
        },
        {
            "design_id": "D",
            "design_name": "Focused conserved mosaic",
            "genotype_coverage_25": subtype_score,
            "epitope_conservation_20": 20 if e2_regions and tcell_regions else (15 if e2_regions else 0),
            "hla_coverage_15": min(15, len(hla_regions) * 5),
            "developability_15": 14 if e2_regions and tcell_regions else 8,
            "mrna_dna_manufacturability_15": 14 if has_final_export else 8,
            "interpretability_10": 7 if e2_regions and tcell_regions else 4,
            "multivalency_bonus_15": 0,
            "decision_notes": (
                "Focused peptide/mosaic design emphasizing conserved E2 windows and reviewed IEDB T-cell epitopes."
                if e2_regions and tcell_regions
                else "Needs both conserved E2 windows and reviewed T-cell epitope rows before nomination."
            ),
        },
    ]

    for row in rows:
        base_total = sum(int(row[field]) for field in SCORE_FIELDS)
        bonus_total = sum(int(row[field]) for field in BONUS_FIELDS)
        row["base_total"] = base_total
        row["total_100"] = min(100, base_total + bonus_total)

    context = {
        "manifest_rows": len(manifest),
        "included_rows": len(included),
        "included_subtypes": ", ".join(sorted(included_subtypes)) or "none yet",
        "top_window": top_window,
        "e2_region_count": len(e2_regions),
        "tcell_region_count": len(tcell_regions),
        "hla_region_count": len(hla_regions),
        "consensus_length": len(consensus),
        "final_protein_length": len(final_protein),
        "final_dna_length": len(final_dna),
        "best_design": max(rows, key=lambda row: int(row["total_100"])),
    }
    return rows, context


def write_snippet(path: Path, context: dict[str, object]) -> None:
    top_window = context["top_window"]
    if isinstance(top_window, dict) and top_window:
        window_text = (
            f"{top_window.get('start_alignment_position')} to "
            f"{top_window.get('end_alignment_position')} "
            f"(mean conservation {top_window.get('mean_conservation')})"
        )
    else:
        window_text = "[run conservation analysis first]"

    best = context["best_design"]
    assert isinstance(best, dict)
    best_total = int(best["total_100"])
    if best_total > 0:
        scorecard_text = (
            f"The current draft scorecard nominates design {best['design_id']} "
            f"({best['design_name']}) with a draft score of {best_total}/100. "
            "This is a decision-support score, not efficacy evidence."
        )
    else:
        scorecard_text = (
            "No design is nominated yet because the required dataset, conservation, "
            "candidate-region, or export artifacts are still missing."
        )
    lines = [
        "# Draft Final-Page Results Snippet",
        "",
        "Use this as editable draft text. Replace bracketed or weak claims after manual review.",
        "",
        "## Dataset",
        "",
        (
            f"The current manifest contains {context['manifest_rows']} public sequence rows, "
            f"with {context['included_rows']} marked for inclusion. Included E2 subtypes: "
            f"{context['included_subtypes']}."
        ),
        "",
        "## Conservation",
        "",
        f"The top conserved-window result is {window_text}.",
        "",
        "## Candidate Regions",
        "",
        (
            f"The candidate-region table currently includes {context['e2_region_count']} included E2 "
            f"region(s), {context['tcell_region_count']} included NS3/NS5B T-cell region(s), and "
            f"{context['hla_region_count']} T-cell region(s) with explicit HLA restrictions."
        ),
        "",
        "## Draft Scorecard",
        "",
        scorecard_text,
        "",
        "## Construct Export",
        "",
        (
            f"Current exported final candidate lengths: protein {context['final_protein_length']} aa; "
            f"DNA {context['final_dna_length']} nt. If either value is 0, run the export helper after "
            "consensus generation."
        ),
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Draft the HCV workbench scorecard.")
    parser.add_argument("--manifest", type=Path, default=PACKAGE_ROOT / "data" / "sequence-manifest.tsv")
    parser.add_argument("--candidate-regions", type=Path, default=PACKAGE_ROOT / "data" / "candidate-regions.tsv")
    parser.add_argument("--conserved-windows", type=Path, default=OUTPUT_ROOT / "data" / "e2-conserved-windows.csv")
    parser.add_argument("--consensus-protein", type=Path, default=OUTPUT_ROOT / "constructs" / "consensus-e2.protein.fasta")
    parser.add_argument("--final-protein", type=Path, default=OUTPUT_ROOT / "constructs" / "final-candidate.protein.fasta")
    parser.add_argument("--final-dna", type=Path, default=OUTPUT_ROOT / "constructs" / "final-candidate.dna.fasta")
    parser.add_argument("--results-dir", type=Path, default=OUTPUT_ROOT / "data")
    args = parser.parse_args()

    rows, context = build_scorecard(args)
    scorecard_path = args.results_dir / "design-scorecard.tsv"
    snippet_path = args.results_dir / "final-page-results-snippet.md"
    write_tsv(scorecard_path, rows)
    write_snippet(snippet_path, context)

    print(f"Wrote {scorecard_path}")
    print(f"Wrote {snippet_path}")
    best = context["best_design"]
    if int(best["total_100"]) > 0:
        print(f"Draft winner: {best['design_id']} ({best['total_100']}/100)")
    else:
        print("Draft winner: none yet; required analysis artifacts are still missing.")


if __name__ == "__main__":
    main()
