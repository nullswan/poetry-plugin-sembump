import os
from typing import Generator

TARGET_FILE = "pyproject.toml"


def find_pyproject_files(
    root_directory: str,
) -> Generator[str, None, None]:
    for root, directories, files in os.walk(root_directory, topdown=True):
        directories[:] = [d for d in directories if not d.startswith(".")]

        if TARGET_FILE in files:
            yield os.path.join(root, TARGET_FILE)
