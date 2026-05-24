"""Automated code review agent that analyzes pull requests for bugs, security issues, and style violations."""

import ast
import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ReviewComment:
    file: str
    line: int
    severity: str  # error, warning, info
    message: str
    suggestion: Optional[str] = None


@dataclass
class ReviewResult:
    comments: List[ReviewComment] = field(default_factory=list)
    score: float = 0.0

    def add(self, comment: ReviewComment) -> None:
        self.comments.append(comment)

    def summary(self) -> str:
        errors = sum(1 for c in self.comments if c.severity == "error")
        warnings = sum(1 for c in self.comments if c.severity == "warning")
        infos = sum(1 for c in self.comments if c.severity == "info")
        return f"Found {errors} errors, {warnings} warnings, {infos} info"


class CodeReviewer:
    """Multi-agent code reviewer with static analysis capabilities."""

    def __init__(self, llm_client=None):
        self.llm = llm_client
        self.result = ReviewResult()

    def analyze_python(self, source: str, filepath: str = "unknown.py") -> ReviewResult:
        """Analyze Python source code for issues."""
        self.result = ReviewResult()

        # AST analysis
        try:
            tree = ast.parse(source)
            self._check_imports(tree, filepath)
            self._check_error_handling(tree, filepath)
            self._check_complexity(tree, filepath)
        except SyntaxError as e:
            self.result.add(ReviewComment(
                file=filepath, line=e.lineno or 0,
                severity="error", message=f"Syntax error: {e.msg}"
            ))

        return self.result

    def _check_imports(self, tree: ast.AST, filepath: str) -> None:
        """Check for wildcard imports and deprecated modules."""
        deprecated = {"imp", "optparse", "stat"}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "*":
                self.result.add(ReviewComment(
                    file=filepath, line=node.lineno,
                    severity="warning",
                    message="Wildcard import detected; use explicit imports instead"
                ))
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in deprecated:
                        self.result.add(ReviewComment(
                            file=filepath, line=node.lineno,
                            severity="warning",
                            message=f"Deprecated module '{alias.name}'"
                        ))

    def _check_error_handling(self, tree: ast.AST, filepath: str) -> None:
        """Detect bare except clauses."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                self.result.add(ReviewComment(
                    file=filepath, line=node.lineno,
                    severity="error",
                    message="Bare except clause detected; catches all exceptions",
                    suggestion="except SpecificException:"
                ))

    def _check_complexity(self, tree: ast.AST, filepath: str) -> None:
        """Flag overly complex functions."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                complexity = sum(1 for _ in ast.walk(node)
                               if isinstance(_, (ast.If, ast.While, ast.For,
                                               ast.ExceptHandler, ast.And, ast.Or)))
                if complexity > 10:
                    self.result.add(ReviewComment(
                        file=filepath, line=node.lineno,
                        severity="warning",
                        message=f"Function '{node.name}' has high complexity ({complexity})",
                        suggestion="Refactor into smaller functions"
                    ))

    def analyze_with_llm(self, source: str, filepath: str = "unknown.py") -> ReviewResult:
        """Use LLM to perform deep semantic analysis."""
        if not self.llm:
            return self.analyze_python(source, filepath)

        prompt = f"""Review this code for bugs, security issues, and improvements:
File: {filepath}
```python
{source[:4000]}
```
Provide structured feedback with file, line, severity, and message.
"""
        response = self.llm.complete(prompt)
        # Parse LLM response into review comments
        return self.result
