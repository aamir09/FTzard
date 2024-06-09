import mlflow as mf 
import os


def get_mlflow_client()->mf.MlflowClient:
    tracking_uri = os.environ.get('MLFLOW_TRACKING_SERVER_URI')
    if not tracking_uri:
        raise EnvironmentError("""No environment variable named `MLFLOW_TRACKING_SERVER_URI` found, please assign the mlflow tracking value
                               to the environment variable""")
    return mf.MlflowClient(tracking_uri=tracking_uri)
    
def is_run_exists(run_id:str)->bool:
    client = get_mlflow_client()
    return True if client.get_run(run_id=run_id) else False

def create_experiment(exp_name:str)->str:
    client = get_mlflow_client()
    if client.get_experiment_by_name(name=exp_name):
        raise mf.MlflowException(message="""
                                 The provided experiment name {experiment_name} already exists, kindly provide a different name.
                                 """.format(experiment_name=exp_name))
    return client.create_experiment(name=exp_name)

    
    