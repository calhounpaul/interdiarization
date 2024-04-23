import os, sys, json, shutil, getpass, atexit, time, hashlib, random
import requests

trivia_file_url = "https://raw.githubusercontent.com/calhounpaul/GPT-NeoX-20B-8bit-inference/main/trivia_qa.json"

this_dir = tests_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(tests_dir)
shared_dir_path = os.path.join(root_dir, "shared")
cache_path = os.path.join(shared_dir_path, "dot_cache")
libs_path = os.path.join(shared_dir_path, "libs")
workspace_path = os.path.join(shared_dir_path, "workspace")
tmp_dir_path = os.path.join(workspace_path, "tmp")

sys.path.append(libs_path)

from vllm_docker_tools import init_vllm_container
from vllm_tools import query_vllm_chat_with_schema

init_vllm_container()
#time.sleep(900)

if not os.path.exists(tmp_dir_path):
    os.makedirs(tmp_dir_path)

trivia_file_path = os.path.join(tmp_dir_path, "trivia_qa.json")
if not os.path.exists(trivia_file_path):
    response = requests.get(trivia_file_url)
    with open(trivia_file_path, "wb") as f:
        f.write(response.content)

trivia_file_contents = open(trivia_file_path, "r").read()

trivia_json = json.loads(trivia_file_contents)

json_schema = {
    "type": "object",
    "properties": {
        "answer": {
            "type": "string",
            "description": "The answer to the trivia question.",
            "maxLength": 80,
        }
    },
    "required": ["answer"]
}

print("Starting VLLM container...")

time.sleep(20)

random.shuffle(trivia_json)

for qa_data in trivia_json:
    while True:
        try:
            post_instruction = "Provide the answer as a JSON object with the single key \"answer\" corresponding to the answer."
            question = qa_data["q"]+"\n"+post_instruction
            answer = qa_data["a"]
            response_string = query_vllm_chat_with_schema(question, schema=json_schema, max_tokens=1024)
            bot_answer = json.loads(response_string)["answer"]
            formatted_string = f"Question: {question}\nAnswer: {answer}\nResponse: {bot_answer}\n\n"
            print(formatted_string)
            with open(os.path.join(this_dir, "vllm_outlines.txt"), "a") as f:
                f.write(formatted_string)
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
            continue