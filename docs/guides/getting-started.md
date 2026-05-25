# Getting Started

## Prerequisites

- Python 3.12+
- API keys for LLM providers (Claude, MiMo, etc.)
- Git

## Installation

```bash
git clone https://github.com/SalfianF/forge-orchestra.git
cd forge-orchestra
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and fill in your API keys:

```env
ANTHROPIC_API_KEY=sk-ant-...
MIMO_API_KEY=mimo-...
MAX_CONCURRENCY=5
LOG_LEVEL=INFO
```

## Quick Start

List available pipelines:
```bash
python orchestrator/run.py list
```

Run a code review pipeline:
```bash
python orchestrator/run.py orchestrate code-review
```

## Project Structure

```
forge-orchestra/
  agents/              # Agent implementations
  orchestrator/        # Core orchestration engine
  integrations/        # LLM and tool connectors
  docs/               # Documentation
  examples/           # Usage examples
  tests/              # Test suite
  scripts/            # Utility scripts
```
