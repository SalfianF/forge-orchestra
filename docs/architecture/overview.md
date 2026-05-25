# Architecture Overview

## System Design

Forge Orchestra uses a **hub-and-spoke orchestration pattern**:

```
 ┌─────────────────────────────────────────┐
 │           Orchestration Engine          │
 │  ┌───────────────────────────────────┐  │
 │  │         Workflow Planner          │  │
 │  │  Decompose -> Schedule -> Execute   │  │
 │  └──────────┬────────────────────────┘  │
 │             │                           │
 │    ┌────────┼────────┬────────┐         │
 │    v        v        v        v         │
 │ Agent 1  Agent 2  Agent 3  Agent N     │
 │ (Code    (DevOps  (Analyzer) (Custom)  │
 │  Review)  Agent)                       │
 │    │        │        │        │        │
 │    +--------+--------+--------+        │
 │             v                          │
 │      ┌──────────┐                     │
 │      │  Results  │                     │
 │      │  Pipeline │                     │
 │      └──────────┘                     │
 └─────────────────────────────────────────┘
```

## Key Components

1. **Orchestration Engine** — Central coordinator that manages agent lifecycle and task distribution
2. **Workflow Planner** — Decomposes high-level goals into executable task graphs
3. **Agents** — Specialized workers that handle specific domains (code review, devops, analysis)
4. **Integrations** — Model adapters for Claude, MiMo, Hermes Agent, and more
5. **Pipeline Templates** — Pre-built workflow definitions for common use cases

## Data Flow

1. User submits a goal (e.g., "review this PR")
2. Planner decomposes goal into task graph with dependencies
3. Engine assigns tasks to appropriate agents
4. Agents execute tasks using configured LLM backends
5. Results flow back through the pipeline for aggregation
6. Final output is compiled and returned to the user
