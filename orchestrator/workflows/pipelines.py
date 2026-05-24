"""Pre-built workflow pipeline templates for common use cases."""

from typing import Dict, List, Any


class PipelineTemplate:
    """Base class for pipeline workflow templates."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def get_workflow(self) -> Dict[str, Any]:
        """Return the workflow definition."""
        raise NotImplementedError


class CodeReviewPipeline(PipelineTemplate):
    """End-to-end code review pipeline."""

    def __init__(self):
        super().__init__(
            name="code-review",
            description="Automated PR review with static analysis + LLM review"
        )

    def get_workflow(self) -> Dict[str, Any]:
        return {
            "workflow_id": "code-review-pipeline",
            "parallel_stages": [
                {
                    "stage": "analysis",
                    "agents": ["analyzer"],
                    "tasks": [
                        {"id": "static-analysis", "action": "scan_codebase"},
                        {"id": "metrics", "action": "compute_metrics"},
                    ]
                },
                {
                    "stage": "review",
                    "agents": ["code-reviewer"],
                    "depends_on": ["analysis"],
                    "tasks": [
                        {"id": "llm-review", "action": "deep_llm_review"},
                    ]
                },
                {
                    "stage": "report",
                    "agents": ["code-reviewer"],
                    "depends_on": ["review"],
                    "tasks": [
                        {"id": "generate-summary", "action": "create_review_summary"},
                        {"id": "suggest-fixes", "action": "suggest_corrections"},
                    ]
                }
            ]
        }


class DevOpsPipeline(PipelineTemplate):
    """CI/CD deployment pipeline with health verification."""

    def __init__(self):
        super().__init__(
            name="devops-deploy",
            description="Build, test, deploy, and verify pipeline"
        )

    def get_workflow(self) -> Dict[str, Any]:
        return {
            "workflow_id": "devops-pipeline",
            "parallel_stages": [
                {
                    "stage": "build",
                    "agents": ["devops-agent"],
                    "tasks": [
                        {"id": "build-artifact", "action": "compile_and_build"},
                        {"id": "unit-tests", "action": "run_unit_tests"},
                    ]
                },
                {
                    "stage": "deploy",
                    "agents": ["devops-agent"],
                    "depends_on": ["build"],
                    "tasks": [
                        {"id": "deploy-staging", "action": "deploy_to_staging"},
                    ]
                },
                {
                    "stage": "verify",
                    "agents": ["devops-agent"],
                    "depends_on": ["deploy"],
                    "tasks": [
                        {"id": "health-check", "action": "verify_deployment"},
                        {"id": "smoke-tests", "action": "run_smoke_tests"},
                    ]
                }
            ]
        }


class FullAuditPipeline(PipelineTemplate):
    """Comprehensive codebase audit pipeline."""

    def __init__(self):
        super().__init__(
            name="full-audit",
            description="Complete codebase analysis with risk assessment"
        )

    def get_workflow(self) -> Dict[str, Any]:
        return {
            "workflow_id": "audit-pipeline",
            "parallel_stages": [
                {
                    "stage": "collect",
                    "agents": ["analyzer"],
                    "tasks": [
                        {"id": "gather-metrics", "action": "collect_all_metrics"},
                        {"id": "map-deps", "action": "dependency_graph"},
                    ]
                },
                {
                    "stage": "analyze",
                    "agents": ["analyzer", "code-reviewer"],
                    "depends_on": ["collect"],
                    "tasks": [
                        {"id": "security-scan", "action": "vulnerability_scan"},
                        {"id": "quality-check", "action": "code_quality_analysis"},
                        {"id": "performance", "action": "performance_audit"},
                    ]
                },
                {
                    "stage": "report",
                    "agents": ["code-reviewer"],
                    "depends_on": ["analyze"],
                    "tasks": [
                        {"id": "exec-summary", "action": "executive_summary"},
                        {"id": "remediation", "action": "remediation_plan"},
                    ]
                }
            ]
        }


# Registry of available pipelines
PIPELINE_REGISTRY: Dict[str, PipelineTemplate] = {
    "code-review": CodeReviewPipeline(),
    "devops-deploy": DevOpsPipeline(),
    "full-audit": FullAuditPipeline(),
}


def get_pipeline(name: str) -> PipelineTemplate:
    """Get a pipeline template by name."""
    pipeline = PIPELINE_REGISTRY.get(name)
    if not pipeline:
        raise ValueError(f"Pipeline '{name}' not found. Available: {list(PIPELINE_REGISTRY.keys())}")
    return pipeline


def list_pipelines() -> List[str]:
    """List all available pipeline templates."""
    return list(PIPELINE_REGISTRY.keys())
