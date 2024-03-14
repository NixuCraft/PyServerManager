import os
import shutil
import time
import subprocess

# Quick dirty test to pop 10 servers 
# To reuse for the actual server

for file in os.listdir("instances"):
    if os.path.isdir(file):
        shutil.rmtree(file)

processes: list[subprocess.Popen] = []

for i in range(10):
    foldername = f"instances/fuckoeoeoe-{i}"
    os.makedirs(foldername)
    for file in os.listdir("cache/"):
        dir = f"cache/{file}"
        if os.path.isdir(dir):
            shutil.copytree(dir, f"{foldername}/{file}")
        else:
            shutil.copy(dir, foldername)

    propfile = f"{foldername}/server.properties"
    with open(propfile, "r") as file: content = file.read()
    content = content.replace("server-port=25565", f"server-port={25565+i}")
    with open(propfile, "w") as file: file.write(content)
    
    start_bat_path = os.path.join(foldername, "start.bat")
    if not os.path.exists(start_bat_path):
        print(f"Error: {start_bat_path} does not exist.")
        continue  # Skip to the next iteration
    if os.name == 'nt':
        process = subprocess.Popen(["cmd.exe", "/c", "start.bat"], cwd=foldername, stdout=None)
    else:
        process = subprocess.Popen(["sh", f"start.sh"], cwd=foldername, stdout=None)
    time.sleep(10)
    processes.append(process)


input("enter to kill all")

for process in processes:
    process.kill()