# Sample workflows for OoT

## Getting Started

1.  Copy `.env.template` to `.env`
2.  `source .env`
3.  `docker network create oot`


#### Get some NCOM data

```bash
noglob scp axiom@sthelens.axiomptk:/mnt/store/data/packrat/ncom/socal/processed/2017/2017_01/socal_2017-01-0[1-9].nc ./data/ncom_socal
```

#### Kafka

```bash
docker-compose up -d kafka-int
```

#### Jupyter Lab

```bash
docker build -t oot-pyenv ./python-env
docker-compose up -d jupyterlab
```

### Particle Run Listener

```bash
docker build -t oot-pyenv ./python-env
docker-compose up particle-release-listener
```
