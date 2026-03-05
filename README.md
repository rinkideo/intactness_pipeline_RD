# Intactness Pipeline

## Part 1: For coders (Miniforge / Conda)

Quick start
- Create env: `conda env create -f environment.yml`
- Activate: `conda activate intactness`
- Run (default input `data/seqs.fasta`): `python -m intactness`
- Run with custom input: `python -m intactness --input data/yourfile.fasta`
- Plasmidsaurus run: `python -m intactness --plasmid --input data/yourfile.fasta`

## Part 2: For non-coders (Docker)

This section is for users who do not use Python/Conda.
You only need Docker Desktop and a Terminal.

Before you start
- Keep your folders like this:
  - `intactness_pipeline_RD/data` (input FASTA and outputs)
  - `intactness_pipeline_RD/database` (reference files)
  - `intactness_pipeline_RD/intactness` (pipeline scripts)

1. Open Docker Desktop and wait until it says it is running.
2. Open Terminal.
3. Go to the project root folder:
   - `cd "/path/to/intactness_pipeline_RD"`
4. Put your FASTA file inside `data/`.
5. Run one of these commands:

- Default input (`data/seqs.fasta`):
  - `docker run --rm -v "$PWD/data:/work/data" -v "$PWD/database:/work/database" intactness:latest`

- Custom input:
  - `docker run --rm -v "$PWD/data:/work/data" -v "$PWD/database:/work/database" intactness:latest --input data/yourfile.fasta`

- Plasmidsaurus mode:
  - `docker run --rm -v "$PWD/data:/work/data" -v "$PWD/database:/work/database" intactness:latest --plasmid --input data/yourfile.fasta`

How to know it worked
- Terminal ends with: `Pipeline finished. Good bye!`
- Output files are created in `data/seqs` or `data/seqs_<inputname>`.

Inputs
- Unaligned FASTA contigs
- Headers should be unique and contain no spaces

Outputs
- Default output folder: `data/seqs`
- With `--input data/foo.fasta`, output folder: `data/seqs_foo`

Key behavior
- MUSCLE alignment is skipped if the alignment file already exists at `MSA:file_aln`
- GeneCutter is skipped if `summary_psc.tsv` already exists in the output folder

External dependencies
- GeneCutter requires internet access
