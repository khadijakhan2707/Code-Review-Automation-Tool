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
1️⃣ Clone the Repository
```
git clone https://github.com/your-username/code-review-automation-tool.git
cd code-review-automation-tool
```

2️⃣ Install Dependencies
```
pip install -r requirements.txt
```

3️⃣ Enable Git Hook
```
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

▶️ Usage

Once installed, the tool runs automatically on every commit.
```

git commit -m "Your commit message"
```

If issues are found:

The commit is blocked

Errors and warnings are displayed

Developer fixes issues before retrying

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

⭐ Future Enhancements

CI/CD pipeline integration

Pull request bot comments

Language-agnostic support

HTML / JSON report generation
