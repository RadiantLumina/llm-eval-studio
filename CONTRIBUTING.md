# Contributing to LLM Evaluation Studio 🤝

Thank you for your interest in contributing to LLM Evaluation Studio! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- 🐛 Report bugs and issues
- 💡 Suggest new features or improvements
- 📝 Improve documentation
- 🔧 Submit bug fixes
- ✨ Implement new features
- 🧪 Add test cases

## 🚀 Getting Started

### 1. Fork the Repository

Click the "Fork" button on the GitHub repository page to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/RadiantLumina/llm-eval-studio.git
cd llm-eval-studio
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .  # Install in editable mode
```

### 5. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

## 📝 Coding Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and concise

### Documentation

- Update docstrings when modifying functions
- Update README.md if adding new features
- Add examples for new functionality

### Testing

- Add unit tests for new features
- Ensure all tests pass before submitting
- Aim for >80% test coverage

```bash
# Run tests
pytest tests/

# Run tests with coverage
pytest --cov=src tests/
```

## 🔍 Submitting Changes

### 1. Commit Your Changes

```bash
git add .
git commit -m "Add: brief description of your changes"
```

**Commit Message Format:**
- `Add:` for new features
- `Fix:` for bug fixes
- `Update:` for updates to existing features
- `Docs:` for documentation changes
- `Test:` for adding or updating tests

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create a Pull Request

- Go to your fork on GitHub
- Click "New Pull Request"
- Fill in the PR template
- Link any related issues

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Detailed steps to reproduce the bug
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: OS, Python version, package versions
6. **Additional Context**: Screenshots, error messages, etc.

## 💡 Suggesting Features

For feature suggestions, please include:

1. **Problem Description**: What problem does this feature solve?
2. **Proposed Solution**: Detailed description of the proposed feature
3. **Use Cases**: Examples of how this feature would be used
4. **Alternatives Considered**: Other approaches you've considered

## 📧 Contact

If you have questions or need help, feel free to reach out:

- Email: Rong-0202@outlook.com
- GitHub: [@RadiantLumina](https://github.com/RadiantLumina)

## 🎉 Recognition

Contributors will be recognized in:
- Release notes
- Project documentation
- Special thanks section

Thank you for contributing to LLM Evaluation Studio! 🚀