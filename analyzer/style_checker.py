"""
Style Checker Module
Uses flake8 to check code style and formatting violations
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple


class StyleChecker:
    """Checks Python code style using flake8"""

    def __init__(self, max_line_length: int = 88, ignore_errors: List[str] = None):
        """
        Initialize StyleChecker

        Args:
            max_line_length: Maximum line length (default: 88 for Black compatibility)
            ignore_errors: List of error codes to ignore (e.g., ['E203', 'W503'])
        """
        self.max_line_length = max_line_length
        self.ignore_errors = ignore_errors or []

    def check_file(self, file_path: str) -> Tuple[bool, List[Dict]]:
        """
        Check a single file for style violations

        Args:
            file_path: Path to the Python file

        Returns:
            Tuple of (is_clean, list of violations)
        """
        if not Path(file_path).exists():
            return False, [{'error': f'File not found: {file_path}'}]

        if not file_path.endswith('.py'):
            return True, []  # Skip non-Python files

        violations = []

        # Build flake8 command
        cmd = [
            sys.executable, '-m', 'flake8',
            '--max-line-length', str(self.max_line_length),
            '--format', '%(path)s:%(row)d:%(col)d: %(code)s %(text)s',
        ]

        if self.ignore_errors:
            cmd.extend(['--ignore', ','.join(self.ignore_errors)])

        cmd.append(file_path)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        violations.append(self._parse_flake8_output(line))

            is_clean = len(violations) == 0
            return is_clean, violations

        except subprocess.TimeoutExpired:
            return False, [{'error': 'Style check timed out'}]
        except FileNotFoundError:
            return False, [{'error': 'flake8 not installed. Run: pip install flake8'}]
        except Exception as e:
            return False, [{'error': f'Style check failed: {str(e)}'}]

    def check_files(self, file_paths: List[str]) -> Tuple[bool, Dict[str, List[Dict]]]:
        """
        Check multiple files for style violations

        Args:
            file_paths: List of file paths to check

        Returns:
            Tuple of (all_clean, dict of file_path: violations)
        """
        all_violations = {}
        all_clean = True

        for file_path in file_paths:
            is_clean, violations = self.check_file(file_path)
            if not is_clean:
                all_clean = False
                all_violations[file_path] = violations

        return all_clean, all_violations

    def _parse_flake8_output(self, line: str) -> Dict:
        """
        Parse flake8 output line into structured format

        Args:
            line: Output line from flake8

        Returns:
            Dictionary with violation details
        """
        try:
            # Format: path:row:col: code message
            parts = line.split(':', 3)
            if len(parts) >= 4:
                file_path = parts[0]
                row = parts[1]
                col = parts[2]
                message_parts = parts[3].strip().split(' ', 1)
                code = message_parts[0] if len(message_parts) > 0 else 'UNKNOWN'
                message = message_parts[1] if len(message_parts) > 1 else ''

                return {
                    'file': file_path,
                    'line': int(row),
                    'column': int(col),
                    'code': code,
                    'message': message,
                    'severity': self._get_severity(code)
                }
        except Exception:
            pass

        return {
            'file': 'unknown',
            'line': 0,
            'column': 0,
            'code': 'PARSE_ERROR',
            'message': line,
            'severity': 'error'
        }

    def _get_severity(self, code: str) -> str:
        """
        Get severity level based on error code

        Args:
            code: Flake8 error code (e.g., 'E501', 'W503')

        Returns:
            Severity level: 'error' or 'warning'
        """
        if code.startswith('E'):
            return 'error'
        elif code.startswith('W'):
            return 'warning'
        elif code.startswith('F'):
            return 'error'
        elif code.startswith('C'):
            return 'warning'
        else:
            return 'warning'

    def get_summary(self, violations: Dict[str, List[Dict]]) -> Dict:
        """
        Get summary statistics of violations

        Args:
            violations: Dictionary of file_path: violations

        Returns:
            Dictionary with summary statistics
        """
        total_errors = 0
        total_warnings = 0
        files_with_issues = len(violations)

        for file_violations in violations.values():
            for violation in file_violations:
                if violation.get('severity') == 'error':
                    total_errors += 1
                else:
                    total_warnings += 1

        return {
            'files_checked': files_with_issues,
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'total_issues': total_errors + total_warnings
        }

    def format_report(self, violations: Dict[str, List[Dict]]) -> str:
        """
        Format violations into a readable report

        Args:
            violations: Dictionary of file_path: violations

        Returns:
            Formatted report string
        """
        if not violations:
            return "✓ No style violations found!"

        report = []
        report.append("\n" + "="*70)
        report.append("STYLE VIOLATIONS REPORT")
        report.append("="*70 + "\n")

        for file_path, file_violations in violations.items():
            report.append(f"\n📄 {file_path}")
            report.append("-" * 70)

            for violation in file_violations:
                if 'error' in violation and violation.get('code') != 'PARSE_ERROR':
                    report.append(f"  {violation['error']}")
                else:
                    severity_icon = "❌" if violation['severity'] == 'error' else "⚠️"
                    report.append(
                        f"  {severity_icon} Line {violation['line']}, Col {violation['column']}: "
                        f"{violation['code']} - {violation['message']}"
                    )

        summary = self.get_summary(violations)
        report.append("\n" + "="*70)
        report.append("SUMMARY")
        report.append("="*70)
        report.append(f"Files with issues: {summary['files_checked']}")
        report.append(f"Total errors: {summary['total_errors']}")
        report.append(f"Total warnings: {summary['total_warnings']}")
        report.append(f"Total issues: {summary['total_issues']}")
        report.append("="*70 + "\n")

        return "\n".join(report)
