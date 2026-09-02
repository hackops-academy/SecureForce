#!/bin/bash
# Quick setup script for PayloadForce

set -e

echo "╔══════════════════════════════════════════════════════╗"
echo "║          PayloadForce Quick Setup                   ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Install it first:"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   macOS: brew install python3"
    exit 1
fi

PYTHON_VER=$(python3 --version | awk '{print $2}')
echo "✓ Python $PYTHON_VER detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv payloadforce-venv
source payloadforce-venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements-payloadforce.txt --quiet

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║             Setup Complete!                         ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "🚀 To start PayloadForce:"
echo ""
echo "   # Activate virtual environment"
echo "   source payloadforce-venv/bin/activate"
echo ""
echo "   # Run PayloadForce"
echo "   python3 payloadforce.py"
echo ""
echo "📚 For help, type: help"
echo ""
