from hashlib import sha256
from modules.vfs.handlers import SyncHandler, MountHandler, SyncValidatorHandler

class vCore:
    
    class VContentType:
        DIR="dir"
        FILE="file"
    
    class Operations:
        CREATED_FILE="created_file"
        MODIFIED_FILE="modified_file"
        RENAMED_FILE="renamed_file"
        MOVED_FILE="moved_file"
        DELTED_FILE="deleted_file"
        CREATED_DIR="created_dir"
        RENAMED_DIR="renamed_dir"
        MOVED_DIR="moved_dir"
        DELTED_DIR="deleted_dir"
    
    def __init__(self):
        self.core = {}
    
    def _operation(self, operation, *args):
        return {
            "op": operation,
            "args": args
        }
    
    def get_paths(self):
        return tuple(self.core.keys())
    
    def get_components(self):
        return tuple(self.core.values())

    def create_file(self, path, content):
        self.core[path] = {
            "hash": sha256(content).hexdigest(),
            "type": self.VContentType.FILE
        }
        return self._operation(self.Operations.CREATED_FILE, path, content.decode())
    
    def modified_file(self, path, content):
        self.core[path]["hash"] = sha256(content).hexdigest()
        return self._operation(self.Operations.MODIFIED_FILE, path, content.decode())
    
    def move_file(self, path, new_path):
        vcontent = self.core.pop(path)
        self.core[new_path] = vcontent
        return self._operation(self.Operations.MOVED_FILE, path, new_path)
    
    def rename_file(self, path, name):
        components = path.split("/")
        last_component = components[-1]
        new_path = path.replace(f"/{last_component}", name)
        vcontent = self.core.pop(path)
        self.core[new_path] = vcontent
        return self._operation(self.Operations.RENAMED_FILE, path, name)
    
    def delete_file(self, path):
        self.core.pop(path)
        return self._operation(self.Operations.DELTED_FILE, path)
    
    def create_dir(self, path):
        components = path.split("/")
        dir_name = components[-1]
        sing = sha256(dir_name.encode()).hexdigest()
        self.core[path] = {
            "hash": sing,
            "type": self.VContentType.DIR
        }
        return self._operation(self.Operations.CREATED_DIR, path)
    
    def move_dir(self, path, new_path):
        vcontent = self.core.pop(path)
        self.core[new_path] = vcontent
        return self._operation(self.Operations.MOVED_FILE, path, new_path)
    
    def rename_dir(self, path, name):
        components = path.split("/")
        last_component = components[-1]
        new_path = path.replace(f"/{last_component}", name)
        sing = sha256(name.encode()).hexdigest()
        vcontent = self.core.pop(path)
        vcontent["hash"] = sing
        self.core[new_path] = vcontent
        return self._operation(self.Operations.RENAMED_DIR, path, name)
    
    def delete_dir(self, path):
        self.core.pop(path)
        return self._operation(self.Operations.DELTED_DIR, path)

class vFS:
    def __init__(self, sync_handle, mount_handle):
        self.vcore = vCore()
        self.sync_handle: SyncHandler.SyncHandler = sync_handle
        self.mount_hadle: MountHandler.MountHandler = mount_handle
        self.operations = []
        self.sync_buffer = []
        self.history = []
    
    def _add_opearation(self, function, *args):
        self.operations.append((function, *args))
    
    def flush_operations(self):
        for operation in self.operations:
            function = operation[0]
            args = operation[1:]
            op = function(*args)
            self.sync_buffer.append(op)
            self.history.append(op)
        self.operations.clear()
    
    def reflect(self):
        call_ref = {
            vCore.Operations.CREATED_FILE: self.sync_handle.create_file,
            vCore.Operations.MODIFIED_FILE: self.sync_handle.modified_file,
            vCore.Operations.MOVED_FILE: self.sync_handle.move_file,
            vCore.Operations.RENAMED_FILE: self.sync_handle.rename_file,
            vCore.Operations.DELTED_FILE: self.sync_handle.delete_file,
            vCore.Operations.CREATED_DIR: self.sync_handle.create_dir,
            vCore.Operations.MOVED_DIR: self.sync_handle.move_dir,
            vCore.Operations.RENAMED_DIR: self.sync_handle.rename_dir,
            vCore.Operations.DELTED_DIR: self.sync_handle.delete_dir
        }
        for sync in self.sync_buffer:
            op = sync["op"]
            args = sync["args"]
            call = call_ref[op]
            call(*args) 
        self.sync_buffer.clear()

    def mount(self):
        paths = self.vcore.get_paths()
        components = self.vcore.get_components()
        self.sync_handle.dellete_all()
        for idx, path in enumerate(paths):
            component = components[idx]
            match component["type"]:
                case vCore.VContentType.DIR:
                    self.sync_handle.create_dir(path)
                case vCore.VContentType.FILE:
                    content = self.mount_hadle.get_file_content(path)
                    self.sync_handle.create_file(path, content)
    
    def create_file(self, path, content):
        bytes = content.encode()
        self._add_opearation(self.vcore.create_file,
                                path,
                                bytes
                            )
    
    def modified_file(self, path, content):
        bytes = content.encode()
        self._add_opearation(self.vcore.modified_file,
                                path,
                                bytes
                            )
    
    def move_file(self, path, new_path):
        self._add_opearation(self.vcore.move_file,
                                path,
                                new_path
                            )
    
    def rename_file(self, path, name):
        self._add_opearation(self.vcore.rename_file,
                                path,
                                name
                            )
    
    def create_dir(self, path):
        self._add_opearation(self.vcore.create_dir,
                                path
                            )
    
    def move_dir(self, path, new_path):
        self._add_opearation(self.vcore.move_dir,
                                path,
                                new_path
                            )
    
    def rename_dir(self, path, name):
        self._add_opearation(self.vcore.rename_dir,
                                path,
                                name
                            )

    def delete_dir(self, path):
        self._add_opearation(self.vcore.delete_dir,
                                path
                            )
