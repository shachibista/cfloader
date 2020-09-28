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

    reader: readers.Reader

    if isinstance(path, pathlib.Path) or isinstance(path, str):
        reader = readers.Path(path)

    if isinstance(path, dict):
        reader = readers.Dict(path)

    return Loader(reader.read_config())