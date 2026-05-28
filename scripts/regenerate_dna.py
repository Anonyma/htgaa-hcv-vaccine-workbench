#!/usr/bin/env python3
"""Deterministically back-translate bundled protein FASTAs to DNA with provenance."""

from __future__ import annotations

import argparse
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PACKAGE_ROOT / "notebook-output"

BT = {
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

DESIGNS = [
    ("A", "natural"),
    ("B", "consensus"),
    ("C", "e2-ferritin"),
    ("D", "focused-mosaic"),
]


def wrap(sequence: str, width: int = 60) -> str:
    return "\n".join(sequence[i : i + width] for i in range(0, len(sequence), width))


def read_fasta_sequence(path: Path) -> str:
    sequence = "".join(
        line.strip().upper()
        for line in path.read_text().splitlines()
        if line.strip() and not line.startswith(">")
    )
    bad = sorted(set(sequence) - set(BT))
    if bad:
        raise ValueError(f"{path} contains unsupported residues: {bad}")
    return sequence


def main() -> None:
    parser = argparse.ArgumentParser(description="Regenerate deterministic DNA FASTAs for Designs A-D.")
    parser.add_argument(
        "--constructs-dir",
        type=Path,
        default=PACKAGE_ROOT / "constructs",
        help="Directory containing bundled protein FASTAs.",
    )
    parser.add_argument(
        "--exports-dir",
        type=Path,
        default=OUTPUT_ROOT / "constructs",
        help="Directory for regenerated DNA FASTAs.",
    )
    args = parser.parse_args()

    args.exports_dir.mkdir(parents=True, exist_ok=True)
    for tag, name in DESIGNS:
        stem = f"design-{tag}-{name}"
        protein_path = args.constructs_dir / f"{stem}.protein.fasta"
        protein = read_fasta_sequence(protein_path)
        dna = "GCCACC" + "".join(BT[aa] for aa in protein) + "TAA"
        header = f">{stem} source=deterministic_backtranslation status=computational_candidate kozak=yes"
        output_path = args.exports_dir / f"{stem}.dna.fasta"
        output_path.write_text(f"{header}\n{wrap(dna)}\n")
        print(f"{output_path}: {len(protein)} aa -> {len(dna)} nt")


if __name__ == "__main__":
    main()
