#!/usr/bin/env python3
"""Build the Design C E2-ferritin fusion construct for review.

The output is a computational antigen-design artifact only. It contains no HCV
genome, replication machinery, viral rescue instructions, or wet-lab protocol.
"""

from __future__ import annotations

import argparse
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PACKAGE_ROOT / "notebook-output"

SPYTAG = "AHIVMVDAYKPTK"
LINKER_LONG = "GGGGSGGGGSGGGGS"
LINKER_SHORT = "GSGSG"
HIS_TAG = "HHHHHH"

FERRITIN = (
    "MLSKDIIKLLNEQVNKEMNSSNLYMSMSSWCYTHSLDGAGLFLFDHAAEEYEHAKKLIVF"
    "LNENNVPVQLTSISAPEHKFEGLTQIFQKAYEHEQHISESINNIVDHAIKGKDHATFNFL"
    "QWYVSEQHEEEVLFKDILDKIELIGNENHGLYLADQYVKGIAKSRKS"
)

CONSENSUS_E2 = (
    "MMMNWSPTTALVVSQLLRIPQAILDMIAGAHWGVLAGIAYFSMVGNWAKVVVVLLLFAGV"
    "DAQTHTTGGSAGREASGFTSLFTLGPSQKVQLINTNGSWHINRTALNCNDSLNTGFLAGL"
    "FYYHKFNSSGCPERMASCRPITSFEQGWGPITYADNISGSSDDRPYCWHYAPRPCGIVPA"
    "SSVCGPVYCFTPSPVVVGTTDRKGVPTYTWGENETDVFLLNNTRPPQGNWFGCTWMNSTG"
    "FTKTCGAPPCDIGGVGKKPDNNNTTDLFCPTDCFRKHPEATYSRCGSGPWLTPRCLVDYP"
    "YRLWHYPCTVNFSIFKVRMYVGGVEHRLSAACNWTRGERCNLEDRDRSELSPLLLSTTEW"
    "QVLPCSFTTLPALSTGLIHLHQNIVDVQYLYGVGSGIVSWAIKWEYVVLLFLLLADARVC"
    "ACLWMMLLISQAEA"
)


def wrap(sequence: str, width: int = 60) -> str:
    return "\n".join(sequence[start : start + width] for start in range(0, len(sequence), width))


def build_components() -> tuple[str, list[tuple[str, int, int]]]:
    full_fusion = SPYTAG + LINKER_LONG + CONSENSUS_E2 + LINKER_SHORT + FERRITIN + HIS_TAG
    starts = [
        ("SpyTag", 0, len(SPYTAG)),
        ("(G4S)x3 linker", len(SPYTAG), len(SPYTAG) + len(LINKER_LONG)),
        (
            "Consensus E2",
            len(SPYTAG) + len(LINKER_LONG),
            len(SPYTAG) + len(LINKER_LONG) + len(CONSENSUS_E2),
        ),
        (
            "GSGSG linker",
            len(SPYTAG) + len(LINKER_LONG) + len(CONSENSUS_E2),
            len(SPYTAG) + len(LINKER_LONG) + len(CONSENSUS_E2) + len(LINKER_SHORT),
        ),
        (
            "Ferritin (P52093)",
            len(SPYTAG) + len(LINKER_LONG) + len(CONSENSUS_E2) + len(LINKER_SHORT),
            len(SPYTAG)
            + len(LINKER_LONG)
            + len(CONSENSUS_E2)
            + len(LINKER_SHORT)
            + len(FERRITIN),
        ),
        ("His6 tag", len(full_fusion) - len(HIS_TAG), len(full_fusion)),
    ]
    return full_fusion, starts


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Design C E2-ferritin construct files.")
    parser.add_argument(
        "--exports-dir",
        type=Path,
        default=OUTPUT_ROOT / "constructs",
        help="Directory for regenerated construct outputs.",
    )
    args = parser.parse_args()

    full_fusion, components = build_components()
    args.exports_dir.mkdir(parents=True, exist_ok=True)

    fasta_path = args.exports_dir / "design-C-e2-ferritin.protein.fasta"
    ann_path = args.exports_dir / "design-C-e2-ferritin.annotations.tsv"

    fasta_header = (
        ">Design_C_E2_ferritin_nanoparticle|spytag-e2-ferritin-his6|"
        f"{len(full_fusion)}aa|computational_candidate|source=NCBI+UniProt+consensus"
    )
    fasta_path.write_text(f"{fasta_header}\n{wrap(full_fusion)}\n")

    lines = ["component\tstart\tend\tlength_aa\tnotes"]
    for name, start, end in components:
        lines.append(f"{name}\t{start + 1}\t{end}\t{end - start}\t")
    lines.append("AR3_epitope_footprint\t~230\t~280\t~50\tCD81 binding region; see Pierce 2010 PNAS")
    lines.append("Ferritin_assembly_interface\t~470\t~640\t~170\tSelf-assembles into 24-mer")
    ann_path.write_text("\n".join(lines) + "\n")

    print("=== E2-Ferritin Nanoparticle Fusion Construct ===")
    print(f"Total length: {len(full_fusion)} aa")
    print(f"Wrote {fasta_path}")
    print(f"Wrote {ann_path}")


if __name__ == "__main__":
    main()
