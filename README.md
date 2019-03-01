# Sample workflows for OoT

This repo contains an encasulated set of notebooks and scripts to prepare, run, and visualize drifter simulations that communicate via Kafka messages.

The general workflow is as follows:

1. Prepare the work environment including Kafka, Jupyter Lab, and the required applications in the Getting Stared section.
2. Register the required, example schema in Jupyter Notebook `002_Create_Schema.ipynb`
3. Start a drifter simulations in the Jupter Notebook `003_Start_Kafka_Run.ipynb`
4. View a simple visualization of the drifter results through Jupyter Lab in the directory `/work/plots/`

## Bootstrapping
### Prerequisites
- Docker
- Git

### Download this demo

```bash
git clone https://github.com/axiom-data-science/oot-workflows.git
cd oot-workflows
```

### Download NCOM data

The data is available in the `drifter_demo_data` directory on the Axiom FTP site when you log in via the `leidos_oot` account.  The data should be saved in the `oot-workflows/data/ncom_socal/`.

## Getting Started

1.  Copy `.env.template` to `.env`
2.  `source .env`
3.  `docker network create oot`

### Kafka

Start a containerized Kafka instance.

```bash
docker-compose up -d kafka-int
```

### Jupyter Lab

Start a containerized Jupyter Lab instance.  Jupyter Lab will then be available at `127.0.0.0.1:8888/lab?` in a web browser.

```bash
docker build -t oot-pyenv ./python-env
docker-compose up -d jupyterlab
```

The building of this image can take over 10 mintues.  An alternative is to pull the image from Dockerhub.

```bash
docker pull jesseaxiom/oot-pyenv:latest
docker-compose up -d jupyterlab
```


### Particle Simulation Plotter

Starts a containerized application that listens for completed drifter simulations and creates a simple plot upon receipt of Kafka message.

```bash
docker build -t oot-pyenv ./python-env
docker-compose up particle-release-plotter
```

### Particle Run Listener

Starts a containerized application that listens for particle release times and locations and starts simulation upon receipt of Kafka message.

```bash
docker build -t oot-pyenv ./python-env
docker-compose up particle-release-listener
```

#### Developing outside of Docker (not required)

```bash
conda create -n oot-workflows python=3.7
conda install -c conda-forge -c axiom-data-science --file python-env/requirements.txt

docker-compose up -d kafka-ext  # All `kafka-int` references need to change to `localhost`
jupyter lab
python scripts/listen_for_tracks.py
```


## Examples of Kafka and schemas

### Examples Schemas
- Drifter example: Jupyter Notebook `002_Create_Schema.ipynb`
- Simple trigger example: Jupyter Notebook `002_Create_Schema.ipynb`

### Examples of Kafka Producer (send message)
- Send drifter locations to perform particle tracking simulation: Jupyter Notebook `003_Start_Kafka_Run.ipynb`
- Send trigger to of completed simulation to create plot: Python script `scripts/listen_for_completed_simulations.py"

### Example of Kafka Consumer (read message)
- Listen for drifter locations: Python script `scripts/listen_for_tracks.py`
- Listen for completed simulations: Python script `scripts/listen_for_completed_simulations.py`





## Jupyter Notebook descriptions
1. 001\_Manual\_Run.ipynb - Demo of drifters contained completely within a Jupyter Notebook.
2. 002\_Create\_Schema.ipynb - Create AVRO schema for drifter simulation inputs.
3. 003\_Start\_Kafka\_Run.ipynb - Reads a csv file with definition of drifter release locations and times, then parses the release locations into a message that is produced.
4. 004\_View\_Run.ipynb - Manually examples of visualization from the drifter simulation. 
4. Alguhas.ipynb - Example notebook from Parcels library
5. Parcles.ipynb - Example notebook from Parcels library
