import os, sys, json, shutil, getpass, atexit, time, hashlib, requests, json_repair

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

def llama_3_chatify(chat_history):
    chat_history_string = "<|begin_of_text|>"
    for chat in chat_history:
        chat_history_string += f"<|start_header_id|>{chat['speaker']}<|end_header_id|>\n{chat['text']}<|eot_id|>"
    chat_history_string += "<|start_header_id|>assistant<|end_header_id>"
    return chat_history_string

def query_vllm_chat_with_schema(assistant_and_user_chat_history,max_tokens=1024,temperature=0.9,sys_prompt=None,other_payload_params={},schema=None):
    if type(assistant_and_user_chat_history) == str:
        assistant_and_user_chat_history = [{"speaker": "user", "text": assistant_and_user_chat_history},]
    if assistant_and_user_chat_history[0]["speaker"] != "system":
        sys_prompt = "You are a helpful AI assistant."
        assistant_and_user_chat_history = [{"speaker": "system", "text": sys_prompt},] + assistant_and_user_chat_history
    if not schema:
        schema = {"type": "object", "properties": {"response": {"type": "string"}}, "required": ["response"]}
    json_payload = {
        "prompt": llama_3_chatify(assistant_and_user_chat_history),
        "schema": schema,
        "max_tokens": max_tokens,
        "stop_token_ids": [128001, 128009],
    }
    print(json.dumps(json_payload, indent=2))
    json_payload.update(other_payload_params.copy())
    response = requests.post("http://localhost:8000/generate", json=json_payload)
    response_string = json.dumps(json_repair.loads(response.json()["text"][0].split("<|end_header_id>")[-1].strip()), indent=2)
    return response_string