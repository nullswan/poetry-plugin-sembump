# Sembump

Poetry plugin to semantically bump the version of your project.

## Installation

The easiest way to install the export plugin is via the self add command of Poetry.

```
poetry self add poetry-plugin-sembump
```

If you used pipx to install Poetry you can add the plugin via the pipx inject command.

```
pipx inject poetry poetry-plugin-sembump
```

Otherwise, if you used pip to install Poetry you can add the plugin packages via the pip install command.

```
pip install poetry-plugin-sembump
```

## Usage

```
poetry bump -h

Description:
  Bump the version of the project dependencies.

Usage:
  bump [options]

Options:
  -r, --recursive            Bump the dependencies of all pyproject.toml files found in subdirectories.
  -d, --dry-run              Do not write any changes to the files.
  -D, --dev-dependencies     Update dev dependencies as well.
```
