from os import path, walk
from typing import Generator

TARGET_FILE = "pyproject.toml"


def find_pyproject_files(
    root_directory: str,
) -> Generator[str, None, None]:
    for root, directory, files in walk(root_directory):
        for subdirectory in directory:
            if subdirectory.startswith("."):
                continue
            yield from find_pyproject_files(path.join(root, subdirectory))

        if TARGET_FILE not in files:
            continue

        full_path = path.join(root, TARGET_FILE)
        yield full_path
