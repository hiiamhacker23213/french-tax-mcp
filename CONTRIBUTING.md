# Contributing to French Tax MCP Server

Thank you for your interest in contributing to the French Tax MCP Server! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use the issue templates** when available
3. **Provide detailed information** including:
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages and stack traces

### Suggesting Features

1. **Check existing feature requests** to avoid duplicates
2. **Describe the use case** and why it would be valuable
3. **Provide examples** of how the feature would work
4. **Consider implementation complexity** and maintenance burden

### Code Contributions

1. **Fork the repository** and create a feature branch
2. **Follow the coding standards** (see below)
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Submit a pull request** with a clear description

## 🛠️ Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- A text editor or IDE

### Local Development

```bash
# Clone your fork
git clone https://github.com/your-username/french-tax-mcp.git
cd french-tax-mcp

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=french_tax_mcp --cov-report=html

# Run specific test file
pytest tests/test_scrapers.py

# Run tests matching a pattern
pytest -k "test_tax_brackets"
```

### Code Quality

```bash
# Format code
black french_tax_mcp/
isort french_tax_mcp/

# Check formatting
black --check french_tax_mcp/
isort --check-only french_tax_mcp/

# Lint code
flake8 french_tax_mcp/

# Type checking
mypy french_tax_mcp/
```

## 📝 Coding Standards

### Python Style

- Follow **PEP 8** style guidelines
- Use **Black** for code formatting (line length: 100)
- Use **isort** for import sorting
- Use **type hints** for all functions and methods
- Write **docstrings** for all public functions, classes, and modules

### Code Organization

- Keep functions focused and small
- Use descriptive variable and function names
- Separate concerns into appropriate modules
- Follow the existing project structure

### Documentation

- Update README.md for user-facing changes
- Add docstrings following Google style
- Include examples in docstrings when helpful
- Update type hints when changing function signatures

### Testing

- Write unit tests for all new functionality
- Use descriptive test names that explain what is being tested
- Mock external dependencies (web requests, file system)
- Aim for high test coverage (>90%)

## 🏗️ Project Structure

```
french-tax-mcp/
├── french_tax_mcp/           # Main package
│   ├── constants.py          # All constants and configuration
│   ├── server.py            # MCP server implementation
│   ├── scrapers/            # Web scrapers
│   ├── analyzers/           # Tax calculators
│   ├── static/templates/    # Report templates
│   └── report_generator.py  # Report generation
├── tests/                   # Test files
├── scripts/                 # Development scripts
├── .github/workflows/       # CI/CD workflows
└── docs/                    # Documentation (if needed)
```

## 🧪 Testing Guidelines

### Test Categories

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows

### Test Naming

```python
def test_calculate_income_tax_with_valid_input():
    """Test that income tax calculation works with valid input."""
    pass

def test_calculate_income_tax_raises_error_with_negative_income():
    """Test that income tax calculation raises error with negative income."""
    pass
```

### Mocking External Dependencies

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
@patch('french_tax_mcp.scrapers.base_scraper.AsyncClient')
async def test_scraper_handles_network_error(mock_client):
    """Test that scraper handles network errors gracefully."""
    mock_client.return_value.__aenter__.return_value.get.side_effect = Exception("Network error")
    # Test implementation
```

## 📋 Pull Request Process

### Before Submitting

1. **Ensure all tests pass**: `pytest`
2. **Check code quality**: `black --check . && isort --check . && flake8 . && mypy .`
3. **Update documentation** if needed
4. **Add tests** for new functionality
5. **Update CHANGELOG.md** if applicable

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainers
3. **Testing** in different environments
4. **Approval** and merge by maintainers

## 🎯 Areas for Contribution

### High Priority

- **New Tax Schemes**: Support for additional French tax schemes
- **Enhanced Scrapers**: Improve reliability and add new data sources
- **Better Error Handling**: More graceful error handling and recovery
- **Performance Optimization**: Caching improvements and faster calculations

### Medium Priority

- **Additional Calculators**: More tax calculation scenarios
- **Improved Documentation**: Better examples and guides
- **Internationalization**: Support for multiple languages
- **CLI Interface**: Command-line interface for direct usage

### Low Priority

- **Web Interface**: Simple web UI for testing
- **Export Formats**: Additional report formats (PDF, Excel)
- **Historical Data**: Support for historical tax rates
- **Advanced Analytics**: Tax optimization suggestions

## 🐛 Bug Reports

### Good Bug Report

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Call `calculate_income_tax(50000, 2.0)`
2. Observe the result
3. Expected X, got Y

**Environment**
- Python version: 3.10.5
- OS: macOS 13.0
- Package version: 1.0.0

**Additional Context**
Any other relevant information
```

### Security Issues

For security-related issues, please email directly instead of creating a public issue.

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the Apache License 2.0.

## 🙋‍♀️ Getting Help

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bug reports and feature requests
- **Code Review**: Ask questions in pull request comments

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

Thank you for contributing to the French Tax MCP Server! 🇫🇷