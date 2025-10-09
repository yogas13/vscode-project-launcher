# Copilot Instructions for Project Launcher

## Project Overview
This is a project launcher tool that helps developers quickly initialize, configure, and manage development projects. The tool should streamline project setup workflows and provide consistent development environments.

## Architecture Guidelines

### Core Components
- **Project Templates**: Standardized project scaffolding for different tech stacks
- **Configuration Management**: Environment-specific settings and workspace configuration
- **Dependency Management**: Automated installation and version management
- **Development Workflow**: Build scripts, testing, and deployment automation

### Directory Structure (Expected)
```
src/
├── cli/              # Command-line interface
├── templates/        # Project templates and scaffolding
├── config/          # Configuration management
├── utils/           # Shared utilities
└── workflows/       # Development workflow automation

tests/               # Test suites
docs/               # Documentation
scripts/            # Build and automation scripts
```

## Development Patterns

### CLI Design
- Use a command-based structure (e.g., `projectlauncher create`, `projectlauncher init`)
- Implement interactive prompts for project configuration
- Support both interactive and non-interactive modes with flags
- Provide clear help text and examples for each command

### Template System
- Templates should be modular and composable
- Support variable substitution in template files
- Include post-generation hooks for custom setup steps
- Maintain templates for popular frameworks (React, Node.js, Python, etc.)

### Configuration Management
- Use YAML or JSON for configuration files
- Support environment-specific overrides
- Include validation for configuration schemas
- Provide sensible defaults for common use cases

## Key Workflows

### Project Creation
```bash
# Interactive mode
projectlauncher create

# Non-interactive with template
projectlauncher create --template react-typescript --name my-app
```

### Development Commands
- `projectlauncher dev` - Start development server
- `projectlauncher build` - Build project for production
- `projectlauncher test` - Run test suite
- `projectlauncher lint` - Run linting and formatting

## Dependencies and Tools

### Expected Tech Stack
- **CLI Framework**: Commander.js, Click (Python), or Cobra (Go)
- **Template Engine**: Handlebars, Mustache, or similar
- **Configuration**: YAML parser, JSON schema validation
- **File Operations**: Cross-platform file system utilities
- **Process Management**: Child process spawning for commands

### Package Management
- Support multiple package managers (npm, yarn, pnpm for Node.js projects)
- Detect and use the appropriate package manager for each project type
- Handle lock file generation and dependency caching

## Testing Strategy

### Unit Tests
- Test template rendering with various inputs
- Validate configuration parsing and merging
- Test CLI command parsing and validation

### Integration Tests
- End-to-end project creation workflows
- Template application and post-processing
- Cross-platform compatibility testing

### Test Organization
```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # End-to-end workflow tests
├── fixtures/       # Test data and mock templates
└── helpers/        # Test utilities and setup
```

## Error Handling

### User-Friendly Messages
- Provide clear error messages with suggested solutions
- Include context about what the tool was trying to do when the error occurred
- Offer troubleshooting steps for common issues

### Validation
- Validate user inputs before processing
- Check system requirements and dependencies
- Verify template integrity and compatibility

## Documentation Standards

### Code Documentation
- Document CLI commands with examples
- Include JSDoc/docstrings for all public functions
- Maintain inline comments for complex logic

### User Documentation
- Keep README.md updated with installation and usage instructions
- Provide template documentation in `docs/templates/`
- Include troubleshooting guide for common issues

## Performance Considerations

### Template Processing
- Cache compiled templates to avoid re-parsing
- Use streaming for large file operations
- Implement progress indicators for long-running operations

### Dependency Installation
- Parallelize dependency downloads where possible
- Provide options to skip dependency installation for faster scaffolding
- Cache downloaded dependencies locally

## Security Guidelines

### Template Safety
- Validate template sources and integrity
- Sanitize user inputs in template variables
- Avoid executing arbitrary code from templates

### File Operations
- Validate file paths to prevent directory traversal
- Check permissions before file operations
- Use secure temporary directories for intermediate files

## Contributing Guidelines

When adding new features:
1. Update relevant templates if the feature affects project scaffolding
2. Add comprehensive tests for new functionality
3. Update documentation and help text
4. Ensure cross-platform compatibility
5. Follow existing code style and patterns

## Common Patterns to Follow

- **Error First**: Use error-first callback patterns or proper error handling in async code
- **Immutable Config**: Treat configuration objects as immutable
- **Composable Commands**: Design CLI commands to be composable and chainable
- **Progressive Enhancement**: Start with basic functionality and add advanced features progressively