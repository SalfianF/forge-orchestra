# Agent Lifecycle

## States

```
 +--------+              +----------+
 |  IDLE  | <-----------+ COMPLETED |
 +---^----+              +----------+
     |                        ^
     | task assigned          |
     v                        |
 +--------+   task completes  |
 |  BUSY  | ------------------+
 +---^----+
     | error
     v
 +--------+
 | ERROR  |
 +--------+
```

## Registration

Agents self-register with the engine on startup, declaring:
- Name and role identifier
- Capability list (what tasks they can handle)
- LLM client configuration
- Resource requirements

## Health Monitoring

The engine periodically pings agents for:
- Heartbeat status
- Resource utilization (CPU, memory, tokens)
- Queue depth (pending tasks)
- Error rate

## Graceful Shutdown

On SIGTERM:
1. Engine stops accepting new tasks
2. Waits for running tasks to complete (with timeout)
3. Persists incomplete task state to disk
4. Deregisters all agents
