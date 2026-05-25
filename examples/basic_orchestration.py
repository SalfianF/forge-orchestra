#!/usr/bin/env python3
"""Basic example: orchestrate a simple multi-agent workflow."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from orchestrator.core.engine import OrchestrationEngine, Agent, Task
from orchestrator.workflows.pipelines import get_pipeline


def main():
    engine = OrchestrationEngine(max_concurrency=3)

    # Register agents
    engine.register_agent(Agent(
        name="analyzer", role="Codebase Analysis",
        capabilities=["scan", "metrics", "analyze"]
    ))
    engine.register_agent(Agent(
        name="code-reviewer", role="Code Review",
        capabilities=["review", "analyze", "report"]
    ))

    # Load a pipeline
    pipeline = get_pipeline("code-review")
    workflow = pipeline.get_workflow()

    print(f"Loaded pipeline: {pipeline.name}")
    print(f"Description: {pipeline.description}")
    print(f"Stages: {len(workflow['parallel_stages'])}")

    # Create tasks from pipeline
    task_count = 0
    for stage in workflow["parallel_stages"]:
        for task_def in stage["tasks"]:
            task = Task(
                id=task_def["id"],
                description=f"Execute {task_def['action']}",
                agent=stage["agents"][0] if stage["agents"] else None,
            )
            engine.create_task(task)
            task_count += 1

    print(f"Created {task_count} tasks")
    print("\nEngine ready. Agents:", list(engine.agents.keys()))
    print("Tasks:", list(engine.tasks.keys()))


if __name__ == "__main__":
    main()
