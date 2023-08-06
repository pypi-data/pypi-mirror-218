import boto3
import os
from git import Repo,rmtree
import subprocess
from loguru import logger
import sys

def init_logger():

    logger.remove(0)
    logger.add(sys.stderr, format="{time:MMMM D, YYYY , HH:mm:ss!UTC} | {level} | {message}")
    os.environ['repo_dir'] ="tah_data_repo"
    os.environ['wd'] = os.getcwd()


def init_Repo(Repo_url,branch):
    init_logger()
    
    logger.info("Initiating filesystem")

    try:
        repo = Repo.clone_from(Repo_url,os.environ['repo_dir'])
    except Exception as e:
        logger.error(e)
        logger.error("This Repo already exists and is not an empty directory")
        exit()

    git_ = repo.git
    git_.checkout(branch)

    prepare_creds()


def prepare_creds():
    logger.info("checking credentials .....")
    os.chdir(os.environ['repo_dir'])
    try:
        subprocess.run('dvc remote modify --local storage access_key_id $AWS_ACCESS_KEY_ID', shell=True,env={'AWS_ACCESS_KEY_ID': os.environ['AWS_ACCESS_KEY_ID']})
        subprocess.run('dvc remote modify --local storage secret_access_key $AWS_SECRET_ACCESS_KEY', shell=True,env={'AWS_SECRET_ACCESS_KEY': os.environ['AWS_SECRET_ACCESS_KEY']})
    except Exception as e:
        clean_repo()
        logger.error(e)
        exit()

    os.chdir("../")
    logger.info("credentials checked successfully .....")


def get_dvc(dir_path,data_version,local_absolute_data_path):
    check_data_exist(data_version,local_absolute_data_path)
    try:
        os.chdir(os.environ['repo_dir']+"/"+dir_path)
        logger.info("Cloning Data .....")
        subprocess.run('dvc pull $dataset', shell=True,check=True,env={'dataset': data_version})
    except subprocess.CalledProcessError as e:
        clean_repo()
        logger.error(e)
        logger.error(" dvc "+ data_version +" not found")
        exit()
    except Exception as e:
        clean_repo()
        logger.error(e)
        exit()
    logger.info("Moving Data .....")
    subprocess.run('cp -r $src $dst', shell=True,check=True,env={'src': data_version ,'dst':local_absolute_data_path })

def get_stage(dir_path,stage_name,local_absolute_data_path):
    check_data_exist(stage_name,local_absolute_data_path)
    try:
        os.chdir(os.environ['repo_dir']+"/"+dir_path)
        logger.info("Cloning Data .....")
        subprocess.run('dvc repro $stage', shell=True,check=True,env={'stage': stage_name})
    except subprocess.CalledProcessError as e:
        clean_repo()
        logger.error(e)
        logger.error(" Stage "+ stage_name +" not found")
        exit()
    except Exception as e:
        clean_repo()
        logger.error(e)
        exit()        
    logger.info("Moving Data .....")
    subprocess.run('cp -r $src $dst', shell=True,env={'src': stage_name ,'dst':local_absolute_data_path })

def clean_repo():
    os.chdir(os.environ['wd'])
    rmtree(os.environ['repo_dir'])

def check_data_exist(data_version,local_absolute_data_path):
    if (os.path.isdir(local_absolute_data_path+"/"+data_version)):
        logger.warning("This Data already exists")
        logger.warning("Skiping download ")
        clean_repo()
        exit()
        

