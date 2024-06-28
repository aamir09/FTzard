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
    outs={"tokenized_dataset": Out(dict, io_manager_key="io_manager_td"),
          "step2_run_metadata": Out(dict, io_manager_key="io_manager_step2_metadata")},
    ins={"data_cleaned": In(DataFrame, input_manager_key="io_manager_cd")}
)

@graph
def data_preprocessor_graph():
    tokenized_data, metadata, _ = data_preprocessor_op()
    dvc_logger_op(metadata=metadata)
    return tokenized_data, metadata

data_preprocessor_job = data_preprocessor_graph.to_job(
    name="data_preprocessor_job",
    resource_defs={
        "output_notebook_io_manager": local_output_notebook_io_manager,
        "io_manager_cd": pandas_csv_io_manager ,
        "io_manager_td": joblib_io_manager,
        "io_manager_metadata": joblib_io_manager,
        "io_manager_step2_metadata": joblib_io_manager
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

### LOGGING MODEL JOB ###


model_logger_op = define_dagstermill_op(
    name="model_logger_op",
    notebook_path=file_relative_path(__file__, "notebooks/Step4_ChooseBestModel.ipynb"),
    output_notebook_name="output_model_logging",
    ins={"datasets": In(dict, input_manager_key="io_manager_ds")}
)

@graph
def model_logger_graph():
    model_logger_op()
    return 

model_logger_job = model_logger_graph.to_job(
    name="model_logger_job",
    resource_defs={
        "output_notebook_io_manager": local_output_notebook_io_manager,
        "io_manager_ds": joblib_io_manager ,
        
    }
)

### RND LOGGING MODEL JOB ###

## CREATING DATA INFERENCE JOB ####

data_inference_op = define_dagstermill_op(
    name="data_inference_op",
    notebook_path=file_relative_path(__file__, "notebooks/Step5_Inference.ipynb"),
    output_notebook_name="output_data_inferencing",
    outs={"predictions_logits": Out(dict, io_manager_key="io_manager_pl"),
          "step5_run_metadata": Out(dict, io_manager_key="io_manager_step5_metadata")},
    ins={"datasets": In(dict, input_manager_key="io_manager_ds")}
)

@graph
def data_inference_graph():
    p_l, metadata, _ = data_inference_op()
    dvc_logger_op(metadata=metadata)
    return p_l, metadata

data_inference_job = data_inference_graph.to_job(
    name="data_inference_job",
    resource_defs={
        "output_notebook_io_manager": local_output_notebook_io_manager,
        "io_manager_ds": joblib_io_manager ,
        "io_manager_step5_metadata": joblib_io_manager,
        "io_manager_pl": joblib_io_manager,
         "io_manager_metadata": joblib_io_manager
    }
)

### END DATA INFERENCE JOB ###

### SAMPLING JOB ###
sampler_op = define_dagstermill_op(
    name="sampler_op",
    notebook_path=file_relative_path(__file__, "notebooks/Step6_Sampling.ipynb"),
    output_notebook_name="output_sampling",
    outs={"retraining_data": Out(dict, io_manager_key="io_manager_rd"),
          "step6_run_metadata": Out(dict, io_manager_key="io_manager_step6_metadata")},
    ins={"predictions_data": In(dict, input_manager_key="io_manager_pd")}
)

@graph
def sampler_graph():
    rd, metadata, _ = sampler_op()
    dvc_logger_op(metadata=metadata)
    return rd, metadata

sampling_job = sampler_graph.to_job(
    name="sampler_job",
    resource_defs={
        "output_notebook_io_manager": local_output_notebook_io_manager,
        "io_manager_rd": joblib_io_manager ,
        "io_manager_step6_metadata": joblib_io_manager,
        "io_manager_pd": joblib_io_manager,
         "io_manager_metadata": joblib_io_manager
    }
)
### END SAMPLING JOB ###

### RETRAINING JOB ###
retrainer_op = define_dagstermill_op(
    name="retrainer_op",
    notebook_path=file_relative_path(__file__, "notebooks/Step7_Retraining.ipynb"),
    output_notebook_name="output_retraining",
    ins={"datasets": In(dict, input_manager_key="io_manager_ds"),
         "sampled_dataset": In(dict, input_manager_key="io_manager_sd")}
)

@graph
def retrainer_graph():
    _ = retrainer_op()
    return

retrainer_job = retrainer_graph.to_job(
    name="retrainer_job",
    resource_defs={
        "output_notebook_io_manager": local_output_notebook_io_manager,
        "io_manager_ds": joblib_io_manager,
        "io_manager_sd": joblib_io_manager
    }
)

### END RETRAINING JOB ###

all_jobs = [data_cleaner_job,
            data_preprocessor_job,
            hp_trainer_job,
            dvc_logger_job,
            data_inference_job,
            model_logger_job,
            sampling_job,
            retrainer_job]


