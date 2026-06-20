# Complete Setup & Deployment Guide

## 🚀 Quick Start (10 Minutes)

### Step 1: Get Anthropic API Key
```bash
# Visit https://console.anthropic.com
# Sign up or log in
# Generate an API key (starts with sk-)
```

### Step 2: Setup Environment
```bash
cd /home/ubuntu/Capstone

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_enhanced.txt

# Setup environment file
cp .env.complete .env
# Edit .env and add your CLAUDE_API_KEY
```

### Step 3: Run Demo
```bash
python example_notebook.py
```

### Step 4: Start Full System
```bash
# Terminal 1: Start FastAPI Server
python main.py

# Terminal 2: Start Streamlit UI
streamlit run streamlit_app.py

# Terminal 3: Start MCP Gateway (optional)
python mcp_servers.py gateway
```

Access:
- **Streamlit UI**: http://localhost:8501
- **FastAPI API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📋 Complete Setup Instructions

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Terminal/Command line
- Anthropic API key
- Modern web browser

### Step-by-Step Installation

#### 1. Clone/Navigate to Project
```bash
cd /home/ubuntu/Capstone
```

#### 2. Create Virtual Environment
```bash
# Create venv
python3 -m venv venv

# Activate venv
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Verify activation (should show (venv) prefix)
python --version
```

#### 3. Install Enhanced Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements_enhanced.txt

# Verify installations
python -c "import fastapi, streamlit, langgraph; print('✅ All dependencies installed')"
```

#### 4. Configure Environment
```bash
# Copy complete environment template
cp .env.complete .env

# Edit .env file
nano .env
# OR
code .env

# Replace placeholder values:
# CLAUDE_API_KEY=sk-your-actual-key-here
# FASTAPI_PORT=8000
# STREAMLIT_PORT=8501
```

#### 5. Verify Setup
```bash
# Test imports
python -c "
import anthropic
import fastapi
import streamlit
import langgraph
print('✅ All imports successful')
"

# Test environment variables
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv('CLAUDE_API_KEY')
if key and key.startswith('sk-'):
    print('✅ API key configured')
else:
    print('❌ API key not configured')
"
```

---

## 🏗️ Architecture Overview

### Component Stack

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                            │
├─────────────────────────────────────────────────────────────┤
│  Streamlit UI (Port 8501) | FastAPI Docs (Port 8000)       │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                         │
├─────────────────────────────────────────────────────────────┤
│  • Streamlit Application (streamlit_app.py)                │
│  • FastAPI REST API (main.py)                              │
│  • LangGraph Orchestrator (langgraph_orchestrator.py)      │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                  ORCHESTRATION LAYER                        │
├─────────────────────────────────────────────────────────────┤
│  • Agent Orchestrator (orchestrator.py)                    │
│  • LangGraph Workflow Engine                               │
│  • State Management                                         │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                    AGENT LAYER                              │
├─────────────────────────────────────────────────────────────┤
│  • Document Verification Agent                             │
│  • Credit Analysis Agent                                   │
│  • Risk Assessment Agent                                   │
│  • Compliance Agent                                        │
│  • Decision Agent                                          │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                    MCP LAYER                                │
├─────────────────────────────────────────────────────────────┤
│  • Document Verification MCP (Port 8502)                   │
│  • Credit Analysis MCP (Port 8503)                         │
│  • Compliance MCP (Port 8504)                              │
│  • MCP Registry (Port 8505)                                │
│  • MCP Gateway (Port 8506)                                 │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                   LLM & EXTERNAL                            │
├─────────────────────────────────────────────────────────────┤
│  • Anthropic Claude API                                    │
│  • (Future: Database, Cache, External Services)           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Running Components

### Option 1: Single Demo (Simplest)
```bash
# Just run the demo - no servers needed
python example_notebook.py
```
- Analyzes 3 sample applications
- Shows agent-by-agent analysis
- Displays summary statistics
- **Time**: ~2-3 minutes

### Option 2: FastAPI Server + Docs
```bash
# Terminal 1: Start API server
python main.py

# Browser: http://localhost:8000/docs
# Try endpoints in interactive documentation
```

### Option 3: Streamlit UI (Recommended)
```bash
# Terminal 1: Start FastAPI backend
python main.py

# Terminal 2: Start Streamlit frontend
streamlit run streamlit_app.py

# Browser: http://localhost:8501
```

### Option 4: Full System (Advanced)
```bash
# Terminal 1: FastAPI Server
python main.py

# Terminal 2: Streamlit UI
streamlit run streamlit_app.py

# Terminal 3: MCP Document Server
python mcp_servers.py document

# Terminal 4: MCP Credit Server
python mcp_servers.py credit

# Terminal 5: MCP Compliance Server
python mcp_servers.py compliance

# Terminal 6: MCP Registry
python mcp_servers.py registry

# Terminal 7: MCP Gateway
python mcp_servers.py gateway
```

### Option 5: LangGraph Orchestrator
```bash
# Use LangGraph orchestrator instead of default
from langgraph_orchestrator import LangGraphOrchestrator

orchestrator = LangGraphOrchestrator()
result = orchestrator.execute(app_id, loan_app)
```

---

## 🖥️ Component Details

### 1. Streamlit UI (`streamlit_app.py`)

**Purpose**: Interactive user interface for loan applications

**Features**:
- Submit new loan applications
- View application results
- Browse application history
- Monitor system status

**Access**:
- URL: http://localhost:8501
- Run: `streamlit run streamlit_app.py`
- Port: 8501 (configurable via `STREAMLIT_PORT`)

**Pages**:
1. **Submit Application** - Form to enter applicant details
2. **View Results** - See latest analysis results
3. **Application History** - Browse all submitted applications
4. **System Status** - Monitor system health

---

### 2. FastAPI Server (`main.py`)

**Purpose**: REST API backend

**Endpoints**:
- `POST /loans/analyze` - Submit application
- `GET /loans/{id}` - Get decision
- `GET /loans/{id}/details` - Get detailed analysis
- `GET /loans` - List all applications
- `GET /health` - Health check

**Access**:
- URL: http://localhost:8000
- Docs: http://localhost:8000/docs
- Run: `python main.py`
- Port: 8000 (configurable via `FASTAPI_PORT`)

---

### 3. Agents (`agents.py`)

**5 AI Agents** using Claude API:

1. **Document Verification Agent**
   - Validates documents
   - Checks confidence levels
   - Flags inconsistencies

2. **Credit Analysis Agent**
   - Analyzes credit score
   - Evaluates payment history
   - Assesses credit risk

3. **Risk Assessment Agent**
   - Calculates debt-to-income
   - Evaluates loan viability
   - Flags risk factors

4. **Compliance Agent**
   - Checks regulatory requirements
   - Validates loan amount
   - Ensures AML/KYC compliance

5. **Decision Agent**
   - Synthesizes all findings
   - Makes final decision
   - Provides reasoning

---

### 4. Orchestrators

#### Standard Orchestrator (`orchestrator.py`)
- Simple sequential + parallel execution
- In-memory caching
- Lightweight, fast

#### LangGraph Orchestrator (`langgraph_orchestrator.py`)
- Complex state management
- Conditional branching
- Retry logic
- Better for complex workflows

**Choose based on needs**:
- Simple: Use `orchestrator.py`
- Complex: Use `langgraph_orchestrator.py`

---

### 5. MCP Servers (`mcp_servers.py`)

**Model Context Protocol** for standardized agent communication

**Servers** (each can run independently):

1. **Document Verification MCP** (Port 8502)
   - Endpoint: `POST /mcp/document_verify`
   - Validates documents

2. **Credit Analysis MCP** (Port 8503)
   - Endpoint: `POST /mcp/credit_analyze`
   - Analyzes credit

3. **Compliance MCP** (Port 8504)
   - Endpoint: `POST /mcp/compliance_check`
   - Checks compliance

4. **MCP Registry** (Port 8505)
   - Endpoint: `GET /mcp/registry`
   - Service discovery

5. **MCP Gateway** (Port 8506)
   - Unified endpoint
   - Routes to all services

**Run individual MCP servers**:
```bash
python mcp_servers.py document    # Port 8502
python mcp_servers.py credit      # Port 8503
python mcp_servers.py compliance  # Port 8504
python mcp_servers.py registry    # Port 8505
python mcp_servers.py gateway     # Port 8506
```

---

## 🔌 Port Reference

| Component | Port | URL |
|-----------|------|-----|
| Streamlit UI | 8501 | http://localhost:8501 |
| FastAPI API | 8000 | http://localhost:8000 |
| FastAPI Docs | 8000 | http://localhost:8000/docs |
| Doc Verification MCP | 8502 | http://localhost:8502 |
| Credit Analysis MCP | 8503 | http://localhost:8503 |
| Compliance MCP | 8504 | http://localhost:8504 |
| MCP Registry | 8505 | http://localhost:8505 |
| MCP Gateway | 8506 | http://localhost:8506 |

**Custom ports**: Edit `.env` file to change ports

---

## 📊 Testing the System

### Quick Verification
```bash
# Test 1: Check Python environment
python --version

# Test 2: Check imports
python -c "import anthropic, fastapi, streamlit; print('✅ OK')"

# Test 3: Check API key
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv('CLAUDE_API_KEY')
print('✅ API key configured' if key else '❌ API key missing')
"

# Test 4: Run demo
python example_notebook.py
```

### API Testing
```bash
# Start server
python main.py

# In another terminal:

# Health check
curl http://localhost:8000/health

# Submit application
curl -X POST http://localhost:8000/loans/analyze \
  -H "Content-Type: application/json" \
  -d @sample_application.json

# View results
curl http://localhost:8000/loans
```

### Streamlit Testing
```bash
# Start FastAPI first
python main.py

# Then start Streamlit
streamlit run streamlit_app.py

# Open browser to http://localhost:8501
# Try submitting an application through the UI
```

---

## 🐛 Troubleshooting

### Issue: "API key not found"
```bash
# Solution 1: Check .env exists
ls -la .env

# Solution 2: Verify key format
grep CLAUDE_API_KEY .env

# Solution 3: Recreate .env
cp .env.complete .env
# Edit and add your key
```

### Issue: "Module not found"
```bash
# Solution 1: Verify venv is activated
source venv/bin/activate

# Solution 2: Reinstall dependencies
pip install --upgrade -r requirements_enhanced.txt

# Solution 3: Check Python version (need 3.9+)
python --version
```

### Issue: "Port already in use"
```bash
# Solution 1: Find process using port
lsof -i :8000  # or :8501, :8502, etc.

# Solution 2: Kill process
kill -9 <PID>

# Solution 3: Use different port
python main.py --port 9000
```

### Issue: "Very slow processing"
```bash
# Solution 1: Check internet connection
ping api.anthropic.com

# Solution 2: Check API quota
# Visit console.anthropic.com to check usage

# Solution 3: Try simpler test
python example_notebook.py
```

---

## 🚀 Deployment to Production

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_enhanced.txt .
RUN pip install -r requirements_enhanced.txt

COPY . .

ENV CLAUDE_API_KEY=${CLAUDE_API_KEY}
ENV FASTAPI_HOST=0.0.0.0
ENV FASTAPI_PORT=8000

EXPOSE 8000 8501

CMD ["python", "main.py"]
```

**Build & Run**:
```bash
# Build image
docker build -t loan-approval-system .

# Run container
docker run -e CLAUDE_API_KEY=sk-... -p 8000:8000 loan-approval-system
```

### Cloud Deployment

#### AWS (using App Runner/ECS)
```bash
# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag loan-approval-system:latest <account>.dkr.ecr.us-east-1.amazonaws.com/loan-approval-system:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/loan-approval-system:latest

# Deploy using App Runner or ECS
```

#### Google Cloud (Cloud Run)
```bash
# Build and deploy
gcloud run deploy loan-approval-system \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars CLAUDE_API_KEY=sk-...
```

#### Azure (Container Instances)
```bash
# Build and push to ACR
az acr build --registry <registry> --image loan-approval-system:latest .

# Deploy
az container create --resource-group <rg> --name loan-approval --image <registry>.azurecr.io/loan-approval-system:latest
```

---

## 📈 Performance Optimization

### Caching
- Results cached in memory (add Redis for distributed)
- Agent responses cached when identical inputs

### Parallel Execution
- Risk, Credit, Compliance agents run in parallel
- Document verification runs first (prerequisite)

### Async Operations
- FastAPI uses async/await for concurrency
- Non-blocking I/O for API calls

### Monitoring
- Add `/metrics` endpoint for Prometheus
- Enable structured logging (JSON format)

---

## 📚 Documentation Reference

| Document | Purpose |
|----------|---------|
| README.md | Overview & features |
| ARCHITECTURE.md | System design |
| CLAUDE.md | Project structure |
| GETTING_STARTED.md | Quick start |
| TESTING.md | Test procedures |
| SETUP_GUIDE.md | This file! |

---

## ✅ Success Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] .env file configured with API key
- [ ] Example demo runs successfully
- [ ] FastAPI server starts without errors
- [ ] Streamlit UI loads
- [ ] Can submit loan application via UI
- [ ] Decision appears with agent analysis
- [ ] Processing time < 30 seconds
- [ ] MCP servers (optional) start without errors

---

## 🎓 Next Steps

1. **Understand** - Read ARCHITECTURE.md
2. **Run** - Execute example_notebook.py
3. **Explore** - Try Streamlit UI at port 8501
4. **Test** - Use FastAPI docs at port 8000/docs
5. **Customize** - Modify thresholds in config.py
6. **Extend** - Add new agents or MCP servers
7. **Deploy** - containerize and deploy to cloud

---

Built with ❤️ using Python, Anthropic Claude, FastAPI, Streamlit, and LangGraph
