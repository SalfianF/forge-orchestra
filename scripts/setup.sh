#!/bin/bash
# Forge Orchestra setup script

set -e

echo "=== Forge Orchestra Setup ==="

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env template..."
    cat > .env << 'ENVEOF'
# Forge Orchestra Configuration
ANTHROPIC_API_KEY=
MIMO_API_KEY=
MAX_CONCURRENCY=5
LOG_LEVEL=INFO
ENVEOF
    echo "Please edit .env with your API keys"
fi

echo ""
echo "Setup complete! Run: source venv/bin/activate"
