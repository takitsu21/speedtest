# Contributing

We welcome contributions to **speedtest-cli**! This guide will help you get started with development, testing, and submitting your changes.

## Ways to Contribute

### Report Bugs

Found a bug? Please report it at [GitHub Issues](https://github.com/takitsu21/speedtest/issues).

When reporting a bug, include:

- Operating system name and version
- Python version
- speedtest-cli version (`speedtest-cli --version`)
- Steps to reproduce the bug
- Expected vs. actual behavior
- Error messages or logs
- Network configuration (if relevant)

### Suggest Features

Have an idea for a new feature? Open an issue with the `enhancement` label.

Include:

- Clear description of the feature
- Use cases and benefits
- Proposed implementation (if you have ideas)
- Any alternatives you've considered

### Fix Bugs

Look for issues tagged with `bug` and `help wanted`. These are great starting points!

### Implement Features

Check issues tagged with `enhancement` and `help wanted` for feature requests.

### Improve Documentation

Documentation improvements are always welcome:

- Fix typos or unclear explanations
- Add examples
- Improve API documentation
- Write tutorials or guides
- Translate documentation

### Submit Feedback

Share your experience using speedtest-cli, suggest improvements, or ask questions in [GitHub Discussions](https://github.com/takitsu21/speedtest/discussions).

## Development Setup

### Prerequisites

- **Git**: Version control
- **Python**: 3.9 or higher (3.12+ recommended)
- **uv**: Modern Python package manager ([install uv](https://github.com/astral-sh/uv))

### 1. Fork and Clone

Fork the repository on GitHub, then clone your fork:

```bash
git clone git@github.com:YOUR_USERNAME/speedtest.git
cd speedtest
```

### 2. Install Dependencies

Use `uv` to create a virtual environment and install all dependencies:

```bash
uv sync
```

This installs:
- Main dependencies (httpx, rich, etc.)
- Development dependencies (pytest, mypy, ruff, etc.)
- The package in editable mode

### 3. Install Pre-commit Hooks

Pre-commit hooks run linters and formatters automatically before each commit:

```bash
uv run pre-commit install
```

This ensures code quality standards are met before committing.

### 4. Verify Installation

Test that everything is set up correctly:

```bash
# Run speedtest-cli from source
uv run speedtest-cli --help

# Run tests
uv run pytest

# Run linters
uv run ruff check .
```

## Development Workflow

### 1. Create a Branch

Create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

**Branch Naming Conventions:**
- `feature/`: New features
- `fix/`: Bug fixes
- `docs/`: Documentation changes
- `refactor/`: Code refactoring
- `test/`: Test improvements

### 2. Make Changes

Edit the code as needed. Key directories:

```
speedtest/
├── speedtest_cloudflare_cli/
│   ├── core/              # Core functionality
│   │   ├── speedtest.py   # Main SpeedTest class
│   │   └── dashboard.py   # Dashboard generation
│   ├── models/            # Data models
│   │   ├── result.py      # Result dataclass
│   │   └── metadata.py    # Metadata model
│   └── main.py            # CLI entry point
├── tests/                 # Test files
├── docs/                  # Documentation
└── templates/             # Jinja2 templates
```

### 3. Add Tests

Write tests for your changes in the `tests/` directory:

```python
# tests/test_your_feature.py
import pytest
from speedtest_cloudflare_cli.core.speedtest import SpeedTest

def test_your_feature():
    """Test your new feature."""
    test = SpeedTest()
    # Your test code here
    assert result == expected
```

**Testing Guidelines:**
- Write tests for new features
- Ensure existing tests still pass
- Aim for good code coverage
- Use pytest fixtures for common setup
- Mock external API calls

### 4. Run Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=speedtest_cloudflare_cli

# Run specific test file
uv run pytest tests/test_your_feature.py

# Run specific test
uv run pytest tests/test_your_feature.py::test_specific_function
```

### 5. Code Quality Checks

Run code quality tools before committing:

```bash
# Run all checks (recommended)
make check

# Individual tools:
uv run ruff check .           # Linting
uv run ruff format .          # Formatting
uv run mypy .                 # Type checking
uv run deptry .               # Dependency checking
```

**Fix Issues Automatically:**

```bash
# Auto-fix linting issues
uv run ruff check --fix .

# Auto-format code
uv run ruff format .
```

### 6. Build and Test Locally

```bash
# Build the package
make build

# Install locally
uv pip install -e .

# Test the CLI
speedtest-cli --help
```

### 7. Update Documentation

If your changes affect user-facing functionality:

- Update relevant documentation in `docs/`
- Add docstrings to new functions/classes
- Update README.md if needed
- Add examples for new features

### 8. Commit Changes

```bash
git add .
git commit -m "feat: add awesome new feature"
```

**Commit Message Format:**

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build/tooling changes

**Examples:**
```
feat: add support for custom server selection
fix: correct latency calculation for IPv6
docs: update installation guide for Windows
refactor: simplify progress bar logic
test: add tests for upload functionality
```

### 9. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a pull request on GitHub.

## Code Style

### Python Code Style

We use **Ruff** for linting and formatting (configured in `pyproject.toml`):

**Key Guidelines:**

- Line length: 120 characters
- Use type hints for function signatures
- Write descriptive docstrings (Google style)
- Follow PEP 8 conventions
- Prefer f-strings for formatting
- Use meaningful variable names

**Example:**

```python
def calculate_speed(
    bytes_transferred: int,
    duration: float,
) -> float:
    """
    Calculate speed in Mbps from bytes and duration.
    
    Args:
        bytes_transferred: Number of bytes transferred
        duration: Time duration in seconds
    
    Returns:
        Speed in megabits per second (Mbps)
    """
    bits = bytes_transferred * 8
    megabits = bits / 1_000_000
    return megabits / duration if duration > 0 else 0.0
```

### Type Hints

All functions should have type hints:

```python
from typing import Optional
from speedtest_cloudflare_cli.models.result import Result

def run_test(silent: bool = False) -> Optional[Result]:
    """Run speed test."""
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Short description of function.
    
    Longer description if needed, explaining what the function
    does in more detail.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When param2 is negative
    """
    ...
```

## Testing

### Running Tests

```bash
# All tests
uv run pytest

# With coverage report
uv run pytest --cov=speedtest_cloudflare_cli --cov-report=html

# Specific test file
uv run pytest tests/core/test_speedtest.py

# Verbose output
uv run pytest -v

# Stop on first failure
uv run pytest -x
```

### Writing Tests

Use pytest fixtures and mocking:

```python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_speedtest():
    """Mock SpeedTest instance."""
    with patch('speedtest_cloudflare_cli.core.speedtest.SpeedTest') as mock:
        yield mock

def test_with_mock(mock_speedtest):
    """Test using mock."""
    mock_speedtest.return_value.run.return_value = Mock(download=100.0)
    # Your test code
```

### Test Coverage

Aim for good test coverage:

```bash
# Generate coverage report
uv run pytest --cov=speedtest_cloudflare_cli --cov-report=term-missing

# HTML report for detailed view
uv run pytest --cov=speedtest_cloudflare_cli --cov-report=html
open htmlcov/index.html
```

## Building Documentation

### Local Documentation Server

```bash
# Serve documentation locally
make docs

# Or manually
uv run mkdocs serve
```

Open http://127.0.0.1:8000 in your browser.

### Build Documentation

```bash
# Build static documentation
uv run mkdocs build

# Output in site/ directory
```

### Documentation Style

- Use clear, concise language
- Include code examples
- Add links to related pages
- Use admonitions for important notes
- Test all code examples

## Pull Request Process

### Before Submitting

**Checklist:**

- [ ] Tests pass locally (`uv run pytest`)
- [ ] Code passes linting (`uv run ruff check .`)
- [ ] Code is formatted (`uv run ruff format .`)
- [ ] Type checking passes (`uv run mypy .`)
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow conventions
- [ ] Branch is up to date with main

### PR Description

Include in your PR:

1. **Summary**: What does this PR do?
2. **Motivation**: Why is this change needed?
3. **Changes**: List of key changes
4. **Testing**: How was this tested?
5. **Screenshots**: If UI changes
6. **Related Issues**: Link to issues

**Template:**

```markdown
## Summary
Brief description of changes

## Motivation
Why is this change needed?

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] All tests pass

## Related Issues
Closes #123
```

### Review Process

1. **Automated Checks**: CI/CD runs tests and linters
2. **Code Review**: Maintainers review your code
3. **Feedback**: Address any requested changes
4. **Approval**: PR approved by maintainer
5. **Merge**: PR merged to main branch

### After Merge

- Delete your feature branch
- Update your fork
- Celebrate! 🎉

## Development Tools

### Makefile Commands

Convenient commands available via `make`:

```bash
make help          # Show all available commands
make install       # Install dependencies
make check         # Run all quality checks
make test          # Run tests
make build         # Build package
make docs          # Serve documentation
make clean         # Clean build artifacts
```

### Pre-commit Hooks

Configured in `.pre-commit-config.yaml`:

- **ruff**: Linting and formatting
- **mypy**: Type checking
- **trailing-whitespace**: Remove trailing spaces
- **end-of-file-fixer**: Ensure newline at EOF
- **check-yaml**: Validate YAML files

### Tox

Test across multiple Python versions:

```bash
# Test all Python versions (3.9-3.13)
tox

# Test specific version
tox -e py312

# List all environments
tox -l
```

## Release Process

Releases are automated via GitHub Actions:

1. Update version in code
2. Create git tag: `git tag v1.2.3`
3. Push tag: `git push origin v1.2.3`
4. GitHub Actions builds and publishes to PyPI
5. Docker images built and pushed to ghcr.io

## Getting Help

### Resources

- **Documentation**: https://takitsu21.github.io/speedtest/
- **Issues**: https://github.com/takitsu21/speedtest/issues
- **Discussions**: https://github.com/takitsu21/speedtest/discussions
- **Source Code**: https://github.com/takitsu21/speedtest

### Contact

- Open an issue for bugs or features
- Use discussions for questions
- Mention maintainers in PRs for review

## Code of Conduct

Please be respectful and constructive:

- Be welcoming to newcomers
- Respect different viewpoints
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy towards others

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors are recognized in:

- GitHub contributors page
- Release notes
- Project documentation

Thank you for contributing to speedtest-cli! 🚀
