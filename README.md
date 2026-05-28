# Computational HCV Vaccine Design Workbench

**Author:** Z  
**Project:** HTGAA Spring 2026 — Individual Final Project

> A reproducible, fully in-silico pipeline that designs, scores, and nominates an annotated HCV immunogen construct ready for future experimental validation.

---

## Start Here — Reviewer Priority List

1. **Primary Submission** — `docs/HTGAA-2026-Final-Project.html`  
   One-page formal project page with design rationale, scorecard, nominated construct, and all key figures.
2. **Plain-text fallback** — `docs/HTGAA-2026-Final-Project.md`  
   Markdown source of the project page (identical content; use if HTML rendering is unavailable).
3. **Verification** — `docs/Verification-Guide.md`  
   Exact tools, commands, URLs, and pass criteria to independently check every claim in the submission.
4. **Re-run the pipeline** — `docs/How-to-Run.md`  
   Step-by-step instructions to reproduce the entire workflow locally or on Google Colab.
5. **Non-specialist overview** — `docs/Project-Explainer.md`  
   High-level summary for readers who want the story without domain jargon.
6. **Interactive notebook** — `HCV_Workbench_Reviewer_Notebook.ipynb`  
   One-click Colab workflow that re-executes the pipeline and writes outputs to `notebook-output/`.

---

## Folder Map

| Folder | What it contains |
|---|---|
| `docs/` | Submission documents, design rationales, IEDB summaries, and the guides listed above |
| `figures/` | SVG plots (conservation, scorecard, pipeline flow, HLA coverage, construct architecture) |
| `data/` | Sequence manifests, conservation tables, epitope regions, scorecard, and workbench summary |
| `constructs/` | Protein FASTA, DNA FASTA, annotations, construct maps, and ferritin PDB for Designs A–D |
| `scripts/` | Python pipeline scripts (alignment, scoring, plotting, codon optimization, construct export) |
| `tests/` | Colab reproducibility test (`test_colab_reproducibility.py`) |

---

## Important Disclaimer

This is a **computational nomination only**. No animal or human validation has been performed. The constructs and scores are in-silico design artifacts intended for future experimental testing — they are **not a licensed or validated vaccine**.

---

## Quick Start for Reviewers

1. Open `HCV_Workbench_Reviewer_Notebook.ipynb` in Colab and run all cells.
2. Open `docs/HTGAA-2026-Final-Project.md` for the full submission.
3. Open `data/design-scorecard.tsv` to see the curated 100-point scoring rubric.

For a complete file listing, see `File-Index.md`.
