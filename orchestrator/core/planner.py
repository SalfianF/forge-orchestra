"""Workflow planner — decomposes complex goals into executable task graphs."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class PlanStep:
    id: str
    action: str
    agent_type: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)
    priority: int = 0


@dataclass
class ExecutionPlan:
    goal: str
    steps: List[PlanStep] = field(default_factory=list)
    estimated_cost: float = 0.0
    estimated_tokens: int = 0


class WorkflowPlanner:
    """Decomposes high-level goals into orchestrated multi-agent plans."""

    def plan_code_review(self, repo_path: str, depth: str = "standard") -> ExecutionPlan:
        """Generate a code review execution plan."""
        plan = ExecutionPlan(goal=f"Comprehensive code review of {repo_path}")

        plan.steps = [
            PlanStep(id="scan-1", action="scan_structure", agent_type="analyzer",
                     inputs={"path": repo_path}),
            PlanStep(id="analyze-1", action="static_analysis", agent_type="analyzer",
                     inputs={"path": repo_path}, depends_on=["scan-1"]),
            PlanStep(id="review-1", action="deep_review", agent_type="code-reviewer",
                     inputs={"path": repo_path}, depends_on=["analyze-1"]),
            PlanStep(id="report-1", action="generate_report", agent_type="code-reviewer",
                     inputs={}, depends_on=["review-1"]),
        ]

        plan.estimated_tokens = 50000
        return plan

    def plan_deployment(self, service: str, environment: str = "staging") -> ExecutionPlan:
        """Generate a deployment execution plan."""
        plan = ExecutionPlan(goal=f"Deploy {service} to {environment}")

        plan.steps = [
            PlanStep(id="build-1", action="build_image", agent_type="devops-agent",
                     inputs={"service": service, "tag": "latest"}),
            PlanStep(id="test-1", action="run_tests", agent_type="devops-agent",
                     inputs={"service": service}, depends_on=["build-1"]),
            PlanStep(id="deploy-1", action="deploy_service", agent_type="devops-agent",
                     inputs={"service": service, "env": environment}, depends_on=["test-1"]),
            PlanStep(id="verify-1", action="health_check", agent_type="devops-agent",
                     inputs={"service": service}, depends_on=["deploy-1"]),
        ]

        plan.estimated_tokens = 35000
        return plan

    def plan_codebase_audit(self, path: str) -> ExecutionPlan:
        """Generate a full codebase audit plan."""
        plan = ExecutionPlan(goal=f"Full audit of {path}")

        plan.steps = [
            PlanStep(id="metrics-1", action="compute_metrics", agent_type="analyzer",
                     inputs={"path": path}),
            PlanStep(id="deps-1", action="analyze_dependencies", agent_type="analyzer",
                     inputs={"path": path}),
            PlanStep(id="risk-1", action="risk_assessment", agent_type="analyzer",
                     inputs={"path": path}, depends_on=["metrics-1", "deps-1"]),
            PlanStep(id="report-1", action="audit_report", agent_type="analyzer",
                     inputs={}, depends_on=["risk-1"]),
        ]

        plan.estimated_tokens = 60000
        return plan
