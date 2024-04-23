from templating.entity_extractions import podcast_entity_extraction_schema
import os, sys, json, shutil, getpass, atexit, time, hashlib, requests, json_repair

from vllm_tools import query_vllm_chat_with_schema

this_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir_path = os.path.join(this_dir, "shared")
cache_path = os.path.join(shared_dir_path, "dot_cache")
libs_path = os.path.join(shared_dir_path, "libs")
workspace_path = os.path.join(shared_dir_path, "workspace")

outputs_dir_path = os.path.join(workspace_path, "outputs")

def analyze_transcript(output_data_dir_path):
    transcript_path = os.path.join(output_data_dir_path, "transcription.txt")
    if not os.path.exists(transcript_path):
        return
    channel_info_path = os.path.join(output_data_dir_path, "channel_info.json")
    if not os.path.exists(channel_info_path):
        return
    info_path = os.path.join(output_data_dir_path, "info.json")
    if not os.path.exists(info_path):
        return
    channel_info = json.load(open(channel_info_path, 'r'))
    info = json.load(open(info_path, 'r'))
    transcript = open(transcript_path, "r").read()
    entity_schema = podcast_entity_extraction_schema()
    full_desc_string = channel_info['title'] + "\n" + channel_info['description']
    prompt = f"Your task is to extract people, places, and things from the following podcast/radio source: {full_desc_string}\n\n"
    prompt += f"The excerpt to analyze is from the episode titled \"{info['title']}\""
    if len(info['description']) > 0:
        prompt += f" and the description is: \"{info['description']}\""
    prompt += ".\n\nThe transcript excerpt to be analyzed is as follows:\n\n<transcript>\n{tscpt}\n</transcript>\n\n"
    prompt += "Provide the extracted entities as a JSON object with the keys \"people\", \"places\",\"things\", \"relationships\" and \"identityIndicators\"."
    responses = []
    for chunk in [transcript[i:i + 1024] for i in range(0, len(transcript), 1024)]:
        response = query_vllm_chat_with_schema(prompt.format(tscpt=chunk), schema=entity_schema, max_tokens=1024)
        responses.append(response)
        print(response)
    return responses