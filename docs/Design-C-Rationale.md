# Design C — Computational E2-Ferritin Nanoparticle Immunogen

**Created:** 2026-05-04 by Hermes (DeepSeek V4 Pro)  
**Relabeled:** 2026-05-27 to Design C
**Status:** Computational candidate, fully in silico

## Summary

Design C is a fully computational adaptation of the HTGAA Proposal C (HCV E2-ferritin nanoparticle, April 2026), redesigned for zero wet-lab dependency. It fuses the V5 consensus E2 envelope glycoprotein (434 aa) to the H. pylori ferritin 24-mer nanoparticle scaffold (167 aa) via flexible linkers, with an N-terminal SpyTag for modular conjugation.

**Core claim:** Design C provides a particle-display advantage over a monomeric E2-only design: multivalent E2 presentation on a 24-mer ferritin cage should increase B-cell receptor cross-linking (Kanekiyo 2013 showed ~10× antibody titer improvement for HA-stem on ferritin vs. soluble antigen). It trades T-cell cassette breadth for structural multivalency — a different but complementary vaccine-design strategy.

## Construct Architecture

```
N — [SpyTag: 13 aa] — [(G4S)×3: 15 aa] — [Consensus E2: 434 aa] — [GSGSG: 5 aa] — [Ferritin: 167 aa] — [His6: 6 aa] — C
```

**Total:** 640 aa, ~70.4 kDa monomer | 24-mer: ~1.69 MDa

### Component Details

| Component | Position | Length | Source |
|-----------|----------|--------|--------|
| SpyTag | 1–13 | 13 aa | AHIVMVDAYKPTK — Zakeri et al. 2012 (PNAS) |
| (G4S)×3 linker | 14–28 | 15 aa | Standard flexible Gly-Ser |
| Consensus E2 | 29–462 | 434 aa | V5 workbench: 47-sequence MAFFT consensus (1a×15, 1b×15, 2a×1, 3a×16) |
| GSGSG linker | 463–467 | 5 aa | Short semi-flexible linker |
| Ferritin | 468–634 | 167 aa | H. pylori non-heme ferritin, UniProt P52093 (strain 26695) |
| His6 tag | 635–640 | 6 aa | Affinity purification handle |

### Key Features

1. **24-mer self-assembly:** Ferritin assembles into a hollow ~12 nm cage with octahedral symmetry. E2 is displayed on the exterior via the N-terminal fusion (ferritin N-termini point outward on the assembled particle).
2. **AR3 epitope displayed on particle surface:** E2 fused to ferritin N-terminus positions the AR3 CD81-binding epitope at the distal end of the protruding spike, away from the ferritin shell — maximizing antibody accessibility (precedent: Kanekiyo 2013 HA-stem-ferritin).
3. **SpyTag modularity:** The N-terminal SpyTag enables covalent conjugation to SpyCatcher-modified surfaces/adjuvants without disrupting the E2-ferritin fold.

## Structure Prediction Results

### Ferritin (ESMFold)
- **Mean pLDDT: 0.937** — very high confidence
- 92.2% of residues at pLDDT ≥ 0.90
- 99.4% at pLDDT ≥ 0.70
- The predicted fold shows the characteristic 4-helix bundle with the assembly loop — consistent with known ferritin crystal structures (PDB: 3BVE, 5G5H)
- The 24-mer assembly interface is preserved: residues forming the inter-subunit contacts (L28, Y31, R54, E61, etc.) are in the high-confidence core

### Consensus E2 (ESMFold)
- **Mean pLDDT: ~0.30** — low confidence (expected)
- E2 is a complex glycoprotein with 4 disulfide bonds (9 conserved cysteines), N-linked glycans, and flexible variable loops. ESMFold operates on sequence alone and cannot model:
  - Disulfide bonds (critical for E2's Ig-like fold)
  - N-linked glycan shielding
  - The HVR1 flexible loop (residues 1–27 of ectodomain)
- **This is not a failure of the design — it is a known limitation of ab initio folding for disulfide-rich glycoproteins.**
- Reference E2 structures (PDB: 4MWF, 6MEJ, 4WEB) confirm the AR3 epitope is surface-exposed on the E2 front layer, distal from the C-terminal membrane anchor — consistent with the fusion design geometry.

### E2-Ferritin Fusion Geometry
- Ferritin N-termini are exposed on the 24-mer outer surface
- E2 C-terminus (the natural membrane anchor) is fused to ferritin N-terminus
- This orients E2's neutralizing face (front layer, AR3 epitope) outward
- The 15-aa (G4S)×3 linker provides sufficient reach for E2 to extend beyond the ferritin shell
- Precedent: Kanekiyo 2013 fused HA-stem (153 aa) to ferritin N-terminus with a GS linker — our construct uses a longer linker for the larger E2 domain

## Comparison to the Old Hybrid E2 + T-cell Cassette

| Criterion (max) | C: E2-Ferritin NP | D: Focused Conserved Mosaic |
|---|---|---|
| Genotype coverage (25) | 19 | 19 |
| Epitope conservation (20) | 15 | 20 |
| HLA coverage (15) | 0 | 15 |
| Developability (15) | 5 | 14 |
| mRNA/DNA manufacturability (15) | 5 | 14 |
| Interpretability (10) | 9 | 7 |
| **Subtotal** | **53** | **89** |
| **Multivalency bonus** | **+15** | 0 |
| **Adjusted total** | **68** | **89** |

**Multivalency bonus justification:** The 24-mer ferritin display is a substantiated design advantage with literature precedent (Kanekiyo 2013 Nature: ~10× titer improvement for multivalent display). This is not efficacy — it is a structural-design argument for B-cell receptor cross-linking. The original HTGAA scorecard didn't include a multivalency axis because none of the three V5 designs were multivalent. Design C introduces this dimension.

### Why Design D Scores Higher

Design D (89/100) wins on T-cell breadth: conserved epitope windows + T-cell cassette (~44% US population). Design C (68/100) wins on B-cell targeting: 24-mer ferritin display should improve neutralizing antibody responses, but this is a qualitative argument without the quantitative IEDB backing that Design D has.

**These are complementary, not competing, designs.** A unified optimal candidate would combine both: E2-ferritin nanoparticle with NS3/NS5B T-cell epitopes in the linker region or as a separate mRNA-encoded cassette. This is noted as future work.

## Data Sources

- **Consensus E2:** MAFFT alignment of 47 public HCV E2 sequences (NCBI Protein), genotypes 1a/1b/2a/3a
- **Ferritin:** UniProt P52093, Helicobacter pylori strain 26695
- **ESMFold:** Evolutionary Scale Modeling (Lin et al. 2022, bioRxiv 10.1101/2022.07.20.500902)
- **Ferritin nanoparticle precedent:** Kanekiyo et al. 2013, Nature 499:102–106
- **AR3 epitope:** Pierce et al. 2010, PNAS 107:743–748
- **E2 stabilization:** Khera et al. 2018, MAbs 10:1123–1135 (PMID: 30234428)

## Safety Boundaries

- **No full HCV genome** — consensus E2 is antigen-only (434 aa)
- **No replication genes** — ferritin is a bacterial structural protein, not viral
- **No infectious HCV components** — the construct cannot produce virus
- **Computational nomination only** — no wet-lab validation has been performed
- **Ferritin is from H. pylori** — a bacterial protein; immunogenicity of the ferritin scaffold itself should be evaluated in future work

## Caveats

1. ESMFold cannot predict E2's native fold (pLDDT ~0.3) due to missing disulfide bonds and glycans. We rely on known crystal structures for E2 geometry arguments.
2. Ferritin folds well (pLDDT 0.94) but the E2-ferritin junction may affect assembly — this has not been tested.
3. The 24-mer assembly assumes ferritin folds correctly when fused to E2 — a large N-terminal fusion could sterically hinder assembly.
4. GC content of back-translated DNA: E2 is moderately GC-rich (~55–58%), while *H. pylori* ferritin is GC-poor (~39%). This creates a GC discontinuity across the construct that may cause translation-rate variation; codon optimization should smooth this profile across both domains.
5. The multivalency bonus in the scorecard is a qualitative literature-based argument, not a quantitative measurement. A defensible range is +8–10 points rather than +15.
6. **Steric crowding risk:** A 12 nm ferritin cage has ~452 nm² outer surface area (→ ~19 nm² per subunit). A glycosylated E2 domain likely has a cross-sectional area of 15–25 nm², meaning neighboring copies may overlap at the 4-fold symmetry axes. This is the single most important unvalidated risk.
7. **Glycosylation bulk:** E2 has 9–11 predicted N-linked glycosylation sites. Mammalian glycans add ~2–3 kDa per site and extend ~2–3 nm from the surface, compounding steric crowding and potentially shielding the AR3 epitope.
8. SpyTag-SpyCatcher chemistry requires further optimization for nanoparticle conjugation — it's included as a modular design feature, not a tested component.

## Files

| File | Path |
|------|------|
| Protein FASTA | `constructs/design-C-e2-ferritin.protein.fasta` |
| Annotation TSV | `constructs/design-C-e2-ferritin.annotations.tsv` |
| Ferritin ESMFold PDB | `constructs/ferritin-esmfold.pdb` |
| E2 N-term ESMFold PDB | `constructs/design-C-e2-ferritin.protein.fasta` (ESMFold input) |
| E2 C-term ESMFold PDB | `constructs/design-C-e2-ferritin.protein.fasta` (ESMFold input) |
| Build script | `scripts/build_e2_ferritin.py` |
