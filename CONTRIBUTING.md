# Contributing to BRAID-DSPy

Thank you for your interest in contributing to BRAID-DSPy! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue using the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md). Include:

- A clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)
- Code examples and error messages if applicable

### Suggesting Features

Feature requests are welcome! Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md) to:

- Describe the feature clearly
- Explain the motivation and use case
- Provide examples of how it would be used

### Pull Requests

1. **Fork the repository** and create a new branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Write or update tests** for your changes

4. **Ensure all tests pass** locally:
   ```bash
   pytest tests/ -v
   ```

5. **Run code formatting**:
   ```bash
   black braid/ tests/ examples/
   ```

6. **Run type checking**:
   ```bash
   mypy braid/
   ```

7. **Update documentation** if needed

8. **Commit your changes** with clear commit messages:
   ```bash
   git commit -m "Add feature: description of changes"
   ```

9. **Push to your fork** and create a Pull Request

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip or uv

### Installation

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/braid-dspy.git
   cd braid-dspy
   ```

2. Install in development mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

   Or using uv:
   ```bash
   uv pip install -e ".[dev]"
   ```

### Running Tests

Run all tests:
```bash
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ -v --cov=braid --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_module.py -v
```

### Code Style

We use [Black](https://black.readthedocs.io/) for code formatting with a line length of 100.

Format code:
```bash
black braid/ tests/ examples/
```

Check formatting without making changes:
```bash
black --check braid/ tests/ examples/
```

### Type Checking

We use [mypy](https://mypy.readthedocs.io/) for static type checking.

Run type checking:
```bash
mypy braid/
```

### Pre-commit Hooks

We recommend using pre-commit hooks to ensure code quality:

```bash
pip install pre-commit
pre-commit install
```

This will automatically run black, mypy, and tests before each commit.

## Code Standards

### Python Style

- Follow PEP 8 guidelines
- Use Black for formatting (line length: 100)
- Add type hints to function signatures
- Write docstrings for all public functions and classes

### Documentation

- Update docstrings when adding or modifying functions
- Update README.md if adding new features
- Update CHANGELOG.md for user-facing changes
- Keep API documentation in `docs/` up to date

### Testing

- Write tests for new features
- Aim for good test coverage
- Use descriptive test names
- Follow the existing test structure

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in imperative mood (e.g., "Add", "Fix", "Update")
- Reference issue numbers when applicable: "Fix #123"

Example:
```
Add support for custom GRD validation

- Added validate_grd parameter to BraidReasoning
- Updated parser to handle validation errors
- Added tests for validation logic

Closes #45
```

## Project Structure

```
braid-dspy/
├── braid/              # Main package
│   ├── __init__.py
│   ├── module.py      # Core BRAID module
│   ├── parser.py      # Mermaid parser
│   ├── generator.py   # GRD generator
│   ├── optimizer.py   # BRAID optimizer
│   ├── signatures.py  # DSPy signatures
│   └── utils.py       # Utility functions
├── tests/             # Test suite
├── examples/           # Example scripts
├── docs/              # Documentation
└── .github/           # GitHub templates and workflows
```

## Review Process

1. All pull requests require at least one review
2. CI checks must pass (tests, linting, type checking)
3. Code should follow project standards
4. Documentation should be updated as needed

## Questions?

- Check existing [Issues](https://github.com/ziyacivan/braid-dspy/issues)
- Start a [Discussion](https://github.com/ziyacivan/braid-dspy/discussions)
- Create a [Question issue](.github/ISSUE_TEMPLATE/question.md)

Thank you for contributing to BRAID-DSPy!

