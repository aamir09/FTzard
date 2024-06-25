from dagster import Definitions

from ftzard.pipeline.pipeline import all_jobs


defs = Definitions(
    # resources = dagster_pipeline.asset_resource_defs,
    jobs = all_jobs,
    # sensors = [dagster_pipeline.do_inference_from_featurestore_sensor,
    #            dagster_pipeline.new_data_sensor, dagster_pipeline.new_training_sensor,
    #            dagster_pipeline.train_on_new_data_sensor]
)