class FsHandler:
    def __init__(self, path_base):
        self.path_base = path_base
    
    def create_file(self, path, content):
        pass
    
    def modified_file(self, path, content):
        pass
    
    def move_file(self, path, new_path):
        pass
    
    def rename_file(self, path, name):
        pass
    
    def file_exists(self, path):
        pass
    
    def is_file(self, file_path):
        pass

    def get_file_content(self, path):
        pass
    
    def delete_file(self, path):
        pass
    
    def create_dir(self, path):
        pass
    
    def move_dir(self, path, new_path):
        pass
    
    def rename_dir(self, path, name):
        pass
    
    def dir_exists(self, path):
        pass

    def is_dir(self, dir_path):
        pass
    
    def delete_dir(self, path):
        pass

    def list_files(self, path=""):
        pass

