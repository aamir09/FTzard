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
</p>

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
git remote set-url origin https://${GITHUB_USERNAME}:${GITHUB_PASSWORD}@github.com/${GITHUB_USERNAME}:/ftzard.git

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
