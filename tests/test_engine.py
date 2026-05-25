"""Tests for the orchestration engine."""

import pytest
from orchestrator.core.engine import OrchestrationEngine, Agent, Task


class TestOrchestrationEngine:
    """Test suite for the core orchestration engine."""

    def setup_method(self):
        self.engine = OrchestrationEngine(max_concurrency=3)

    def test_register_agent(self):
        agent = Agent(name="test-agent", role="Tester", capabilities=["test"])
        self.engine.register_agent(agent)
        assert "test-agent" in self.engine.agents
        assert self.engine.agents["test-agent"].role == "Tester"

    def test_create_task(self):
        task = Task(id="task-1", description="Test task")
        task_id = self.engine.create_task(task)
        assert task_id == "task-1"
        assert self.engine.tasks["task-1"].status == "pending"

    def test_assign_task(self):
        self.engine.register_agent(Agent(name="agent-1", role="Worker", capabilities=["x"]))
        self.engine.create_task(Task(id="t1", description="Do something"))
        result = self.engine.assign_task("t1", "agent-1")
        assert result is True
        assert self.engine.tasks["t1"].agent == "agent-1"

    def test_workflow_creation(self):
        self.engine.create_task(Task(id="a", description="Step A"))
        self.engine.create_task(Task(id="b", description="Step B"))
        self.engine.create_workflow("test-flow", ["a", "b"])
        assert "test-flow" in self.engine.workflows
        assert self.engine.workflows["test-flow"] == ["a", "b"]

    def test_agent_status_report(self):
        self.engine.register_agent(Agent(name="agent-a", role="A", capabilities=["x"]))
        self.engine.register_agent(Agent(name="agent-b", role="B", capabilities=["y"]))
        status = self.engine.get_agent_status()
        assert status["agent-a"] == "idle"
        assert status["agent-b"] == "idle"
