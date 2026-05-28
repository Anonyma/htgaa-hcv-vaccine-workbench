# IEDB T-Cell Epitope Summary

Scoring formula: `(assay_count × 0.4) + (unique_pmids × 0.3) + (unique_hla_types × 0.2) + (max_hla_coverage × 10 × 0.1)`

HLA coverage estimates from Sidney et al. 2008 (US population).

## Top 10 NS3 Epitopes

| Rank | Epitope | Len | Pos | Assays | PMIDs | HLA types | Best HLA cov | Score |
|---:|:---|---:|:---|---:|---:|---:|---:|---:|
| 1 | `KLVALGINAV` | 10 | 33–389 | 90 | 18 | 3 | 44% | 42.4 |
| 2 | `CINGVCWTV` | 9 | 39–55 | 57 | 17 | 4 | 44% | 29.1 |
| 3 | `VIKGGRHLIFCHSKKKCD` | 18 | 22–375 | 13 | 3 | 2 | 0% | 6.5 |
| 4 | `GYKVLVLNPSVAAT` | 14 | 222–235 | 11 | 2 | 6 | 0% | 6.2 |
| 5 | `HSKKKCDEL` | 9 | 33–41 | 7 | 2 | 2 | 12% | 3.9 |
| 6 | `GAVQNEVTL` | 9 | 603–611 | 7 | 3 | 1 | 0% | 3.9 |
| 7 | `KLSGLGLNAV` | 10 | 44–53 | 7 | 1 | 1 | 44% | 3.7 |
| 8 | `ATDALMTGY` | 9 | 74–82 | 7 | 1 | 1 | 16% | 3.5 |
| 9 | `GHVVGIFRAAVCTRG` | 15 | 151–165 | 6 | 1 | 2 | 0% | 3.1 |
| 10 | `LCPSGHVVGIFRAAV` | 15 | 147–161 | 6 | 1 | 2 | 0% | 3.1 |

## Top 10 NS5B Epitopes

| Rank | Epitope | Len | Pos | Assays | PMIDs | HLA types | Best HLA cov | Score |
|---:|:---|---:|:---|---:|---:|---:|---:|---:|
| 1 | `ALYDVVTKL` | 9 | 159–167 | 4 | 3 | 2 | 44% | 3.3 |
| 2 | `IMAKNEVFCV` | 10 | 123–132 | 4 | 1 | 1 | 44% | 2.5 |
| 3 | `MSYSWTGAL` | 9 | 2–10 | 4 | 1 | 2 | 0% | 2.3 |
| 4 | `KLPINALSNSLLRHH` | 15 | 5–19 | 3 | 1 | 1 | 0% | 1.7 |
| 5 | `ARMILLTHF` | 9 | 106–114 | 3 | 1 | 1 | 0% | 1.7 |
| 6 | `TYSVTPLDL` | 9 | 451–459 | 2 | 1 | 2 | 0% | 1.5 |
| 7 | `RMILMTHFF` | 9 | 193–201 | 1 | 1 | 1 | 15% | 1.1 |
| 8 | `SQRQKKVTF` | 9 | 46–54 | 1 | 1 | 1 | 0% | 0.9 |
| 9 | `ARMILMTHF` | 9 | 192–200 | 1 | 1 | 1 | 0% | 0.9 |
| 10 | `RYLLLCLLI` | 9 | 570–578 | 1 | 1 | 1 | 0% | 0.9 |

## Design C Cassette Candidates

Suggested: top 3 NS3 + top 2 NS5B by score, all ≤15 aa (fits within typical string-of-beads cassette).

| Protein | Epitope | Length | Score | Rationale |
|:---|:---|---:|---:|:---|
| NS3 | `KLVALGINAV` | 10 | 42.4 | 18 PMIDs, best HLA 44% |
| NS3 | `CINGVCWTV` | 9 | 29.1 | 17 PMIDs, best HLA 44% |
| NS5B | `ALYDVVTKL` | 9 | 3.3 | 3 PMIDs, best HLA 44% |
| NS5B | `IMAKNEVFCV` | 10 | 2.5 | 1 PMIDs, best HLA 44% |
| NS5B | `MSYSWTGAL` | 9 | 2.3 | 1 PMIDs, best HLA 0% |

## Safe Interpretation

These epitopes are candidates based on historical assay counts in IEDB. They are not validated for cross-reactivity, immunodominance hierarchy, or effectiveness in an mRNA vaccine context. Use as computational starting points only.
