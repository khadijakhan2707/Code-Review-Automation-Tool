#!/usr/bin/env python3
"""
Setup Script for Code Review Automation Tool

This script installs the git pre-commit hook and dependencies.

Usage:
    python setup.py install
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def print_header(message):
    """Print formatted header"""
    print("\n" + "="*70)
    print(message)
    print("="*70 + "\n")


def check_git_repo():
    """Check if current directory is a git repository"""
    if not Path('.git').exists():
        print("❌ Error: Not a git repository")
        print("   Please run this script from the root of a git repository")
        return False
    return True


def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")

    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            check=True
        )
        print("✓ Dependencies installed successfully\n")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def install_pre_commit_hook():
    """Install the pre-commit hook"""
    print("🔗 Installing pre-commit hook...")

    hook_source = Path('hooks/pre-commit')
    hook_dest = Path('.git/hooks/pre-commit')

    if not hook_source.exists():
        print(f"❌ Hook file not found: {hook_source}")
        return False

    # Create hooks directory if it doesn't exist
    hook_dest.parent.mkdir(parents=True, exist_ok=True)

    # Copy hook
    shutil.copy2(hook_source, hook_dest)

    # Make executable (Unix-like systems)
    if os.name != 'nt':  # Not Windows
        os.chmod(hook_dest, 0o755)

    print(f"✓ Pre-commit hook installed to {hook_dest}\n")
    return True


def test_installation():
    """Test if installation is working"""
    print("🧪 Testing installation...")

    # Test if main.py exists
    if not Path('main.py').exists():
        print("❌ main.py not found")
        return False

    # Test if dependencies are installed
    try:
        import flake8
        import bandit
        import radon
        print("✓ All dependencies are available\n")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False


def main():
    """Main installation function"""
    print_header("Code Review Automation Tool - Setup")

    print("This script will:")
    print("  1. Install Python dependencies (flake8, bandit, radon)")
    print("  2. Install git pre-commit hook")
    print("  3. Test the installation")
    print()

    # Check if in git repo
    if not check_git_repo():
        return 1

    # Install dependencies
    if not install_dependencies():
        return 1

    # Install pre-commit hook
    if not install_pre_commit_hook():
        return 1

    # Test installation
    if not test_installation():
        print("\n⚠️  Installation completed with warnings")
        print("   Please check the errors above")
        return 1

    # Success!
    print_header("✅ Installation Complete!")

    print("The Code Review Automation Tool is now active!")
    print()
    print("What happens next:")
    print("  • Every time you commit, the pre-commit hook will run")
    print("  • It will check your code for style, security, and complexity issues")
    print("  • If issues are found, the commit will be blocked")
    print("  • Fix the issues and try committing again")
    print()
    print("Manual usage:")
    print("  python main.py --staged       # Review staged files")
    print("  python main.py --all          # Review all Python files")
    print("  python main.py file1.py       # Review specific files")
    print()
    print("To bypass the hook (not recommended):")
    print("  git commit --no-verify")
    print()

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
