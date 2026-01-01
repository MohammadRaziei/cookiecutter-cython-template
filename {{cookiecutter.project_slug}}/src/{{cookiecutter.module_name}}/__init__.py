"""{{ cookiecutter.package_description }}"""

__version__ = "{{ cookiecutter.version }}"

# Import the compiled Cython module
from .{{ cookiecutter.module_name }} import hello_world, Calculator

__all__ = ["hello_world", "Calculator"]