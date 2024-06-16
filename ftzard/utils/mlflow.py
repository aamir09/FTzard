import mlflow as mf 
import os
from typing import List


def get_mlflow_client()->mf.MlflowClient:
    tracking_uri = os.environ.get('MLFLOW_TRACKING_URI')
    if not tracking_uri:
        raise EnvironmentError("""No environment variable named `MLFLOW_TRACKING_URI` found, please assign the mlflow tracking value
                               to the environment variable""")
    return mf.MlflowClient(tracking_uri=tracking_uri)
    
def is_run_exists(run_id:str)->bool:
    client = get_mlflow_client()
    return True if client.get_run(run_id=run_id) else False

def create_experiment(exp_name:str)->str:
    client = get_mlflow_client()
    experiment = client.get_experiment_by_name(name=exp_name)
    if experiment:
        print("""The provided experiment name {experiment_name} already exists, the run will be logged in this experiment.
                                 """.format(experiment_name=exp_name))
        return experiment.experiment_id
    return client.create_experiment(name=exp_name)

def get_run_id_by_name(run_name:str, experiment_ids:List[str], nested:bool=False)->str:
    client = get_mlflow_client()
    run = mf.search_runs(experiment_ids=experiment_ids,
                       filter_string=f"run_name='{run_name}'", output_format='list')
    if run:
        return run[0].info.run_id
    else:
        if experiment_ids:
            run = mf.start_run(run_name=run_name, experiment_id=experiment_ids[0],
                              nested=nested)
            mf.end_run()
            return run.info.run_id
    return None

    
    