#!/bin/bash

echo "🏦 Agentic AI Loan Approval System - Setup Verification"
echo "=========================================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1)
if [[ $python_version == *"3."* ]]; then
    echo "  ✅ Python installed: $python_version"
else
    echo "  ❌ Python 3 not found"
    exit 1
fi

# Check if in project directory
echo ""
echo "✓ Checking project files..."
required_files=(
    "main.py"
    "agents.py"
    "orchestrator.py"
    "models.py"
    "config.py"
    "streamlit_app.py"
    "example_notebook.py"
    "requirements_enhanced.txt"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file NOT FOUND"
        exit 1
    fi
done

# Check virtual environment
echo ""
echo "✓ Checking virtual environment..."
if [ -d "venv" ]; then
    echo "  ✅ Virtual environment exists"
    
    # Check if activated
    if [[ "$VIRTUAL_ENV" == *"venv"* ]]; then
        echo "  ✅ Virtual environment is activated"
    else
        echo "  ⚠️  Virtual environment not activated"
        echo "     Run: source venv/bin/activate"
    fi
else
    echo "  ⚠️  Virtual environment not created yet"
    echo "     Run: python3 -m venv venv && source venv/bin/activate"
fi

# Check environment file
echo ""
echo "✓ Checking environment configuration..."
if [ -f ".env" ]; then
    if grep -q "CLAUDE_API_KEY" .env; then
        echo "  ✅ .env file found with API key placeholder"
        if grep -q "sk-" .env; then
            echo "  ✅ API key appears to be configured"
        else
            echo "  ⚠️  API key not configured (starts with sk-)"
        fi
    else
        echo "  ❌ .env file missing CLAUDE_API_KEY"
    fi
else
    echo "  ⚠️  .env file not found"
    echo "     Run: cp .env.complete .env"
fi

# Check documentation
echo ""
echo "✓ Checking documentation..."
docs=(
    "README.md"
    "ARCHITECTURE.md"
    "SETUP_GUIDE.md"
    "GETTING_STARTED.md"
    "PROJECT_SUMMARY.md"
)

for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo "  ✅ $doc"
    else
        echo "  ⚠️  $doc not found"
    fi
done

# Summary
echo ""
echo "=========================================================="
echo "Setup Verification Complete!"
echo "=========================================================="
echo ""
echo "Next Steps:"
echo "1. Ensure Python 3.9+ is installed ✓"
echo "2. Create virtual environment: python3 -m venv venv"
echo "3. Activate it: source venv/bin/activate"
echo "4. Install dependencies: pip install -r requirements_enhanced.txt"
echo "5. Configure .env with your CLAUDE_API_KEY"
echo "6. Run demo: python example_notebook.py"
echo "7. Start UI: streamlit run streamlit_app.py"
echo ""
echo "For help, see:"
echo "  • Quick Start: GETTING_STARTED.md"
echo "  • Full Setup: SETUP_GUIDE.md"
echo "  • Overview: PROJECT_SUMMARY.md"
echo ""
