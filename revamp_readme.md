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

## Overview

<p align="justify">
The advent of large language models (LLMs) has revolutionized the field of language modeling, giving rise to a multitude of use cases and applications. Evaluating these models for specific tasks can be challenging, and as experiments grow in complexity, tracking results, data, and fine-tuned models becomes increasingly difficult for data scientists.

To address these challenges, I created FTzard, a comprehensive framework designed to assist data scientists in managing their LLM experiments. FTzard offers an end-to-end continual learning pipeline, integrating orchestration with Dagster, experiment and model tracking with MLflow, and data versioning with DVC. This framework streamlines the development lifecycle, accelerates progress by ensuring organization, and reduces hassle.

There's no need to jump between folders and piles of notebooks—simply use FTzard's structure for all your projects and stay organized.
</p>

<div align="center">
<img src="https://github.com/aamir09/FTzard/assets/62461730/b63097eb-f97c-4dfb-a0f3-e6e9a1369636" alt="FTzard_LOGO" width="700" height=500/>
</div>

## Key Features

- **End-to-End Continual Learning Pipeline:** Integrates Dagster, MLflow, and DVC for a seamless workflow.
- **Reproducible Environment:** Uses Pixi for environment management and Hydra for configuration management.
- **Simplified Project Structure:** Reduces the complexity of managing multiple notebooks and folders.
- **Enhanced Organization:** Tracks experiments, data, and models efficiently.

## Quick Start Guide

### 1. Fork and Clone the Repository

It is recommended to first fork the repository and then clone it to your server, as DVC needs to commit & push .dvc files to git for tracking.

### 2. Environment Setup

The environment setup is easy thanks to Pixi. Use the provided Dockerfile for a streamlined setup.

**Build the Docker Image:**

Ensure you have Docker installed and the Docker daemon is running.

```bash
docker build -t ftzard_image .
```

**Run the Docker Container:**

```bash
docker run --gpus all --rm -it --mount type=bind,source="$(pwd)",target=/app -p 8082:8080 -p 8081:8081 ftzard_image
```

Inside the container, activate the environment:

```bash
cd /app
pixi shell
```

### 3. DVC Setup

DVC (Data Version Control) is used to manage and version control large datasets and machine learning models.

**Initialize DVC:**

```bash
dvc init
```

**Add Data Directory to Track:**

```bash
dvc add ftzard/data
```

**Define a Remote Location to Save Data:**

```bash
dvc remote add -d <name> <location>
```

### 4. Git Configuration

Install Git and configure it for automatic logging of DVC file changes.

**Install Git:**

```bash
yum install -y git
```

**Set Git Username and Password (Token) Environment Variables:**

```bash
export GITHUB_USERNAME=your_username
export GITHUB_PASSWORD=your_git_token
```

**Modify the URL of Origin:**

```bash
git remote set-url origin https://${GITHUB_USERNAME}:${GITHUB_PASSWORD}@github.com/${GITHUB_USERNAME}/ftzard.git
```

### 5. Dagster Setup

Dagster is an open-source data orchestrator that helps manage and automate complex data pipelines.

**Set DAGSTER_HOME Environment Variable:**

```bash
export DAGSTER_HOME=/path/to/your/dagster/home
source ~/.bashrc
```

## Running the Pipeline

The core of FTzard is its end-to-end continual learning pipeline for large language models (LLMs). For example, we have successfully trained Falcon 7B on a sentiment analysis task, demonstrating the pipeline's capabilities.

**Starting the Dagster Server:**

```bash
pixi run dagster_ui
```

**Running a Dagster Job:**

Dagster provides multiple ways to execute a job, including command line, sensors, and Launchpad in the Dagster UI. Here is a sample config for the `DATA_CLEANING` job in the Launchpad:

```yaml
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

### Config Management

The `config` folder under `ftzard` stores the global configurations of the project, managed by Hydra. This setup allows for scalable and manageable configurations as the project scope increases.

## References

1. [mlops2_with_dagster, Dr Rahul Dave](https://github.com/univai-community/mlops2_with_dagster)
2. [Fine-tuning LLAMA 3, Trade Mamba](https://github.com/adidror005/youtube-videos/blob/main/LLAMA_3_Fine_Tuning_for_Sequence_Classification_Actual_Video.ipynb)

---
