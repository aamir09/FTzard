from dagster import Definitions

from ftzard.pipeline.pipeline import all_jobs, all_sensors


defs = Definitions(
    jobs = all_jobs,
    sensors = all_sensors
)