from datetime import datetime
import os
import shutil
import threading

import psutil

from variables import logs_server_dir

def cleanup_files():
    shutil.rmtree("instances/")
    os.mkdir("instances/")
    if not os.path.exists(logs_server_dir + "/lobbies"):
        os.makedirs(logs_server_dir + "/lobbies")


def get_date_formatted():
    return datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")

def kill_process_tree(pid: int) -> bool:
    """
    Tries to kill the process with provided pid.\n
    Returns True if the PID exists, False if it doesn't.
    """
    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return False
        
    children = parent.children(recursive=True)
    for child in children:
        try:
            child.kill()
        except psutil.NoSuchProcess: pass

    def wait_and_terminate():
        psutil.wait_procs(children, timeout=5)
        try:
            parent.kill()
        except psutil.NoSuchProcess: pass
        parent.wait(timeout=5) 

    # Thread to avoid blocking the main thread for wait_procs & wait
    threading.Thread(target=wait_and_terminate).start()
    return True
    