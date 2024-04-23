import os, json, shutil, getpass, atexit, time, hashlib

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

VLLM_CONTAINER_NAME = "vllm_server"
VLLM_IMAGE_NAME = "outlines_vllm_server"

def init_vllm_container(container_name=VLLM_CONTAINER_NAME,gpu_id=0,detach=True,model_name="casperhansen/llama-3-8b-instruct-awq"): #"astronomer-io/Llama-3-8B-Instruct-GPTQ-8-Bit"):
    volumes = {
        dot_cache_path: {'bind': '/root/.cache/huggingface', 'mode': 'rw'},
    }
    ports = {
        8000: 8000
    }
    #network_mode = "host"
    environment = {
        "HUGGING_FACE_HUB_TOKEN": secrets["HF_TOKEN"],
        "CUDA_VISIBLE_DEVICES": str(gpu_id),
    }
    init_command = "--dtype=float16 --model=" + model_name
    container = init_container(VLLM_IMAGE_NAME, init_command, container_name, volumes, ports, environment, detach, runtime="nvidia")
    return container
