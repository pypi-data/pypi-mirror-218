import pathlib
from pathlib import Path


def mkdir(path):
    pathlib.Path(path).mkdir(exist_ok=True)