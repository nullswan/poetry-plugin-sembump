from os import path, walk
from typing import Generator

TARGET_FILE = "pyproject.toml"


def find_pyproject_files(root_directory: str) -> Generator[str, None, None]:
    for root, _, files in walk(root_directory):
        if TARGET_FILE not in files:
            continue

        full_path = path.join(root, TARGET_FILE)
        yield full_path
