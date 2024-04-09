import requests

from sembump.bumper.exceptions import UnknownVersionError

PYPI_URL = "https://pypi.org/pypi"
PYPI_TIMEOUT = 5


def pypi_get_latest_package_version(package_name: str) -> str:
    pypi_url = f"{PYPI_URL}/{package_name}/json"

    try:
        response = requests.get(pypi_url, timeout=PYPI_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        raise UnknownVersionError(f"Request to PyPI failed: {e}")

    try:
        data = response.json()
        version = data["info"]["version"]
    except (ValueError, KeyError):
        raise UnknownVersionError(
            f"Response data is invalid or does not contain version info for {package_name}"
        )

    if not isinstance(version, str):
        raise UnknownVersionError(f"Version format is invalid for {package_name}")

    return version
