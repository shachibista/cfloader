import json
import pathlib
from typing import Union
from abc import ABC, abstractmethod

PathLike = Union[pathlib.Path, str]

def _get_path(_path: PathLike) -> pathlib.Path:
    if isinstance(_path, str):
        return pathlib.Path(_path)

    return _path

class Reader(ABC):
    @abstractmethod
    def read_config(self) -> dict:
        pass

class Path(Reader):
    path: pathlib.Path

    def __init__(self, path: PathLike):
        self.path = _get_path(path)

    def read_config(self):
        return json.loads(self.path.read_text())

class Archive(Reader):
    path: pathlib.Path
    config_filepath: str

    def __init__(self, path: PathLike, config_filepath: str = "config.json"):
        self.path = _get_path(path)
        self.config_filepath = config_filepath

    def _read_zip(self):
        import zipfile

        with zipfile.ZipFile(self.path, "r") as archive:
            with archive.open(self.config_filepath) as config_file:
                return json.load(config_file)
    
    def _read_tar(self, compression: str = ""):
        import tarfile

        with tarfile.open(self.path, ":".join(["r", compression])) as archive:
            config_fileinfo = archive.getmember(self.config_filepath)
            config_file = archive.extractfile(config_fileinfo)

            if config_file is None:
                raise Exception(f"configuration file {self.config_filepath} not found in archive {self.path}")

            return json.loads(config_file.read())

    def read_config(self):
        suffix = "".join(self.path.suffixes).lower()

        if suffix == ".zip":
            return self._read_zip()
        elif suffix == ".tar":
            return self._read_tar()
        elif suffix == ".tar.gz":
            return self._read_tar("gz")
        elif suffix == ".tar.xz":
            return self._read_tar("xz")
        else:
            raise Exception(f"unsupported archive format {suffix}")