#!/usr/bin/env python3
"""Export a beginner-scale antigen-only construct package.

This helper starts from a protein FASTA candidate and writes an annotated
protein FASTA, a simple DNA ORF FASTA made by deterministic back-translation,
    an annotation TSV, and a plain-text construct map.

The DNA is a computational design artifact for the HTGAA page. It is not a
validated expression cassette and it intentionally contains no HCV genome,
replication machinery, viral rescue instructions, or wet-lab protocol.
"""

from __future__ import annotations

import argparse
from pathlib import Path


BACKTRANSLATION = {
    "A": "GCC",
    "C": "TGC",
    "D": "GAC",
    "E": "GAG",
    "F": "TTC",
    "G": "GGC",
    "H": "CAC",
    "I": "ATC",
    "K": "AAG",
    "L": "CTG",
    "M": "ATG",
    "N": "AAC",
    "P": "CCC",
    "Q": "CAG",
    "R": "CGC",
    "S": "AGC",
    "T": "ACC",
    "V": "GTG",
    "W": "TGG",
    "Y": "TAC",
}

ALLOWED_AA = set(BACKTRANSLATION)
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PACKAGE_ROOT / "notebook-output"


def read_first_fasta(path: Path) -> tuple[str, str]:
    header = ""
    chunks: list[str] = []

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header:
                break
            header = line[1:].strip()
        else:
            chunks.append(line.upper())

    sequence = "".join(chunks).replace("-", "")
    if not header or not sequence:
        raise ValueError(f"No FASTA record found in {path}.")

    bad = sorted(set(sequence) - ALLOWED_AA)
    if bad:
        raise ValueError(
            "Protein sequence contains unsupported residues "
            f"{bad}. Resolve ambiguous residues before export."
        )

    return header, sequence


def wrap(sequence: str, width: int = 60) -> str:
    return "\n".join(sequence[start : start + width] for start in range(0, len(sequence), width))


def backtranslate(sequence: str) -> str:
    return "".join(BACKTRANSLATION[aa] for aa in sequence)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def gc_fraction(sequence: str) -> float:
    return (sequence.count("G") + sequence.count("C")) / len(sequence) if sequence else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Export antigen-only HCV construct artifacts.")
    parser.add_argument(
        "--protein",
        type=Path,
        default=OUTPUT_ROOT / "constructs" / "consensus-e2.protein.fasta",
        help="Input protein FASTA candidate. Defaults to the regenerated consensus in notebook-output.",
    )
    parser.add_argument(
        "--name",
        default="hcv_candidate_antigen_only",
        help="Short construct name for FASTA headers and map labels.",
    )
    parser.add_argument(
        "--exports-dir",
        type=Path,
        default=OUTPUT_ROOT / "constructs",
        help="Directory for construct outputs.",
    )
    parser.add_argument(
        "--include-kozak",
        action="store_true",
        help="Prepend GCCACC before the ORF to mark a mammalian-expression placeholder.",
    )
    args = parser.parse_args()

    source_header, protein = read_first_fasta(args.protein)
    coding_orf = backtranslate(protein) + "TAA"
    dna_export = ("GCCACC" if args.include_kozak else "") + coding_orf
    coding_start = 7 if args.include_kozak else 1
    coding_end = len(dna_export)

    args.exports_dir.mkdir(parents=True, exist_ok=True)
    protein_path = args.exports_dir / "final-candidate.protein.fasta"
    dna_path = args.exports_dir / "final-candidate.dna.fasta"
    annotations_path = args.exports_dir / "final-candidate.annotations.tsv"
    map_path = args.exports_dir / "final-candidate.construct-map.txt"

    protein_header = f">{args.name} scope=antigen_only status=computational_candidate"
    # Include origin info as a comment if the source header has useful metadata
    if source_header and source_header != args.name:
        protein_header += f" origin={source_header}"
    write_text(
        protein_path,
        f"{protein_header}\n"
        f"{wrap(protein)}\n",
    )
    write_text(
        dna_path,
        f">{args.name} source=deterministic_backtranslation status=computational_placeholder "
        f"kozak={'yes' if args.include_kozak else 'no'}\n{wrap(dna_export)}\n",
    )
    annotation_rows = [
        ("feature", "start_nt", "end_nt", "note"),
        (
            "kozak_placeholder",
            "1" if args.include_kozak else "",
            "6" if args.include_kozak else "",
            "GCCACC placeholder; omit if not using a mammalian-expression framing",
        ),
        (
            "antigen_orf_plus_stop",
            str(coding_start),
            str(coding_end),
            "Deterministic back-translation of protein candidate plus TAA stop codon",
        ),
    ]
    write_text(annotations_path, "\n".join("\t".join(row) for row in annotation_rows) + "\n")
    write_text(
        map_path,
        "\n".join(
            [
                f"Construct name: {args.name}",
                f"Source protein FASTA: {args.protein}",
                f"Source protein header: {source_header}",
                "Scope: antigen-only computational candidate",
                "Safety boundary: no full HCV genome, no replication genes, no viral rescue system",
                "",
                "Architecture:",
                "5' annotation placeholder | Kozak placeholder if selected | antigen ORF | stop codon | 3' annotation placeholder",
                "",
                "Features:",
                f"- protein_length_aa: {len(protein)}",
                f"- dna_length_nt: {len(dna_export)}",
                f"- coding_feature_nt: {coding_start}..{coding_end}",
                "- stop_codon: TAA",
                f"- gc_fraction: {gc_fraction(dna_export):.3f}",
                "",
                "Interpretation:",
                "This file supports the HTGAA computational final page by making the final design explicit and inspectable.",
                "It is not codon-optimization validation, expression validation, folding validation, or evidence of vaccine efficacy.",
                "",
            ]
        ),
    )

    print(f"Wrote {protein_path}")
    print(f"Wrote {dna_path}")
    print(f"Wrote {annotations_path}")
    print(f"Wrote {map_path}")
    print(f"Protein length: {len(protein)} aa")
    print(f"DNA length: {len(dna_export)} nt")
    print(f"GC fraction: {gc_fraction(dna_export):.3f}")


if __name__ == "__main__":
    main()
