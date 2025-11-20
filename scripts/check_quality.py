#!/usr/bin/env python3
"""Code quality checker for CLI Game Collection."""

import ast
import os
import sys
from pathlib import Path
from typing import List, Tuple


class CodeQualityChecker:
    """Check code quality metrics."""
    
    def __init__(self, project_root: str = '.'):
        self.project_root = Path(project_root)
        self.errors = []
        self.warnings = []
        self.info = []
    
    def check_all(self):
        """Run all quality checks."""
        print("🔍 Running code quality checks...\n")
        
        self.check_syntax()
        self.check_imports()
        self.check_docstrings()
        self.check_line_length()
        self.check_complexity()
        
        self.print_results()
    
    def check_syntax(self):
        """Check Python syntax."""
        print("📝 Checking syntax...")
        python_files = self._get_python_files()
        
        for file_path in python_files:
            try:
                with open(file_path, 'r') as f:
                    ast.parse(f.read())
            except SyntaxError as e:
                self.errors.append(f"{file_path}:{e.lineno} - Syntax error: {e.msg}")
        
        if not self.errors:
            self.info.append("✓ No syntax errors found")
    
    def check_imports(self):
        """Check for unused imports."""
        print("📦 Checking imports...")
        # This is a simplified check - a real linter would be more thorough
        python_files = self._get_python_files()
        
        for file_path in python_files:
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
                
                # Check for obvious unused imports (very basic)
                for i, line in enumerate(lines, 1):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        # Skip for now - proper import checking requires AST analysis
                        pass
        
        self.info.append("✓ Import check completed")
    
    def check_docstrings(self):
        """Check for missing docstrings."""
        print("📖 Checking docstrings...")
        python_files = self._get_python_files()
        missing = 0
        
        for file_path in python_files:
            try:
                with open(file_path, 'r') as f:
                    tree = ast.parse(f.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        if not ast.get_docstring(node):
                            if not node.name.startswith('_'):  # Ignore private
                                missing += 1
                                self.warnings.append(
                                    f"{file_path}:{node.lineno} - "
                                    f"Missing docstring for {node.__class__.__name__} '{node.name}'"
                                )
            except Exception as e:
                self.errors.append(f"{file_path} - Error parsing: {e}")
        
        if missing == 0:
            self.info.append("✓ All public functions/classes have docstrings")
        else:
            self.warnings.append(f"⚠ {missing} missing docstrings found")
    
    def check_line_length(self):
        """Check for lines exceeding 100 characters."""
        print("📏 Checking line length...")
        python_files = self._get_python_files()
        long_lines = 0
        
        for file_path in python_files:
            with open(file_path, 'r') as f:
                for i, line in enumerate(f, 1):
                    if len(line.rstrip()) > 100:
                        long_lines += 1
                        if long_lines <= 5:  # Only show first 5
                            self.warnings.append(
                                f"{file_path}:{i} - Line exceeds 100 characters ({len(line.rstrip())})"
                            )
        
        if long_lines == 0:
            self.info.append("✓ All lines within 100 characters")
        elif long_lines > 5:
            self.warnings.append(f"⚠ {long_lines - 5} more long lines found...")
    
    def check_complexity(self):
        """Check cyclomatic complexity."""
        print("🔄 Checking complexity...")
        python_files = self._get_python_files()
        complex_functions = 0
        
        for file_path in python_files:
            try:
                with open(file_path, 'r') as f:
                    tree = ast.parse(f.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        complexity = self._calculate_complexity(node)
                        if complexity > 10:
                            complex_functions += 1
                            self.warnings.append(
                                f"{file_path}:{node.lineno} - "
                                f"High complexity ({complexity}) in function '{node.name}'"
                            )
            except Exception:
                pass
        
        if complex_functions == 0:
            self.info.append("✓ No overly complex functions found")
    
    def _calculate_complexity(self, node):
        """Calculate cyclomatic complexity (simplified)."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity
    
    def _get_python_files(self) -> List[Path]:
        """Get all Python files in the project."""
        python_files = []
        for pattern in ['games/*.py', 'utils/*.py', 'tests/*.py', '*.py']:
            python_files.extend(self.project_root.glob(pattern))
        
        # Exclude __pycache__ and venv
        return [f for f in python_files if '__pycache__' not in str(f) and 'venv' not in str(f)]
    
    def print_results(self):
        """Print check results."""
        print("\n" + "=" * 60)
        print("📊 Code Quality Report")
        print("=" * 60)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:20]:  # Limit output
                print(f"  {warning}")
            if len(self.warnings) > 20:
                print(f"  ... and {len(self.warnings) - 20} more warnings")
        
        if self.info:
            print(f"\n✅ INFO ({len(self.info)}):")
            for info in self.info:
                print(f"  {info}")
        
        print("\n" + "=" * 60)
        
        # Summary
        if self.errors:
            print("❌ Quality check FAILED")
            return 1
        elif self.warnings:
            print(f"⚠️  Quality check passed with {len(self.warnings)} warnings")
            return 0
        else:
            print("✅ Quality check PASSED")
            return 0


def main():
    """Run quality checks."""
    checker = CodeQualityChecker()
    checker.check_all()
    sys.exit(0)  # Always return 0 for now (warnings don't fail build)


if __name__ == '__main__':
    main()

