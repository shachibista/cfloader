import json
import pickle
import pathlib
import zipfile
from typing import Union, List, Any

from mloader.loader import Loader
import mloader.readers as readers

def open(path: Union[pathlib.Path, str, dict, readers.Reader]):
    if isinstance(path, readers.Reader):
        return Loader(path.read_config())

    if isinstance(path, pathlib.Path) or isinstance(path, str):
        reader = readers.Path(path)

    if isinstance(path, dict):
        reader = readers.Dict(path)

    return Loader(reader.read_config())

def save(path: Union[pathlib.Path, str], artefacts: dict):
    with zipfile.ZipFile(path, "w") as archive:
        for filename, data in artefacts:
            if isinstance(data, pathlib.Path):
                archive.write(data, filename)
            elif isinstance(data, Loader):
                archive.writestr(filename, json.dumps(data.config))
            elif isinstance(data, dict):
                archive.writestr(filename, json.dumps(data))
            else:
                archive.writestr(filename, pickle.dumps(data))