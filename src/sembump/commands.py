from dataclasses import dataclass

from cleo.helpers import option
from poetry.console.commands.group_command import GroupCommand

from sembump.bumper.updater import (
    update_versions_in_pyproject,
)
from sembump.bumper.walker import find_pyproject_files


@dataclass
class BumpOptions:
    recursive: bool = False
    dry_run: bool = False
    dev_dependencies: bool = False


class BumpCommand(GroupCommand):
    name = "bump"
    description = "Bump the version of the project dependencies."

    options = [
        option(
            "recursive",
            "r",
            "Bump the dependencies of all pyproject.toml files found in subdirectories.",
            flag=True,
        ),
        option(
            "dry-run",
            "d",
            "Do not write any changes to the files.",
            flag=True,
        ),
        option(
            "dev-dependencies",
            "D",
            "Update dev dependencies as well.",
            flag=True,
        ),
    ]

    def handle(self) -> int:
        options = self.parse_options()

        targets = {"./pyproject.toml"}
        if options.recursive:
            targets.update(find_pyproject_files("."))

        dependency_paths = {
            "dependencies": ["tool", "poetry", "dependencies"],
            "dev_dependencies": ["tool", "poetry", "group", "dev", "dependencies"],
        }

        for target in targets:
            try:
                update_versions_in_pyproject(
                    target,
                    dry=options.dry_run,
                    dependency_path=dependency_paths["dependencies"],
                    dependency_type="dependencies",
                )

                if options.dev_dependencies:
                    update_versions_in_pyproject(
                        target,
                        dry=options.dry_run,
                        dependency_path=dependency_paths["dev_dependencies"],
                        dependency_type="dev dependencies",
                    )
            except Exception as e:
                self.line(f"Error: {e}")

        return 0

    def parse_options(self) -> BumpOptions:
        options = BumpOptions(
            recursive=self.option("recursive"),
            dry_run=self.option("dry-run"),
            dev_dependencies=self.option("dev-dependencies"),
        )

        self.line("Bumping the version of the project dependencies.")
        if options.recursive:
            self.line(
                "Using the recursive option, bumping the dependencies of all pyproject.toml files found in subdirectories."
            )
        if options.dry_run:
            self.line("Using the dry-run option, not writing any changes to the files.")
        if options.dev_dependencies:
            self.line(
                "Using the dev-dependencies option, updating dev dependencies as well."
            )

        return options
