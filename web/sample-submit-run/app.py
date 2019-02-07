import json
from io import StringIO

import pandas as pd
from avro import schema
from easyavro import EasyAvroProducer
from flask import Flask, render_template, request
from confluent_kafka.avro import CachedSchemaRegistryClient

app = Flask(__name__, template_folder='.')
kafka_base = 'kafka-int'


def process_csv(csv):

    schema_dict = {
        "name": "mil.darpa.oot.particles.releases",
        "type": "record",
        "doc": "A particle release",
        "fields": [
            { "name": "id", "type": "string", "doc": "Unique particle release identifier"},
            {
                "name": "records",
                "type": {
                    "type": "array",
                    "items": {
                        "type": "record",
                        "name": "release",
                        "fields": [
                            {"name": "time",       "type": "string",   "doc": "ISO8601 Date String"},
                            {"name": "lat",        "type": "double",   "doc": "wgs84 latitude"},
                            {"name": "lon",        "type": "double",   "doc": "wgs84 longitude"},
                            {"name": "nparticles", "type": "int",      "doc": "Number of particles released"}
                        ]
                    }
                }
            }
        ]
    }

    subject = 'mil-darpa-oot-particle-releases-value'
    client = CachedSchemaRegistryClient(url=f'http://{kafka_base}:7002')
    client.update_compatibility('NONE', subject=subject)

    avro_schema = schema.Parse(json.dumps(schema_dict))
    client.register(subject, avro_schema)

    df = pd.read_csv(
        StringIO(csv),
        header=None,
        names=['time', 'lat', 'lon', 'nparticles'],
        parse_dates=[0],
        infer_datetime_format=True
    )
    records_to_send = []
    for i, x in df.iterrows():
        x.time = x.time.isoformat()
        records_to_send.append(x.to_dict())

    if not records_to_send:
        raise ValueError("No particles to run")

    to_send = [(
        None,
        {
            'id': 'website-run',
            'records': records_to_send
        }
    )]

    p = EasyAvroProducer(
        schema_registry_url=f'http://{kafka_base}:7002',
        kafka_brokers=[f'{kafka_base}:7001'],
        kafka_topic='mil-darpa-oot-particle-releases',
        key_schema='nokey'
    )
    p.produce(to_send)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            process_csv(request.form.get('particlecsv'))
            message = "Run Submitted"
        except BaseException as e:
            message = str(e)
        return render_template('index.html', message=message)

    return render_template('index.html', message='')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889, debug=True)
