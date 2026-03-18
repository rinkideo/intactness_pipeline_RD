ARG BASE_IMAGE=intactness:latest
FROM ${BASE_IMAGE}

RUN micromamba run -n intactness pip install --no-cache-dir "streamlit>=1.33,<2"
COPY --chown=$MAMBA_USER:$MAMBA_USER intactness /opt/intactness

ENTRYPOINT []
WORKDIR /work
ENV PYTHONPATH=/opt
EXPOSE 8501

CMD ["micromamba", "run", "-n", "intactness", "streamlit", "run", "/opt/intactness/streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
