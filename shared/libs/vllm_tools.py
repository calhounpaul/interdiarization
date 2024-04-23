import os, sys, json, shutil, getpass, atexit, time, hashlib

from secrets_handler import get_secrets

HF_TOKEN = get_secrets()["HF_TOKEN"]

import multiprocessing, atexit

this_dir = libs_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir_path = os.path.dirname(libs_dir)
workspace_dir_path = os.path.join(shared_dir_path, "workspace")
tmp_dir_path = os.path.join(workspace_dir_path, "tmp")
logs_dir_path = os.path.join(tmp_dir_path, "logs")
inputs_path = os.path.join(workspace_dir_path, "inputs")
outputs_path = os.path.join(workspace_dir_path, "outputs")