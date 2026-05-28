#!/usr/bin/env python3
"""
analyze_iedb.py — Rank HCV NS3/NS5B T-cell epitopes for Design C cassette selection.

Reads iedb-NS3-tcell.csv and iedb-NS5B-tcell.csv.
Outputs:
  notebook-output/data/iedb-NS3-ranked.csv
  notebook-output/data/iedb-NS5B-ranked.csv
  notebook-output/data/iedb-summary.md
"""
import argparse
import csv
from collections import defaultdict
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PACKAGE_ROOT / "notebook-output"

# HLA supertypes and approximate US-population coverage
# Source: Sidney et al. 2008 (Immunome Research); Sette & Sidney 1999
HLA_COVERAGE = {
    "HLA-A*02:01": 0.44, "HLA-A*02": 0.44,
    "HLA-A*01:01": 0.16, "HLA-A*01": 0.16,
    "HLA-A*03:01": 0.13, "HLA-A*03": 0.13,
    "HLA-A*24:02": 0.15, "HLA-A*24": 0.15,
    "HLA-A*11:01": 0.08, "HLA-A*11": 0.08,
    "HLA-B*07:02": 0.14, "HLA-B*07": 0.14,
    "HLA-B*08:01": 0.12, "HLA-B*08": 0.12,
    "HLA-B*44:02": 0.10, "HLA-B*44": 0.10,
}

def parse_file(path):
    rows = []
    with open(path) as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows

def rank_epitopes(rows, protein_label):
    epitope_data = defaultdict(lambda: {
        "assay_count": 0,
        "pmids": set(),
        "hla_types": set(),
        "start": None,
        "end": None,
        "max_hla_cov": 0.0,
        "qualitative": set(),
    })

    for row in rows:
        seq = row["Epitope Name"].strip()
        if not seq or seq == "N/A":
            continue
        d = epitope_data[seq]
        d["assay_count"] += 1
        pmid = row["PMID"].strip()
        if pmid:
            d["pmids"].add(pmid)
        hla = row["MHC Restriction Name"].strip()
        if hla:
            d["hla_types"].add(hla)
            cov = HLA_COVERAGE.get(hla, 0.0)
            d["max_hla_cov"] = max(d["max_hla_cov"], cov)
        try:
            start = int(row["Starting Position"])
            end = int(row["Ending Position"])
            if d["start"] is None or start < d["start"]:
                d["start"] = start
            if d["end"] is None or end > d["end"]:
                d["end"] = end
        except (ValueError, TypeError):
            pass
        qual = row["Qualitative Measurement"].strip()
        if qual:
            d["qualitative"].add(qual)

    results = []
    for seq, d in epitope_data.items():
        length = len(seq)
        n_pmids = len(d["pmids"])
        n_hla = len(d["hla_types"])
        # Score: weighted combination of validation depth and HLA coverage
        score = (d["assay_count"] * 0.4) + (n_pmids * 0.3) + (n_hla * 0.2) + (d["max_hla_cov"] * 10 * 0.1)
        results.append({
            "protein": protein_label,
            "epitope": seq,
            "length": length,
            "start": d["start"] or "",
            "end": d["end"] or "",
            "assay_count": d["assay_count"],
            "unique_pmids": n_pmids,
            "unique_hla_types": n_hla,
            "hla_types": "; ".join(sorted(d["hla_types"])[:5]),
            "max_hla_coverage": round(d["max_hla_cov"], 3),
            "score": round(score, 3),
            "qualitative": "; ".join(sorted(d["qualitative"])),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def write_csv(path, rows):
    if not rows:
        print(f"  No rows for {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser(description="Rank bundled IEDB epitope exports when raw exports are available.")
    parser.add_argument("--ns3", type=Path, default=PACKAGE_ROOT / "data" / "iedb-NS3-tcell.csv")
    parser.add_argument("--ns5b", type=Path, default=PACKAGE_ROOT / "data" / "iedb-NS5B-tcell.csv")
    parser.add_argument("--results-dir", type=Path, default=OUTPUT_ROOT / "data")
    args = parser.parse_args()

    missing = [str(path) for path in [args.ns3, args.ns5b] if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Raw IEDB CSV exports are not bundled in the reviewer package. "
            "Use docs/IEDB-Summary.md and data/candidate-regions.tsv for the reproducible reviewer flow. "
            f"Missing: {', '.join(missing)}"
        )

    args.results_dir.mkdir(parents=True, exist_ok=True)

    ns3_rows = parse_file(args.ns3)
    ns5b_rows = parse_file(args.ns5b)

    ns3_ranked = rank_epitopes(ns3_rows, "NS3")
    ns5b_ranked = rank_epitopes(ns5b_rows, "NS5B")

    write_csv(args.results_dir / "iedb-NS3-ranked.csv", ns3_ranked)
    write_csv(args.results_dir / "iedb-NS5B-ranked.csv", ns5b_ranked)

    # Summary report
    with (args.results_dir / "iedb-summary.md").open("w") as f:
        f.write("# IEDB T-Cell Epitope Summary\n\n")
        f.write("Scoring formula: `(assay_count × 0.4) + (unique_pmids × 0.3) + (unique_hla_types × 0.2) + (max_hla_coverage × 10 × 0.1)`\n\n")
        f.write("HLA coverage estimates from Sidney et al. 2008 (US population).\n\n")

        for label, ranked in [("NS3", ns3_ranked), ("NS5B", ns5b_ranked)]:
            f.write(f"## Top 10 {label} Epitopes\n\n")
            f.write("| Rank | Epitope | Len | Pos | Assays | PMIDs | HLA types | Best HLA cov | Score |\n")
            f.write("|---:|:---|---:|:---|---:|---:|---:|---:|---:|\n")
            for i, row in enumerate(ranked[:10], 1):
                pos = f"{row['start']}–{row['end']}" if row["start"] else "—"
                f.write(f"| {i} | `{row['epitope']}` | {row['length']} | {pos} | "
                        f"{row['assay_count']} | {row['unique_pmids']} | {row['unique_hla_types']} | "
                        f"{row['max_hla_coverage']:.0%} | {row['score']:.1f} |\n")
            f.write("\n")

        f.write("## Design C Cassette Candidates\n\n")
        f.write("Suggested: top 3 NS3 + top 2 NS5B by score, all ≤15 aa (fits within typical string-of-beads cassette).\n\n")
        f.write("| Protein | Epitope | Length | Score | Rationale |\n")
        f.write("|:---|:---|---:|---:|:---|\n")
        for row in [r for r in ns3_ranked[:3] if len(r["epitope"]) <= 15]:
            f.write(f"| NS3 | `{row['epitope']}` | {row['length']} | {row['score']:.1f} | "
                    f"{row['unique_pmids']} PMIDs, best HLA {row['max_hla_coverage']:.0%} |\n")
        for row in [r for r in ns5b_ranked[:3] if len(r["epitope"]) <= 15]:
            f.write(f"| NS5B | `{row['epitope']}` | {row['length']} | {row['score']:.1f} | "
                    f"{row['unique_pmids']} PMIDs, best HLA {row['max_hla_coverage']:.0%} |\n")
        f.write("\n")
        f.write("## Safe Interpretation\n\n")
        f.write("These epitopes are candidates based on historical assay counts in IEDB. "
                "They are not validated for cross-reactivity, immunodominance hierarchy, "
                "or effectiveness in an mRNA vaccine context. Use as computational starting points only.\n")

    print(f"NS3: {len(ns3_rows)} assay rows → {len(ns3_ranked)} unique epitopes")
    print(f"NS5B: {len(ns5b_rows)} assay rows → {len(ns5b_ranked)} unique epitopes")
    print(f"\nTop 5 NS3 epitopes:")
    for r in ns3_ranked[:5]:
        print(f"  {r['epitope']:<20} score={r['score']:.1f}  pmids={r['unique_pmids']}  hla_cov={r['max_hla_coverage']:.0%}")
    print(f"\nTop 5 NS5B epitopes:")
    for r in ns5b_ranked[:5]:
        print(f"  {r['epitope']:<20} score={r['score']:.1f}  pmids={r['unique_pmids']}  hla_cov={r['max_hla_coverage']:.0%}")
    print(
        "\nOutputs: "
        f"{args.results_dir / 'iedb-NS3-ranked.csv'}, "
        f"{args.results_dir / 'iedb-NS5B-ranked.csv'}, "
        f"{args.results_dir / 'iedb-summary.md'}"
    )

if __name__ == "__main__":
    main()
