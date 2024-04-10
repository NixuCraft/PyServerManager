import importlib
import os

from types.instance import ServerInstance


class Presetarr:
    BASE_PRESETS_PATH: str = "presets/"
    presets: list[ServerInstance]
    def __init__(self) -> None:
        self.presets = []
        for file in os.listdir(self.BASE_PRESETS_PATH):
            self._load_preset(file)
    
    def _load_preset(self, file: str):
        if file == "__pycache__": 
            return
        if not os.path.isfile(f"parsers/{file}"):
            print(f"{file} is not a file.")
            return
        try:
            module_name = f"parsers.{file[:-3]}"
            my_module = importlib.import_module(module_name)
            preset: list[ServerInstance] | ServerInstance
            self.presets.append(my_module.load())
        except:
            print(f"{file} is not a module.")