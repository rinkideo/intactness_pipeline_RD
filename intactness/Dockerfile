FROM mambaorg/micromamba:2.3.2

# Install all pipeline dependencies into a dedicated conda env.
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.docker.yml /tmp/environment.yml
RUN micromamba create -y -n intactness -f /tmp/environment.yml && \
    micromamba clean --all --yes

# Copy pipeline source as a Python package directory.
COPY --chown=$MAMBA_USER:$MAMBA_USER . /opt/intactness

# Run from /work so users can mount input/output data there.
WORKDIR /work
ENV PYTHONPATH=/opt

# Usage examples:
# docker run --rm -v "$PWD/data:/work/data" intactness:latest
# docker run --rm -v "$PWD/data:/work/data" intactness:latest --input data/yourfile.fasta
ENTRYPOINT ["micromamba", "run", "-n", "intactness", "python", "-m", "intactness"]
