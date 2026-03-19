This repository is a modified derivative of the upstream intactness pipeline (https://github.com/BWH-Lichterfeld-Lab/Intactness-Pipeline, MIT License).

## v0.1.0 (based on upstream v0.0.1, 2020)
Forked from upstream release v0.0.1

## v0.1.1
- Updated pipeline run behavior and CLI flow.
- Added support for custom input file names (`--input`).
- Added Plasmidsaurus mode (`--plasmid`) to force primer handling.
- Added Docker support for non-coder usage.
- Added Docker-specific environment file for container builds (`environment.docker.yml`).
- Added a Streamlit-based app for running the intactness pipeline through a browser interface.
- Added Docker-based app launchers for macOS/Linux (`run_app.sh`) and Windows (`run_app.bat`).
- Added a containerized app workflow so users can pull a centralized Docker image and run the app locally without setting up Conda.
- Added the app workflow to open automatically in the browser and write inputs/outputs through the repository `data/` folder.
- Added an email address field to the app UI so app users no longer need to edit `default.cfg`.
- Added Docker run guide (`README.md`).


## Fixed
- Improved duplicate FASTA header validation with a clear error message listing duplicated sequence names.
- Fixed containerized output path issues for alignment view PDFs and 5' deletion summary output.
- Updated app Docker packaging to use the current pipeline code inside the container.
