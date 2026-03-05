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

First-time setup (required for first run only)
  Build image locally:
   - `cd intactness`
   - `docker build -t intactness:latest .`
   - `cd ..`


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

If MUSCLE fails
1. Stop the run and open Docker Desktop.
2. Go to `Settings` -> `Resources`.
3. Increase `Memory` to `16 GB` (minimum `12 GB`), then click `Apply & Restart`.
4. Run the same command again.
5. If it still fails, use a smaller input FASTA file (split into smaller files).
