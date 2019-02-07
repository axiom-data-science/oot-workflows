FROM continuumio/miniconda3

RUN conda config \
        --set always_yes yes \
        --set changeps1 no \
        --set show_channel_urls True \
        && \
    conda config \
        --add channels axiom-data-science \
        --add channels conda-forge \
        && \
    conda update -n base conda

COPY requirements.txt /tmp/
RUN conda install --yes --file /tmp/requirements.txt && \
    conda clean -tipsy

COPY . /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["app.py"]
