#!/bin/bash
# Run Forge Orchestra test suite

set -e

echo "=== Forge Orchestra Test Suite ==="

# Activate venv if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with coverage
python -m pytest tests/ -v --cov=orchestrator --cov=agents --cov=integrations
