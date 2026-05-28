#!/usr/bin/env python3
"""Regression checks for the reviewer/Colab workflow."""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PACKAGE_ROOT / "notebook-output"


def run_script(script_name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, f"scripts/{script_name}", *args],
        cwd=PACKAGE_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def read_fasta_sequence(path: Path) -> str:
    return "".join(
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip() and not line.startswith(">")
    )


class ColabReproducibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        if OUTPUT_ROOT.exists():
            shutil.rmtree(OUTPUT_ROOT)

    def test_colab_entrypoints_and_scripts_are_portable(self) -> None:
        self.assertTrue((PACKAGE_ROOT / "requirements.txt").exists())
        notebook_path = PACKAGE_ROOT / "HCV_Workbench_Reviewer_Notebook.ipynb"
        self.assertTrue(notebook_path.exists())
        notebook = json.loads(notebook_path.read_text())
        self.assertGreaterEqual(len(notebook.get("cells", [])), 6)

        forbidden = ["/Users/z", "hcv-workbench", "data/processed"]
        for path in (PACKAGE_ROOT / "scripts").glob("*.py"):
            text = path.read_text()
            for token in forbidden:
                self.assertNotIn(token, text, f"{path.name} still contains {token}")

    def test_default_core_pipeline_writes_only_notebook_output(self) -> None:
        curated_before = {
            path: path.read_text()
            for path in [
                PACKAGE_ROOT / "data" / "e2-conservation.csv",
                PACKAGE_ROOT / "data" / "design-scorecard.tsv",
                PACKAGE_ROOT / "constructs" / "consensus-e2.protein.fasta",
            ]
        }

        run_script("summarize_manifest.py")
        run_script("run_basic_workbench.py")
        run_script("export_construct.py", "--include-kozak")
        run_script("draft_scorecard.py")

        expected = [
            OUTPUT_ROOT / "data" / "sequence-manifest-summary.tsv",
            OUTPUT_ROOT / "data" / "sequence-manifest-qa.md",
            OUTPUT_ROOT / "data" / "e2-conservation.csv",
            OUTPUT_ROOT / "data" / "e2-conserved-windows.csv",
            OUTPUT_ROOT / "data" / "workbench-run-summary.md",
            OUTPUT_ROOT / "data" / "design-scorecard.tsv",
            OUTPUT_ROOT / "figures" / "e2-conservation.svg",
            OUTPUT_ROOT / "constructs" / "consensus-e2.protein.fasta",
            OUTPUT_ROOT / "constructs" / "final-candidate.protein.fasta",
            OUTPUT_ROOT / "constructs" / "final-candidate.dna.fasta",
            OUTPUT_ROOT / "constructs" / "final-candidate.annotations.tsv",
            OUTPUT_ROOT / "constructs" / "final-candidate.construct-map.txt",
        ]
        for path in expected:
            self.assertTrue(path.exists(), f"missing generated output: {path}")

        for path, original_text in curated_before.items():
            self.assertEqual(path.read_text(), original_text, f"curated artifact was overwritten: {path}")

    def test_generated_outputs_have_reviewer_sanity_checks(self) -> None:
        run_script("summarize_manifest.py")
        run_script("run_basic_workbench.py")
        run_script("export_construct.py", "--include-kozak")
        run_script("draft_scorecard.py")

        with (OUTPUT_ROOT / "data" / "sequence-manifest-summary.tsv").open(newline="") as handle:
            manifest_rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertTrue(manifest_rows)
        self.assertEqual(
            set(manifest_rows[0]),
            {"protein", "subtype", "included", "excluded", "needs_review", "blank_include", "total"},
        )

        with (OUTPUT_ROOT / "data" / "e2-conservation.csv").open(newline="") as handle:
            conservation_rows = list(csv.DictReader(handle))
        self.assertTrue(conservation_rows)
        for row in conservation_rows:
            conservation = float(row["conservation"])
            self.assertGreaterEqual(conservation, 0.0)
            self.assertLessEqual(conservation, 1.0)

        with (OUTPUT_ROOT / "data" / "design-scorecard.tsv").open(newline="") as handle:
            score_rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertGreaterEqual(len(score_rows), 4)
        base_fields = [
            "genotype_coverage_25",
            "epitope_conservation_20",
            "hla_coverage_15",
            "developability_15",
            "mrna_dna_manufacturability_15",
            "interpretability_10",
        ]
        for row in score_rows:
            base_total = sum(int(row[field]) for field in base_fields)
            bonus = int(row.get("multivalency_bonus_15", 0))
            self.assertEqual(base_total, int(row["base_total"]))
            self.assertEqual(min(100, base_total + bonus), int(row["total_100"]))

        protein = read_fasta_sequence(OUTPUT_ROOT / "constructs" / "final-candidate.protein.fasta")
        dna = read_fasta_sequence(OUTPUT_ROOT / "constructs" / "final-candidate.dna.fasta")
        self.assertGreater(len(protein), 300)
        self.assertEqual(len(dna), (len(protein) * 3) + 9)


if __name__ == "__main__":
    unittest.main()
