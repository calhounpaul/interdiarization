import os, sys, json, shutil, getpass, atexit, time, hashlib

this_dir = container_workspace_dir = os.path.dirname(os.path.abspath(__file__))
container_shared_dir_path = os.path.dirname(container_workspace_dir)
container_libs_dir = os.path.join(container_shared_dir_path, "libs")
urls_list_path = os.path.join(container_workspace_dir, "urls_list.txt")
inputs_dir = os.path.join(container_workspace_dir, "inputs")
outputs_dir = os.path.join(container_workspace_dir, "outputs")
if not os.path.exists(inputs_dir):
    os.makedirs(inputs_dir)
if not os.path.exists(outputs_dir):
    os.makedirs(outputs_dir)

sys.path.append(container_libs_dir)

import whisperx_tools
from whisperx_tools import transcribe_and_diarize_all_audio
from youtube_tools import download_yt_data

import multiprocessing

download_pool = multiprocessing.Pool(4)
download_pool.apply_async(download_yt_data)
download_pool.close()

for n in range(100):
    transcribe_and_diarize_all_audio()
    time.sleep(60)

download_pool.join()