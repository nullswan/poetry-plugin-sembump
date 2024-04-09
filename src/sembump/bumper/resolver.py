import requests

from sembump.bumper.exceptions import UnknownVersion

PYPI_URL = "https://pypi.org/pypi"


def pypi_get_latest_package_version(package_name: str) -> str:
    response = requests.get(f"{PYPI_URL}/{package_name}/json", timeout=5)
    if response.status_code == 200:
        data = response.json()
        version = data["info"]["version"]
        assert isinstance(version, str), "Version must be a string"

        return version

    raise UnknownVersion(f"Failed to get the latest version for {package_name}")
