import os
import subprocess
import mlflow
import logging
import datetime
import mlflow as mf 

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_current_date_time():
    now = datetime.datetime.now()
    date = str(now.date())
    hour = str(now.hour)
    minute = str(now.minute)
    return "_".join([date, f"{hour}:{minute}"])
    

def run_command(command):
    """Run a shell command and return the output"""
    result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
    return result.stdout.strip()

def check_dvc_files(directory):
    """Check if DVC files exist in the given directory"""
    dvc_files = [f for f in os.listdir(directory) if f.endswith('.dvc')]
    
    if not dvc_files:
        logger.warning(f"No .dvc files found in {directory}")
        return False
    return True


def git_commit(directory:str):
    try:
        os.chdir(direcctory)
        parent_dir = os.getcwd()
        
        logger.info(f"Changed working directory to: {parent_dir}")

        # Check for DVC files in the parent directory
        if not check_dvc_files(parent_dir):
            raise FileNotFoundError("DVC files not found in the parent directory.")

        # 1. Add the DVC lock file
        run_command("git add -f *.dvc")
        
        # 2. Commit the DVC lock file
        commit_message = f"Update DVC lock file {run_name}"
        run_command(f'git commit -m "{commit_message}"')
        
        # 3. Push changes to GitHub
        run_command("git push origin main")  # Adjust branch name if needed
        
        # 4. Get the commit ID
        commit_id = run_command("git rev-parse HEAD")
        logger.info(f"Commit ID: {commit_id}")
        
        # 5. Perform DVC checkout
        run_command("dvc checkout")

        return commit_id
    
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command: {e.cmd}")
        logger.error(f"Error output: {e.stderr}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")