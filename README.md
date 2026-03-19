# Intactness Pipeline

## Part 1: For coders (Miniforge / Conda)

Quick start
- Update the email in `default.cfg`
- Create env: `conda env create -f environment.yml`
- Activate: `conda activate intactness`
- Run (default input `data/seqs.fasta`): `python -m intactness`
- Run with custom input: `python -m intactness --input data/yourfile.fasta`
- Plasmidsaurus run: `python -m intactness --plasmid --input data/yourfile.fasta`

Inputs
- Unaligned FASTA contigs
- Headers should be unique and contain no spaces

Outputs
- Default output folder: `data/seqs_inputfilename`
- With `--input data/foo.fasta`, output folder: `data/seqs_foo`

Key behavior
- MUSCLE alignment is skipped if the alignment file already exists at `MSA:file_aln`
- GeneCutter is skipped if `summary_psc.tsv` already exists in the output folder

External dependencies
- GeneCutter requires internet access

Notes
- Thresholds and cutoffs are defined in `default.cfg`


## Part 2: RUN THE APP

This section is for users who do not use Python/Conda.
You only need Docker Desktop and a Terminal.

Before you start
1. Install Docker Desktop
2. Open Docker Desktop and wait until it says it is running.
3. Clone the repo so the top-level project still contains:
  - `database/`
  - `intactness/`
  - The `data/` folder will be created automatically on first run if it does not already exist. This folder is for input FASTA and outputs

### Start the app

#### macOS or Linux
1. Open Terminal and from the `intactness` folder:

```bash
chmod +x run_app.sh
./run_app.sh
```


#### Windows
From the `intactness` folder:

```bat
run_app.bat
```

The app opens automatically in your browser.

### Use the app
1. Enter your email address
2. Upload a FASTA file
3. Select `Yes` or `No`
4. Click `Run pipeline`
5. Output files are created in `data/seqs_<inputname>`.
6. Can also download the results ZIP when finished


### Stop the app
From the `intactness` folder:

```bash
docker compose -f docker-compose.app.yml down
```

How to know it worked
- Terminal ends with: `Pipeline finished. Good bye!`

OPTIONAL STEP for debugging
If MUSCLE fails
1. Stop the run and open Docker Desktop.
2. Go to `Settings` -> `Resources`.
3. Increase `Memory` to `16 GB` (minimum `12 GB`), then click `Apply & Restart`.
4. Run the same command again.
5. If it still fails, use a smaller input FASTA file (split into smaller files).
