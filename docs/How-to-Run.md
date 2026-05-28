# How to Run This Project

A concise guide for reviewers to re-execute the bundled, reviewer-safe HCV workbench pipeline.

The recommended path is the notebook. It uses the submitted local files as inputs and writes regenerated artifacts to `notebook-output/`, leaving the curated submission files in `data/`, `figures/`, and `constructs/` untouched.

---

## Recommended: Colab Notebook

1. Open `HCV_Workbench_Reviewer_Notebook.ipynb` in Google Colab.
2. Upload the full `final-submission/` folder, or clone/copy the repository so Colab can see `final-submission/data/sequence-manifest.tsv`.
3. Run all notebook cells from top to bottom.
4. Review regenerated outputs in `notebook-output/`.

Expected runtime: about 1 minute. No GPU, external API key, internet database query, or wet-lab step is required after the project files are available.

The notebook runs these reviewer-safe steps:

- manifest summary and QA
- E2 conservation analysis and conserved-window ranking
- construct export from the regenerated consensus
- scorecard regeneration
- SVG figure rendering
- validation checks for expected files, conservation bounds, score totals, and FASTA lengths

---

## Local Command-Line Fallback

Prerequisite: Python 3.10 or newer.

From inside `final-submission/`:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/summarize_manifest.py
python3 scripts/run_basic_workbench.py
python3 scripts/export_construct.py --include-kozak
python3 scripts/draft_scorecard.py
python3 scripts/generate_plots.py
python3 -m unittest discover -s tests -v
```

All default outputs go to:

```text
final-submission/notebook-output/
├── data/
├── figures/
└── constructs/
```

---

## Core Script Defaults

| Script | Bundled inputs | Default regenerated outputs |
|---|---|---|
| `scripts/summarize_manifest.py` | `data/sequence-manifest.tsv` | `notebook-output/data/sequence-manifest-summary.tsv`, `notebook-output/data/sequence-manifest-qa.md` |
| `scripts/run_basic_workbench.py` | `data/e2_aligned.fasta` | conservation CSVs, run summary, `notebook-output/figures/e2-conservation.svg`, `notebook-output/constructs/consensus-e2.protein.fasta` |
| `scripts/export_construct.py` | `notebook-output/constructs/consensus-e2.protein.fasta` | final-candidate FASTA, annotations, and construct map in `notebook-output/constructs/` |
| `scripts/draft_scorecard.py` | bundled manifest/candidate regions plus regenerated outputs | `notebook-output/data/design-scorecard.tsv`, `notebook-output/data/final-page-results-snippet.md` |
| `scripts/generate_plots.py` | regenerated outputs when present, otherwise bundled tables | `notebook-output/figures/conservation-plot.svg`, `construct-architecture.svg`, `scorecard-bars.svg` |

---

## Scope Notes

- The reviewer flow starts from the bundled curated data. It does not recollect NCBI, IEDB, MAFFT, or structure-prediction inputs.
- `scripts/analyze_iedb.py` is retained for optional raw IEDB CSV exports, but the reviewer package uses `docs/IEDB-Summary.md` and `data/candidate-regions.tsv`.
- The generated DNA/protein files are computational antigen-design artifacts only. They are not validated expression constructs, vaccine efficacy evidence, or wet-lab instructions.
