"""
Security Checker Module
Uses bandit to detect security vulnerabilities and unsafe patterns
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple


class SecurityChecker:
    """Checks Python code for security vulnerabilities using bandit"""

    def __init__(self, confidence_level: str = 'LOW', severity_level: str = 'LOW'):
        """
        Initialize SecurityChecker

        Args:
            confidence_level: Minimum confidence level (LOW, MEDIUM, HIGH)
            severity_level: Minimum severity level (LOW, MEDIUM, HIGH)
        """
        self.confidence_level = confidence_level.upper()
        self.severity_level = severity_level.upper()

    def check_file(self, file_path: str) -> Tuple[bool, List[Dict]]:
        """
        Check a single file for security vulnerabilities

        Args:
            file_path: Path to the Python file

        Returns:
            Tuple of (is_secure, list of vulnerabilities)
        """
        if not Path(file_path).exists():
            return False, [{'error': f'File not found: {file_path}'}]

        if not file_path.endswith('.py'):
            return True, []  # Skip non-Python files

        vulnerabilities = []

        # Build bandit command
        cmd = [
            sys.executable, '-m', 'bandit',
            '-f', 'json',
            '-ll',  # Report only LOW and above
            file_path
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.stdout:
                try:
                    bandit_output = json.loads(result.stdout)
                    results = bandit_output.get('results', [])

                    for issue in results:
                        # Filter by confidence and severity
                        if self._should_report(issue):
                            vulnerabilities.append(self._format_issue(issue))

                except json.JSONDecodeError:
                    return False, [{'error': 'Failed to parse bandit output'}]

            is_secure = len(vulnerabilities) == 0
            return is_secure, vulnerabilities

        except subprocess.TimeoutExpired:
            return False, [{'error': 'Security check timed out'}]
        except FileNotFoundError:
            return False, [{'error': 'bandit not installed. Run: pip install bandit'}]
        except Exception as e:
            return False, [{'error': f'Security check failed: {str(e)}'}]

    def check_files(self, file_paths: List[str]) -> Tuple[bool, Dict[str, List[Dict]]]:
        """
        Check multiple files for security vulnerabilities

        Args:
            file_paths: List of file paths to check

        Returns:
            Tuple of (all_secure, dict of file_path: vulnerabilities)
        """
        all_vulnerabilities = {}
        all_secure = True

        for file_path in file_paths:
            is_secure, vulnerabilities = self.check_file(file_path)
            if not is_secure:
                all_secure = False
                all_vulnerabilities[file_path] = vulnerabilities

        return all_secure, all_vulnerabilities

    def _should_report(self, issue: Dict) -> bool:
        """
        Check if issue should be reported based on confidence and severity

        Args:
            issue: Bandit issue dictionary

        Returns:
            True if issue should be reported
        """
        severity_levels = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}
        confidence_levels = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}

        issue_severity = severity_levels.get(issue.get('issue_severity', 'LOW'), 1)
        issue_confidence = confidence_levels.get(issue.get('issue_confidence', 'LOW'), 1)

        min_severity = severity_levels.get(self.severity_level, 1)
        min_confidence = confidence_levels.get(self.confidence_level, 1)

        return issue_severity >= min_severity and issue_confidence >= min_confidence

    def _format_issue(self, issue: Dict) -> Dict:
        """
        Format bandit issue into standardized format

        Args:
            issue: Bandit issue dictionary

        Returns:
            Formatted issue dictionary
        """
        return {
            'file': issue.get('filename', 'unknown'),
            'line': issue.get('line_number', 0),
            'code': issue.get('test_id', 'UNKNOWN'),
            'test_name': issue.get('test_name', 'unknown'),
            'issue_text': issue.get('issue_text', ''),
            'severity': issue.get('issue_severity', 'LOW'),
            'confidence': issue.get('issue_confidence', 'LOW'),
            'more_info': issue.get('more_info', '')
        }

    def get_summary(self, vulnerabilities: Dict[str, List[Dict]]) -> Dict:
        """
        Get summary statistics of vulnerabilities

        Args:
            vulnerabilities: Dictionary of file_path: vulnerabilities

        Returns:
            Dictionary with summary statistics
        """
        severity_counts = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0}
        confidence_counts = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0}
        total_issues = 0
        files_with_issues = len(vulnerabilities)

        for file_vulnerabilities in vulnerabilities.values():
            for vulnerability in file_vulnerabilities:
                if 'severity' in vulnerability:
                    severity = vulnerability.get('severity', 'LOW')
                    confidence = vulnerability.get('confidence', 'LOW')
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1
                    confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1
                    total_issues += 1

        return {
            'files_checked': files_with_issues,
            'total_issues': total_issues,
            'severity': severity_counts,
            'confidence': confidence_counts
        }

    def format_report(self, vulnerabilities: Dict[str, List[Dict]]) -> str:
        """
        Format vulnerabilities into a readable report

        Args:
            vulnerabilities: Dictionary of file_path: vulnerabilities

        Returns:
            Formatted report string
        """
        if not vulnerabilities:
            return "✓ No security vulnerabilities found!"

        report = []
        report.append("\n" + "="*70)
        report.append("SECURITY VULNERABILITIES REPORT")
        report.append("="*70 + "\n")

        for file_path, file_vulnerabilities in vulnerabilities.items():
            report.append(f"\n🔒 {file_path}")
            report.append("-" * 70)

            for vuln in file_vulnerabilities:
                if 'error' in vuln:
                    report.append(f"  {vuln['error']}")
                else:
                    severity_icon = {
                        'HIGH': '🔴',
                        'MEDIUM': '🟡',
                        'LOW': '🟢'
                    }.get(vuln['severity'], '⚠️')

                    report.append(
                        f"  {severity_icon} Line {vuln['line']}: "
                        f"[{vuln['severity']}] {vuln['issue_text']}"
                    )
                    report.append(f"     Code: {vuln['code']} | Confidence: {vuln['confidence']}")
                    if vuln.get('more_info'):
                        report.append(f"     More info: {vuln['more_info']}")
                    report.append("")

        summary = self.get_summary(vulnerabilities)
        report.append("\n" + "="*70)
        report.append("SUMMARY")
        report.append("="*70)
        report.append(f"Files with vulnerabilities: {summary['files_checked']}")
        report.append(f"Total issues: {summary['total_issues']}")
        report.append(f"\nSeverity breakdown:")
        report.append(f"  🔴 HIGH: {summary['severity']['HIGH']}")
        report.append(f"  🟡 MEDIUM: {summary['severity']['MEDIUM']}")
        report.append(f"  🟢 LOW: {summary['severity']['LOW']}")
        report.append("="*70 + "\n")

        return "\n".join(report)
