# Computational HCV Vaccine Design Workbench

**Purpose:** This is a high-level explainer for non-specialist readers (mentors, family, industry council). It is NOT the HTGAA submission document. For the formal submission, see `docs/HTGAA-2026-Final-Project.md`.

**Status:** 4 active designs (A, B, C, D). Design C is PRIMARY NOMINEE.  
**Last updated:** May 13, 2026

---

## TLDR (One-Paragraph Summary)

I built a fully computational, reproducible pipeline that designs and ranks HCV vaccine immunogens. Starting from 47 public E2 sequences across 4 genotypes, I aligned them with MAFFT, computed per-position conservation (87.2% mean), mined 398 validated T-cell epitopes from IEDB, and used a transparent 100-point scorecard to compare four active designs: a natural baseline (A, 45/100), a consensus E2 (B, 66/100), an E2-ferritin nanoparticle (C, 68/100), and a focused conserved mosaic (D, 89/100). Design C -- a 640-aa monomer displaying 24 copies of consensus E2 on a self-assembling ferritin scaffold -- is the primary nomination, anchored by clinical precedent showing ~10x antibody titer improvement for ferritin-displayed antigens. Every number traces to a source file.

---

## What Is This Project?

A fully computational pipeline that collects public hepatitis C virus (HCV) sequence data, identifies the most conserved and immunologically validated regions of the viral envelope, designs a family of candidate immunogens using different strategies, scores each candidate against a transparent multi-criterion rubric, and exports the top-ranked construct as an annotated, codon-optimized DNA and protein sequence ready for experimental testing.

The project does not claim to have built a vaccine. The claim is specific and defensible: **a reproducible workbench that nominates an annotated HCV immunogen construct for future experimental validation.**

> **TLDR:** I built a Python pipeline that goes from public sequence data to a scored, synthesis-ready construct. No wet lab. Every step is documented and re-runnable.

---

## The Problem It Addresses

Hepatitis C virus (HCV) chronically infects roughly 50 million people worldwide and kills around 242,000 per year (WHO 2024). Despite 35+ years of research, there is no licensed vaccine.

The core obstacle is the E2 envelope protein -- the part of the virus that binds host cells and is the primary antibody target. E2 is a difficult target for three reasons:

1. **Extreme genetic diversity.** HCV has 8 confirmed genotypes and 93+ subtypes (ICTV 2026). A vaccine designed against a single reference strain trains the immune system on one variant of a constantly shifting target.

2. **The glycan shield.** E2 carries 9-11 N-linked glycosylation sites that act as molecular camouflage, physically blocking antibody access to the conserved surfaces that would actually be worth targeting.

3. **Conformational instability.** E2 adopts different shapes depending on context. Linear sequence-level approaches cannot fully capture the neutralizing epitopes that only exist as three-dimensional structures.

Computational approaches help by aggregating diversity data, identifying what is *conserved despite* the variability, and systematically comparing design strategies before committing to synthesis or animal studies.

> **TLDR:** HCV has no vaccine because E2 is hypervariable, glycosylated, and conformationally flexible. My pipeline addresses the diversity problem computationally before any lab work.

---

## The Pipeline -- 7 Stages

### Stage 1 -- Sequence Collection
Public HCV E2 protein sequences were downloaded from NCBI Virus. A curated panel spanning four genotypes (1a x15, 1b x15, 2a x1, 3a x16) was assembled, covering an estimated 65-75% of global HCV infections. All sequences are logged in `sequence-manifest.tsv` with accession numbers and source metadata.

- **How:** Manual curation from NCBI Virus + LANL HCV Database cross-reference.
- **Why:** A computational design is only as good as its input data. Every accession is traceable.

### Stage 2 -- Multiple Sequence Alignment
All sequences aligned using MAFFT v7 (auto-select algorithm), producing a column-level alignment. Alignment quality was verified manually for frameshifts and all-gap columns.

- **How:** MAFFT v7 web server + manual inspection.
- **Why:** Conservation analysis requires a high-quality alignment. Garbage in, garbage out.

### Stage 3 -- Conservation Analysis
Per-position Shannon entropy calculated in Python across all alignment columns. A 15-amino-acid sliding window was used to identify contiguous conserved regions. The most conserved window (positions 297-311, overlapping the CD81 binding loop) reached 99.15% conservation. Mean conservation across all positions: 87.2%.

- **How:** Custom Python script (`run_basic_workbench.py`) using Biopython and NumPy.
- **Why:** Conserved regions represent functional constraint -- the virus cannot easily mutate these positions without losing fitness. These are the best vaccine targets.

### Stage 4 -- Epitope Mining
The Immune Epitope Database (IEDB) was queried for positive T-cell assay results from HCV NS3 and NS5B proteins in human hosts. Results were ranked by a composite score weighting assay count, number of independent publications (PMIDs), HLA type count, and population coverage.

**Top hits:**
- KLVALGINAV (NS3, 90 assays, 18 PMIDs, HLA-A*02:01)
- CINGVCWTV (NS3, 57 assays, 17 PMIDs)
- ALYDVVTKL (NS5B, 4 assays)
- IMAKNEVFCV (NS5B, 4 assays)

- **How:** IEDB web query + composite ranking script.
- **Why:** T-cell epitopes with high assay counts and multiple independent publications are the most robustly validated. I wanted quantitative evidence, not just predictions.

### Stage 5 -- Construct Design
Five candidate immunogens were originally designed. After review, the old hybrid E2 + T-cell cassette design was removed from the active project. The current active designs are:

| Design | Strategy | Length | Score | Status |
|--------|----------|--------|-------|--------|
| A -- Natural Baseline | Single genotype 1a reference (strain H77) | ~420 aa | 45/100 | Active (floor) |
| B -- Consensus E2 | Statistical consensus of all curated sequences | 434 aa | 66/100 | Active (intermediate) |
| C -- E2-Ferritin Nanoparticle | Consensus E2 displayed on H. pylori ferritin 24-mer scaffold | 640 aa | 68/100 | **PRIMARY NOMINEE** |
| D -- Focused Conserved Mosaic | Only the top conserved E2 windows + T-cell cassette | 97 aa | 89/100 | Proof-of-concept |

**Old hybrid E2 + T-cell cassette** (492 aa, 76/100) was removed from the active project on 2026-05-12. Files are retained for archival context.

- **How:** Python scripts for consensus generation (`build_e2_ferritin.py`, etc.).
- **Why:** Comparing multiple strategies makes trade-offs explicit. A single design hides the counterfactual.

### Stage 6 -- Multi-Criterion Scoring
Each design scored on a 100-point, 6-axis rubric:

| Criterion | Weight | What It Measures |
|-----------|--------|------------------|
| Genotype Coverage | 25 | Breadth of genotype representation |
| Epitope Conservation | 20 | Per-position amino acid identity at functional sites |
| HLA Coverage | 15 | Population coverage of T-cell epitopes |
| Developability | 15 | Expression feasibility, folding confidence |
| Manufacturability | 15 | Construct length, GC content, synthesis cost |
| Interpretability | 10 | Clarity and communicability of design rationale |

**Final scores:** A = 45, B = 66, C = 53 raw + 15 multivalency bonus = **68**, Design D = 89.

- **How:** `draft_scorecard.py` -- transparent, documented weights.
- **Why:** A reviewer who disagrees with the weights can re-score using the same raw data. The scorecard is a decision-support tool, not an oracle.

> **TLDR:** Seven stages: collect -> align -> conserve -> mine epitopes -> design -> score -> export. All scripted in Python. All inputs/outputs traceable.

---

## The Lead Nomination -- Design C: E2-Ferritin Nanoparticle

Design C scores 68/100 (53 base + 15 multivalency bonus) and is the primary nomination. Here is why.

**Architecture:** Consensus E2 (434 aa) genetically fused via a flexible (G4S)3 linker to H. pylori ferritin (UniProt P52093, 167 aa). The monomer is 640 aa and self-assembles into a 24-subunit octahedral nanoparticle of approximately 1.69 MDa.

```
N -- [SpyTag: 13 aa] -- [(G4S)x3: 15 aa] -- [Consensus E2: 434 aa] -- [GSGSG: 5 aa] -- [Ferritin: 167 aa] -- [His6: 6 aa] -- C
```

**Why ferritin display matters:** Presenting 24 copies of the same antigen on a symmetric scaffold drives B-cell receptor cross-linking -- the same signal a real virus surface sends. Kanekiyo et al. 2013 (*Nature* 499:102-106) demonstrated approximately a 10-fold increase in neutralizing antibody titers when the influenza HA-stem antigen was displayed on the same H. pylori ferritin scaffold compared to soluble antigen. The scaffold itself is well-characterized and the particle size (~1.69 MDa, ~10-15 nm) is in the range optimal for lymph node trafficking and B-cell engagement.

**The scorecard:** Design C scores 68/100 (53 base + 15 multivalency bonus). The base score reflects the consensus E2 foundation; the +15 bonus is literature-anchored from Kanekiyo et al. 2013. The scorecard is a decision-support tool, not an efficacy oracle. It captures what can be computed from sequence. The Kanekiyo precedent captures what biology does with geometry.

> **TLDR:** Design C is a 640-aa E2-ferritin fusion that self-assembles into a 24-mer nanoparticle. It scores 68/100 and is biologically the most serious candidate because multivalent display amplifies B-cell responses ~10x per literature.

---

## The Scorecard Runner-Up -- Design D: Focused Conserved Mosaic

Design D wins the raw scorecard at 89/100. It is a 97-amino-acid linear construct made entirely of: the two most conserved E2 windows (99.15% and 97.73% conservation) connected by GGGGS linkers, plus the same four-epitope T-cell cassette.

It scores so high because it maximizes conservation efficiency (only top-1% positions included), retains full HLA coverage, and is dramatically cheaper to synthesize than any full-length design.

It does not lead because linear peptides stripped of structural context rarely elicit neutralizing antibodies. The surfaces that broadly neutralizing antibodies recognize on E2 are conformational -- they require the native fold. Design D is the right candidate for T-cell peptide assays, cost-limited settings, or for display ON the ferritin scaffold (a combined C+D construct is the highest-priority future design).

> **TLDR:** Design D (89/100) is a 97-aa computational proof-of-concept. Highest score but not a realistic vaccine alone. Best use case: T-cell assays or display on the ferritin scaffold.

---

## Validation -- What Was Done Computationally

### Sequence-Level Validation
- All 47 accession numbers logged and traceable in `sequence-manifest.tsv`
- Conservation calculated by Shannon entropy (standard method)
- Top conserved windows cross-referenced against known structural data: positions 297-311 overlap the CD81 binding loop, target of broadly neutralizing antibodies HEPC3, AR3C, and AR5A (Kong et al. 2013 *Science*; Flyak et al. 2018 *Cell*)

### Epitope Validation
- All T-cell epitopes sourced from IEDB positive human assays only
- Top epitope KLVALGINAV: 90 independent assays, 18 peer-reviewed publications
- HLA coverage estimated at A02 supertype (~44% US phenotypic coverage per Sidney et al. 2008)

### Structure Prediction
- Ferritin scaffold (Design C): ESMFold mean pLDDT **0.900**, 63.5% of residues above 0.90 -- high-confidence autonomous folding
- Full E2 consensus: ESMFold pLDDT ~0.3 -- low confidence, expected for a disulfide-rich glycoprotein (8+ disulfide bonds and N-linked glycans cannot be modeled by ESMFold). Crystal structures of related strains exist (PDB: 4MWF, 4WEB, 6MEJ) but our consensus sequence has not been structurally characterized

### Codon Optimization
- Design C DNA sequence codon-optimized for human expression using human codon frequency tables
- GC content balanced to **42.2%** overall (1,929 nt), within the 40-60% mRNA synthesis sweet spot
- Kozak sequence `GCCACC` at positions 1-6
- **0** internal restriction sites (EcoRI, BamHI, HindIII, XhoI, NheI)

> **TLDR:** Validation at sequence, epitope, structure, and DNA levels. Ferritin scaffold is high-confidence (pLDDT 0.900). E2 is low-confidence by ESMFold but that's expected -- we use PDB crystal structures for E2 reference.

---

## Why the old hybrid design was removed (Project Evolution)

The old hybrid design (consensus E2 + T-cell cassette, 492 aa, 76/100) was originally the primary nominee. It was removed on 2026-05-12 for two reasons:

1. **Scope focus.** The project's deepest biological argument is multivalent B-cell display (Design C), which has direct clinical precedent.

2. **Construct clarity.** Design C has a single, structurally coherent architecture (E2-ferritin fusion).

The IEDB-mined epitopes (398 assay rows) and T-cell analysis are documented in `docs/IEDB-Summary.md` and scoped as future work for linker-region insertion into Design C.

> **TLDR:** Old hybrid removed 2026-05-12 to sharpen the project's biological narrative around ferritin nanoparticle display. T-cell epitope data is preserved as future work.

---

## Limitations -- What Was Not Done

- No experimental expression, purification, or binding assay
- No immunization data, no efficacy claim
- E2 structural context not validated for the consensus sequence -- conformational epitopes may differ from reference structures
- Genotype 2a represented by a single sequence; genotypes 4-7 are absent (genotype 4 alone accounts for ~8-17% of global infections, dominant in Egypt and North Africa)
- HLA coverage limited to the A02 supertype; other HLA supertypes not analyzed
- CINGVCWTV Class II MHC presentation not confirmed (9-mer is Class I-typical)
- Steric crowding on the ferritin surface not modeled -- glycosylated E2 domains may overlap at 4-fold symmetry axes
- The +15 multivalency bonus is literature-anchored but NOT measured for this specific construct

> **TLDR:** No wet lab. Limited genotype panel (no G4-G7). HLA coverage is A02-only. E2 structure is unvalidated. Multivalency bonus is theoretical. All limitations are documented, not hidden.

---

## Future Validation Plan

**Phase 1 -- Expression and Binding (3-6 months)**
1. Gene-synthesize Design C codon-optimized DNA (1,929 nt, 42.2% GC)
2. Express in HEK293 or CHO cells (E2 requires mammalian glycosylation)
3. Confirm protein by Western blot (~70.4 kDa monomer)
4. Test binding against broadly neutralizing antibody panel: HEPC3, AR3C, AR5A, AP33
5. Negative-stain EM to confirm 24-mer assembly

**Phase 2 -- Computational Refinement (parallel)**
- ColabFold / AlphaFold2 with disulfide constraints for consensus E2 structural prediction
- NetMHCpan 4.1 and NetMHCIIpan 4.1 for HLA coverage beyond A02
- Expand genotype panel to include genotypes 4-7
- Design the combined candidate: conserved E2 windows (Design C) displayed on the ferritin nanoparticle (Design C) with T-cell cassette in the linker

**Phase 3 -- In Vivo Testing (aspirational)**
- Head-to-head mouse immunization: Designs A, B, D, and combined candidate
- HCVcc / HCVpp neutralization assays, epitope mapping, durability assessment

> **TLDR:** Next steps: gene synthesis -> mammalian expression -> bnAb binding assay -> EM confirmation. Parallel computational work: expand genotypes, broaden HLA, model disulfide-constrained structure.

---

## Tools Used

| Tool | Purpose |
|------|---------|
| NCBI Virus | Public HCV E2 sequence retrieval |
| MAFFT v7 | Multiple sequence alignment |
| Python (Biopython, NumPy) | Shannon entropy, sliding window conservation, FASTA handling |
| IEDB (Immune Epitope Database) | T-cell epitope mining and ranking |
| ESMFold | Protein structure confidence prediction (pLDDT scoring) |
| Python codon optimization script | Human codon-usage optimization, GC content balancing |
| Custom scoring framework | 6-axis, 100-point scorecard (`design-scorecard.tsv`) |

All tools are public and free. The pipeline is fully scripted in Python and re-runnable.

---

## File Map

| File | Contents |
|------|----------|
|| `data/design-scorecard.tsv` | Raw scorecard data (3 active + Design D) |
|| `docs/Design-C-Rationale.md` | Design C detailed rationale |
|| `constructs/design-C-e2-ferritin.dna.fasta` | Codon-optimized DNA (1,929 nt, 42.2% GC) |
|| `constructs/design-C-e2-ferritin.protein.fasta` | Protein sequence (640 aa) |
|| `constructs/design-C-e2-ferritin.annotations.tsv` | Construct element annotations |
|| `constructs/ferritin-esmfold.pdb` | Ferritin structure prediction |
|| `docs/IEDB-Summary.md` | IEDB epitope mining results |
|| `docs/Verification-Guide.md` | Step-by-step verification guide |

---

## Related Documents

| Document | What it covers | Path |
|----------|---------------|------|
|| This explainer | Project overview, TLDRs, problem statement, designs, validation, limitations | `Project-Explainer.md` |
|| Verification guide | Step-by-step verification steps and pass criteria | `docs/Verification-Guide.md` |
|| Scorecard data (TSV) | Raw numbers, sub-scores, manual sum verification | `data/design-scorecard.tsv` |

---

*Project: HTGAA Spring 2026 -- Computational HCV Vaccine Design Workbench*
*Active designs: A(45), B(66), C(68=53+15), D(89). Design C is PRIMARY NOMINEE.*
*Old hybrid design removed 2026-05-12. Files retained for archival context.*
