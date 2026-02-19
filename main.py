#!/usr/bin/env python3
"""
Code Review Automation Tool - Main Entry Point

Automated code review system that integrates static analysis into Git workflows.
Checks for style violations, security issues, and code complexity.

Usage:
    python main.py [files...]
    python main.py --all
    python main.py --staged
"""

import sys
import argparse
import subprocess
from pathlib import Path
from typing import List

from analyzer import StyleChecker, SecurityChecker, ComplexityChecker


class CodeReviewTool:
    """Main orchestrator for code review checks"""

    def __init__(self, strict: bool = False, verbose: bool = False):
        """
        Initialize Code Review Tool

        Args:
            strict: If True, fail on warnings; if False, fail only on errors
            verbose: If True, show detailed output
        """
        self.strict = strict
        self.verbose = verbose

        # Initialize checkers
        self.style_checker = StyleChecker(
            max_line_length=88,
            ignore_errors=['E203', 'W503']  # Black compatibility
        )
        self.security_checker = SecurityChecker(
            confidence_level='LOW',
            severity_level='LOW'
        )
        self.complexity_checker = ComplexityChecker(
            max_complexity=10,
            min_maintainability='B'
        )

    def get_staged_files(self) -> List[str]:
        """
        Get list of staged Python files

        Returns:
            List of file paths
        """
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
                capture_output=True,
                text=True,
                check=True
            )

            files = [
                f.strip() for f in result.stdout.split('\n')
                if f.strip().endswith('.py')
            ]

            return files

        except subprocess.CalledProcessError:
            print("⚠️  Warning: Not a git repository or git command failed")
            return []
        except FileNotFoundError:
            print("⚠️  Warning: git not found")
            return []

    def get_all_python_files(self) -> List[str]:
        """
        Get all Python files in the current directory

        Returns:
            List of file paths
        """
        return [str(f) for f in Path('.').rglob('*.py')]

    def review_files(self, file_paths: List[str]) -> int:
        """
        Review the given files

        Args:
            file_paths: List of file paths to review

        Returns:
            Exit code (0 = success, 1 = issues found)
        """
        if not file_paths:
            print("✓ No Python files to review")
            return 0

        print("\n" + "="*70)
        print("CODE REVIEW AUTOMATION TOOL")
        print("="*70)
        print(f"\nReviewing {len(file_paths)} file(s)...\n")

        if self.verbose:
            for f in file_paths:
                print(f"  • {f}")
            print()

        has_issues = False

        # Run style check
        print("[1/3] Checking code style...")
        style_clean, style_violations = self.style_checker.check_files(file_paths)

        if not style_clean:
            has_issues = True
            print(self.style_checker.format_report(style_violations))
        else:
            print("✓ No style violations found\n")

        # Run security check
        print("[2/3] Checking for security vulnerabilities...")
        security_clean, security_issues = self.security_checker.check_files(file_paths)

        if not security_clean:
            has_issues = True
            print(self.security_checker.format_report(security_issues))
        else:
            print("✓ No security vulnerabilities found\n")

        # Run complexity check
        print("[3/3] Checking code complexity...")
        complexity_clean, complexity_issues = self.complexity_checker.check_files(file_paths)

        if not complexity_clean:
            has_issues = True
            print(self.complexity_checker.format_report(complexity_issues))
        else:
            print("✓ No complexity issues found\n")

        # Print final result
        print("="*70)
        if has_issues:
            print("❌ CODE REVIEW FAILED - Issues found")
            print("="*70)
            print("\nPlease fix the issues above before committing.\n")
            return 1
        else:
            print("✅ CODE REVIEW PASSED - No issues found")
            print("="*70)
            print()
            return 0


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Automated code review tool for Python projects',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py file1.py file2.py      Review specific files
  python main.py --staged                Review staged files (git)
  python main.py --all                   Review all Python files
  python main.py --strict --verbose      Strict mode with verbose output
        """
    )

    parser.add_argument(
        'files',
        nargs='*',
        help='Files to review'
    )

    parser.add_argument(
        '--staged',
        action='store_true',
        help='Review only staged files (git)'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Review all Python files in directory'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='Strict mode: fail on warnings'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )

    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()

    # Initialize tool
    tool = CodeReviewTool(strict=args.strict, verbose=args.verbose)

    # Determine which files to review
    if args.staged:
        files = tool.get_staged_files()
        if not files:
            print("✓ No staged Python files to review")
            return 0
    elif args.all:
        files = tool.get_all_python_files()
        if not files:
            print("✓ No Python files found")
            return 0
    elif args.files:
        files = args.files
    else:
        # Default: review staged files
        files = tool.get_staged_files()
        if not files:
            print("ℹ️  No staged files. Use --all to review all Python files.")
            print("   Usage: python main.py --all")
            return 0

    # Run review
    exit_code = tool.review_files(files)
    return exit_code


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Review interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if '--verbose' in sys.argv or '-v' in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
