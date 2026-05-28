# Independent Verification Guide

This guide lists the public tools and databases used in this project, what to save from each, and how an independent reviewer can verify the outputs.

## Public Tools And Databases

| Tool/site | Use in this project | Output to save |
|---|---|---|
| NCBI Virus [↗](https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/) | Collect representative HCV E2 sequences by genotype. | Raw FASTA plus accession metadata. |
| NCBI Protein [↗](https://www.ncbi.nlm.nih.gov/protein/) | Cross-check protein accessions and reference sequences. | Accession records and source URLs. |
| LANL HCV Database [↗](https://hcv.lanl.gov/content/index) | HCV-specific orientation and historical sequence/immunology context. | Notes, not the sole dataset source. |
| MAFFT [↗](https://mafft.cbrc.jp/alignment/server/) | Align E2 sequences before conservation scoring. | Aligned FASTA. |
| IEDB [↗](https://www.iedb.org/) | Find experimentally reported HCV epitopes and HLA restrictions. | Epitope table with evidence notes. |
| IEDB Population Coverage [↗](https://tools.iedb.org/population/) | Estimate population coverage for epitope-HLA pairs. | Coverage report or screenshot. |
| ExPASy ProtParam [↗](https://web.expasy.org/protparam/) | Check simple protein properties. | MW, pI, instability, GRAVY notes. |
| Benchling [↗](https://www.benchling.com/molecular-biology) or SnapGene Viewer [↗](https://www.snapgene.com/snapgene-viewer) | Visualize annotated DNA/protein construct. | Optional construct map or GenBank file. |

## What To Save From Public Websites

| Website | Search/query | Save for final page |
|---|---|---|
| NCBI Virus [↗](https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/) | `Hepatitis C virus E2 genotype 1a`, repeat for 1b, 2a, 3a | raw FASTA, accession IDs, genotype notes |
| NCBI Protein [↗](https://www.ncbi.nlm.nih.gov/protein/) | accession lookup from NCBI Virus records | record pages or URLs for traceability |
| LANL HCV Database [↗](https://hcv.lanl.gov/content/index) | HCV genotype/diversity and immunology context | short notes only; do not mix untracked sequences into the dataset |
| MAFFT [↗](https://mafft.cbrc.jp/alignment/server/) | curated E2 FASTA | aligned FASTA saved as `data/e2_aligned.fasta` |
| IEDB [↗](https://www.iedb.org/) | HCV NS3 and NS5B T-cell epitopes | epitope sequence, HLA restriction, evidence notes |
| IEDB Population Coverage [↗](https://tools.iedb.org/population/) | epitope plus HLA table | population coverage output or screenshot, with caveat |
| ExPASy ProtParam [↗](https://web.expasy.org/protparam/) | final candidate protein | MW, pI, instability, GRAVY notes |

## 1. Verify sequence manifest

**Tool:** NCBI Virus (https://www.ncbi.nlm.nih.gov/labs/virus/vssi/) — free, no login required for search.

**Input file:** `data/sequence-manifest.tsv`

**Expected output:** The manifest lists every E2 sequence accession with its assigned genotype (1a, 1b, 2a, 3a). The per-genotype counts should match the sequences downloaded from NCBI Virus.

**Pass criterion:** Total accession count in the manifest equals the count of sequences actually downloaded. No duplicate accessions are present.

## 2. Verify alignment

**Tool:** Jalview (https://www.jalview.org) or EBI MView (https://www.ebi.ac.uk/jdispatcher/msa/mview) — both free.

**Input file:** `data/e2_aligned.fasta`

**Expected output:** A multiple sequence alignment in FASTA format. When opened in Jalview or MView, the HVR1 hypervariable region at the N-terminus of E2 should appear as a zone of high amino-acid variability.

**Pass criterion:** The alignment opens without parsing errors. HVR1 is visibly variable across sequences, while downstream structural regions show greater conservation.

## 3. Verify conservation scores

**Tool:** Re-run `python3 scripts/run_basic_workbench.py` from inside `final-submission/`, or open the CSV in any spreadsheet (e.g., Google Sheets https://sheets.new or LibreOffice Calc https://www.libreoffice.org).

**Input file:** `data/e2-conservation.csv`

**Expected output:** One row per alignment position with a conservation score on a 0–1 scale. Positions in known structural or epitope regions should tend toward higher values.

**Pass criterion:** The CSV contains the same number of data rows as there are columns in the alignment. Every conservation value is between 0 and 1 (inclusive).

## 4. Verify scorecard arithmetic

**Tool:** Any spreadsheet program (e.g., Google Sheets https://sheets.new or LibreOffice Calc https://www.libreoffice.org), or command-line tools such as `awk` or `python`.

**Input file:** `data/design-scorecard.tsv`

**Expected output:** A TSV with design categories, weights, and per-design scores. The weights should sum to 100, and every score should fall within the 0–100 range.

**Pass criterion:** Sum of category weights equals exactly 100. No design score is less than 0 or greater than 100.

## 5. Verify construct length

**Tool:** ExPASy ProtParam (https://web.expasy.org/protparam/) — free, or `grep -v "^>" file | tr -d '\n' | wc -c` on the command line.

**Input files:** The exported construct file (e.g., `constructs/design-C-e2-ferritin.protein.fasta` or `constructs/final-candidate.protein.fasta`) and its corresponding `.dna.fasta`.

**Expected output:** The protein sequence is approximately 640 amino acids. The DNA sequence is approximately 1,920 nucleotides without the Kozak sequence; with Kozak it is slightly longer.

**Pass criterion:** Protein length is between 600 and 700 amino acids. DNA length is between 1,800 and 2,100 nucleotides.
