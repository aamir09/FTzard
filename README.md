# FTzard
<div align="center">
<img alt="License" src="https://img.shields.io/badge/General%20Public%20License%20v3.0-black?style=plastic&label=License&labelColor=black&color=green&cacheSeconds=https%3A%2F%2Fwww.gnu.org%2Flicenses%2Fquick-guide-gplv3.html&link=https%3A%2F%2Fwww.gnu.org%2Flicenses%2Fquick-guide-gplv3.html">

<br>

<a href="https://www.python.org/"><img src="https://shields.io/badge/Python-3.8%2B-blue?style=plastic&labelColor=black&color=blue" alt="Python"></a>
  <a href="https://www.mlflow.org/"><img src="https://shields.io/badge/MLflow-2.13.x-blue?style=plastic&labelColor=black&color=blue" alt="MLflow"></a>
  <a href="https://www.dagster.io/"><img src="https://shields.io/badge/Dagster-1.7.x-purple?style=plastic&labelColor=black&color=purple" alt="Dagster"></a>
  <a href="https://www.dvc.org/"><img src="https://shields.io/badge/DVC-3.5.x-red?style=plastic&label=DVC&labelColor=black" alt="DVC"></a>
  <a href="https://github.com/prefix-dev/pixi"><img src="https://shields.io/badge/Env-Prefix%20Dev%20Pixi-yellow?style=plastic&labelColor=black" alt="Pixi"></a>


</div>

<br>

<p align="justify">
  
The advent of large language models (LLMs) has revolutionized the field of language modeling, giving rise to a multitude of use cases and applications. With a wide variety of LLMs now available, evaluating them for specific tasks has become a challenging endeavor. Additionally, as experiments grow in complexity, tracking results, data, and fine-tuned models becomes increasingly difficult for data scientists.

<br>
<div align="center">
<img src="https://github.com/aamir09/FTzard/assets/62461730/b63097eb-f97c-4dfb-a0f3-e6e9a1369636" alt="FTzard_LOGO" width="700" height=500/>
</div>
<br>

To address these challenges, I created FTzard, a comprehensive framework designed to assist data scientists in managing their LLM experiments. FTzard offers an end-to-end continual learning pipeline, integrating orchestration with Dagster, experiment and model tracking with MLflow, and data versioning with DVC. This framework not only streamlines the development lifecycle but also accelerates progress by ensuring organization and reducing hassle. In addition to that, it allows you the flexibility of having a reproducible environment using <b>pixi</b> (superfast alternative to tools like poetry) with an inplace config structure harvested using <b>hydra</b>. 

There's no need to jump between folders and piles of notebooks, simply use FTzard's structure for all your projects and remain organised. To get started, simply modify the code in the provided Jupyter notebooks, and your pipeline will be ready to go. 


**[UPDATE]** [05/07/2024] I have removed all dvc related files, so that you can start fresh. However, I have kept `/ftzard/pipeline/notebooks/mlflow.db` so that when you'll run mlflow ui using the pixi task defined in pyprojet.toml, you can see the structure I am referring to in the file. For a new project, delete the db and create a file with the same or any other name ending with `.db`
<br>

</p>


| SubModule | Doc Link|
|--------------|-------------|
| Pipeline      | [Link](https://github.com/aamir09/FTzard/blob/main/ftzard/pipeline/Pipeline.md) |


## Installation & Setup 

<h4>It is recommended that you first fork the reppository and then clone it to your server as dvc needs to commit & push .dvc files to git for tracking.</h4>
<br><br>
<b>1. Environment</b><br>
The environment is quite easy to setup, all thanks to pixi. The pixi setup is already given in the Dockerfile and it is recommended to use the Dockerfile. 
a) Build the docker Image (Ensure you have docker installed and docker daemon is running)

```
docker build -t ftzard_image .  
```
Note: Make sure you are in the directory where the `Dockerfile` resides; the project directory.

b) Run the docker dcotainer for the image
```
docker run --gpus all --rm -it --mount type=bind,source="$(pwd)",target=/app -p 8082:8080 -p 8081:8081  ftzard_image
```
We use all the available gpus and mount the project directory so that development becomes easier and you can add data easily. In the container our project directory will be `/app` and hence all the paths are with respect to that in the notebook wherever relative paths couldn't cut it. You can expose more ports to run mflow, dagster and jupyter seperately. 

c) Activating the environment<br><br>
Pixi is quite similar to `pip-env` in terms of activation of the environment. Once you are inside the docker container, go to the project folder,
```
cd /app
```
Now to activate the environment,
```
pixi shell 
```
It will provide you a terminal with environment activated using the pixi.lock file provided. A folder named `.pixi` will be created which will contain the virtual env, by default named as `default`

Note: If you  have added new deps ore removed any, then you can run any pixi command line command and it will update the lock file.

<b>2. DVC</b><br>
DVC (Data Version Control) is an open-source tool designed to manage and version control large datasets and machine learning models. It integrates seamlessly with Git, enabling data scientists to track data changes and collaborate effectively. 

We are going to harvest powers of dvc and use it log and track our data artifacts. In the pipeline, after every step that produces data artifacts, a dvc and git commit step is executed which saves the current 
`git commid id` to the mlflow run and adds it to the `commit_history.json` file that each run will have. This makes our life easier as we know when and which data is changed and how to get it.

a) To intialize dvc, execute the following from the project root; `/app`,
```
dvc init 
```
b) Add data a file or directory to track (in our case we want to track the whole data directory as it will contain all the data artifacts)
```
dvc add ftzard/data
```
When you'll open the folder `ftzard`, you'll notice a file is created namely `data.dvc` that contains metadata for the data directory, like the hash value, hash algorithm, number of file etc. It is basically the file that will help us track any changes in the data directory as the hash and other meta data will change and git will detect it.


c) Define a remote locaation to save data (It can be local, hdfs, s3, azure, etc, we saving in local at the moment)
```
dvc add remote -d <name for remote> <location>
```
This will let `dvc` know that it is one of the locations where you want push you data and it's information can be found in `.dvc/config` file. Once there are any changes in the data, you push this new data to this remote storage and we can then commit the new `data.dvc` file to git.

There are a few more steps involved in between however, they are taken care of in the `Git_Dvc.ipynb` notebook. This is all you have to do to setup DVC.

Note: For using any 3rd party storage like aszure, s3, gcloud, you need to install dvc extensions for the same, have these services configured on your server beforehand or follow standard dvc procedure to set such remotes.


 <b>3. Git</b><br>
Git is an essential part of this workflow, that combines with dvc to store the `.dvc` files and make them tractable. 

a) Install Git
```
yum install -y git
```

In the container, to allow git automatically log dvc file changes, we have to re-configure the origin url so that it doesn't keep popping up the questions like Username and Passowrd.

b) Add Git username and password (token) env variables

```
export GITHUB_USERNAME=your_username
export GITHUB_PASSWORD=your_git_token

```

c) Modify the url of origin of the repository to, 
```
git remote set-url origin https://${GITHUB_USERNAME}:${GITHUB_PASSWORD}@github.com/${GITHUB_USERNAME}/ftzard.git

```
Note: I am assuming that you have `forked` the repository before cloning it. 

 <b>4. Dagster</b><br>
Dagster is an open-source data orchestrator that helps manage and automate complex data pipelines. It enables robust workflow management, seamless integration with various data tools, and efficient handling of dependencies, making it ideal for building and maintaining data-intensive applications. 

The only thing to do here is to set the `DAGSTER_HOME` environment variable, which is essential for configuring Dagster's storage location for its metadata, such as pipeline runs, logs, and other important information. This ensures that all operational data is stored consistently in a specified directory, facilitating easier management and debugging. If this is not specified, then each time you run Dagster server, it will create a new `tmp` folder to store the above.

```
export DAGSTER_HOME=/path/to/your/dagster/home
```
To make sure the changes take effet, restart the terminal or refersh the bashrc using, 
```
source ~/.bashrc
```

## Pipeline
It is the core of the project, dedicated to an end-to-end continual learning pipeline for large language models (LLMs). This pipeline is designed to streamline and automate the training and evaluation process for LLMs. Here, we have successfully trained Falcon 7B on a Sentiment Analysis task, demonstrating the pipeline's capabilities. The organized structure ensures efficient tracking of experiments, data, and models. Dive in to explore and extend this robust setup for your own LLM projects.

A generic data pipeline has two components to it:<br><br>
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

**Note: We are generating test data while the data preprocessing step and hence the Step4 proceeds with Step5.**

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

This can be easily viewed by running the `mlflow ui`. I have made this easier by making a pixi task named `mlflow_ui` in the `pyproject.toml` file. The UI runs at port 5000 by default by executing the following,
```
pixi run mlflow_ui
```


### Running a Dagster Job 

Dagster provides multiple ways of executing a job; from the command line, using a sensor and from the Launchpad in the Dagster UI. I would say that while development Launchpad is your best friend as writing the config yaml is easier and it persists the config, so that when you launch a run again, you wouldn't have to write the config again. After, that you can leave this work for the sensor. 

To start the dagster server, there's another pixi task that I have defined that you can use,
```
pixi run dagster_ui
```
Also, one noticeable thing is that dagster will always accept paths from the `root directory` of your project; `app`. Here is a sample of how to write a config in Dagster Launchpad, this is for the `DATA_CLEANING` JOB:
<img width="1312" alt="image" src="https://github.com/aamir09/FTzard/assets/62461730/f8fab0d8-d75d-40c8-9fc9-0e36f4218814">
<br>
The whole config for this job is given below. Also, I'll add the configs for the rest of the jobs in `ftzard/config/dagster`, which can be used as a reference.
```
resources:
  output_notebook_io_manager:
    config:
      asset_key_prefix: []
      
  io_manager_cd:
    config:
      base_path: /app/ftzard/data
      file_name: cleaned_data.csv
      
  io_manager_step1_metadata:
    config:
      base_path: /app/ftzard/data
      file_name: step1_run_metadata.joblib
      
  raw_data_input_manager:
    config:
      base_path: /app/ftzard/data
      file_name: training.csv
      
  io_manager_metadata:
    config:
      base_path: /app/ftzard/data
      file_name: step1_run_metadata.joblib
      

```
In production, we can configure sensors that would get triggred based on the criteria defined and these jobs will be executed by those sensors.

## Config

The `config` folder under `ftzard` stores the global configurations of the project but it can be designed according to the needs for your project. I have used `hydra` to manage my configurations. It might seem to be redundant at the momemnt but as the project scope increases the importance of `hydra` and the configs increases. It handles complexity with ease and is a handy tool to have in your arsenal.  

## References 
1. [mlops2_with_dagster, Dr Rahul Dave](https://github.com/univai-community/mlops2_with_dagster)
2. [Fine-tuning LLAMA 3, Trade Mamba](https://github.com/adidror005/youtube-videos/blob/main/LLAMA_3_Fine_Tuning_for_Sequence_Classification_Actual_Video.ipynb)
***
