from services.adb.contracts import *

_platformtools = ""

def set_platformtools(value):
    global _platformtools
    _platformtools = value

def get_GenericAdb():
    if _platformtools:
        return GenericAdb.GenericAdb(_platformtools)

if __name__ == "__main__":
    set_platformtools("/home/daniel/projects/python/debuggerMCpackages/platform-tools")
    GenericAdb = get_GenericAdb()
    serials = GenericAdb.get_all_serials()
    print(GenericAdb.get_device_info())
