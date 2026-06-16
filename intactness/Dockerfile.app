# Self-contained app image for the Intactness pipeline (Streamlit UI).
# Build context: the repository root (so both intactness/ and its env file are visible).
#
# Multi-arch build + publish:
#   docker buildx build --platform linux/amd64,linux/arm64 \
#     -f intactness/Dockerfile.app \
#     -t ghcr.io/rinkideo/intactness-app:latest --push .
#
# (See intactness/build_and_push.sh for the wrapped version.)
FROM mambaorg/micromamba:2.3.2

# Install all pipeline dependencies into a dedicated conda env.
COPY --chown=$MAMBA_USER:$MAMBA_USER intactness/environment.docker.yml /tmp/environment.yml
RUN micromamba create -y -n intactness -f /tmp/environment.yml && \
    micromamba clean --all --yes

# Streamlit powers the web app and is kept out of the conda env file.
RUN micromamba run -n intactness pip install --no-cache-dir "streamlit>=1.33,<2"

# Copy pipeline source as a Python package directory (import path: intactness).
COPY --chown=$MAMBA_USER:$MAMBA_USER intactness /opt/intactness

# Reference database/ and data/ are mounted at runtime (see docker-compose.app.yml),
# so they are intentionally not baked into the image.
ENTRYPOINT []
WORKDIR /work
ENV PYTHONPATH=/opt
EXPOSE 8501

CMD ["micromamba", "run", "-n", "intactness", "streamlit", "run", \
     "/opt/intactness/streamlit_app.py", \
     "--server.address=0.0.0.0", "--server.port=8501"]
