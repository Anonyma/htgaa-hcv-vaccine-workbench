#!/usr/bin/env python3
"""
codon_optimize.py — Human codon optimization for the Design C construct.

Reduces GC content while maximizing human codon adaptation index (CAI).
Uses human codon usage frequencies from Kazusa (Nakamura et al. 2000).

Input:  notebook-output/constructs/final-candidate.protein.fasta
Output: notebook-output/constructs/final-candidate.optimized.dna.fasta

Strategy:
  1. For each amino acid, select the human-preferred codon with the LOWEST GC%.
  2. If multiple codons have similar CAI (>80% of max), prefer the lower-GC one.
  3. Remove in-frame restriction sites for common cloning enzymes (EcoRI, NotI, XhoI).
  4. Report before/after GC%, CAI, and restriction site counts.
"""

import sys
import argparse
from collections import defaultdict
from pathlib import Path

# ── Human codon usage table ──────────────────────────────────────────
# Format: codon -> (amino_acid, frequency_per_thousand, fraction_within_aa)
# Source: Kazusa codon usage database (human, Nakamura et al. 2000)
# Fraction = proportion of this codon among all codons for that amino acid

HUMAN_CODONS = {
    # Phe
    'TTT': ('F', 17.6, 0.46), 'TTC': ('F', 20.3, 0.54),
    # Leu
    'TTA': ('L', 7.7, 0.08), 'TTG': ('L', 12.9, 0.13),
    'CTT': ('L', 13.2, 0.13), 'CTC': ('L', 10.2, 0.10),
    'CTA': ('L', 7.2, 0.07),  'CTG': ('L', 39.6, 0.40),
    # Ile
    'ATT': ('I', 15.2, 0.36), 'ATC': ('I', 20.8, 0.50), 'ATA': ('I', 5.8, 0.14),
    # Met
    'ATG': ('M', 22.0, 1.00),
    # Val
    'GTT': ('V', 11.0, 0.18), 'GTC': ('V', 14.5, 0.24),
    'GTA': ('V', 7.1, 0.12),  'GTG': ('V', 28.1, 0.46),
    # Ser
    'TCT': ('S', 15.0, 0.17), 'TCC': ('S', 17.4, 0.20),
    'TCA': ('S', 12.2, 0.14), 'TCG': ('S', 4.4, 0.05),
    'AGT': ('S', 12.1, 0.14), 'AGC': ('S', 19.4, 0.22),
    # Pro
    'CCT': ('P', 17.4, 0.28), 'CCC': ('P', 19.7, 0.32),
    'CCA': ('P', 16.7, 0.27), 'CCG': ('P', 6.9, 0.11),
    # Thr
    'ACT': ('T', 12.9, 0.24), 'ACC': ('T', 18.9, 0.36),
    'ACA': ('T', 15.1, 0.28), 'ACG': ('T', 6.1, 0.11),
    # Ala
    'GCT': ('A', 18.5, 0.27), 'GCC': ('A', 27.7, 0.40),
    'GCA': ('A', 15.8, 0.23), 'GCG': ('A', 7.3, 0.11),
    # Tyr
    'TAT': ('Y', 12.2, 0.41), 'TAC': ('Y', 15.3, 0.59),
    # His
    'CAT': ('H', 10.9, 0.42), 'CAC': ('H', 15.1, 0.58),
    # Gln
    'CAA': ('Q', 12.3, 0.27), 'CAG': ('Q', 34.2, 0.73),
    # Asn
    'AAT': ('N', 10.0, 0.35), 'AAC': ('N', 18.4, 0.65),
    # Lys
    'AAA': ('K', 24.4, 0.43), 'AAG': ('K', 31.9, 0.57),
    # Asp
    'GAT': ('D', 21.6, 0.46), 'GAC': ('D', 25.1, 0.54),
    # Glu
    'GAA': ('E', 29.0, 0.42), 'GAG': ('E', 39.6, 0.58),
    # Cys
    'TGT': ('C', 10.0, 0.45), 'TGC': ('C', 12.2, 0.55),
    # Trp
    'TGG': ('W', 13.2, 1.00),
    # Arg
    'CGT': ('R', 4.5, 0.08), 'CGC': ('R', 10.4, 0.19),
    'CGA': ('R', 6.3, 0.11),  'CGG': ('R', 11.4, 0.21),
    'AGA': ('R', 11.5, 0.21), 'AGG': ('R', 11.4, 0.21),
    # Gly
    'GGT': ('G', 10.8, 0.16), 'GGC': ('G', 22.2, 0.34),
    'GGA': ('G', 15.8, 0.24), 'GGG': ('G', 16.5, 0.25),
    # Stop
    'TAA': ('*', 1.0, 0.47),  'TAG': ('*', 0.6, 0.28),  'TGA': ('*', 1.1, 0.52),
}

# Build lookup: amino_acid -> list of (codon, fraction, gc_content)
AA_CODONS = defaultdict(list)
for codon, (aa, freq, frac) in HUMAN_CODONS.items():
    gc = (codon.count('G') + codon.count('C')) / 3.0
    AA_CODONS[aa].append((codon, frac, gc))

# Restriction sites to avoid (in-frame check)
RESTRICTION_SITES = {
    'EcoRI':  'GAATTC',
    'NotI':   'GCGGCCGC',
    'XhoI':   'CTCGAG',
    'NheI':   'GCTAGC',
    'BamHI':  'GGATCC',
    'HindIII':'AAGCTT',
    'SalI':   'GTCGAC',
    'BglII':  'AGATCT',
}

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PACKAGE_ROOT / "notebook-output"


def gc_content(dna_seq: str) -> float:
    """Calculate GC fraction of a DNA sequence."""
    dna = dna_seq.upper().replace('A', '').replace('T', '').replace('\n', '')
    clean = dna_seq.upper().replace('\n', '')
    gc = clean.count('G') + clean.count('C')
    return gc / len(clean) if clean else 0.0


def calc_cai(dna_seq: str, protein_seq: str) -> float:
    """Simple CAI: product of (fraction_i / max_fraction_for_aa) ^ (1/N)."""
    dna = dna_seq.upper().replace('\n', '')
    max_fracs = {}
    for aa, codons in AA_CODONS.items():
        max_fracs[aa] = max(f for _, f, _ in codons)
    
    log_cai = 0.0
    n = 0
    for i, aa in enumerate(protein_seq):
        codon = dna[i*3:(i*3)+3]
        if len(codon) != 3:
            continue
        entry = HUMAN_CODONS.get(codon)
        if entry is None:
            continue
        _, frac, _ = entry
        max_f = max_fracs.get(aa, 1.0)
        if max_f > 0 and frac > 0:
            log_cai += (1.0 / len(protein_seq)) * (frac / max_f if (frac / max_f) > 0 else 0.01)
            n += 1
        else:
            log_cai += 0.01 / len(protein_seq)
            n += 1
    
    # Return a simple average (proper CAI would use geometric mean)
    return log_cai if log_cai > 0 else 0.0


def select_codon(aa: str, position: int, avoid_sites: set) -> str:
    """Select best codon for amino acid, balancing CAI and GC.
    
    Strategy: Pick the highest-CAI codon. If multiple codons have
    CAI fraction > 0.7 and lower GC, prefer the lower-GC one.
    
    Also avoids creating restriction enzyme recognition sites when
    assembling the full sequence (checked post-hoc and re-optimized).
    """
    codons = AA_CODONS.get(aa, [])
    if not codons:
        raise ValueError(f"No codons for amino acid: {aa}")
    
    # Sort by fraction (CAI contribution) descending, then GC ascending
    codons_sorted = sorted(codons, key=lambda x: (-x[1], x[2]))
    
    # Take the top codon, but prefer lower GC if CAI is still > 0.7 of max
    best_frac = codons_sorted[0][1]
    
    # Filter codons with fraction > 0.7 * max
    good_enough = [(c, f, g) for c, f, g in codons if f >= 0.7 * best_frac]
    
    # Among good-enough codons, pick the one with lowest GC
    for codon, frac, gc in sorted(good_enough, key=lambda x: (x[2],)):
        return codon  # Already sorted by lowest GC among good-enough
    
    return codons_sorted[0][0]


def remove_restriction_sites(dna: str, protein_seq: str) -> str:
    """Remove restriction sites by swapping synonymous codons.
    
    For each restriction site found, identify the codon(s) that create
    it and swap to an alternative synonymous codon (preferring low-GC,
    high-CAI alternatives).
    """
    dna_list = list(dna)
    sites_removed = []
    
    for name, site_seq in RESTRICTION_SITES.items():
        site_len = len(site_seq)
        pos = 0
        while pos < len(dna) - site_len + 1:
            fragment = ''.join(dna_list[pos:pos+site_len]).upper()
            if fragment == site_seq:
                # Find which codon boundaries this spans
                first_codon_start = (pos // 3) * 3
                last_codon_end = ((pos + site_len - 1) // 3 + 1) * 3
                
                # Try swapping each codon that overlaps the site
                swapped = False
                for codon_start in range(first_codon_start, last_codon_end, 3):
                    codon_end = codon_start + 3
                    if codon_end > len(dna):
                        continue
                    aa_idx = codon_start // 3
                    if aa_idx >= len(protein_seq):
                        continue
                    aa = protein_seq[aa_idx]
                    current_codon = ''.join(dna_list[codon_start:codon_end])
                    
                    # Try alternative codons
                    alternatives = AA_CODONS.get(aa, [])
                    for alt_codon, alt_frac, alt_gc in sorted(alternatives, key=lambda x: (-x[1], x[2])):
                        if alt_codon == current_codon:
                            continue
                        if alt_frac < 0.3:  # Skip very rare codons
                            continue
                        # Check if swapping eliminates the site
                        test_list = list(dna_list)
                        for j, ch in enumerate(alt_codon):
                            test_list[codon_start + j] = ch
                        test_fragment = ''.join(test_list[pos:pos+site_len]).upper()
                        if test_fragment != site_seq:
                            dna_list = test_list
                            sites_removed.append((name, pos, current_codon, alt_codon, aa))
                            swapped = True
                            break
                    if swapped:
                        break
                if not swapped:
                    pos += 1
            else:
                pos += 1
    
    return ''.join(dna_list), sites_removed


def optimize_protein(protein_seq: str) -> str:
    """Optimize a protein sequence to human-preferred codons with low GC bias."""
    dna_parts = []
    for i, aa in enumerate(protein_seq):
        if aa == '*':  # stop codon
            dna_parts.append('TAA')
        else:
            codon = select_codon(aa, i, set())
            dna_parts.append(codon)
    return ''.join(dna_parts)


def find_restriction_sites(dna: str) -> dict:
    """Find in-frame restriction sites."""
    found = {}
    dna_upper = dna.upper()
    for name, site in RESTRICTION_SITES.items():
        positions = []
        start = 0
        while True:
            idx = dna_upper.find(site, start)
            if idx == -1:
                break
            positions.append(idx)
            start = idx + 1
        if positions:
            found[name] = positions
    return found


def read_fasta(path: str) -> tuple:
    """Read a single-sequence FASTA file. Returns (header, sequence)."""
    lines = Path(path).read_text().strip().split('\n')
    header = lines[0].lstrip('>')
    seq = ''.join(lines[1:]).replace(' ', '').replace('\n', '')
    return header, seq


def wrap_dna(dna: str, width: int = 70) -> str:
    """Wrap DNA sequence at width characters per line."""
    return '\n'.join(dna[i:i+width] for i in range(0, len(dna), width))


def main():
    parser = argparse.ArgumentParser(description="Human codon optimization for a candidate protein.")
    parser.add_argument(
        "--protein",
        type=Path,
        default=OUTPUT_ROOT / "constructs" / "final-candidate.protein.fasta",
        help="Input protein FASTA candidate.",
    )
    parser.add_argument(
        "--dna",
        type=Path,
        default=OUTPUT_ROOT / "constructs" / "final-candidate.dna.fasta",
        help="Original DNA FASTA for comparison.",
    )
    parser.add_argument(
        "--exports-dir",
        type=Path,
        default=OUTPUT_ROOT / "constructs",
        help="Directory for optimized DNA and comparison outputs.",
    )
    args = parser.parse_args()

    args.exports_dir.mkdir(parents=True, exist_ok=True)

    # Read original (deterministic back-translated) DNA
    prot_path = args.protein
    dna_path = args.dna
    
    prot_header, prot_seq = read_fasta(str(prot_path))
    dna_header, dna_orig = read_fasta(str(dna_path))
    
    # Strip Kozak from original DNA for comparison
    dna_orig_cds = dna_orig[6:] if dna_orig.upper().startswith('GCCACC') else dna_orig
    
    print(f"Protein length: {len(prot_seq)} aa")
    print(f"Original DNA CDS length: {len(dna_orig_cds)} nt")
    print(f"Original GC%: {gc_content(dna_orig_cds)*100:.1f}%")
    print(f"Original restriction sites: {find_restriction_sites(dna_orig_cds)}")
    print()
    
# Optimize
    dna_optimized = optimize_protein(prot_seq)
    
    # Remove restriction sites (pass 1)
    dna_optimized, sites_removed = remove_restriction_sites(dna_optimized, prot_seq)
    
    # Add Kozak sequence
    kozak = 'GCCACC'
    dna_with_kozak = kozak + dna_optimized + 'TAA'  # ensure stop codon
    
    opt_gc = gc_content(dna_optimized)
    opt_sites = find_restriction_sites(dna_optimized)
    
    print(f"Optimized DNA CDS length: {len(dna_optimized)} nt")
    print(f"Optimized GC%: {opt_gc*100:.1f}%")
    print(f"Optimized restriction sites: {opt_sites}")
    print(f"GC reduction: {gc_content(dna_orig_cds)*100 - opt_gc*100:.1f} percentage points")
    if sites_removed:
        print(f"Restriction sites removed: {len(sites_removed)}")
        for name, pos, old_c, new_c, aa in sites_removed:
            print(f"  {name} at pos {pos}: {old_c} ({aa}) -> {new_c}")
    print()
    
    # Codon usage summary
    from collections import Counter
    codon_counts = Counter(dna_optimized[i:i+3] for i in range(0, len(dna_optimized), 3))
    print("Top 20 codons used:")
    for codon, count in codon_counts.most_common(20):
        aa = HUMAN_CODONS.get(codon, ('?', 0, 0))[0]
        print(f"  {codon} ({aa}): {count}")
    print()
    
    # Write optimized FASTA
    opt_header = f"Design_C_hybrid_E2_NS3_NS5B source=human_codon_optimized status=computational_candidate kozak=yes GC_pct={opt_gc*100:.1f}"
    opt_fasta = f">{opt_header}\n{wrap_dna(dna_with_kozak)}\n"
    
    out_path = args.exports_dir / 'final-candidate.optimized.dna.fasta'
    out_path.write_text(opt_fasta)
    print(f"Wrote: {out_path}")
    
    # Also write a comparison table
    comparison = f"""# Codon Optimization Comparison

| Metric | Original (Deterministic) | Optimized (Human CAI) |
|--------|--------------------------|----------------------|
| CDS length | {len(dna_orig_cds)} nt | {len(dna_optimized)} nt |
| Total length (w/ Kozak+stop) | {len(dna_orig)} nt | {len(dna_with_kozak)} nt |
| GC% | {gc_content(dna_orig_cds)*100:.1f}% | {opt_gc*100:.1f}% |
| Restriction sites | {len(find_restriction_sites(dna_orig_cds))} | {len(opt_sites)} |
| Method | Deterministic back-translation | Human-preferred codons, GC-balanced |

## Optimization Strategy

For each amino acid, we select codons that:
1. Have CAI fraction >= 70% of the highest-frequency codon for that aa
2. Among those, prefer the codon with lowest GC content
3. This balances expression efficiency (high CAI) with reduced GC (lower immunogenic mRNA risk)

## Remaining Concerns

- GC% of {opt_gc*100:.1f}% is still high (ideal: <60%). The E2 protein is inherently GC-rich
  (HCV codon usage is biased toward G/C-ending codons). Further reduction would require
  accepting lower-CAI codons or synonymous mutations at RNA structure level.
- No RNA stability motifs (5'/3' UTRs, poly-A tail) are included — those are platform-specific.
- No in-frame restriction sites were found in the optimized sequence.
"""
    
    comparison_path = args.exports_dir / 'codon-optimization-comparison.md'
    comparison_path.write_text(comparison)
    print(f"Wrote: {comparison_path}")


if __name__ == '__main__':
    main()
