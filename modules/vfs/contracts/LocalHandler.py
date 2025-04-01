from pathlib import Path
from modules.vfs.handlers.FsHandler import FsHandler

class LocalHandler(FsHandler):
    def __init__(self, path_base):
        self.path_base = Path(path_base)

    def _resolve_path(self, path):
        return self.path_base.joinpath(path)

    def create_file(self, path, content):
        full_path = self._resolve_path(path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)

    def modified_file(self, path, content):
        full_path = self._resolve_path(path)
        if not full_path.is_file():
            raise FileNotFoundError(f"Arquivo não encontrado: {full_path}")
        full_path.write_text(content)

    def move_file(self, path, new_path):
        full_path = self._resolve_path(path)
        new_full_path = self._resolve_path(new_path)
        new_full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.rename(new_full_path)

    def rename_file(self, path, name):
        full_path = self._resolve_path(path)
        new_full_path = full_path.with_name(name)
        full_path.rename(new_full_path)

    def file_exists(self, path):
        full_path = self._resolve_path(path)
        return full_path.is_file()

    def is_file(self, file_path):
        full_path = self._resolve_path(file_path)
        return full_path.is_file()

    def get_file_content(self, path):
        full_path = self._resolve_path(path)
        if not full_path.is_file():
            raise FileNotFoundError(f"Arquivo não encontrado: {full_path}")
        return full_path.read_text()

    def delete_file(self, path):
        full_path = self._resolve_path(path)
        if full_path.is_file():
            full_path.unlink()

    def create_dir(self, path):
        full_path = self._resolve_path(path)
        full_path.mkdir(parents=True, exist_ok=True)

    def move_dir(self, path, new_path):
        full_path = self._resolve_path(path)
        new_full_path = self._resolve_path(new_path)
        new_full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.rename(new_full_path)

    def rename_dir(self, path, name):
        full_path = self._resolve_path(path)
        new_full_path = full_path.with_name(name)
        full_path.rename(new_full_path)

    def dir_exists(self, path):
        full_path = self._resolve_path(path)
        return full_path.is_dir()

    def is_dir(self, dir_path):
        full_path = self._resolve_path(dir_path)
        return full_path.is_dir()

    def delete_dir(self, path):
        full_path = self._resolve_path(path)
        if full_path.is_dir():
            for item in full_path.iterdir():
                if item.is_file():
                    item.unlink()
                else:
                    self.delete_dir(item)
            full_path.rmdir()

    def list_files(self, path=None):
        items_buffer = []
        full_path = self._resolve_path(path if path else self.path_base)
        if not full_path.is_dir():
            raise NotADirectoryError(f"Não é um diretório: {full_path}")
        for item in full_path.iterdir():
            if item.is_dir():
                items = self.list_files(item)
                items_buffer.append(str(item.relative_to(self.path_base)))
                items_buffer.extend(items)
                continue
            items_buffer.append(str(item.relative_to(self.path_base)))
        return items_buffer