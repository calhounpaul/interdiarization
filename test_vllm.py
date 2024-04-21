import os, sys, json, shutil, getpass, atexit, time, hashlib
import requests

json_schema = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"}
    }
}



json_payload = {
    "prompt": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\nYou are a helpful AI assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>\nWhat is the capital of France? Respond with a JSON object.<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
    "schema": json_schema
}

response = requests.post("http://ub22-base-srv-240420.lan:8001/generate", json=json_payload)

print(json.dumps(json.loads(response.json()["text"][0].split("<|end_header_id|>")[-1].strip()), indent=4))