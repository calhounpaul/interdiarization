import os, sys, json, shutil, getpass, atexit, time, hashlib

GPU_IDS = [0,1]
WORKER_TO_GPU_IDS_MAP = {0:0, 1:0, 2:1, 3:1}
WX_DIA_IMAGE_NAME = "interdia_whisperx"
VLLM_IMAGE_NAME = "interdia_vllm"
VLLM_MODEL = "TheBloke/Mistral-7B-Instruct-v0.2-AWQ"
WX_MODEL = "large-v3"

this_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir_path = os.path.join(this_dir, "shared")
cache_path = os.path.join(shared_dir_path, "dot_cache")
libs_path = os.path.join(shared_dir_path, "libs")
workspace_path = os.path.join(shared_dir_path, "workspace")

sys.path.append(libs_path)

from hashing_tools import hybrid_hash_filename
from secrets_handler import init_secrets, get_secrets
from docker_tools import init_container, stop_and_remove_all_containers, get_container_logs
from whisperx_docker_tools import init_whisperx_container

atexit.register(stop_and_remove_all_containers)
init_secrets()

container_0 = init_whisperx_container(gpu_id=0)
container_1 = init_whisperx_container(gpu_id=0)
container_2 = init_whisperx_container(gpu_id=1)
container_3 = init_whisperx_container(gpu_id=1)

prior_outputs_qty = [len(os.listdir(os.path.join(workspace_path, "outputs",d))) for d in os.listdir(os.path.join(workspace_path, "outputs"))]
while True:
    time.sleep(1500)
    new_outputs_qty = [len(os.listdir(os.path.join(workspace_path, "outputs",d))) for d in os.listdir(os.path.join(workspace_path, "outputs"))]
    if new_outputs_qty == prior_outputs_qty:
        break
    prior_outputs_qty = new_outputs_qty