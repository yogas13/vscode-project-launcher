# Contributing to VS Code Project Launcher

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bug fix
4. Make your changes
5. Test your changes thoroughly
6. Submit a pull request

## Development Environment

### Prerequisites

- Python 3.7 or higher
- VS Code (for testing)
- Git
- Linux environment (preferred)

### Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/vscode-project-launcher.git
cd vscode-project-launcher

# Install dependencies
./setup_launcher.sh

# Run the application
./launch.sh
```

## Code Style

- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Add docstrings to all classes and functions
- Keep functions small and focused
- Use type hints where appropriate

## Testing

Currently, the project relies on manual testing. We welcome contributions to add automated tests:

- Unit tests for core functionality
- Integration tests for workspace scanning
- GUI tests for the interface

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with clear, descriptive commits
3. Update documentation as needed
4. Ensure your code follows the style guidelines
5. Test your changes thoroughly
6. Submit a pull request with a clear description

### Pull Request Template

Please include:
- Description of changes
- Type of change (bug fix, feature, documentation, etc.)
- Testing performed
- Screenshots (for UI changes)

## Areas for Contribution

### High Priority
- Unit and integration tests
- Windows/macOS support
- Performance optimizations
- Accessibility improvements

### Medium Priority
- Additional workspace file formats
- Themes and customization
- Workspace templates
- Integration with other editors

### Low Priority
- Advanced search features
- Workspace synchronization
- Plugin system
- Advanced configuration options

## Bug Reports

When reporting bugs, please include:
- Operating system and version
- Python version
- VS Code version
- Steps to reproduce
- Expected vs actual behavior
- Any error messages or logs

## Feature Requests

For feature requests, please:
- Check if the feature already exists
- Describe the use case clearly
- Explain how it would benefit users
- Consider implementation complexity

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help maintain a positive environment

## Questions?

Feel free to open an issue for any questions about contributing!