import os, sys, json, shutil, getpass, atexit, time, hashlib
import requests

jokes_file_url = "https://mirror2.evolution-host.com/textfiles/humor/TAGLINES/1liners.cap"
this_dir = os.path.dirname(os.path.abspath(__file__))
root_dir_path = os.path.dirname(this_dir)
shared_dir_path = os.path.join(root_dir_path, "shared")
workspace_dir_path = os.path.join(shared_dir_path, "workspace")
tmp_dir_path = os.path.join(workspace_dir_path, "tmp")

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
Explain why this joke is funny: "{joke}"
""".strip()

json_schema = {
    "type": "object",
    "properties": {
        "explanation": {"type": "string"}
    },
    "required": ["explanation"]
}

for oneliner in jokes_lines:
    try:
        oneliner = oneliner.strip().replace("     "," ").replace("\n"," ").replace("  "," ")
        json_payload = {
            "prompt": f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\nYou are a helpful AI assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>\n{question_string.format(joke=oneliner)}. Provide your explanation as a JSON object with the single key \"explanation\" corresponding to the joke explanation.<|eot_id|><|start_header_id|>assistant<|end_header_id>",
            "schema": json_schema,
            "max_tokens": 1024
        }

        response = requests.post("http://localhost:8001/generate", json=json_payload)
        response_string = json.loads(response.json()["text"][0].split("<|end_header_id>")[-1])["explanation"]
        formatted_string = f"Joke: {oneliner}\n\nExplanation: {response_string}\n--------\n"
        print(formatted_string)
        with open(os.path.join(this_dir, "vllm_outlines.txt"), "a") as f:
            f.write(formatted_string)
    except Exception as e:
        print(f"Error processing joke: {oneliner}")
        print(e)
        print("--------")