import os
import sys

def run_as_build():
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")

def get_safe_path(path):
    if run_as_build():
        return os.path.join(APP_ROOT, path)
    return path

def get_path_root(path):
    if run_as_build():
        return os.path.join(ROOT, path)
    return os.path.join(os.getcwd(), path)

INTERNAL = getattr(sys, "_MEIPASS") if run_as_build() else ""
ROOT = INTERNAL.removesuffix("/_internal") if run_as_build() else "./"
APP_ROOT = os.path.join(INTERNAL, "root")