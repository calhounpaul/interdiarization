import os, sys, json, shutil, getpass, atexit, time, hashlib

from secrets_handler import get_secrets
from reformatting_tools import reformat_all_transcription_json_to_transcripts

HF_TOKEN = get_secrets()["HF_TOKEN"]

import whisperx, yt_dlp, multiprocessing, atexit

this_dir = libs_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir_path = os.path.dirname(libs_dir)
workspace_dir_path = os.path.join(shared_dir_path, "workspace")
tmp_dir_path = os.path.join(workspace_dir_path, "tmp")
logs_dir_path = os.path.join(tmp_dir_path, "logs")
inputs_path = os.path.join(workspace_dir_path, "inputs")
outputs_path = os.path.join(workspace_dir_path, "outputs")
wx_model_name = os.environ.get("WX_MODEL")

wx_model = None
dz_model = None

def transcribe_and_diarize_single_audio(input_audio_filename,aggregate_dir):
    try:
        input_audio_path = os.path.join(inputs_path, aggregate_dir, input_audio_filename)
        input_audio_filename_noext = ".".join(input_audio_filename.split(".")[:-1])
        output_data_dir = os.path.join(outputs_path, aggregate_dir, input_audio_filename_noext)
        if not os.path.exists(os.path.join(outputs_path, aggregate_dir)):
            os.makedirs(os.path.join(outputs_path, aggregate_dir))
        if not os.path.exists(output_data_dir):
            os.makedirs(output_data_dir)
        transcription_path = os.path.join(output_data_dir, "transcription.json")
        if os.path.exists(transcription_path):
            #make sure the file is larger than 100 bytes
            if os.path.getsize(transcription_path) > 100:
                print(f"Skipping {input_audio_filename} as it has already been processed")
                return
        device = "cuda"
        global wx_model
        global dz_model
        if not wx_model:
            wx_model = whisperx.load_model(wx_model_name, device, language="en")
        if not dz_model:
            dz_model = whisperx.DiarizationPipeline(use_auth_token=HF_TOKEN, device=device) #,download_root=models_dir)
        audio = whisperx.load_audio(input_audio_path)
        result = wx_model.transcribe(audio, batch_size=16)
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
        diarize_segments = dz_model(audio)
        result = whisperx.assign_word_speakers(diarize_segments, result)
        with open(transcription_path, 'w') as f:
            json.dump(result, f)
    except Exception as e:
        #log the error
        with open(os.path.join(logs_dir_path, f"error_{input_audio_filename_noext}.log"), 'w') as f:
            f.write(str(e))
        print(f"Error processing {input_audio_filename}: {e}")


def transcribe_and_diarize_all_audio():
    audio_dirs = os.listdir(inputs_path)
    for folder in audio_dirs:
        audio_files = os.listdir(os.path.join(inputs_path, folder))
        for file in audio_files:
            reformat_all_transcription_json_to_transcripts()
            if not file.endswith(".flac"):
                continue
            transcribe_and_diarize_single_audio(file, folder)
            print(f"Processed {file}")