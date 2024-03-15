import os
import shutil


def cleanup_files():
    shutil.rmtree("instances/")
    os.mkdir("instances/")