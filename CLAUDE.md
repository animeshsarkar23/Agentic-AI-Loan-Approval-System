# Agentic AI Intelligent Loan Approval System

## Project Overview
A Multi-Agent Agentic AI system that analyzes loan applications and classifies them as Approved, Rejected, or Requires Manual Review using Claude API.

## Architecture

### Five-Agent System
1. **Document Verification Agent** - Validates applicant documents (income verification, employment confirmation)
2. **Credit Analysis Agent** - Analyzes credit history, credit score, payment patterns
3. **Risk Assessment Agent** - Evaluates risk indicators (debt-to-income ratio, industry, loan-to-value)
4. **Compliance Agent** - Checks regulatory compliance and anti-fraud rules
5. **Decision Agent** - Synthesizes all findings and makes final decision

### Tech Stack
- **Language**: Python 3.9+
- **Framework**: FastAPI (async, production-ready)
- **AI**: Claude API (multi-turn conversations, tool use)
- **Database**: SQLite (development), PostgreSQL (production)
- **Validation**: Pydantic
- **HTTP Client**: httpx (async)

### Key Files
- `main.py` - FastAPI application and API endpoints
- `agents/` - Individual agent implementations
- `models.py` - Pydantic data models
- `orchestrator.py` - Multi-agent orchestration logic
- `db.py` - Database and persistence layer
- `config.py` - Configuration and constants
- `example_notebook.ipynb` - Demonstration and testing

## Development Flow
1. Setup environment and install dependencies
2. Configure Claude API key
3. Define loan application data models
4. Implement individual agents
5. Create orchestrator for agent coordination
6. Build FastAPI endpoints
7. Test with sample loan applications
8. Deploy and monitor

## API Endpoints
- `POST /loans/analyze` - Submit loan application for analysis
- `GET /loans/{application_id}` - Get decision and detailed analysis
- `GET /loans` - List all applications
- `GET /health` - System health check

## Decision Classification
- **APPROVED**: Meets all criteria, low risk, compliant
- **REJECTED**: Fails critical checks or high risk
- **MANUAL_REVIEW**: Borderline case requiring human judgment
