"""{{ cookiecutter.package_description }}"""

__version__ = "{{ cookiecutter.version }}"

# Import the compiled Cython module
from .{{ cookiecutter.module_name }} import Curl, CurlResponse

__all__ = ["Curl", "CurlResponse"]