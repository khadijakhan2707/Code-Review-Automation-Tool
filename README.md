# Code-Review-Automation-Tool
An automated code review tool built in Python to enforce coding standards, detect potential issues early, and improve code quality by integrating static analysis checks directly into the Git workflow using Git Hooks.
📌 Project Overview

Manual code reviews are time-consuming and error-prone. This project automates the initial layer of code review by scanning code changes before they are committed or merged. It helps teams maintain consistent quality, reduce bugs, and enforce best practices early in the development lifecycle.

The tool analyzes code for:

* Formatting and style violations

* Missing or insufficient test coverage

* Security smells and risky patterns

* High cyclomatic complexity

* Poor maintainability indicators

🚀 Key Features

🔍 Static Code Analysis for early issue detection
🧪 Test Presence Validation to ensure reliability
🔐 Security Smell Detection (unsafe patterns, bad practices)
📏 Code Complexity Warnings

🪝 Git Hook Integration for automated enforcement

✅ Pre-commit & Pre-push Safety Checks

🧠 How It Works

Developer makes code changes

Git hook triggers automatically before commit or push

Python scripts analyze modified files

Issues are reported in the terminal

Commit is blocked if critical issues are found

This ensures only clean, secure, and maintainable code enters the repository.

🛠️ Tech Stack

Language: Python

Version Control: Git

Automation: Git Hooks (pre-commit)

Analysis Type: Static Code Analysis

Tools Used:

flake8 – style & linting

bandit – security analysis

radon – complexity checks

📂 Project Structure
```
code-review-automation-tool/
│
├── hooks/
│   └── pre-commit
│
├── analyzer/
│   ├── style_checker.py
│   ├── security_checker.py
│   └── complexity_checker.py
│
├── main.py
├── requirements.txt
└── README.md
```

⚙️ Installation & Setup

### Quick Setup (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/your-username/code-review-automation-tool.git
cd code-review-automation-tool

# 2. Run the setup script
python setup.py
```

The setup script will automatically:
- Install Python dependencies (flake8, bandit, radon)
- Install the git pre-commit hook
- Test the installation

### Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy pre-commit hook
cp hooks/pre-commit .git/hooks/pre-commit

# Make hook executable (Unix/Mac)
chmod +x .git/hooks/pre-commit
```

---

## ▶️ Usage

### Automatic (Recommended)

Once installed, the tool runs automatically on every commit:

```bash
git add myfile.py
git commit -m "Your commit message"

# The pre-commit hook will automatically run
# If issues are found, the commit will be blocked
```

### Manual Usage

#### Review staged files
```bash
python main.py --staged
```

#### Review all Python files
```bash
python main.py --all
```

#### Review specific files
```bash
python main.py file1.py file2.py
```

#### Additional options
```bash
python main.py --help
python main.py --all --verbose    # Detailed output
python main.py --all --strict     # Fail on warnings
```

---

## 📊 What Gets Checked

The tool performs three types of analysis:

### 1. Style Checking (flake8)
- ✅ PEP8 compliance
- ✅ Line length violations
- ✅ Unused imports
- ✅ Formatting issues
- ✅ Naming conventions

### 2. Security Analysis (bandit)
- 🔒 Unsafe function usage (eval, exec, pickle)
- 🔒 SQL injection risks
- 🔒 Hard-coded passwords/secrets
- 🔒 Insecure random number generation
- 🔒 Weak cryptography

### 3. Complexity Analysis (radon)
- 📊 Cyclomatic complexity
- 📊 Maintainability index
- 📊 Overly complex functions
- 📊 Code quality grades

---

## 📝 Sample Output

### ✅ Clean Code
```
======================================================================
CODE REVIEW AUTOMATION TOOL
======================================================================

Reviewing 3 file(s)...

[1/3] Checking code style...
✓ No style violations found

[2/3] Checking for security vulnerabilities...
✓ No security vulnerabilities found

[3/3] Checking code complexity...
✓ No complexity issues found

======================================================================
✅ CODE REVIEW PASSED - No issues found
======================================================================
```

### ❌ Code with Issues

```
======================================================================
STYLE VIOLATIONS REPORT
======================================================================

📄 example.py
----------------------------------------------------------------------
  ❌ Line 12, Col 80: E501 - line too long (95 > 88 characters)
  ⚠️  Line 25, Col 1: W293 - blank line contains whitespace

======================================================================
SECURITY VULNERABILITIES REPORT
======================================================================

🔒 example.py
----------------------------------------------------------------------
  🔴 Line 45: [HIGH] Use of exec detected
     Code: B102 | Confidence: HIGH

======================================================================
❌ CODE REVIEW FAILED - Issues found
======================================================================

Please fix the issues above before committing.
```

---

## 🔧 Configuration

You can customize the tool by editing `main.py`:

```python
# Adjust max line length
self.style_checker = StyleChecker(max_line_length=100)

# Change complexity threshold
self.complexity_checker = ComplexityChecker(max_complexity=15)

# Adjust security sensitivity
self.security_checker = SecurityChecker(
    confidence_level='MEDIUM',
    severity_level='MEDIUM'
)
```

---

## 🚫 Bypassing the Hook

**Not recommended**, but if necessary:

```bash
git commit --no-verify
```

Use this only in emergencies when you're certain the code is correct.

📊 Sample Output
❌ Code Review Failed

- Formatting issue detected in app.py (line 23)
- High cyclomatic complexity in utils.py
- Security smell: use of eval() detected

✔ Fix the above issues before committing

🧪 Checks Performed
Category	Description
Formatting	PEP8 violations, unused imports
Tests	Missing test files or cases
Security	Unsafe functions, insecure patterns
Complexity	Functions exceeding complexity threshold
🔐 Benefits

Prevents buggy or unsafe code from being merged

Enforces consistent coding standards

Reduces review overhead for teams

Encourages disciplined development practices

⚠️ Disclaimer

This tool is intended for educational and internal development use.
Security checks are advisory and should not replace professional security audits.

👩‍💻 Author

Khadija Khan

Portfolio: https://khadijasportfolio.tiiny.site

LinkedIn: https://www.linkedin.com/in/khadija-khan-aaa3a4240/

## 🧪 Testing the Tool

Test the tool on itself:

```bash
# Review all files in the project
python main.py --all

# Review with verbose output
python main.py --all --verbose
```

---

## 🔌 CI/CD Integration

### GitHub Actions

```yaml
name: Code Review

on: [push, pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run code review
        run: python main.py --all
```

### GitLab CI

```yaml
code_review:
  image: python:3.9
  script:
    - pip install -r requirements.txt
    - python main.py --all
```

---

## 📚 Documentation

- [USAGE.md](USAGE.md) - Detailed usage guide with examples
- [README.md](README.md) - This file (project overview)

---

## ⭐ Future Enhancements

- [ ] CI/CD pipeline integration
- [ ] Pull request bot comments
- [ ] Language-agnostic support
- [ ] HTML / JSON report generation
- [ ] Custom rule configuration files
- [ ] Automatic fix suggestions
- [ ] IDE integration (VSCode, PyCharm)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the code review tool on your changes
5. Submit a pull request

---

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## ✅ Requirements

- Python 3.8 or higher
- Git
- pip (Python package manager)

---

## 🐛 Troubleshooting

### Hook not running?
```bash
chmod +x .git/hooks/pre-commit
```

### Dependencies not found?
```bash
pip install -r requirements.txt
```

### Python version issues?
```bash
python --version  # Should be 3.8+
```

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- See [USAGE.md](USAGE.md) for detailed documentation
