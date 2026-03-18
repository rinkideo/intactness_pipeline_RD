from __future__ import annotations

import io
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = REPO_ROOT.parent
DATABASE_DIR = PROJECT_ROOT / "database"
DATA_DIR = PROJECT_ROOT / "data"


st.markdown(
    """
    <style>
    div.stButton > button[kind="primary"]:disabled {
        background-color: #b9cdef;
        border: 1px solid #b9cdef;
        color: #f7f9fc;
        cursor: not-allowed;
    }
    div.stButton > button[kind="primary"] {
        background-color: #1f5fbf;
        border: 1px solid #1f5fbf;
        color: #ffffff;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #184d9a;
        border-color: #184d9a;
        color: #ffffff;
    }
    div.stButton > button[kind="primary"]:focus {
        box-shadow: 0 0 0 0.2rem rgba(31, 95, 191, 0.25);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def sanitize_filename(filename: str) -> str:
    cleaned = Path(filename).name
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "_", cleaned)
    if not cleaned.lower().endswith((".fa", ".fasta", ".fna")):
        cleaned += ".fasta"
    return cleaned


def expected_output_dir(input_name: str) -> str:
    return f"seqs_{Path(input_name).stem}"


def make_job_zip(output_dir: Path) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in output_dir.rglob("*"):
            if path.is_file():
                zf.write(path, arcname=path.relative_to(output_dir.parent))
    return buffer.getvalue()


def prepare_job(uploaded_file) -> dict:
    if not DATABASE_DIR.exists():
        raise RuntimeError(f"Expected reference database directory was not found: {DATABASE_DIR}")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    input_name = sanitize_filename(uploaded_file.name or "uploaded_sequences.fasta")
    input_path = DATA_DIR / input_name
    input_path.write_bytes(uploaded_file.getvalue())

    output_name = expected_output_dir(input_name)
    output_dir = DATA_DIR / output_name

    return {
        "input_name": input_name,
        "output_name": output_name,
        "output_dir": output_dir,
        "input_path": input_path,
    }


def run_pipeline(job: dict, plasmid: bool, log_placeholder, status_placeholder) -> dict:
    cmd = [
        sys.executable,
        "-m",
        "intactness",
        "--input",
        f"data/{job['input_name']}",
    ]
    if plasmid:
        cmd.insert(3, "--plasmid")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT.parent)

    process = subprocess.Popen(
        cmd,
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
        bufsize=1,
    )

    log_lines = []
    if process.stdout is None:
        raise RuntimeError("Pipeline process did not expose a readable stdout stream.")

    for line in process.stdout:
        log_lines.append(line.rstrip())
        log_placeholder.text_area(
            "Pipeline logs",
            value="\n".join(log_lines),
            height=320,
        )
        if job["output_dir"].exists():
            status_placeholder.success("Output directory created. Pipeline is running.")
        else:
            status_placeholder.info("Pipeline started. Waiting for output files.")

    return_code = process.wait()
    combined_log = "\n".join(log_lines).strip()

    if return_code != 0:
        raise RuntimeError(
            "Pipeline run failed.\n\n"
            f"Command: {' '.join(cmd)}\n\n"
            f"Logs:\n{combined_log or '(no output)'}"
        )

    if not job["output_dir"].exists():
        raise RuntimeError(
            f"Pipeline finished but expected output folder was not found: {job['output_dir']}"
        )

    return {
        "job_id": job["input_name"],
        "output_dir": str(job["output_dir"]),
        "zip_bytes": make_job_zip(job["output_dir"]),
        "zip_name": f"{job['output_name']}.zip",
        "log_text": combined_log or "Pipeline completed without console output.",
    }


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


st.set_page_config(page_title="Intactness Pipeline", layout="wide")

st.title("Intactness Pipeline")
st.caption("Local run mode. Uses the standard project `data/` folder and existing intermediate files when available.")

control_col, status_col = st.columns([1.1, 0.9])

with control_col:
    uploaded_file = st.file_uploader(
        "FASTA input",
        type=["fa", "fasta", "fna"],
        help="Headers should be unique and contain no spaces.",
    )

with status_col:
    st.warning("Select Yes or No")
    plasmid_choice = st.radio(
        "Are these Plasmidsaurus sequences",
        options=["Yes", "No"],
        index=None,
    )

if "last_run" not in st.session_state:
    st.session_state.last_run = None

run_disabled = uploaded_file is None or plasmid_choice is None

if st.button("Run pipeline", type="primary", disabled=run_disabled):
    try:
        job = prepare_job(uploaded_file)
        st.success(f"Running `{job['input_name']}`")
        path_col1, path_col2 = st.columns(2)
        path_col1.text_input(
            "Input file",
            value=display_path(job["input_path"]),
            disabled=True,
            key="active_input_file",
        )
        path_col2.text_input(
            "Output directory",
            value=display_path(job["output_dir"]),
            disabled=True,
            key="active_output_directory",
        )

        live_col, status_col = st.columns([1.4, 1])
        log_placeholder = st.empty()
        status_placeholder = st.empty()
        with live_col:
            log_placeholder.text_area(
                "Run log",
                value="Starting pipeline...",
                height=360,
                key="active_run_log",
            )
        with status_col:
            status_placeholder.info("Pipeline started. Results will be available when the run completes.")

        with st.spinner("Running pipeline. This can take a while because GeneCutter is remote."):
            st.session_state.last_run = run_pipeline(
                job,
                plasmid_choice == "Yes",
                log_placeholder,
                status_placeholder,
            )
    except Exception as exc:  # noqa: BLE001
        st.session_state.last_run = None
        st.error(str(exc))

last_run = st.session_state.last_run
if last_run:
    st.success("Pipeline completed.")
    result_col, output_col = st.columns([0.8, 1.2])
    with result_col:
        st.download_button(
            "Download results ZIP",
            data=last_run["zip_bytes"],
            file_name=last_run["zip_name"],
            mime="application/zip",
        )
    with output_col:
        st.text_input(
            "Output directory",
            value=display_path(Path(last_run["output_dir"])),
            disabled=True,
            key="final_output_directory",
        )
    st.text_area(
        "Final log",
        value=last_run["log_text"],
        height=260,
        key="final_run_log",
    )
