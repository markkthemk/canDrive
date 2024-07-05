from pathlib import Path
from typing import AnyStr


def get_relative_path(relative_path: str) -> Path:
    base_path = Path(__file__).parents[1]
    return Path(base_path / Path(relative_path))


def read_file(path: str) -> AnyStr:
    relative_path = get_relative_path(path)
    with open(relative_path, "r") as f:
        return f.read()
