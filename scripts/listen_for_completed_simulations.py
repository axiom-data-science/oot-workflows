from pathlib import Path

from easyavro import EasyAvroConsumer
from parcels import plotTrajectoriesFile

import matplotlib.pyplot as plt

import logging

L = logging.getLogger()
L.addHandler(logging.StreamHandler())
L.setLevel(logging.INFO)

ea = logging.getLogger('easyavro')
ea.addHandler(logging.StreamHandler())
ea.setLevel(logging.INFO)


def plot_parcles_run(k, v):
    """k,v from Kafka message"""

    L.info(f'Received Input: {v}')

    L.info(f"Plotting results from: {v['filepath']}")

    plotpath = Path(__file__).parent.parent / 'plots'
    filename = v['id'] + '.png'
    plotfile = str(plotpath / filename) 

    plotTrajectoriesFile(v['filepath'], mode='2d', show_plt=False)
    f = plt.gcf()
    f.savefig(plotfile)

    L.info(f'Saved plot to: {plotfile}')


if __name__ == '__main__':

    kafka_base = 'kafka-int'
    c = EasyAvroConsumer(
        schema_registry_url=f'http://{kafka_base}:7002',
        kafka_brokers=[f'{kafka_base}:7001'],
        consumer_group='listen-for-tracks',
        kafka_topic='mil-darpa-oot-particle-completed'
    )
    c.consume(on_recieve=plot_parcles_run)
