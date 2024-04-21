import os, sys, json, shutil, getpass, atexit, time, hashlib, docker
from secrets_handler import init_secrets, get_secrets

this_dir = libs_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir_path = os.path.dirname(libs_dir)
workspace_dir_path = os.path.join(shared_dir_path, "workspace")
dot_cache_path = os.path.join(shared_dir_path, "dot_cache")
if not os.path.exists(dot_cache_path):
    os.makedirs(dot_cache_path)

secrets = get_secrets()

from docker_tools import init_container, stop_and_remove_all_containers, get_container_logs

WHISPERX_NAME = "interdia_whisperx"

def init_whisperx_container(container_name=None,gpu_id=0,detach=True,wx_model="large-v3"):
    volumes = {
        libs_dir: {'bind': '/shared/libs', 'mode': 'ro'},
        workspace_dir_path: {'bind': '/shared/workspace', 'mode': 'rw'},
        #now join the .cache directory
        dot_cache_path: {'bind': '/root/.cache', 'mode': 'rw'},
    }
    ports = {}
    environment = {
        "CUDA_VISIBLE_DEVICES": str(gpu_id),
        "HF_TOKEN": secrets["HF_TOKEN"],
        "WX_MODEL": wx_model,
    }
    init_command = "python3 wx_run.py"
    if not container_name:
        client = docker.from_env()
        increment = 0
        tmp_name = f"{WHISPERX_NAME}_{increment}"
        while client.containers.list(filters={"name": tmp_name}):
            increment += 1
            tmp_name = f"{WHISPERX_NAME}_{increment}"
        container_name = tmp_name
    print(f"Starting container with name {container_name}")
    return init_container(WHISPERX_NAME, init_command, container_name, volumes, ports, environment, detach, runtime="nvidia")