import os, sys, json, shutil, getpass, atexit, time, hashlib
import requests

jokes_file_url = "https://mirror2.evolution-host.com/textfiles/humor/TAGLINES/1liners.cap"

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

if not os.path.exists(tmp_dir_path):
    os.makedirs(tmp_dir_path)

jokes_file_path = os.path.join(tmp_dir_path, "1liners.cap")
if not os.path.exists(jokes_file_path):
    response = requests.get(jokes_file_url)
    with open(jokes_file_path, "wb") as f:
        f.write(response.content)

#open jokes file and read all lines
jokes_file_contents = open(jokes_file_path, "r").read()

jokes_lines = jokes_file_contents.split("""
     
     """)[10:-10]

question_string = """
Explain why this joke is funny: "{joke}". Provide your explanation as a JSON object with the single key \"explanation\" corresponding to the joke explanation.
""".strip()

json_schema = {
    "type": "object",
    "properties": {
        "explanation": {
            "type": "string",
            "description": "The explanation of the joke."
        }
    },
    "required": ["explanation"]
}

print("Starting VLLM container...")

for oneliner in jokes_lines:
    oneliner = oneliner.strip().replace("     "," ").replace("\n"," ").replace("  "," ")
    response_string = query_vllm_chat_with_schema(question_string.format(joke=oneliner), schema=json_schema, max_tokens=1024)
    formatted_string = f"Joke: {oneliner}\n\nExplanation: {response_string}\n--------\n"
    print(formatted_string)
    with open(os.path.join(this_dir, "vllm_outlines.txt"), "a") as f:
        f.write(formatted_string)