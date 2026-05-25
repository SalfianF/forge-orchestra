"""Tests for the codebase analyzer agent."""

import pytest
import tempfile
import os
from agents.analyzer.metrics import CodebaseAnalyzer


class TestCodebaseAnalyzer:
    """Test the codebase analysis agent."""

    @pytest.fixture
    def temp_project(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.makedirs(f"{tmpdir}/src")
            with open(f"{tmpdir}/src/main.py", "w") as f:
                f.write("def hello():\n    print('hello')\n")
            with open(f"{tmpdir}/README.md", "w") as f:
                f.write("# Test Project\n")
            with open(f"{tmpdir}/config.yaml", "w") as f:
                f.write("version: 1\n")
            yield tmpdir

    def test_analyze_project_structure(self, temp_project):
        analyzer = CodebaseAnalyzer(temp_project)
        metrics = analyzer.analyze()
        assert metrics.total_files == 3
        assert metrics.total_lines >= 3
        assert "Python" in metrics.languages
        assert "Markdown" in metrics.languages

    def test_dependency_analysis(self, temp_project):
        analyzer = CodebaseAnalyzer(temp_project)
        deps = analyzer.dependency_analysis()
        assert isinstance(deps, dict)

    def test_risk_assessment(self, temp_project):
        analyzer = CodebaseAnalyzer(temp_project)
        risks = analyzer.risk_assessment()
        assert isinstance(risks, list)
