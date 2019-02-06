FROM jupyter/tensorflow-notebook:latest

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
    conda remove --quiet --yes --force qt pyqt && \
    conda clean -tipsy && \
    # Activate ipywidgets extension in the environment that runs the notebook server
    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    # Also activate ipywidgets extension for JupyterLab
    # Check this URL for most recent compatibilities
    # https://github.com/jupyter-widgets/ipywidgets/tree/master/packages/jupyterlab-manager
    jupyter labextension install @jupyter-widgets/jupyterlab-manager@^0.38.1 && \
    jupyter labextension install jupyterlab_bokeh@0.6.3 && \
    jupyter labextension install @pyviz/jupyterlab_pyviz  && \
    npm cache clean --force && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    rm -rf /home/$NB_USER/.node-gyp && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

ENV XDG_CACHE_HOME /home/$NB_USER/.cache/

# Install facets which does not have a pip or conda package at the moment
RUN cd /tmp && \
    git clone https://github.com/PAIR-code/facets.git && \
    cd facets && \
    jupyter nbextension install facets-dist/ --sys-prefix && \
    cd && \
    rm -rf /tmp/facets && \
    # Import matplotlib the first time to build the font cache.
    MPLBACKEND=Agg python -c "import matplotlib.pyplot" && \
    # Load parcels examples
    parcels_get_examples parcels_examples && \
    # Fix perms again
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

USER $NB_UID

CMD ["python", "--version"]
