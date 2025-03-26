from pathlib import Path
import json

class JsonConfig:
    def __init__(self, path):
        self.path = Path(path)
        self.json_obj = json.loads(self._load_json())

    def _load_json(self):
        if self.path.exists() and self.path.is_file():
            with open(str(self.path), "r") as file:
                return file.read()
        raise FileNotFoundError(f"Path '{str(self.path)}' not exists")
    
    def _get_modules_in_jpath(self, jpath):
        jpath = jpath.removeprefix("/")
        jpath = jpath.removesuffix("/")
        modules = jpath.split("/")
        return modules
    
    def _idx_is_valid(self, idx, list_size):
        return idx >= 0 and idx < list_size

    def get_attr(self, jpath):
        modules = self._get_modules_in_jpath(jpath)
        
        current_data = self.json_obj

        for module in modules:
            if type(current_data) is dict:
                if module in current_data:
                    current_data = current_data[module]
                    continue
                return False
            elif type(current_data) is list:
                if module.isdigit():
                    idx = int(module)
                    if self._idx_is_valid(idx, len(current_data)):
                        current_data = current_data[idx]
                        continue
                return False
        return current_data
    
    def set_attr(self, jpath, value):
        modules = self._get_modules_in_jpath(jpath)
        current_data = self.json_obj

        for idx, module in enumerate(modules):
            if type(current_data) is dict:
                if module in current_data:
                    if idx == len(modules) - 1:
                        current_data[module] = value
                        continue
                    current_data = current_data[module]
                    continue
                return False
            elif type(current_data) is list:
                if module.isdigit():
                    idx = int(module)
                    if idx == len(modules) - 1:
                        if self._idx_is_valid(idx, len(current_data)):
                            current_data[idx] = value
                            continue
                    if self._idx_is_valid(idx, len(current_data)):
                        current_data = current_data[idx]
                        continue
                return False
        return True
    
    def save(self):
        json_text = json.dumps(self.json_obj)
        with open(str(self.path), "w") as file:
            file.write(json_text)