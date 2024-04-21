import docker, os, sys, json, shutil, getpass, atexit, time, hashlib

from hashing_tools import hybrid_hash_filename
this_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir_path = os.path.dirname(this_dir)
workspace_dir_path = os.path.join(shared_dir_path, "workspace")
tmp_dir_path = os.path.join(workspace_dir_path, "tmp")
logs_dir_path = os.path.join(tmp_dir_path, "logs")
if not os.path.exists(logs_dir_path):
    os.makedirs(logs_dir_path)

client = docker.from_env()

def init_container(image_name, command, container_name, volumes, ports, environment, detach=True,runtime="nvidia"):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
    except:
        pass
    container = client.containers.run(image_name,command, detach=detach, name=container_name, volumes=volumes, ports=ports, environment=environment, runtime=runtime)
    return container

def get_container_logs(container_name):
    container = client.containers.get(container_name)
    return container.logs()

def stop_and_remove_all_containers(de_log=True):
    for container in client.containers.list():
        container.stop()
        if de_log:
            logout = str(container.logs())
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            save_name = os.path.join(logs_dir_path, hybrid_hash_filename(container.name + "_" + timestamp + ".log"))
            with open(save_name, "w") as f:
                f.write(logout)
        container.remove()