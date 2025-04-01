from hashlib import sha256
from modules.vfs.handlers import FsHandler
from modules.vfs.contracts import LocalHandler

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
    
    def has_item(self, path):
        return self.core.get(path, {})
    
    def get_component(self, path):
        return self.core.get(path, {})

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
    def __init__(self, input_handler, out_handler):
        self.input_handle: FsHandler.FsHandler = input_handler
        self.out_handle: FsHandler.FsHandler = out_handler
        self.vcore = vCore()
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
            vCore.Operations.CREATED_FILE: self.out_handle.create_file,
            vCore.Operations.MODIFIED_FILE: self.out_handle.modified_file,
            vCore.Operations.MOVED_FILE: self.out_handle.move_file,
            vCore.Operations.RENAMED_FILE: self.out_handle.rename_file,
            vCore.Operations.DELTED_FILE: self.out_handle.delete_file,
            vCore.Operations.CREATED_DIR: self.out_handle.create_dir,
            vCore.Operations.MOVED_DIR: self.out_handle.move_dir,
            vCore.Operations.RENAMED_DIR: self.out_handle.rename_dir,
            vCore.Operations.DELTED_DIR: self.out_handle.delete_dir
        }
        for sync in self.sync_buffer:
            op = sync["op"]
            args = sync["args"]
            call = call_ref[op]
            call(*args) 
        self.sync_buffer.clear()

    def mount(self):
        paths = self.vcore.get_paths()
        if len(paths) != 0:
            dirs = self.out_handle.list_files()
            for dir in dirs:
                if self.out_handle.is_dir(dir):
                    self.out_handle.delete_dir(dir)
            files = self.out_handle.list_files()
            for file in files:
                self.out_handle.delete_file(file)
            for item in paths:
                if self.input_handle.is_file(item):
                    content = self.input_handle.get_file_content(item)
                    self.out_handle.create_file(item, content)
                    continue
                self.out_handle.create_dir(item)    
    
    def mount_vfs(self):
        files = self.input_handle.list_files()
        for file in files:
            if self.input_handle.is_file(file):
                content = self.input_handle.get_file_content(file)
                self.vcore.create_file(file, content.encode())
                continue
            self.vcore.create_dir(file)
    
    def verify_sync(self):
        items = self.vcore.get_paths()
        items_buffer = []
        for item in items:
            if not self.out_handle.is_dir(item):
                if not self.out_handle.file_exists(item):
                    items_buffer.append(item)
                else:
                    content = self.out_handle.get_file_content(item)
                    sing = sha256(content.encode()).hexdigest()
                    hashv = self.vcore.get_component(item)["hash"]
                    if sing != hashv:
                        items_buffer.append(item)

            else:
                if not self.out_handle.dir_exists(item):
                    items_buffer.append(item)
        return items_buffer

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
    
    def delete_file(self, path):
        self._add_opearation(self.vcore.delete_file,
                                path
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
