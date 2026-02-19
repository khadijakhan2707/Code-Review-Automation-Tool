"""
Complexity Checker Module
Uses radon to analyze code complexity and maintainability
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple


class ComplexityChecker:
    """Checks code complexity using radon"""

    def __init__(
        self,
        max_complexity: int = 10,
        min_maintainability: str = 'B',
        check_cc: bool = True,
        check_mi: bool = True
    ):
        """
        Initialize ComplexityChecker

        Args:
            max_complexity: Maximum cyclomatic complexity allowed (default: 10)
            min_maintainability: Minimum maintainability index (A-F, default: B)
            check_cc: Check cyclomatic complexity
            check_mi: Check maintainability index
        """
        self.max_complexity = max_complexity
        self.min_maintainability = min_maintainability
        self.check_cc = check_cc
        self.check_mi = check_mi

    def check_file(self, file_path: str) -> Tuple[bool, List[Dict]]:
        """
        Check a single file for complexity issues

        Args:
            file_path: Path to the Python file

        Returns:
            Tuple of (is_acceptable, list of complexity issues)
        """
        if not Path(file_path).exists():
            return False, [{'error': f'File not found: {file_path}'}]

        if not file_path.endswith('.py'):
            return True, []  # Skip non-Python files

        issues = []

        # Check cyclomatic complexity
        if self.check_cc:
            cc_issues = self._check_cyclomatic_complexity(file_path)
            issues.extend(cc_issues)

        # Check maintainability index
        if self.check_mi:
            mi_issues = self._check_maintainability_index(file_path)
            issues.extend(mi_issues)

        is_acceptable = len(issues) == 0
        return is_acceptable, issues

    def check_files(self, file_paths: List[str]) -> Tuple[bool, Dict[str, List[Dict]]]:
        """
        Check multiple files for complexity issues

        Args:
            file_paths: List of file paths to check

        Returns:
            Tuple of (all_acceptable, dict of file_path: issues)
        """
        all_issues = {}
        all_acceptable = True

        for file_path in file_paths:
            is_acceptable, issues = self.check_file(file_path)
            if not is_acceptable:
                all_acceptable = False
                all_issues[file_path] = issues

        return all_acceptable, all_issues

    def _check_cyclomatic_complexity(self, file_path: str) -> List[Dict]:
        """
        Check cyclomatic complexity using radon cc

        Args:
            file_path: Path to file

        Returns:
            List of complexity issues
        """
        issues = []

        cmd = [
            sys.executable, '-m', 'radon',
            'cc',
            '-j',  # JSON output
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
                    cc_data = json.loads(result.stdout)

                    for file_key, functions in cc_data.items():
                        for func in functions:
                            complexity = func.get('complexity', 0)
                            if complexity > self.max_complexity:
                                issues.append({
                                    'file': file_path,
                                    'type': 'cyclomatic_complexity',
                                    'function': func.get('name', 'unknown'),
                                    'line': func.get('lineno', 0),
                                    'complexity': complexity,
                                    'max_allowed': self.max_complexity,
                                    'rank': func.get('rank', 'A'),
                                    'message': f"Complexity {complexity} exceeds maximum {self.max_complexity}"
                                })

                except json.JSONDecodeError:
                    issues.append({'error': 'Failed to parse radon cc output'})

        except FileNotFoundError:
            issues.append({'error': 'radon not installed. Run: pip install radon'})
        except Exception as e:
            issues.append({'error': f'Complexity check failed: {str(e)}'})

        return issues

    def _check_maintainability_index(self, file_path: str) -> List[Dict]:
        """
        Check maintainability index using radon mi

        Args:
            file_path: Path to file

        Returns:
            List of maintainability issues
        """
        issues = []

        cmd = [
            sys.executable, '-m', 'radon',
            'mi',
            '-j',  # JSON output
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
                    mi_data = json.loads(result.stdout)

                    for file_key, file_mi in mi_data.items():
                        rank = file_mi.get('rank', 'A')
                        mi_score = file_mi.get('mi', 100)

                        if self._is_rank_below_threshold(rank, self.min_maintainability):
                            issues.append({
                                'file': file_path,
                                'type': 'maintainability_index',
                                'rank': rank,
                                'score': mi_score,
                                'min_required': self.min_maintainability,
                                'message': f"Maintainability rank {rank} is below minimum {self.min_maintainability}"
                            })

                except json.JSONDecodeError:
                    issues.append({'error': 'Failed to parse radon mi output'})

        except FileNotFoundError:
            issues.append({'error': 'radon not installed. Run: pip install radon'})
        except Exception as e:
            issues.append({'error': f'Maintainability check failed: {str(e)}'})

        return issues

    def _is_rank_below_threshold(self, rank: str, threshold: str) -> bool:
        """
        Check if rank is below threshold

        Args:
            rank: Current rank (A-F)
            threshold: Minimum acceptable rank (A-F)

        Returns:
            True if rank is below threshold
        """
        rank_values = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1, 'F': 0}
        return rank_values.get(rank, 0) < rank_values.get(threshold, 0)

    def get_summary(self, issues_dict: Dict[str, List[Dict]]) -> Dict:
        """
        Get summary statistics of complexity issues

        Args:
            issues_dict: Dictionary of file_path: issues

        Returns:
            Dictionary with summary statistics
        """
        cc_issues = 0
        mi_issues = 0
        total_issues = 0
        files_with_issues = len(issues_dict)
        max_complexity_found = 0

        for file_issues in issues_dict.values():
            for issue in file_issues:
                if issue.get('type') == 'cyclomatic_complexity':
                    cc_issues += 1
                    max_complexity_found = max(
                        max_complexity_found,
                        issue.get('complexity', 0)
                    )
                elif issue.get('type') == 'maintainability_index':
                    mi_issues += 1
                total_issues += 1

        return {
            'files_checked': files_with_issues,
            'total_issues': total_issues,
            'complexity_issues': cc_issues,
            'maintainability_issues': mi_issues,
            'max_complexity_found': max_complexity_found
        }

    def format_report(self, issues_dict: Dict[str, List[Dict]]) -> str:
        """
        Format complexity issues into a readable report

        Args:
            issues_dict: Dictionary of file_path: issues

        Returns:
            Formatted report string
        """
        if not issues_dict:
            return "✓ No complexity issues found!"

        report = []
        report.append("\n" + "="*70)
        report.append("CODE COMPLEXITY REPORT")
        report.append("="*70 + "\n")

        for file_path, file_issues in issues_dict.items():
            report.append(f"\n📊 {file_path}")
            report.append("-" * 70)

            for issue in file_issues:
                if 'error' in issue:
                    report.append(f"  {issue['error']}")
                elif issue.get('type') == 'cyclomatic_complexity':
                    report.append(
                        f"  ⚠️  Function '{issue['function']}' at line {issue['line']}"
                    )
                    report.append(f"      Cyclomatic Complexity: {issue['complexity']} (max: {issue['max_allowed']})")
                    report.append(f"      Rank: {issue['rank']}")
                    report.append("")
                elif issue.get('type') == 'maintainability_index':
                    report.append(f"  📉 Maintainability Index")
                    report.append(f"      Rank: {issue['rank']} (minimum: {issue['min_required']})")
                    report.append(f"      Score: {issue['score']:.2f}")
                    report.append("")

        summary = self.get_summary(issues_dict)
        report.append("\n" + "="*70)
        report.append("SUMMARY")
        report.append("="*70)
        report.append(f"Files with issues: {summary['files_checked']}")
        report.append(f"Total issues: {summary['total_issues']}")
        report.append(f"Complexity issues: {summary['complexity_issues']}")
        report.append(f"Maintainability issues: {summary['maintainability_issues']}")
        if summary['max_complexity_found'] > 0:
            report.append(f"Highest complexity found: {summary['max_complexity_found']}")
        report.append("="*70 + "\n")

        return "\n".join(report)
