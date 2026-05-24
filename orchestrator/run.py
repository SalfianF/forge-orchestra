#!/usr/bin/env python3
"""CLI entry point for the Forge Orchestra orchestration engine."""

import argparse
import asyncio
import logging
import sys

from core.engine import OrchestrationEngine, Agent, Task
from core.planner import WorkflowPlanner
from workflows.pipelines import get_pipeline, list_pipelines

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Forge Orchestra — Multi-Agent Orchestration Engine")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Orchestrate command
    orchestrate_parser = subparsers.add_parser("orchestrate", help="Run an orchestrated workflow")
    orchestrate_parser.add_argument("pipeline", choices=list_pipelines(), help="Pipeline to execute")
    orchestrate_parser.add_argument("--agents", nargs="+", default=[], help="Agent names to use")

    # List command
    subparsers.add_parser("list", help="List available pipelines and agents")

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a codebase")
    analyze_parser.add_argument("path", help="Path to analyze")

    args = parser.parse_args()

    if args.command == "list":
        print("\n=== Forge Orchestra ===")
        print("\nAvailable pipelines:")
        for name in list_pipelines():
            pipeline = get_pipeline(name)
            print(f"  ├ {name}: {pipeline.description}")
        print("\nAvailable agents:")
        for agent in ["analyzer", "code-reviewer", "devops-agent"]:
            print(f"  ├ {agent}")
        print()

    elif args.command == "orchestrate":
        logger.info(f"Starting pipeline: {args.pipeline}")
        engine = OrchestrationEngine(max_concurrency=3)

        # Register default agents
        engine.register_agent(Agent(name="analyzer", role="Codebase Analysis", capabilities=["scan", "metrics"]))
        engine.register_agent(Agent(name="code-reviewer", role="Code Review", capabilities=["review", "analyze"]))
        engine.register_agent(Agent(name="devops-agent", role="DevOps Automation", capabilities=["deploy", "monitor"]))

        pipeline = get_pipeline(args.pipeline)
        workflow = pipeline.get_workflow()

        logger.info(f"Workflow: {workflow['workflow_id']}")
        print(f"Executed pipeline: {args.pipeline}")

    elif args.command == "analyze":
        print(f"Analysis of {args.path} requested")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
