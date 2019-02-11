# Sample workflows for OoT

This repo contains notebooks and scripts to prepare, run, and visualize drifter simulations.

## Getting Started

1.  Copy `.env.template` to `.env`
2.  `source .env`
3.  `docker network create oot`


### Get some NCOM data

The data is available in the `drifter_demo_data` directory on the Axiom FTP site when you log in via the `leidos_oot` account.

### Kafka

```bash
docker-compose up -d kafka-int
```

### Jupyter Lab

```bash
docker build -t oot-pyenv ./python-env
docker-compose up -d jupyterlab
```

### Particle Run Listener

```bash
docker build -t oot-pyenv ./python-env
docker-compose up particle-release-listener
```

### Developing outside of Docker

```bash
conda create -n oot-workflows python=3.7
conda install -c conda-forge -c axiom-data-science --file python-env/requirements.txt

docker-compose up -d kafka-ext  # All `kafka-int` references need to change to `localhost`
jupyter lab
python scripts/listen_for_tracks.py
```

## Jupyter Notebook descriptions
1. 001_Manual_Run.ipynb - Demo of drifters contained completely within a Jupyter Notebook.
2. 002_Start_Run.ipynb - Notebook that prepares and initiates a drifter simulation via Kakfa message.
3. 003_View_Run.ipynb - Notebook to review results from drifter simulation started in 002_Start_Run.ipynb
4. Alguhas.ipynb - Example notebook from Parcels library
5. Parcles.ipynb - Example notebook from Parcels library
