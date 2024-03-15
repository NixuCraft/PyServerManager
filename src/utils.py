import os
import shutil
import threading

import psutil


def cleanup_files():
    shutil.rmtree("instances/")
    os.mkdir("instances/")


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
        child.kill()

    def wait_and_terminate():
        psutil.wait_procs(children, timeout=5)
        parent.kill() 
        parent.wait(timeout=5) 

    # Thread to avoid blocking the main thread for wait_procs & wait
    threading.Thread(target=wait_and_terminate).start()
    return True
    