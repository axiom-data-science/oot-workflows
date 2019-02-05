# Sample workflows for OoT

## Getting Started

1.  Copy `.env.template` to `.env`
2.  `source .env`
3.  `docker network create oot`


### Get some NCOM data

```bash
noglob scp axiom@sthelens.axiomptk:/mnt/store/data/packrat/ncom/socal/processed/2017/2017_01/socal_2017-01-0[1-9].nc ./data/ncom_socal
```

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
