# Cookiecutter Cython Template

A modern, opinionated cookiecutter template for creating Cython projects with scikit-build, CMake, and comprehensive tooling.

## Features

- **Cython Integration**: Pre-configured for Cython development with scikit-build
- **CMake Build System**: Includes CMake for complex dependency management
- **Modern Python Packaging**: Uses `pyproject.toml` with scikit-build-core
- **CLI Support**: Optional command-line interface with Click
- **Testing**: Pre-configured with pytest
- **Documentation**: Basic documentation structure
- **CI/CD**: GitHub Actions workflow for building and publishing
- **Code Quality**: Includes black, isort, and flake8 configurations

## Usage

### Prerequisites

Make sure you have cookiecutter installed:

```bash
pip install cookiecutter
```

### Creating a New Project

```bash
cookiecutter gh:mohammadraziei/cookiecutter-cython-template
```

Or if you have the template locally:

```bash
cookiecutter /path/to/cookiecutter-cython-template
```

### Variables

The template prompts for the following variables:

- `project_name`: Your project's human-readable name (e.g. "My Cython Project")
- `package_description`: A short description of the project
- `version`: Initial version number (default: "0.1.0")
- `author_name`: Your name
- `author_email`: Your email address
- `github_username`: Your GitHub username
- `license`: License type (default: "MIT")
- `python_version`: Python version requirement (default: ">=3.8")
- `has_cli`: Whether to include CLI functionality (default: true)
- `use_cmake`: Whether to use CMake (default: true)
- `cython_language_level`: Cython language level (default: "3")

The template automatically computes:
- `project_slug`: URL-friendly version (e.g., "my-cython-project") from project_name
- `module_name`: Python module name (e.g., "my_cython_project") from project_name

## Generated Project Structure

```
my-project/
├── .github/
│   └── workflows/
│       └── wheel.yml          # GitHub Actions CI/CD
├── cmake/
│   ├── FindCython.cmake       # Find Cython module
│   └── UseCython.cmake        # Use Cython module
├── docs/
│   └── index.rst              # Documentation index
├── src/
│   └── my_project/            # Python package
│       ├── __init__.py        # Package init
│       ├── __main__.py        # CLI entry point (if enabled)
│       └── my_project.pyx     # Main Cython module
├── tests/
│   └── test_my_project_basic.py # Basic tests
├── .gitignore                 # Git ignore rules
├── CMakeLists.txt             # CMake build configuration
├── LICENSE.txt                # Project license
├── pyproject.toml             # Python build configuration
├── README.md                  # Project README
└── requirements.txt           # Python dependencies
```

## Development

### Building the Project

```bash
pip install -e .
```

### Building Wheels

```bash
python -m build
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
isort .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## Acknowledgments

- Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
- Uses [scikit-build-core](https://github.com/scikit-build/scikit-build-core) for building
- Inspired by various Python packaging best practices