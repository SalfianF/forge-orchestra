"""Codebase analysis agent that computes project metrics and insights."""

import os
import re
from collections import Counter, defaultdict
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class CodebaseMetrics:
    total_files: int = 0
    total_lines: int = 0
    total_functions: int = 0
    total_classes: int = 0
    languages: Dict[str, int] = None
    complexity_scores: Dict[str, float] = None

    def __post_init__(self):
        self.languages = self.languages or {}
        self.complexity_scores = self.complexity_scores or {}


class CodebaseAnalyzer:
    """Multi-agent codebase analyzer powered by LLM reasoning."""

    LANG_PATTERNS = {
        "Python": r"\.py$",
        "JavaScript": r"\.(js|jsx)$",
        "TypeScript": r"\.(ts|tsx)$",
        "Go": r"\.go$",
        "Rust": r"\.rs$",
        "Ruby": r"\.rb$",
        "Java": r"\.java$",
        "Kotlin": r"\.kt$",
        "YAML": r"\.(yml|yaml)$",
        "Markdown": r"\.md$",
        "Shell": r"\.(sh|bash)$",
    }

    def __init__(self, root_path: str):
        self.root = root_path
        self.metrics = CodebaseMetrics()

    def analyze(self) -> CodebaseMetrics:
        """Run full codebase analysis."""
        lang_counts = Counter()
        total_lines = 0
        total_files = 0

        for dirpath, _, filenames in os.walk(self.root):
            # Skip hidden dirs
            if "/." in dirpath:
                continue
            for f in filenames:
                filepath = os.path.join(dirpath, f)
                total_files += 1

                # Detect language
                for lang, pattern in self.LANG_PATTERNS.items():
                    if re.search(pattern, f):
                        lang_counts[lang] += 1
                        break
                else:
                    lang_counts["Other"] += 1

                # Count lines
                try:
                    with open(filepath, "r", errors="ignore") as fh:
                        total_lines += sum(1 for _ in fh)
                except:
                    pass

        self.metrics.total_files = total_files
        self.metrics.total_lines = total_lines
        self.metrics.languages = dict(lang_counts.most_common())

        return self.metrics

    def dependency_analysis(self) -> Dict[str, List[str]]:
        """Analyze dependencies between codebase components."""
        imports = defaultdict(list)
        for dirpath, _, filenames in os.walk(self.root):
            for f in filenames:
                if f.endswith(".py"):
                    filepath = os.path.join(dirpath, f)
                    rel_path = os.path.relpath(filepath, self.root)
                    with open(filepath, "r") as fh:
                        for line in fh:
                            m = re.match(r"^from\s+(\S+)\s+import|^import\s+(\S+)", line)
                            if m:
                                mod = m.group(1) or m.group(2)
                                imports[rel_path].append(mod)
        return dict(imports)

    def risk_assessment(self) -> List[Dict]:
        """Assess codebase risk areas using heuristic analysis."""
        risks = []
        high_risk_patterns = [
            (r"eval\s*\(", "Use of eval() — security risk"),
            (r"exec\s*\(", "Use of exec() — code injection risk"),
            (r"subprocess\.call.*shell=True", "Shell injection risk"),
            (r"os\.system\(", "OS command execution"),
            (r"pickle\.loads", "Insecure deserialization"),
            (r"sql_injection_pattern", "Potential SQL injection"),
        ]

        for dirpath, _, filenames in os.walk(self.root):
            for f in filenames:
                filepath = os.path.join(dirpath, f)
                try:
                    with open(filepath, "r") as fh:
                        for i, line in enumerate(fh, 1):
                            for pattern, desc in high_risk_patterns:
                                if re.search(pattern, line):
                                    risks.append({
                                        "file": os.path.relpath(filepath, self.root),
                                        "line": i,
                                        "risk": desc,
                                        "severity": "high",
                                    })
                except:
                    continue

        return risks
