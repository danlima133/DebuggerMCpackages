import configparser

from utils.runtime import get_safe_path

CONFIG_PATH = get_safe_path("./config.ini")

_config = configparser.ConfigParser()
_config.read(CONFIG_PATH)

def _save_config():
    with open(CONFIG_PATH, "w") as file:
        _config.write(file)

def has_prop(section, prop):
    return _config.has_option(section, prop)

def set_prop(section, prop, value=""):
    _config.set(section, prop, value)
    _save_config()

def get_prop(section, prop):
    if has_prop(section, prop):
        return _config.get(section, prop)

if __name__ == "__main__":
    print(has_prop("services", "platformtools.path"))