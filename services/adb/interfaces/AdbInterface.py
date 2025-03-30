import os
import subprocess

class NotImplemented(Exception):
    def __init__(self):
        super().__init__("haven't body!")

class DeviceInterface:
    def __init__(self, platformtools):
        self.platformtools = platformtools
    
    def create_file(self, path, name_with_extesion, content, device_id=""):
        raise NotImplemented()

    def delete_file(self, path, device_id=""):
        raise NotImplemented()

    def rename_file(self, path, name):
        raise NotImplemented()

    def move_file(self, path, new_path):
        raise NotImplemented()

    def get_all_serials(self):
        raise NotImplemented()

    def get_device_info(self, device_id=""):
        raise NotImplemented()

    def start_adb_as_tcpip(self, port):
        raise NotImplemented()
     
    def connect_device(self, device_ip, port):
        raise NotImplemented()

    def disconnect_device(self, device_ip, port):
        raise NotImplemented()
    
    def kill_server(self):
        raise NotImplemented()
    
    def is_file(self, path):
        raise NotImplemented()
    
    def is_dir(self, path):
        raise NotImplemented()
    
    def get_tool(self, tool):
        if os.path.exists(self.platformtools):
            return os.path.join(self.platformtools, tool)

    def _execute_comand(self, tool, *args, device_id=""):
        targs = ""
        for arg in args:
            targs += " "
            targs += str(arg)
        command = ""
        if device_id == "":
            command = f"{tool} {targs}"
        else:
            command = f"{tool} -s {device_id} {targs}"
        out = subprocess.run(command, shell=True, capture_output=True)
        return out
    
    def _execute_shell_command(self, command, device_id=""):
        tool = self.get_tool("adb")
        args = ""
        if device_id == "":
            args = f"{tool} shell '{command}'"
        else:
            args = f"{tool} -s {device_id} shell '{command}'"
        out = subprocess.run(args, shell=True, capture_output=True)
        return out

