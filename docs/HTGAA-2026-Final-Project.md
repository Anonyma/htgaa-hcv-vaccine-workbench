---
title: 'Individual Final Project'
weight: 10
---

<!--
  HTGAA 2026 Final Project — Computational HCV Vaccine Design Workbench
  (post-pivot v5, 2026-04-30)
-->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
  .fp{
    --bg:#0a0e1a;--bg-2:#0f1422;--card:#121a2c;--rule:rgba(233,226,207,0.14);
    --ink:#e9e2cf;--ink-dim:#bfb6a0;--ink-mute:#8a8472;
    --gfp:#34d399;--gfp-soft:rgba(52,211,153,0.18);
    --amber:#fbbf24;--crimson:#f87171;
    background:linear-gradient(180deg,var(--bg) 0%,var(--bg-2) 100%);
    color:var(--ink);
    font-family:'EB Garamond', Georgia, serif;
    font-size:18px;line-height:1.62;
    padding:64px max(24px,4vw);
    margin:-24px -24px 0;
  }
  .fp *{box-sizing:border-box}
  .fp .wrap{max-width:920px;margin:0 auto}
  .fp .micro{font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace;font-size:13px;letter-spacing:0.18em;text-transform:uppercase;color:var(--ink-dim)}
  .fp h1{font-family:'Instrument Serif', serif;font-weight:400;font-size:72px;line-height:1.02;letter-spacing:-0.015em;margin:18px 0 18px;color:#fbf6e8}
  .fp h1 em{color:var(--gfp);font-style:italic}
  .fp h2{font-family:'Instrument Serif', serif;font-weight:400;font-size:42px;line-height:1.08;margin:64px 0 14px;color:#fbf6e8;letter-spacing:-0.01em;border-top:1px solid var(--rule);padding-top:30px}
  .fp h2 .num{font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace;font-size:13px;letter-spacing:0.22em;color:var(--gfp);display:block;text-transform:uppercase;margin-bottom:6px}
  .fp h3{font-family:'Instrument Serif', serif;font-weight:400;font-size:28px;line-height:1.15;margin:32px 0 8px;color:#fbf6e8}
  .fp h4{font-family:'Inter', sans-serif;font-weight:600;font-size:14px;letter-spacing:0.12em;text-transform:uppercase;color:var(--ink-dim);margin:22px 0 6px}
  .fp p{margin:0 0 14px;color:var(--ink)}
  .fp p.lede{font-size:22px;line-height:1.45;color:var(--ink);font-style:italic;border-left:2px solid var(--gfp);padding:6px 0 6px 22px;margin:18px 0 26px}
  .fp ul,.fp ol{padding-left:22px;margin:6px 0 16px}
  .fp li{margin:4px 0}
  .fp a{color:var(--gfp);text-decoration:none;border-bottom:1px dotted var(--gfp-soft)}
  .fp a:hover{border-bottom-style:solid}
  .fp code,.fp .mono{font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace;font-size:14px;color:var(--ink);background:rgba(255,255,255,0.04);padding:1px 6px;border-radius:2px}
  .fp .pill{display:inline-block;font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace;font-size:12px;letter-spacing:0.06em;padding:2px 8px;border:1px solid var(--rule);border-radius:2px;margin:0 6px 6px 0;color:var(--ink-dim);background:rgba(255,255,255,0.02)}

  .fp .meta{display:flex;flex-wrap:wrap;gap:18px 28px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:18px 0;margin:22px 0 12px;color:var(--ink-dim);font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace;font-size:12px;letter-spacing:0.16em;text-transform:uppercase}
  .fp .meta div b{display:block;color:var(--gfp);font-weight:500;letter-spacing:0.18em;font-size:11px;margin-bottom:4px}
  .fp .meta div span{color:var(--ink);letter-spacing:0.08em}

  .fp .aim{border-top:1px solid var(--rule);padding-top:18px;margin-top:24px}
  .fp .aim .label{font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace;font-size:12px;letter-spacing:0.22em;color:var(--gfp);text-transform:uppercase}

  .fp .callout{border-left:2px solid var(--amber);padding:12px 18px;margin:22px 0;background:rgba(251,191,36,0.05);color:var(--ink)}
  .fp .callout b{color:var(--amber);font-weight:500}

  .fp table{width:100%;border-collapse:collapse;margin:14px 0 18px;font-size:15px;font-family:'Inter', sans-serif}
  .fp table th,.fp table td{border-bottom:1px solid var(--rule);padding:10px 12px;text-align:left;vertical-align:top}
  .fp table th{font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace;font-size:11px;letter-spacing:0.16em;text-transform:uppercase;color:var(--ink-dim);font-weight:500}
  .fp table td.num{text-align:right;font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace;color:var(--gfp);width:90px}
  .fp .tcells{display:grid;grid-template-columns:1fr 1fr;gap:8px 22px;font-family:'Inter', sans-serif;font-size:15px;margin:6px 0 10px}
  .fp .tcells label{display:flex;gap:10px;align-items:flex-start;color:var(--ink)}
  .fp .tcells .check{width:14px;height:14px;border:1px solid var(--gfp);border-radius:2px;flex:none;margin-top:5px;background:rgba(52,211,153,0.12);position:relative}
  .fp .tcells .check.on::after{content:'';position:absolute;inset:2px;background:var(--gfp);border-radius:1px}
  .fp .tcells .group-h{grid-column:1/-1;font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace;font-size:11px;letter-spacing:0.16em;text-transform:uppercase;color:var(--gfp);margin-top:14px}

  .fp blockquote{margin:18px 0;padding:14px 22px;border-left:2px solid var(--gfp);font-style:italic;color:var(--ink);background:rgba(52,211,153,0.05)}

  .fp .footnote{font-size:14px;color:var(--ink-mute);font-style:italic;margin-top:30px;border-top:1px solid var(--rule);padding-top:16px}

  @media (max-width:720px){
    .fp h1{font-size:48px}
    .fp h2{font-size:30px}
    .fp .tcells{grid-template-columns:1fr}
  }
</style>

<div class="fp"><div class="wrap">

<div class="micro">HTGAA 2026 · MAS.885 · Individual Final Project</div>

<h1>Computational HCV Vaccine Design <em>Workbench</em></h1>

<p class="lede">A reproducible computational pipeline that designs, ranks, and exports candidate HCV vaccine immunogens against viral diversity — without claiming to produce or validate a vaccine.</p>

<div class="meta">
  <div><b>Author</b><span>Zoe Isabel Senon</span></div>
  <div><b>Track</b><span>Committed Listener</span></div>
  <div><b>Presentation</b><span>May 13, 2026</span></div>
  <div><b>Pivot</b><span>v5 · post-2026-04-30</span></div>
  <div><b>Wet-lab</b><span>None — fully computational</span></div>
</div>

<h2><span class="num">Section 1</span>Abstract</h2>

<p>Hepatitis C virus (HCV) remains a major global health problem: roughly 50&nbsp;million people live with chronic infection, around 1.0&nbsp;million new infections occur each year, and HCV caused about 242,000 deaths in 2022 (WHO, 25 July 2025). Direct-acting antivirals cure more than 95% of treated patients, but treatment does not prevent reinfection or solve access gaps, and there is still no effective preventive vaccine. HCV is hard for vaccine design because it is genetically diverse across global genotypes and exists as quasispecies within infected individuals; its envelope protein E2 contains variable, glycan-shielded loops that distract antibodies away from conserved vulnerable sites.</p>

<p>The objective of this project is to build a fully <b>computational HCV vaccine-design workbench</b> that compares candidate immunogens for broad coverage of HCV diversity. The hypothesis is that a <b>consensus</b>, <b>nanoparticle-displayed</b>, or <b>mosaic</b> immunogen can cover more HCV sequence and epitope diversity than a single natural reference strain while remaining plausible as an mRNA/DNA-expressible construct. Three specific aims drive the work: (1) collect a small public HCV sequence panel, align it, and map conserved versus variable regions; (2) generate and rank four candidate designs — a natural E2 baseline (A), a consensus E2 (B), an E2-ferritin nanoparticle (C), and a focused conserved mosaic (D) — using a transparent six-category scorecard; (3) export the highest-ranked design as an annotated mRNA/DNA-ready construct (protein FASTA, codon-optimized DNA FASTA, GenBank-style annotation) and document a future cloud-lab validation path.</p>

<p>Methods are entirely computational: public sequence collection (NCBI Virus, LANL HCV), multiple sequence alignment (MAFFT/Clustal Omega), per-position conservation scoring, IEDB epitope and HLA-population-coverage lookup, ProtParam developability flags, deterministic codon-optimized back-translation, and Twist-style construct annotation. The deliverable is a reproducible analysis package and an annotated antigen nomination — not a vaccine, not a clinical claim.</p>

<h2><span class="num">Section 2</span>Project Aims</h2>

<div class="aim">
  <div class="label">Aim 1 · Experimental (this project)</div>
  <h3>Build a public HCV diversity and conservation map.</h3>
  <p>The first aim of my final project is to <b>map HCV antigen diversity from public sequences</b> by utilizing NCBI Virus and LANL HCV for sequence retrieval, MAFFT or Clustal Omega for multiple sequence alignment, a per-position conservation script, and IEDB for known T-cell epitope and HLA-restriction evidence. I will focus on E2 (genotypes 1a, 1b, 2a, and 3a; 10–20 sequences per genotype) as the antibody-facing antigen and use NS3/NS5B only for T-cell-epitope analysis. Outputs: a sequence manifest (<span class="mono">sequence-manifest.tsv</span>), a curated aligned FASTA, conservation plots, and a candidate-region table for inclusion or avoidance. A detailed step-by-step protocol is in <a href="#sec4">Section 4</a>.</p>
</div>

<div class="aim">
  <div class="label">Aim 2 · Development (completed)</div>
  <h3>Design and rank four candidate HCV immunogens.</h3>
  <p>Following Aim 1, generate four candidate immunogens — a <b>natural E2 reference</b> (A), a <b>consensus E2</b> (B), an <b>E2-ferritin nanoparticle</b> (C), and a <b>focused conserved mosaic</b> (D) — and score each with a transparent 100-point scorecard (genotype coverage, epitope conservation, predicted HLA population coverage, developability, mRNA/DNA manufacturability, interpretability). Design C is the primary nominee for translation (68/100).</p>
  <p>Next development steps, ordered by feasibility:</p>
  <ol>
    <li><b>Structural plausibility check (free, ~1 hour).</b> Submit the consensus E2 sequence to <a href="https://colab.research.google.com/github/sokrypton/ColabFold">ColabFold</a> or <a href="https://esmfold.com">ESMFold</a> (Meta free API) to obtain a predicted PDB. Compare pLDDT scores to known E2 structures. This can be done via a web browser or scripted with API access.</li>
    <li><b>Expand genotype panel (free, ~2–3 hours).</b> Add genotypes 4a, 5a, 6a, and 7a from NCBI Virus and re-run MAFFT + conservation. Can be scripted with NCBI access.</li>
    <li><b>Tune scoring weights against bnAb data (literature review, ~1–2 hours).</b> Cross-reference conserved windows against published broadly neutralizing antibody epitope maps (Keck et al. 2019; Bailey et al. 2019). Requires biological accuracy review [BIO].</li>
    <li><b>AlphaFold-multimer for E2–receptor complexes (free, ~1–2 hours, GPU-optional).</b> Predict E2–CD81 binding interface; requires ColabFold GPU runtime or local AlphaFold 2 installation. Requires a pre-provisioned GPU runtime.</li>
  </ol>
  <p>Design D (89/100) scores higher on the computational rubric because it is a minimal mosaic of only conserved residues and T-cell epitopes, but it is not a realistic stand-alone vaccine immunogen: it lacks the full E2 ectodomain needed for native-like B-cell epitope presentation, has not been structurally validated, and would require a carrier scaffold or VLP platform before expression. Design C, while scoring lower on the rubric, is a complete, literature-grounded nanoparticle display construct (consensus E2 + ferritin) with precedent for ~10× neutralizing-antibody titer improvement (Kanekiyo et al. 2013, Nature). The primary nominee is therefore the design with the clearest path to experimental testing, not the highest computational score.</p>
</div>

<div class="aim">
  <div class="label">Aim 3 · Visionary (long term)</div>
  <h3>Grow the workbench into an open educational antigen down-selection platform.</h3>
  <p>If fully realized, a workbench like this becomes a small, transparent, educational version of a professional antigen down-selection pipeline — pulling viral diversity data, designing candidate immunogens, scoring breadth and manufacturability, and handing the best candidates to experimental expression and immunology workflows. It would lower the barrier for students and small labs to reason rigorously about pan-genotype vaccine design.</p>
</div>

<h2><span class="num">Section 3</span> Background</h2>

<h3>Two peer-reviewed sources</h3>
<p><b>Bailey JR, Barnes E, Cox AL.</b> <i>Approaches, progress, and challenges to hepatitis C vaccine development.</i> Gastroenterology, 2019. The review summarizes why HCV vaccines remain unsolved despite cure-grade DAAs: high genotype diversity, quasispecies evolution within hosts, glycan shielding on E1/E2, and the need to elicit both broadly neutralizing antibodies (bNAbs) and T-cell breadth. It motivates the use of conserved E2 surfaces and T-cell-targeted regions as a design strategy.</p>
<p><b>Keck Z-Y et&nbsp;al.</b> <i>Broadly neutralizing antibodies from HCV-infected patients define conserved vulnerability sites on E2.</i> Multiple isolates of human bNAbs map to overlapping conserved E2 epitope clusters (CD81-binding region, antigenic regions 3 and 4) that are recurrently targeted across genotypes. This is the empirical basis for picking conserved E2 windows over variable hypervariable region 1 (HVR1) when designing a consensus or mosaic antigen.</p>

<h3>Why this project is novel or innovative</h3>
<p>Most beginner HCV-vaccine projects either pick a single reference strain (and ignore genotype diversity) or pick a complex structure-based design (and lose interpretability for a learner). This workbench takes the middle path: a small, fully reproducible, documented pipeline that compares a natural baseline, a consensus design, an E2-ferritin nanoparticle, and a focused conserved mosaic head-to-head with a transparent scorecard. The novelty is methodological — it makes the trade-off between coverage, complexity, and developability explicit and inspectable, instead of hiding it inside a black-box design pipeline. It also frames the deliverable honestly, as a <i>candidate nomination</i> rather than a vaccine, which is the framing the field actually needs at this stage.</p>

<h3>Why it matters</h3>
<p>HCV is a paradigmatic <b>diversity-first</b> vaccine target: chronic infection, no preventive vaccine, no clear single dominant immunogen, and a virus that mutates inside each host. About 50 million people live with chronic HCV, and the WHO 2030 elimination target is at risk because cure alone does not prevent reinfection. A workbench that lets someone reason rigorously about diversity-aware antigen design — with public data, free tools, and a reproducible scorecard — is directly relevant to the bottleneck the field faces. More broadly, the same workflow generalizes to other diversity-first targets (influenza, HIV, malaria stage-specific antigens), where consensus and mosaic designs are an active area of research. If the methods and the scorecard prove useful, they can lower the entry bar for students, citizen scientists, and small labs to participate in pan-genotype vaccine design discussions, and they can make computational antigen design more legible to clinicians and regulators downstream.</p>

<h3>Ethical implications</h3>
<p>The relevant principles are <b>non-maleficence</b>, <b>responsibility</b>, and <b>justice</b>. Non-maleficence: the project must not produce a replication-competent HCV genome, infectious clone, or any wet-lab artifact, and must not over-claim biological efficacy from purely computational scoring. Responsibility: every score, sequence, and design choice must be traceable, with public sources cited and assumptions documented; results must be framed as candidate nominations, not validated vaccines. Justice: HCV burden falls disproportionately on people who inject drugs, people in low- and middle-income countries, and prison populations, and any vaccine work — even computational — must be framed in service of access, not exclusivity.</p>
<p>Concrete measures: (i) only public sequence data from NCBI/LANL is used, with accessions logged in a manifest; (ii) the construct export is antigen-only — no full genome, no replication genes, no rescue components — and is screened against SecureDNA-style biosafety norms before any future synthesis; (iii) the writeup uses the language "candidate immunogen" and "design artifact" rather than "vaccine" anywhere a clinical reader could be misled; (iv) limitations are stated up front (small dataset, computational proxies, no immunogenicity data). Possible unintended consequences include over-reliance on consensus designs that score well by alignment but fold poorly, and the risk that a "ranked" output reads as a clinical recommendation; the mitigation is to keep the scorecard transparent and to require structural and immunological validation before any clinical claim. Alternatives include sticking to a single-strain natural baseline (loses the diversity argument) or jumping directly to structure-based design (loses interpretability for a learner). The chosen path keeps both interpretability and a credible diversity argument while staying entirely computational.</p>

<h2 id="sec4"><span class="num">Section 4</span>Experimental Design, Techniques, Tools, and Technology</h2>

<h3>Detailed plan and timeline</h3>
<ol>
  <li><b>Week of May 5 — Step 1: Define the dataset.</b> Pull 10–20 E2 sequences each from HCV genotypes 1a, 1b, 2a, and 3a from <a href="https://www.ncbi.nlm.nih.gov/labs/virus/">NCBI Virus</a> and the <a href="https://hcv.lanl.gov/">LANL HCV database</a>. Log every record in <span class="mono">sequence-manifest.tsv</span> (accession, genotype, subtype, protein, source, notes). Reject duplicates, fragments, ambiguous-genotype records, and whole-polyprotein entries with unclear E2 boundaries. <i>~1 day.</i> Expected: a 40–80 sequence panel small enough to inspect manually.</li>
  <li><b>Step 2: Align E2 sequences.</b> Run multiple sequence alignment with MAFFT (or Clustal Omega) on the curated panel; export <span class="mono">e2-aligned.fasta</span>. <i>~1–2 hours.</i> Expected: a clean alignment with HVR1 visibly variable and a conserved CD81-binding spine.</li>
  <li><b>Step 3: Compute conservation.</b> Score each alignment column by fraction of sequences carrying the most-common non-gap residue; export <span class="mono">e2-conservation.csv</span>, <span class="mono">e2-conservation.svg</span>, and a conserved-window table. <i>~1 day.</i> Expected: clear high-conservation peaks at known antigenic regions and pronounced troughs at HVR1.</li>
  <li><b>Step 4: Add epitope evidence.</b> Pull HCV T-cell epitope rows from <a href="https://www.iedb.org/">IEDB</a>, with HLA restriction notes; run IEDB Population Coverage where HLA data exists. Build <span class="mono">candidate-regions.tsv</span>. <i>~1 day.</i> Expected: a short list of credible NS3/NS5B epitopes with traceable evidence; reject low-evidence rows.</li>
  <li><b>Step 5: Generate candidate designs.</b> (A) natural E2 from one strain; (B) consensus E2 from the alignment, with gap-heavy positions flagged; (C) E2-ferritin nanoparticle = consensus E2 fused to ferritin scaffold with SpyTag-SpyCatcher; (D) focused conserved mosaic = highest-conservation E2 windows combined with IEDB-validated T-cell epitopes via GGGGS linkers. <i>~1–2 days.</i> Expected: four sequences in <span class="mono">designs/</span>, each with a one-paragraph rationale.</li>
  <li><b>Step 6: Score the designs.</b> Apply the 100-point scorecard (table below) to each design; produce a ranked table with caveats per category. <i>~1 day.</i> Expected: consensus and mosaic score above the natural baseline on coverage; complex designs pay a developability tax that may or may not be justified.</li>
  <li><b>Step 7: Export the top construct.</b> Write protein FASTA, deterministic codon-optimized DNA FASTA, GenBank-style annotation, and a construct map (T7 promoter placeholder → 5′UTR placeholder → Kozak → signal peptide placeholder → antigen ORF → optional T-cell cassette → stop → 3′UTR placeholder → polyA placeholder). Antigen-only — no replication genes. <i>~1 day.</i></li>
  <li><b>Step 8: Write the results.</b> Final-page sections, figures, and a transparent limitations paragraph. <i>~1–2 days.</i></li>
</ol>

<h4>Scorecard (transparent, 100 pts)</h4>
<table>
  <thead><tr><th>Category</th><th>Weight</th><th>Evidence</th></tr></thead>
  <tbody>
    <tr><td>Genotype coverage</td><td class="num">25</td><td>Similarity / conservation against the genotype panel</td></tr>
    <tr><td>Epitope conservation</td><td class="num">20</td><td>Conservation of selected immune regions across panel</td></tr>
    <tr><td>HLA population coverage</td><td class="num">15</td><td>IEDB population coverage where HLA data exists</td></tr>
    <tr><td>Developability</td><td class="num">15</td><td>Length, hydrophobic runs, Cys count, N-X-S/T motifs, repeats</td></tr>
    <tr><td>mRNA/DNA manufacturability</td><td class="num">15</td><td>GC%, codon usage, restriction sites, repeat flags</td></tr>
    <tr><td>Interpretability</td><td class="num">10</td><td>Can the design be explained clearly and honestly?</td></tr>
  </tbody>
</table>

<h3>Synthetic-biology techniques used in this project</h3>
<div class="tcells">
  <div class="group-h">Pipetting</div>
  <label><span class="check on"></span><span><b>Bioethical Considerations</b> — required; addressed in Section 3</span></label>
  <div class="group-h">DNA Editing</div>
  <label><span class="check on"></span><span>DNA Construct Design</span></label>
  <label><span class="check on"></span><span>Databases (GenBank, NCBI, Ensembl, UCSC)</span></label>
  <div class="group-h">Lab Automation</div>
  <label><span class="check on"></span><span>Designing a Twist Order (annotated, future-work)</span></label>
  <div class="group-h">Protein Design</div>
  <label><span class="check on"></span><span>Protein Design</span></label>
  <label><span class="check on"></span><span>Models and Notebooks</span></label>
  <label><span class="check on"></span><span>Databases</span></label>
</div>

<h4>Two techniques expanded</h4>
<p><b>DNA Construct Design.</b> The top-ranked HCV immunogen is exported as an antigen-only DNA construct: T7 promoter placeholder, 5′UTR placeholder, Kozak start, IL-2-style signal peptide placeholder for secretion if desired, the HCV antigen ORF (E2 alone, consensus E2, E2-ferritin nanoparticle, or focused conserved mosaic), <span class="mono">GGGGS</span> linker(s), stop codon, 3′UTR placeholder, and polyA placeholder. The DNA FASTA is a deterministic codon-optimized back-translation for documentation, scrubbed for common restriction sites and homopolymer runs. The construct is intentionally antigen-only — no NS3/NS5B beyond a peptide cassette, no replication genes — so it cannot be assembled into a replicating HCV system.</p>
<p><b>Databases (GenBank, NCBI, IEDB, LANL).</b> Every sequence used in the workbench traces back to a public accession. The dataset manifest lists NCBI accessions per genotype, the LANL diversity browser is used for orientation only (not for untracked sequence mixing), and IEDB rows are filtered for credible HCV epitope evidence with HLA restrictions where available. This makes the entire pipeline auditable — anyone can re-run the alignment and conservation pass from the manifest alone.</p>

<h3>HTGAA Industry Council associations</h3>
<ul>
  <li><a href="https://twistbioscience.com/">Twist Biosciences</a> — annotation target for the exported DNA construct (Twist-style gene-fragment formatting), even though no order is placed for this project.</li>
  <li><a href="https://www.helixnano.com/">Helix Nano</a> — relevant industry context for mRNA-encoded antigen design.</li>
  <li><a href="https://ginkgobioworks.com/">Ginkgo Bioworks</a> — named in the future-work plan for cloud-lab expression and binding tests if access becomes available.</li>
  <li><a href="https://www.asimov.com/">Asimov (Kernel)</a> — referenced as a possible simulation/optimization tool for next-step development beyond the course.</li>
</ul>

<h2><span class="num">Section 5</span>Results &amp; Quantitative Expectations</h2>

<h3>Validated aspect of this final project</h3>
<p>The validated aspect is the <b>computational diversity-and-conservation map for HCV E2</b> (Aim 1) plus the <b>candidate-design and scorecard pass</b> (Aim 2). This satisfies the HTGAA validation requirements via "designing DNA relevant to your final project" + "developing a model or completing a computational analysis relevant to your project" + "creating and running code to validate an aspect of your final project."</p>

<h4>Detailed validation protocol</h4>
<ol>
  <li>Curate the public E2 panel per Step 1; commit the manifest.</li>
  <li>Align with MAFFT; commit <span class="mono">e2-aligned.fasta</span>.</li>
  <li>Run <span class="mono">scripts/run_basic_workbench.py</span> to produce the conservation table (<span class="mono">e2-conservation.csv</span>), conserved-window table, conservation SVG, and consensus E2 protein FASTA.</li>
  <li>Run <span class="mono">scripts/draft_scorecard.py</span> to apply the six-category scorecard to natural / consensus / E2-ferritin / focused-mosaic designs and emit a results-snippet markdown.</li>
  <li>Run <span class="mono">scripts/export_construct.py --include-kozak</span> to emit the antigen-only construct (protein FASTA + DNA FASTA + annotation TSV + construct map) for the top candidate.</li>
  <li>Manually review every score and caveat before publishing the final-page numbers.</li>
</ol>

<h4>Synthetic-biology techniques used in validation</h4>
<p>Validation uses (i) <b>DNA construct design</b> for the exported antigen architecture, (ii) <b>databases</b> (NCBI Virus, LANL, IEDB) for traceable input data, (iii) <b>protein design</b> via consensus, nanoparticle, and mosaic candidate generation, and (iv) <b>models and notebooks</b> for the conservation pass and scorecard. No wet-lab techniques are used in validation; this is by design and is consistent with the post-pivot scope.</p>

<h4>Data and analysis</h4>
<p>The data presented include: a sequence-manifest summary table (records included / excluded per genotype, with reasons), a per-position E2 conservation plot, a conserved- and variable-window table, a candidate-region table merging E2 windows with traceable IEDB epitope rows, and a head-to-head scorecard comparing natural / consensus / E2-ferritin / focused-mosaic designs. All numbers are populated from the completed workbench run: 47 sequences, 434 alignment columns, mean conservation 87.2%, 398 IEDB assay rows, and final scores of A=45, B=66, C=68, D=89. No biological claims of protection are made; outputs are framed as <i>candidate nominations</i> for future experimental testing.</p>

<div class="callout">
<b>Design D note:</b> At 89/100, Design D scores highest on the rubric. It is a 97-residue peptide mosaic and is retained as an active candidate for future epitope-cassette or VLP-scaffold platforms; the rationale for selecting Design C as the primary nominee is detailed in Aim 2.
</div>

<h3>Challenges and limitations</h3>
<p>The dataset is intentionally small and may not capture all global HCV diversity, especially genotypes 4–7. Conservation, HLA population coverage, and developability flags are computational proxies — they are not proof of immunogenicity or protection. Consensus sequences can score well on alignment metrics while still folding poorly, so any consensus design needs structural plausibility checks (AlphaFold/ColabFold) as the next development step. T-cell cassettes can add breadth but also add construct complexity, and not every IEDB row carries HLA restriction information, which weakens the population-coverage estimate. The mitigation is to keep the scorecard transparent, to document every assumption, and to frame outputs as <i>candidate nominations</i>, not validated vaccines.</p>

<h2><span class="num">Section 6</span>Additional Information</h2>

<h3>References</h3>
<ul>
  <li>Bailey JR, Barnes E, Cox AL. <a href="https://doi.org/10.1053/j.gastro.2019.03.032"><i>Approaches, progress, and challenges to hepatitis C vaccine development.</i></a> Gastroenterology, 2019. <a href="https://doi.org/10.1053/j.gastro.2019.03.032">doi: 10.1053/j.gastro.2019.03.032</a>.</li>
  <li>Keck ZY, Pierce BG, Lau P, Lu J, Wang Y, Underwood A, Bull RA, Prentoe J, Velazquez-Moctezuma R, Walker MR, Luciani F, Guest JD, Fauvelle C, Baumert TF, Bukh J, Lloyd AR, Foung SKH. Broadly neutralizing antibodies from an individual that naturally cleared multiple hepatitis C virus infections uncover molecular determinants for E2 targeting and vaccine design. PLoS Pathog. 2019 May 17;15(5):e1007772. <a href="https://doi.org/10.1371/journal.ppat.1007772">doi: 10.1371/journal.ppat.1007772</a>. PMID: 31100098.</li>
  <li>Fauvelle C, Colpitts CC, Keck ZY, Pierce BG, Foung SK, Baumert TF. Hepatitis C virus vaccine candidates inducing protective neutralizing antibodies. Expert Rev Vaccines. 2016 Dec;15(12):1535-1544. <a href="https://doi.org/10.1080/14760584.2016.1194759">doi: 10.1080/14760584.2016.1194759</a>. Epub 2016 Jun 13. PMID: 27267297.</li>
  <li>Kanekiyo M, Wei CJ, Yassine HM, McTamney PM, Boyington JC, Whittle JR, Rao SS, Kong WP, Wang L, Nason MC, et al. Self-assembling influenza nanoparticle vaccines elicit broadly neutralizing H1N1 antibodies. Nature. 2013;499(7456):102–6. <a href="https://doi.org/10.1038/nature12265">doi: 10.1038/nature12265</a>.</li>
  <li>WHO. <i>Hepatitis C — Fact sheet.</i> 25 July 2025. <a href="https://www.who.int/news-room/fact-sheets/detail/hepatitis-c">who.int/.../hepatitis-c</a>.</li>
  <li>NCBI Virus. <a href="https://www.ncbi.nlm.nih.gov/labs/virus/">ncbi.nlm.nih.gov/labs/virus</a>.</li>
  <li>LANL HCV Database. <a href="https://hcv.lanl.gov/">hcv.lanl.gov</a>.</li>
  <li>IEDB and IEDB Analysis Tools. <a href="https://www.iedb.org/">iedb.org</a> · <a href="https://tools.iedb.org/main/analysis-tools/">tools.iedb.org</a>.</li>
  <li>ExPASy ProtParam. <a href="https://web.expasy.org/protparam/">web.expasy.org/protparam</a>.</li>
</ul>

<h3>Supply list and budget</h3>
<p>This is a computational project. There are no consumables, reagents, or DNA orders for the in-class scope.</p>
<ul>
  <li>Compute: personal laptop (no GPU required).</li>
  <li>Software: MAFFT or Clustal Omega (free), Python 3 + NumPy/Pandas/Biopython (free), local workbench scripts (this repo).</li>
  <li>Public data: NCBI Virus, LANL HCV, IEDB, ProtParam — all free.</li>
  <li><b>Estimated cash budget for the in-class project:</b> <span class="mono">$0</span>.</li>
  <li>Future-work cost (not in scope): if a Twist gene fragment is later ordered for cloud-lab validation, ~<span class="mono">$200–$400</span> for a single ~2 kb antigen fragment; cloud-lab expression run via Ginkgo would be additional and quoted separately.</li>
</ul>


</div></div>
