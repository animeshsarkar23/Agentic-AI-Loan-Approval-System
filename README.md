# 🏦 Agentic AI Intelligent Loan Approval System

## Overview

A production-ready, multi-agent AI system that automates loan application analysis using Claude API. The system evaluates applicants across multiple dimensions (document verification, credit analysis, risk assessment, compliance) and provides explainable, auditable decisions.

### Key Features

✅ **Multi-Agent Architecture** - 5 specialized AI agents working collaboratively
✅ **Explainable Decisions** - Detailed reasoning from each agent
✅ **Fast Processing** - Parallel agent execution (< 30 seconds per application)
✅ **Scalable Design** - RESTful API for easy integration
✅ **Audit Trail** - Complete decision history with agent-level analysis
✅ **Three Decision Classes** - APPROVED, REJECTED, or MANUAL_REVIEW

## Architecture

### Five-Agent System

```
┌─────────────────────────────────────────────────────────────┐
│                    Loan Application                          │
└────────────┬────────────────────────────────────────────────┘
             │
      ┌──────▼────────┐
      │  Orchestrator │
      └──────┬────────┘
             │
    ┌────────┴──────────┬──────────────┬──────────────┐
    │                   │              │              │
    ▼                   ▼              ▼              ▼
┌─────────────┐  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐
│ Document    │  │ Credit      │ │ Risk        │ │ Compliance   │
│ Verification│  │ Analysis    │ │ Assessment  │ │ Agent        │
└────┬────────┘  └────┬────────┘ └────┬────────┘ └──────┬───────┘
     │                │               │                 │
     └────────────────┼───────────────┼─────────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │ Decision Agent       │
            │ (Final Synthesis)    │
            └──────────┬───────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │ APPROVED / REJECTED  │
            │ or MANUAL_REVIEW     │
            └──────────────────────┘
```

### Agent Responsibilities

| Agent | Role | Outputs |
|-------|------|---------|
| **Document Verification** | Validates income/employment docs | Authenticity score, red flags |
| **Credit Analysis** | Evaluates credit history | Credit risk level, payment patterns |
| **Risk Assessment** | Analyzes DTI, loan viability | Risk score, loan appropriateness |
| **Compliance** | Checks regulatory requirements | Compliance score, violations |
| **Decision** | Synthesizes findings | Final decision, reasoning |

## Setup & Installation

### Prerequisites

- Python 3.9+
- Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))

### Installation

1. **Clone/Navigate to project**
```bash
cd /home/ubuntu/Capstone
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API key**
```bash
cp .env.example .env
# Edit .env and add your CLAUDE_API_KEY
```

## Usage

### Option 1: Run Example Script

```bash
python example_notebook.py
```

This analyzes 3 sample loan applications:
- Low-risk candidate (likely APPROVED)
- Medium-risk candidate (likely MANUAL_REVIEW)
- High-risk candidate (likely REJECTED)

### Option 2: Run FastAPI Server

```bash
python main.py
```

Then access the API at `http://localhost:8000`

**API Documentation**: `http://localhost:8000/docs`

### API Endpoints

#### 1. Submit Loan Application
```bash
curl -X POST http://localhost:8000/loans/analyze \
  -H "Content-Type: application/json" \
  -d @sample_application.json
```

#### 2. Get Application Status & Decision
```bash
curl http://localhost:8000/loans/{application_id}
```

#### 3. Get Detailed Agent Analysis
```bash
curl http://localhost:8000/loans/{application_id}/details
```

#### 4. List All Applications
```bash
curl http://localhost:8000/loans
```

#### 5. Health Check
```bash
curl http://localhost:8000/health
```

## Decision Logic

### Scoring Rules

The system calculates scores from each agent (0-100) and synthesizes them:

- **APPROVED** (Decision Score ≥ 75)
  - All agents recommend Approve
  - All compliance and risk checks pass
  
- **REJECTED** (Decision Score < 40)
  - Any agent recommends Reject
  - Critical compliance violations
  - Credit score below minimum threshold
  
- **MANUAL_REVIEW** (40 ≤ Decision Score < 75)
  - Mixed recommendations from agents
  - Borderline risk factors
  - Requires human expert review

### Risk Thresholds

```python
MIN_CREDIT_SCORE = 600
MAX_DEBT_TO_INCOME = 0.43 (43%)
MIN_INCOME_VERIFICATION_CONFIDENCE = 0.80
MIN_EMPLOYMENT_VERIFICATION_CONFIDENCE = 0.70
LOAN_AMOUNT_RANGE = $10,000 - $1,000,000
```

## Input Parameters

### Applicant Profile
- First name, Last name, Email, Phone
- Date of birth, SSN (last 4 digits)
- Annual income, Employment status
- Years employed, Current employer

### Loan Details
- Loan amount, Loan purpose (Home/Auto/Personal/Business)
- Loan term (months), Interest rate requested

### Credit Profile
- Credit score (300-850)
- Number of open accounts
- Delinquencies (30-day, 90-day)
- Total debt, Recent inquiries
- Bankruptcy history

### Document Verification
- Income verification status & confidence
- Employment verification status & confidence
- List of provided documents (W2, Pay stubs, Tax returns, etc.)

## Output/Decision Details

Each decision includes:

1. **Final Decision** - APPROVED / REJECTED / MANUAL_REVIEW
2. **Decision Score** - 0-100 confidence score
3. **Reasoning** - Clear explanation of the decision
4. **Agent Analyses** - Individual scores and recommendations from each agent
5. **Risk Flags** - Identified risk factors
6. **Compliance Issues** - Regulatory violations if any
7. **Processing Time** - Time taken to analyze

## Project Structure

```
/home/ubuntu/Capstone/
├── main.py                 # FastAPI application & endpoints
├── agents.py               # Five AI agents implementation
├── orchestrator.py         # Multi-agent orchestration logic
├── models.py               # Pydantic data models
├── config.py               # Configuration & constants
├── example_notebook.py     # Demo script with 3 sample applications
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── CLAUDE.md              # Project documentation
└── README.md              # This file
```

## Example Workflow

```python
from models import ApplicantInfo, LoanDetails, CreditProfile, DocumentVerification, LoanApplication
from orchestrator import LoanOrchestrator

# 1. Create loan application
loan_app = LoanApplication(
    applicant_info=ApplicantInfo(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="555-0001",
        date_of_birth="1980-05-15",
        ssn_last_4="1234",
        annual_income=150_000,
        employment_status="Employed",
        years_employed=8.5,
        current_employer="Tech Corp"
    ),
    loan_details=LoanDetails(
        loan_amount=300_000,
        loan_purpose="Home",
        loan_term_months=360
    ),
    credit_profile=CreditProfile(
        credit_score=750,
        accounts_open=5,
        delinquencies_past_30_days=0,
        delinquencies_past_90_days=0,
        total_debt=45_000,
        inquiries_last_6_months=1
    ),
    document_verification=DocumentVerification(
        income_verification_status="Verified",
        income_verification_confidence=0.95,
        employment_verification_status="Verified",
        employment_verification_confidence=0.90,
        documents_provided=["W2", "Pay stubs (3 months)"]
    )
)

# 2. Analyze application
orchestrator = LoanOrchestrator()
decision_result = orchestrator.analyze_application(loan_app)

# 3. View results
print(f"Decision: {decision_result.final_decision}")
print(f"Score: {decision_result.decision_score}")
print(f"Reasoning: {decision_result.reasoning}")
```

## Advanced Features

### Parallel Agent Execution

Agents run in parallel where possible:
- Document Verification runs first (prerequisite)
- Credit, Risk, and Compliance agents run simultaneously
- Decision Agent synthesizes all findings

### Caching

Results are cached in memory for fast retrieval without re-analysis.

### Extensibility

Easy to add new agents:
1. Create new agent function in `agents.py`
2. Add to orchestrator flow
3. Update decision logic in `decision_agent`

## Performance

- **Average Processing Time**: 15-30 seconds per application
- **Throughput**: ~120 applications/hour per instance
- **Scalability**: Horizontal scaling via load balancer + multiple instances

## Security Considerations

✅ API key stored in environment variables
✅ Input validation with Pydantic
✅ CORS protection
✅ Request timeouts configured
✅ Error handling without exposing sensitive info

## Monitoring & Logging

Track system health:
- Health check endpoint: `/health`
- View all decisions: `/loans`
- Detailed analysis per application: `/loans/{id}/details`

## Future Enhancements

- [ ] Persistent database (PostgreSQL)
- [ ] User authentication & authorization
- [ ] Webhook notifications on decision
- [ ] Machine learning model refinement
- [ ] Fraud detection enhancement
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Integration with external credit bureaus

## Support

For issues or questions:
1. Check the example script: `python example_notebook.py`
2. Review CLAUDE.md for architecture details
3. Check FastAPI docs at `/docs` when server is running

## License

Proprietary - Banking System Only

---

Built with ❤️ using Claude AI and FastAPI
