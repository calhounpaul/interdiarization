import os, sys, json, shutil, getpass, atexit, time, hashlib, random
import yt_dlp
from hashing_tools import hybrid_hash_filename, hybrid_hashname

this_dir = libs_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir_path = os.path.dirname(libs_dir)
workspace_dir_path = os.path.join(shared_dir_path, "workspace")
tmp_dir_path = os.path.join(workspace_dir_path, "tmp")
inputs_path = os.path.join(workspace_dir_path, "inputs")
outputs_path = os.path.join(workspace_dir_path, "outputs")
urls_list_path = os.path.join(workspace_dir_path, "urls_list.txt")

def download_yt_data():
    yt_urls = []
    for url in open(urls_list_path, 'r').readlines():
        if not len(url.strip()):
            continue
        yt_urls.append(url.strip())
    random.shuffle(yt_urls)
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'writeinfojson': True,
        'writeautomaticsub': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
        }],
        'playlistrandom': True,
    }
    for yt_url in yt_urls:
        dirname = "youtube_" + hybrid_hashname(yt_url.split("/")[-1].replace("@", ""))
        if not os.path.exists(os.path.join(inputs_path, dirname)):
            os.makedirs(os.path.join(inputs_path, dirname))
        ydl_opts["outtmpl"] = os.path.join(inputs_path, dirname, "%(title.0:32)s_YTID:%(id)s:YTID.%(ext)s")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])