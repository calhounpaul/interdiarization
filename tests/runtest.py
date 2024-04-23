import os, sys, json, shutil, getpass, atexit, time, hashlib
import requests, random

this_dir = tests_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(tests_dir)
shared_dir_path = os.path.join(root_dir, "shared")
cache_path = os.path.join(shared_dir_path, "dot_cache")
libs_path = os.path.join(shared_dir_path, "libs")
workspace_path = os.path.join(shared_dir_path, "workspace")
outputs_path = os.path.join(workspace_path, "outputs")
tmp_dir_path = os.path.join(workspace_path, "tmp")

sys.path.append(libs_path)

from vllm_docker_tools import init_vllm_container
from vllm_tools import query_vllm_chat_with_schema
from analysis_tools import analyze_transcript

init_vllm_container()


test_path = random.choice(os.listdir(outputs_path))

print(f"Analyzing transcript at {test_path}")

while True:
    try:
        analyze_transcript(test_path)
        break
    except Exception as e:
        print(e)
        time.sleep(5)