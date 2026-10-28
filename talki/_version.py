"""This package's version, and the `User-Agent` every request carries.

`__version__` must equal `version` in pyproject.toml, which a test checks; the
release workflow checks that the tag names the latter.
"""

import platform

import httpx

__version__ = "0.3.0b1"

USER_AGENT = f"talki-python/{__version__} python/{platform.python_version()} httpx/{httpx.__version__}"
