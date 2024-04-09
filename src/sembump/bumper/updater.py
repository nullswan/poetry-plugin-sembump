from os import path

import tomlkit
import tomlkit.exceptions
import tomlkit.items

from sembump.bumper.exceptions import UnprocessableProject
from sembump.bumper.resolver import pypi_get_latest_package_version

DependenciesT = tomlkit.items.Table


def load_dependencies(
    project: tomlkit.TOMLDocument,
    dependency_path: list[str],
) -> DependenciesT:
    try:
        dependencies: DependenciesT = project  # type: ignore[assignment]
        for key in dependency_path:
            dependencies = dependencies[key]  # type: ignore[assignment]
    except tomlkit.exceptions.TOMLKitError as e:
        raise UnprocessableProject("Failed to load dependencies") from e

    return dependencies


def update_versions_in_pyproject(
    project_path: str, dry: bool, dependency_path: list[str], dependency_type: str
) -> None:
    print(f"{project_path} Updating {dependency_type}...")
    project = read_project(project_path)
    dependencies = load_dependencies(project, dependency_path)
    updated_dependencies = update_dependencies(dependencies)

    project_ref = project
    for key in dependency_path[:-1]:
        project_ref = project_ref[key]  # type: ignore[assignment]

    project_ref[dependency_path[-1]] = updated_dependencies

    if not dry:
        save_project(project_path, project)
        print(f"{project_path} {dependency_type} have been updated.")


def update_dependencies(
    dependencies: DependenciesT,
) -> DependenciesT:
    for package, version in dependencies.items():
        if package in ("python", "poetry"):
            continue

        current_version = (
            version if isinstance(version, str) else version.get("version")
        )
        if not current_version:
            continue

        latest_version = pypi_get_latest_package_version(package)
        if not latest_version or latest_version <= current_version:
            continue

        print(f"Updating {package}: {current_version} -> {latest_version}")
        if isinstance(version, str):
            dependencies[package] = latest_version
        else:
            dependencies[package]["version"] = latest_version  # type: ignore[index]

    return dependencies


def save_project(
    project_path: str,
    project: tomlkit.TOMLDocument,
) -> None:
    with open(project_path, "w", encoding="utf-8") as file:
        file.write(tomlkit.dumps(project))


def read_project(
    project_path: str,
) -> tomlkit.TOMLDocument:
    assert path.exists(project_path), f"{project_path} does not exist."

    with open(project_path, "r", encoding="utf-8") as file:
        pyproject = tomlkit.parse(file.read())

    return pyproject
