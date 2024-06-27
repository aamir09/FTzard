from dagstermill import define_dagstermill_op
from dagstermill import local_output_notebook_io_manager
from dagster import (file_relative_path, 
                     In, 
                     Out,
                     graph)
from pandas import DataFrame
from ftzard.utils.dagster_io_managers import (
                            joblib_io_manager,
                            pandas_csv_io_manager
)

### GIT DVC ###

dvc_logger_op = define_dagstermill_op(
    name="dvc_logger_op",
    notebook_path=file_relative_path(__file__, "notebooks/Git_Dvc.ipynb"),
    output_notebook_name="output_dvc_logging",
    ins={"metadata": In(dict, input_manager_key="io_manager_metadata")}
)

@graph
def dvc_logger_graph():
    _ = dvc_logger_op()
    return

dvc_logger_job = dvc_logger_graph.to_job(
    name="dvc_logger_job",
    resource_defs={
        "output_notebook_io_manager": local_output_notebook_io_manager,
        "io_manager_metadata": joblib_io_manager
    }
)

### END GIT DVC ###

## CREATING DATA CLEANING JOB ####

data_cleaner_op = define_dagstermill_op(
    name="data_cleaner_op",
    notebook_path=file_relative_path(__file__, "notebooks/Step1_Data_Cleaning.ipynb"),
    output_notebook_name="output_data_cleaning",
    outs={"cleaned_data": Out(DataFrame, io_manager_key="io_manager_cd"),
          "step1_run_metadata": Out(dict, io_manager_key="io_manager_step1_metadata")},
    ins={"data": In(DataFrame, input_manager_key="raw_data_input_manager")}
)

@graph
def data_cleaner_graph():
    cleaned_data, metadata, _ = data_cleaner_op()
    dvc_logger_op(metadata=metadata)
    return cleaned_data, metadata

data_cleaner_job = data_cleaner_graph.to_job(
    name="data_cleaner_job",
    resource_defs={
        "output_notebook_io_manager": local_output_notebook_io_manager,
        "io_manager_cd": pandas_csv_io_manager ,
        "io_manager_step1_metadata": joblib_io_manager,
        "raw_data_input_manager": pandas_csv_io_manager,
         "io_manager_metadata": joblib_io_manager
    }
)

### END DATA CLEANING JOB ###

### DATA PREPROCESSING ##

data_preprocessor_op = define_dagstermill_op(
    name="data_preprocessor_op",
    notebook_path=file_relative_path(__file__, "notebooks/Step2_Data_Preprocessing.ipynb"),
    output_notebook_name="output_data_preprocessing",
    outs={"tokenized_dataset": Out(dict, io_manager_key="io_manager_td")},
    ins={"data_cleaned": In(DataFrame, input_manager_key="io_manager_cd")}
)

@graph
def data_preprocessor_graph():
    tokenized_data, _ = data_preprocessor_op()
    # _, = dvc_logger_op()
    return tokenized_data

data_preprocessor_job = data_preprocessor_graph.to_job(
    name="data_preprocessor_job",
    resource_defs={
        "output_notebook_io_manager": local_output_notebook_io_manager,
        "io_manager_cd": pandas_csv_io_manager ,
        "io_manager_td": joblib_io_manager,
        #  "io_manager_metadata": joblib_io_manager
    }
)

### END DATA PREPROCESSING ###

### HYPERPARAM_TUNING & TRAINING ###


hp_trainer_op = define_dagstermill_op(
    name="hp_trainer_op",
    notebook_path=file_relative_path(__file__, "notebooks/Step3_HyperParam_Tuning.ipynb"),
    output_notebook_name="output_hp_training",
    # outs={"tokenized_dataset": Out(dict, io_manager_key="io_manager_td")},
    ins={"datasets": In(dict, input_manager_key="io_manager_ds")}
)

@graph
def hp_trainer_graph():
    _ = hp_trainer_op()
    return

hp_trainer_job = hp_trainer_graph.to_job(
    name="hp_trainer_job",
    resource_defs={
        "output_notebook_io_manager": local_output_notebook_io_manager,
        "io_manager_ds": joblib_io_manager
    }
)

### END HYPERPARAM_TUNING & TRAINING ###




### DATA JOBS ### 




all_jobs = [data_cleaner_job,
            data_preprocessor_job,
            hp_trainer_job,
            dvc_logger_job]


