# Usage Guide

## Installation

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/Code-Review-Automation-Tool.git
cd Code-Review-Automation-Tool

# Run setup script
python setup.py
```

The setup script will:
1. Install Python dependencies (flake8, bandit, radon)
2. Install the git pre-commit hook
3. Test the installation

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Copy pre-commit hook
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit  # Unix/Mac only
```

---

## Basic Usage

### Automatic (Git Hook)

Once installed, the tool runs automatically on every commit:

```bash
git add myfile.py
git commit -m "Add new feature"

# The pre-commit hook will automatically run and check your code
# If issues are found, the commit will be blocked
```

### Manual Usage

#### Review Staged Files

```bash
python main.py --staged
```

#### Review All Python Files

```bash
python main.py --all
```

#### Review Specific Files

```bash
python main.py file1.py file2.py file3.py
```

#### Verbose Output

```bash
python main.py --all --verbose
```

#### Strict Mode

Fail on warnings (not just errors):

```bash
python main.py --strict --all
```

---

## Example Output

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
CODE REVIEW AUTOMATION TOOL
======================================================================

Reviewing 2 file(s)...

[1/3] Checking code style...

======================================================================
STYLE VIOLATIONS REPORT
======================================================================

📄 example.py
----------------------------------------------------------------------
  ❌ Line 12, Col 80: E501 - line too long (95 > 88 characters)
  ⚠️  Line 25, Col 1: W293 - blank line contains whitespace

======================================================================
SUMMARY
======================================================================
Files with issues: 1
Total errors: 1
Total warnings: 1
Total issues: 2
======================================================================

[2/3] Checking for security vulnerabilities...

======================================================================
SECURITY VULNERABILITIES REPORT
======================================================================

🔒 example.py
----------------------------------------------------------------------
  🔴 Line 45: [HIGH] Use of exec detected
     Code: B102 | Confidence: HIGH
     More info: https://bandit.readthedocs.io/...

======================================================================
SUMMARY
======================================================================
Files with vulnerabilities: 1
Total issues: 1

Severity breakdown:
  🔴 HIGH: 1
  🟡 MEDIUM: 0
  🟢 LOW: 0
======================================================================

[3/3] Checking code complexity...

======================================================================
CODE COMPLEXITY REPORT
======================================================================

📊 example.py
----------------------------------------------------------------------
  ⚠️  Function 'complex_function' at line 30
      Cyclomatic Complexity: 15 (max: 10)
      Rank: C

======================================================================
SUMMARY
======================================================================
Files with issues: 1
Total issues: 1
Complexity issues: 1
Maintainability issues: 0
Highest complexity found: 15
======================================================================

======================================================================
❌ CODE REVIEW FAILED - Issues found
======================================================================

Please fix the issues above before committing.
```

---

## Bypassing the Hook

**Not recommended**, but if you need to commit without running the review:

```bash
git commit --no-verify
```

Use this only in emergencies or when you're sure the code is correct.

---

## Configuration

### Customizing Style Rules

Edit `main.py` and modify the `StyleChecker` initialization:

```python
self.style_checker = StyleChecker(
    max_line_length=100,  # Change from 88
    ignore_errors=['E203', 'W503', 'E501']  # Add more ignore codes
)
```

### Customizing Security Checks

```python
self.security_checker = SecurityChecker(
    confidence_level='MEDIUM',  # Change from LOW
    severity_level='MEDIUM'     # Change from LOW
)
```

### Customizing Complexity Thresholds

```python
self.complexity_checker = ComplexityChecker(
    max_complexity=15,         # Change from 10
    min_maintainability='C'    # Change from B
)
```

---

## Integrating with CI/CD

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

## Troubleshooting

### Hook Not Running

Make sure the hook is executable:
```bash
chmod +x .git/hooks/pre-commit
```

### Dependencies Not Found

Install dependencies:
```bash
pip install -r requirements.txt
```

### Python Version Issues

Ensure you're using Python 3.8 or higher:
```bash
python --version
```

---

## Tips

1. **Run before committing**: Get in the habit of running `python main.py --staged` before committing

2. **Fix incrementally**: Address issues one category at a time (style, then security, then complexity)

3. **Use `--verbose`**: When debugging, use verbose mode to see which files are being checked

4. **Keep complexity low**: If you hit complexity warnings, consider refactoring into smaller functions

5. **Don't ignore security warnings**: Security issues should be taken seriously, even if they're low severity

---

For more information, see [README.md](README.md)
