It is the core of the project, dedicated to an end-to-end continual learning pipeline for large language models (LLMs). This pipeline is designed to streamline and automate the training and evaluation process for LLMs. Here, we have successfully trained Falcon 7B on a Sentiment Analysis task, demonstrating the pipeline's capabilities. The organized structure ensures efficient tracking of experiments, data, and models. Dive in to explore and extend this robust setup for your own LLM projects.

A generic data piepline has two components to it:<br><br>
<b>1. Directed Acyclic Graph(DAG)</b>: It is crucial in a pipeline as it defines the sequence and dependencies of tasks, ensuring each step is executed in the correct order. This structure helps manage complex workflows, enhances reliability, and simplifies debugging and maintenance.
<br><br>
<b>2. Orchestrator</b>: It automates the execution, scheduling, and coordination of tasks, ensuring efficient and reliable workflow management. It handles dependencies, monitors progress, and manages failures to streamline complex data processes.
<br><br>
In this project both the DAG and the orchestration is implemented with the help of Dagster and the best thing about Dagster is it capability to produce DAG's from notebooks using its extension `dagstermill` which is named quite similarly to papermill(it helps in running jupyter notebook from scrips and command line).
We explore Dagster's `op & job` paradigm to construct and execute our graph.
<br><br>
For the sentiment analysis graph the DAG looks like this:
<br>
<img width="989" alt="image" src="https://github.com/aamir09/FTzard/assets/62461730/a8972306-0f86-4cbb-8a55-190a20c04ba0">
<br>

Each step in the pipeline has two variants, 1) Produces Data Artifacts 2) No Data Artifacts. The former is the case in Step 1, 2, 2.1, 5 and 6. The latter case is displayed in Step 3, 4 and 7. The notebooks of the first case yields some data artifacts and they are tracked by dvc using git, hence an extra step is follows them 
which handles the dvc part. This notebook is named as `Git_Dvc.ipynb`. Apart from data these runs also yield mlflow run metadata including `run_name`, `base_run_name` and their corresponding `run_ids`. In addition to that,
every notebook has mlflow logging and tracking service according the needs of the notebook. 

MLflow's run paradigm involves organizing each experiment or model training session as a "run," capturing essential information like parameters, metrics, artifacts, and source code. This structure enables systematic tracking and comparison of different runs, facilitating reproducibility and performance evaluation.
Runs are logged using a local databse in this project but a central server or local file system can be readily used. In this project, a run signifies `a step in the DAG` and we log the essential information of each step using these mlflow runs for comparison and record keeping. The system overview I designed for this project 
includes a top level run for each step under which every time this step is ran it will be logged as a child run and the date and time at which it was triggered will be its name under the top level run. 

<br>

For instance, for the experiment `sentiment_analysis`, I have some top level runs, namely `DATA_SAMPLING`, `INFERENCE`, etc.

![image](https://github.com/aamir09/FTzard/assets/62461730/4938139c-8946-456c-baff-ea180a342012)

<br>

Now everytime you run a notebook using dagster or just jupyter ID, a new run will be registered under corresponding top level run and as it can be seen the names are in the format `<data>-<time>`

![image](https://github.com/aamir09/FTzard/assets/62461730/a194c83d-b273-4105-a598-db6dc4392b0f)





