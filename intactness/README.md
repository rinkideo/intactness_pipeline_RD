Intactness Pipeline (Miniforge)

Quick start
- Create env: conda env create -f environment.yml
- Activate: conda activate intactness
- Run (default input data/seqs.fasta): python -m intactness
- Run with custom input: python -m intactness --input data/yourfile.fasta
- Plasmidsaurus run (force primer=Yes): python -m intactness --plasmid --input data/yourfile.fasta

Inputs
- Unaligned FASTA contigs
- Headers should be unique and contain no spaces

Outputs
- Default output folder: data/seqs
- With --input data/foo.fasta, output folder: data/seqs_foo

Key behavior
- MUSCLE alignment is skipped if the alignment file already exists at MSA:file_aln
- GeneCutter is skipped if summary_psc.tsv already exists in the output folder

External dependencies
- blastn must be available on PATH (provided by conda env)
- MUSCLE binary should be available on PATH (muscle)
- GeneCutter requires internet access

Notes
- Thresholds and cutoffs are defined in default.cfg

Docker (easy run for non-coders)
- Build image (from this folder):
  `docker build -t intactness:latest .`
- Prepare input:
  put FASTA files in a local `data/` folder (for default run use `data/seqs.fasta`)
- Run with default input (`data/seqs.fasta`):
  - macOS/Linux: `docker run --rm -v "$PWD/data:/work/data" intactness:latest`
  - Windows PowerShell: `docker run --rm -v "${PWD}/data:/work/data" intactness:latest`
- Run with a custom FASTA:
  - macOS/Linux: `docker run --rm -v "$PWD/data:/work/data" intactness:latest --input data/yourfile.fasta`
  - Windows PowerShell: `docker run --rm -v "${PWD}/data:/work/data" intactness:latest --input data/yourfile.fasta`
- Plasmidsaurus mode:
  `docker run --rm -v "$PWD/data:/work/data" intactness:latest --plasmid --input data/yourfile.fasta`

Important
- GeneCutter requires internet access from inside Docker.
- Results are written into your mounted local `data/` folder.
