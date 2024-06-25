from dagstermill import define_dagstermill_asset, define_dagstermill_op
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

## CREATING DATA CLEANING JOB ####

data_cleaner_op = define_dagstermill_op(
    name="data_cleaner_op",
    notebook_path=file_relative_path(__file__, "notebooks/Step1_Data_Cleaning.ipynb"),
    output_notebook_name="output_data_cleaning",
    outs={"cleaned_data": Out(DataFrame, io_manager_key="io_manager_cd")},
    ins={"data": In(DataFrame, input_manager_key="raw_data_input_manager")}
)

@graph
def data_cleaner_graph():
    cleaned_data, _ = data_cleaner_op()
    return cleaned_data

data_cleaner_job = data_cleaner_graph.to_job(
    name="data_cleaner_job",
    resource_defs={
        "output_notebook_io_manager": local_output_notebook_io_manager,
        "io_manager_cd": pandas_csv_io_manager ,
        "raw_data_input_manager": pandas_csv_io_manager,
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
    return tokenized_data

data_preprocessor_job = data_preprocessor_graph.to_job(
    name="data_preprocessor_job",
    resource_defs={
        "output_notebook_io_manager": local_output_notebook_io_manager,
        "io_manager_cd": pandas_csv_io_manager ,
        "io_manager_td": joblib_io_manager,
    }
)

### END DATA PREPROCESSING ###



all_jobs = [data_cleaner_job,
            data_preprocessor_job]
