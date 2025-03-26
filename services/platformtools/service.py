import os
import requests
import zipfile

from pathlib import Path
from tqdm import tqdm
from modules.app_config import get_prop, has_prop, set_prop
from utils.runtime import ROOT

SECTION = "services"
KEY_PATH = "platformtools.path"
KEY_VENV = "platformtools.venv"
URL_PLATFORM_TOOLS = "https://dl.google.com/android/repository/platform-tools-latest-{PLATFORM}.zip"

TEMP_DIR = "temp"
DEST_PATH = f"{TEMP_DIR}/platform_tools.zip"
OUT_PATH = ROOT

def _has_platform_tools_by_venv(venv):
    return venv in os.environ

def _has_platform_tools_by_path(path):
    return os.path.exists(path)

def _get_url_platform_tools_by_device():
    device_name = os.name
    if device_name == "posix":
        return URL_PLATFORM_TOOLS.replace("{PLATFORM}", "linux")
    return ""

def _download_platform_tools():
    if not os.path.exists(TEMP_DIR):
        os.mkdir(TEMP_DIR)
    url = _get_url_platform_tools_by_device()
    file_size = 0
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("content-lenght", 0))
    with open(DEST_PATH, "wb") as file, tqdm(
        desc="Baixando",
        total=file_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024
    ) as progress: 
        for chunck in response.iter_content(1024):
            file.write(chunck)
            progress.update(len(chunck))

def has_platform_tools():
    if has_prop(SECTION, KEY_PATH):
        key_value = get_prop(SECTION, KEY_PATH)
        return _has_platform_tools_by_path(key_value)
    elif has_prop(SECTION, KEY_VENV):
        key_value = get_prop(SECTION, KEY_VENV)
        return _has_platform_tools_by_venv(key_value)
    return False

def get_platform_tools():
    _download_platform_tools()
    with zipfile.ZipFile(DEST_PATH, "r") as zip:
        files = zip.namelist()

        with tqdm(
            desc="Extraindo arquivo",
            total=len(files)
        ) as progress:
            for file in files:
                progress.update(1)
                zip.extract(file, OUT_PATH)
    
    path = Path(OUT_PATH + "/platform-tools")
    set_prop(SECTION, KEY_PATH, str(path))
    os.remove(DEST_PATH)
    os.rmdir(TEMP_DIR)
    
    # TODO: adicionar o platform-tools nas variaves de ambiente e ao path
    # TODO: tornar compativel com windows
    os.system(f"chmod +x {path}/adb")
    os.system(f"{path}/adb version")

if __name__ == "__main__":
    if not has_platform_tools():
        get_platform_tools()
    else:
        print("Ja instalado")