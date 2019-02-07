from pathlib import Path
from datetime import datetime, timedelta

import cftime
import pandas as pd
import xarray as xr
from easyavro import EasyAvroConsumer
from parcels import (
    AdvectionRK4,
    FieldSet,
    JITParticle,
    ParticleSet,
)

import logging

L = logging.getLogger()
L.addHandler(logging.StreamHandler())
L.setLevel(logging.INFO)

ea = logging.getLogger('easyavro')
ea.addHandler(logging.StreamHandler())
ea.setLevel(logging.INFO)


def parcels_particle_run(k, v):

    L.info(f'Received Input: {v}')

    L.info("Loading vectors from model...")
    datapath = Path(__file__).parent.parent / 'data'

    with xr.open_mfdataset(str(datapath / 'ncom_socal' / 'socal_2017-01-0[1-9].nc'), decode_cf=False) as undecoded:
        time_units = undecoded.time.units
        time_calendar = undecoded.time.calendar

    with xr.open_mfdataset(str(datapath / 'ncom_socal' / 'socal_2017-01-0[1-9].nc')) as ds:
        uv = ds[['water_u', 'water_v']]
        uv = uv.isel(depth=0)

        variables = {
            'U': 'water_u',
            'V': 'water_v'
        }

        dimensions = {
            'lat': 'lat',
            'lon': 'lon',
            'time': 'time'
        }

        xr_fieldset = FieldSet.from_xarray_dataset(
            uv,
            variables,
            dimensions,
            allow_time_extrapolation=True
        )
        L.info("Created Fieldset")

    expanded_rows = []
    df = pd.DataFrame.from_records(v['records'])
    for ix, row in df.iterrows():
        expanded_rows.append(pd.concat([row] * int(row.nparticles), ignore_index=True, axis=1).T)
    expanded_df = pd.concat(expanded_rows, axis=0).reset_index()
    expanded_df = expanded_df.drop(columns=['index', 'nparticles'])
    L.info(f"Expanced and Loaded {len(expanded_df)} Particles!")

    L.info("Converting particle release time to the model base unit...")
    expanded_df.time = cftime.date2num(
        pd.DatetimeIndex(expanded_df.time).to_pydatetime(),
        units=time_units,
        calendar=time_calendar
    )

    csv_pset = ParticleSet.from_list(
        fieldset=xr_fieldset,
        pclass=JITParticle,
        lon=expanded_df.lon,
        lat=expanded_df.lat,
        time=expanded_df.time.values
    )
    L.info("Created ParticleSet")

    runlength = timedelta(days=6)
    timestep = timedelta(minutes=5)
    rigthnow = datetime.utcnow()
    output_file = datapath / 'particle_runs' / f'{v["id"]}_{rigthnow:%Y%m%dT%H%M%S.%f}.nc'
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output = csv_pset.ParticleFile(name=str(output_file), outputdt=timedelta(hours=3))

    L.info("Running...")
    csv_pset.execute(
        AdvectionRK4,
        runtime=runlength,
        dt=timestep,
        output_file=output
    )
    L.info(f'Complete! Saved output: {output_file}')


if __name__ == '__main__':

    kafka_base = 'kafka-int'
    c = EasyAvroConsumer(
        schema_registry_url=f'http://{kafka_base}:7002',
        kafka_brokers=[f'{kafka_base}:7001'],
        consumer_group='listen-for-tracks',
        kafka_topic='mil-darpa-oot-particle-releases'
    )
    c.consume(on_recieve=parcels_particle_run)
