"""Core orchestration engine — manages agent lifecycle, task distribution, and workflow execution."""

import asyncio
import logging
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    COMPLETED = "completed"


@dataclass
class Agent:
    name: str
    role: str
    capabilities: List[str]
    status: AgentStatus = AgentStatus.IDLE
    llm_client: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    id: str
    description: str
    agent: Optional[str] = None
    priority: int = 0
    status: str = "pending"
    result: Any = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)


class OrchestrationEngine:
    """Central orchestration engine for multi-agent coordination."""

    def __init__(self, max_concurrency: int = 5):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.workflows: Dict[str, List[str]] = {}
        self.max_concurrency = max_concurrency
        self._task_queue: asyncio.Queue = asyncio.Queue()

    def register_agent(self, agent: Agent) -> None:
        """Register an agent with the orchestration engine."""
        self.agents[agent.name] = agent
        logger.info(f"Agent registered: {agent.name} ({agent.role})")

    def create_task(self, task: Task) -> str:
        """Create a new task in the orchestration queue."""
        self.tasks[task.id] = task
        logger.info(f"Task created: {task.id} -> {task.description[:50]}...")
        return task.id

    def assign_task(self, task_id: str, agent_name: str) -> bool:
        """Assign a task to a specific agent."""
        task = self.tasks.get(task_id)
        agent = self.agents.get(agent_name)

        if not task or not agent:
            return False

        task.agent = agent_name
        task.status = "assigned"
        agent.status = AgentStatus.BUSY
        logger.info(f"Task {task_id} assigned to {agent_name}")
        return True

    def create_workflow(self, workflow_id: str, task_ids: List[str]) -> None:
        """Define a workflow as an ordered sequence of tasks."""
        self.workflows[workflow_id] = task_ids
        logger.info(f"Workflow created: {workflow_id} ({len(task_ids)} tasks)")

    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a full workflow with dependency resolution."""
        task_ids = self.workflows.get(workflow_id)
        if not task_ids:
            return {"error": f"Workflow '{workflow_id}' not found"}

        results = {}
        for task_id in task_ids:
            task = self.tasks.get(task_id)
            if not task:
                continue

            # Wait for dependencies
            for dep_id in task.dependencies:
                if dep_id in results and results[dep_id].get("status") != "completed":
                    logger.warning(f"Dependency {dep_id} not completed for {task_id}")

            # Execute task
            agent = self.agents.get(task.agent) if task.agent else None
            if agent and agent.llm_client:
                task.status = "running"
                try:
                    result = await agent.llm_client.complete(task.description)
                    task.status = "completed"
                    task.result = result
                    task.completed_at = datetime.now()
                    results[task_id] = {"status": "completed", "result": result}
                except Exception as e:
                    task.status = "failed"
                    task.error = str(e)
                    results[task_id] = {"status": "failed", "error": str(e)}
            else:
                task.status = "completed"
                results[task_id] = {"status": "skipped", "reason": "no agent assigned"}

        return results

    def get_agent_status(self) -> Dict[str, str]:
        """Get status of all registered agents."""
        return {name: agent.status.value for name, agent in self.agents.items()}

    def get_task_status(self) -> Dict[str, str]:
        """Get status of all tasks."""
        return {tid: task.status for tid, task in self.tasks.items()}
