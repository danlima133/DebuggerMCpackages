import os
import re
import services.adb.interfaces.AdbInterface as AdbInterface

class GenericAdb(AdbInterface.DeviceInterface):
    def __init__(self, platformtools):
        super().__init__(platformtools)
    
    def start_adb_as_tcpip(self, port):
        adb = self.get_tool("adb")
        out = self._execute_comand(adb, "tcpip", port)
        if out.returncode != 0:
            return out.stderr.decode()
        return out.stdout.decode()
    
    def kill_server(self):
        adb = self.get_tool("adb")
        self._execute_comand(adb, "kill-server")
    
    def connect_device(self, device_ip, port):
        adb = self.get_tool("adb")
        out = self._execute_comand(adb, "connect", f"{device_ip}:{port}")
        if out.returncode != 0:
            raise Exception("Device not anvaliable")
    
    def disconnect_device(self, device_ip, port):
        adb = self.get_tool("adb")
        out = self._execute_comand(adb, "disconnect", f"{device_ip}:{port}")
        if out.returncode != 0:
            raise Exception("Device not anvaliable")
    
    def is_file(self, path):
        out = self._execute_shell_command(f"ls -l {path}")
        if out.returncode == 0:
            return out.stdout.decode()[0] == "-"
        raise Exception(f"Can't check '{path}'")
    
    def is_dir(self, path):
        out = self._execute_shell_command(f"ls -l {path}")
        if out.returncode == 0:
            return out.stdout.decode()[0] == "t"
        raise Exception(f"Can't check '{path}'")

    def create_file(self, path, name_with_extesion, content, device_id=""):
        npath = os.path.join("sdcard", path, name_with_extesion)
        out = self._execute_shell_command(f"echo {content} > {npath}", device_id=device_id)
        if out.returncode != 0:
            raise Exception(f"Can't create file '{name_with_extesion}' in '{path}'")
    
    def delete_file(self, path, device_id=""):
        npath = os.path.join("sdcard", path)
        arg = "rm"
        if self.is_dir(npath):
            arg = "rm -r"
        out = self._execute_shell_command(f"{arg} {npath}")
        if out.returncode != 0:
            raise Exception(f"Can't delete file '{npath}'")
    
    def rename_file(self, path, name):
        npath = os.path.join("sdcard", path)
        components = npath.split("/")
        npath_renamed = npath.replace(f"/{components[-1]}", f"/{name}")
        out = self._execute_shell_command(f"mv {npath} {npath_renamed}")
        if out.returncode != 0:
            raise Exception(f"Can't rename file '{npath}' to '{name}'")
    
    def move_file(self, path, new_path):
        npath = os.path.join("sdcard", path)
        npath_target = os.path.join("sdcard", new_path)
        out = self._execute_shell_command(f"mv {npath} {npath_target}")
        if out.returncode != 0:
            raise Exception(f"Can't move file '{npath}' to '{npath_target}'")
    
    def get_all_serials(self):
        tool = self.get_tool("adb")
        out = self._execute_comand(tool, "devices")
        stdout = out.stdout.decode()
        lines = stdout.splitlines()[1:]
        serials = []
        for line in lines:
            if line != "":
                info = re.sub(r"[\t]", "/", line)
                serial = info.split("/")[0]
                serials.append(serial)
        return tuple(serials)
    
    def get_device_info(self, device_id=""):
        out_device_name = self._execute_shell_command("getprop ro.product.model", device_id)
        out_manufacturer = self._execute_shell_command("getprop ro.product.manufacturer", device_id)
        out_android_version = self._execute_shell_command("getprop ro.build.version.release", device_id)
        device_name = re.sub(r"[\n]", "", out_device_name.stdout.decode())
        manufacturer = re.sub(r"[\n]", "", out_manufacturer.stdout.decode())
        android_version = re.sub(r"[\n]", "", out_android_version.stdout.decode())
        return (
            device_name, 
            manufacturer, 
            android_version
        )