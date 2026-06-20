# Architecture Documentation - Agentic AI Loan Approval System

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          EXTERNAL CLIENTS                                    │
│                    (Web, Mobile, Backend Systems)                            │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                    HTTP/JSON (FastAPI)
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       FASTAPI REST API LAYER                                 │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  POST /loans/analyze          - Submit application                   │   │
│  │  GET  /loans/{id}             - Get decision & status               │   │
│  │  GET  /loans/{id}/details     - Get detailed agent analysis         │   │
│  │  GET  /loans                  - List all applications               │   │
│  │  GET  /health                 - System health check                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                    Request Routing & Validation
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATOR LAYER                                    │
│                  LoanOrchestrator (orchestrator.py)                          │
│                                                                              │
│  • Application ID Generation                                                │
│  • Agent Coordination & Sequencing                                          │
│  • Result Caching & Persistence                                             │
│  • Error Handling & Recovery                                                │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
        ┌────────────────────────┴────────────────────────┐
        │                                                 │
        │         Multi-Agent Execution Layer            │
        │                                                 │
        ▼                                                 ▼
    Phase 1:                                         Phase 2:
  Prerequisite                                    Parallel Agents
    Agent                                         (Concurrent)
        │
        ▼
┌──────────────────────┐
│ Document            │
│ Verification        │
│ Agent               │
│                     │
│ Validates:          │
│ • Income docs       │
│ • Employment docs   │
│ • Document quality  │
│                     │
│ Output:             │
│ • Auth score        │
│ • Red flags         │
│ • Confidence level  │
└──────────┬──────────┘
           │
    ┌──────┴──────┬───────────┬──────────┐
    │             │           │          │
    ▼             ▼           ▼          ▼
┌─────────┐ ┌──────────┐ ┌─────────┐ ┌─────────────┐
│ Credit  │ │ Risk     │ │Compli-  │ │ Each Agent: │
│Analysis │ │Assessment│ │ance     │ │             │
│ Agent   │ │ Agent    │ │ Agent   │ │ • Claude AI │
│         │ │          │ │         │ │ • Receives: │
│Analyzes:│ │Evaluates:│ │Checks:  │ │   App data  │
│• Credit │ │• DTI     │ │• Regs   │ │ • Outputs:  │
│ history │ │• Loan amt│ │• Fraud  │ │   Score    │
│• Payment│ │• Industry│ │• AML    │ │   Rec.     │
│ pattern │ │• Viability│ │• KYC    │ │   Analysis │
│         │ │          │ │         │ │             │
│Output:  │ │Output:   │ │Output:  │ │             │
│• Risk   │ │• Risk    │ │• Compli-│ │             │
│ level   │ │ score    │ │ ance    │ │             │
│* Score  │ │* Flags   │ │ score   │ │             │
│* Recom  │ │*Loan app │ │* Issues │ │             │
└─────────┘ └──────────┘ └─────────┘ └─────────────┘
    │             │           │          │
    └─────────────┼───────────┼──────────┘
                  │
        Collect All Agent Outputs
                  │
                  ▼
       ┌──────────────────────┐
       │ Decision Agent       │
       │ (Synthesis Layer)    │
       │                      │
       │ Orchestrates:        │
       │ • Score synthesis    │
       │ • Decision logic     │
       │ • Reasoning gen.     │
       │ • Risk aggregation   │
       │ • Compliance summary │
       │                      │
       │ Outputs:             │
       │ • Final decision     │
       │ • Reasoning          │
       │ • Risk flags         │
       │ • Compliance issues  │
       └──────────┬───────────┘
                  │
                  ▼
       ┌──────────────────────────────┐
       │ DECISION: APPROVED           │
       │ DECISION: REJECTED           │
       │ DECISION: MANUAL_REVIEW      │
       └──────────┬───────────────────┘
                  │
      Result Caching & Aggregation
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        RESPONSE LAYER (FastAPI)                              │
│                                                                              │
│ {                                                                            │
│   "application_id": "uuid",                                                 │
│   "final_decision": "APPROVED|REJECTED|MANUAL_REVIEW",                     │
│   "decision_score": 85.5,                                                   │
│   "reasoning": "...",                                                       │
│   "agent_analyses": [...],                                                  │
│   "risk_flags": [...],                                                      │
│   "compliance_issues": [...],                                               │
│   "processing_time_seconds": 22.5                                           │
│ }                                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
Loan Application (JSON)
│
├─ Applicant Info
│  ├─ Name, Email, Phone
│  ├─ Income, Employment Status
│  └─ Years Employed
│
├─ Loan Details
│  ├─ Amount, Purpose
│  ├─ Term, Interest Rate
│  └─ Location
│
├─ Credit Profile
│  ├─ Credit Score
│  ├─ Accounts, Delinquencies
│  └─ Total Debt, Inquiries
│
└─ Document Verification
   ├─ Income Verification
   ├─ Employment Verification
   └─ Documents Provided


       ▼ (Orchestrator processes)


Agent 1: Document Verification → Score: 85, Rec: Approve
Agent 2: Credit Analysis → Score: 80, Rec: Approve
Agent 3: Risk Assessment → Score: 75, Rec: Approve
Agent 4: Compliance → Score: 90, Rec: Approve

       ▼ (Decision Agent synthesizes)

Final Decision: APPROVED (Score: 82.5)
Reasoning: "..."
Risk Flags: []
Compliance Issues: []

       ▼ (Response to client)

HTTP 200 OK with complete analysis
```

## Component Descriptions

### 1. FastAPI REST API Layer (`main.py`)
**Responsibility**: HTTP request handling, validation, routing

**Key Components**:
- Route handlers for all endpoints
- Request validation via Pydantic models
- CORS middleware
- Error handling and HTTP status codes
- Response formatting

**Interfaces**:
- Accepts: JSON loan applications
- Returns: JSON decision results
- Status codes: 200 (OK), 404 (Not Found), 500 (Error)

---

### 2. Orchestrator Layer (`orchestrator.py`)
**Responsibility**: Multi-agent coordination, sequencing, result management

**Key Components**:
- `LoanOrchestrator` class
- Phase sequencing (prerequisite + parallel)
- Result caching
- Error recovery

**Methods**:
```python
analyze_application(loan_app) -> LoanDecisionResult
get_result(application_id) -> LoanDecisionResult
get_all_results() -> List[LoanDecisionResult]
```

---

### 3. Agents Layer (`agents.py`)
**Responsibility**: Specialized AI analysis via Claude API

**Five Agents**:

#### 3.1 Document Verification Agent
```python
document_verification_agent(loan_app) -> AgentAnalysis
```
- Validates income documentation
- Validates employment verification
- Returns authenticity score and red flags

#### 3.2 Credit Analysis Agent
```python
credit_analysis_agent(loan_app) -> AgentAnalysis
```
- Analyzes credit score and history
- Evaluates payment patterns
- Returns credit risk level

#### 3.3 Risk Assessment Agent
```python
risk_assessment_agent(loan_app) -> AgentAnalysis
```
- Calculates debt-to-income ratio
- Assesses loan amount viability
- Returns risk score and flags

#### 3.4 Compliance Agent
```python
compliance_agent(loan_app) -> AgentAnalysis
```
- Checks regulatory compliance
- Validates against AML/KYC rules
- Returns compliance score

#### 3.5 Decision Agent
```python
decision_agent(loan_app, agent_analyses) -> dict
```
- Synthesizes all agent outputs
- Applies decision logic
- Returns final decision and reasoning

---

### 4. Data Models (`models.py`)
**Responsibility**: Data validation and structure

**Key Models**:
```
ApplicantInfo
  ├─ Personal (name, email, phone, DOB, SSN)
  ├─ Financial (income, employment, years employed)
  └─ Employment (status, employer)

LoanDetails
  ├─ Loan amount, purpose
  ├─ Term, interest rate
  └─ (extensible for future fields)

CreditProfile
  ├─ Credit score
  ├─ Account metrics
  ├─ Delinquency history
  └─ Bankruptcy info

DocumentVerification
  ├─ Income verification (status, confidence)
  ├─ Employment verification (status, confidence)
  └─ Documents provided (list)

LoanApplication
  ├─ ApplicantInfo
  ├─ LoanDetails
  ├─ CreditProfile
  ├─ DocumentVerification
  └─ ID (generated or provided)

LoanDecisionResult
  ├─ Final decision (APPROVED/REJECTED/MANUAL_REVIEW)
  ├─ Decision score (0-100)
  ├─ Reasoning (explanation)
  ├─ Agent analyses (detailed)
  ├─ Risk flags
  └─ Compliance issues

ApplicationResponse
  ├─ Application ID
  ├─ Status
  ├─ Decision (if complete)
  ├─ Decision result (if complete)
  └─ Error message (if failed)
```

---

### 5. Configuration (`config.py`)
**Responsibility**: Constants, thresholds, settings

**Key Configurations**:
```python
CLAUDE_API_KEY = "sk-..."
MODEL = "claude-3-5-sonnet-20241022"
API_TIMEOUT = 30

MIN_CREDIT_SCORE = 600
MAX_DEBT_TO_INCOME = 0.43
MIN_INCOME_VERIFICATION_CONFIDENCE = 0.80
MIN_EMPLOYMENT_VERIFICATION_CONFIDENCE = 0.70
MAX_LOAN_AMOUNT = 1_000_000
MIN_LOAN_AMOUNT = 10_000
```

---

## Request/Response Lifecycle

### Request Processing Flow

```
1. Client sends POST /loans/analyze
   └─ JSON loan application

2. FastAPI validates request
   └─ Pydantic model validation

3. Orchestrator.analyze_application() called
   ├─ Phase 1: Document Verification Agent
   │   └─ Claude API call (prompt + context)
   │
   ├─ Phase 2: Parallel agents
   │   ├─ Credit Analysis Agent (Claude API)
   │   ├─ Risk Assessment Agent (Claude API)
   │   └─ Compliance Agent (Claude API)
   │
   └─ Phase 3: Decision Agent
       └─ Claude API call (synthesizing all outputs)

4. Results cached in memory

5. Response formatted and returned
   └─ JSON with decision, reasoning, agent analyses

6. Client receives response
   └─ HTTP 200 OK with complete analysis
```

### Decision Logic

```
Calculate Composite Score:
  1. Get scores from all 4 analysis agents
  2. Weight scores equally (25% each)
  3. Synthesize into decision score (0-100)

Decision Rules:
  IF decision_score >= 75 AND all agents recommend Approve
    → APPROVED
  
  ELSE IF decision_score < 40 OR any agent recommends Reject
    → REJECTED
  
  ELSE (40 <= decision_score < 75)
    → MANUAL_REVIEW
```

---

## Scalability & Performance

### Current Architecture (Single Instance)

```
┌─────────────────────────────────┐
│     FastAPI Server              │
│  (localhost:8000)               │
│                                 │
│  • Handles 1 request at a time  │
│  • In-memory caching            │
│  • Local processing             │
└─────────────────────────────────┘
           │
           ▼
    Claude API (remote)
    Rate limited per key
```

### Scalable Architecture (Production)

```
┌──────────────────────────────────┐
│     Load Balancer                │
│  (API Gateway)                   │
└──────┬───────────────────────────┘
       │
   ┌───┴──┬──────┐
   │      │      │
   ▼      ▼      ▼
┌──────┐┌──────┐┌──────┐
│FastAPI│FastAPI│FastAPI│  (3 instances)
│  +    │  +    │  +    │
│Orchs. │Orchs. │Orchs. │
└───┬───┘└───┬──┘└───┬──┘
    │        │       │
    └────┬───┴───┬───┘
         │       │
         ▼       ▼
    ┌────────────────┐
    │ PostgreSQL DB  │  (Shared state)
    │ (Persistent)   │
    └────────────────┘
         │
         ▼
    ┌────────────────┐
    │  Redis Cache   │  (Distributed cache)
    └────────────────┘
```

---

## Error Handling

### Error Propagation

```
Client Request
    │
    ▼
API Validation
    ├─ Invalid JSON → 400 Bad Request
    ├─ Missing fields → 422 Unprocessable Entity
    └─ Valid → proceed

    ▼
Orchestrator Processing
    ├─ Agent fails → Retry logic / Fallback
    ├─ API timeout → 504 Gateway Timeout
    └─ Success → Continue

    ▼
Response Generation
    ├─ Error → 500 Internal Server Error
    └─ Success → 200 OK

    ▼
Client receives response
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────┐
│              SECURITY LAYERS                        │
├─────────────────────────────────────────────────────┤
│ 1. Input Validation                                │
│    └─ Pydantic models enforce schema              │
│                                                     │
│ 2. API Key Management                              │
│    └─ Environment variables (.env)                │
│    └─ Never hardcoded or logged                    │
│                                                     │
│ 3. CORS Protection                                 │
│    └─ Restrict cross-origin requests              │
│                                                     │
│ 4. Data Privacy                                    │
│    └─ SSN last-4 only stored                      │
│    └─ No plaintext sensitive data                  │
│                                                     │
│ 5. Audit Trail                                     │
│    └─ Complete decision history                    │
│    └─ Agent reasoning documented                   │
│    └─ Processing timestamps                        │
│                                                     │
│ 6. Rate Limiting                                   │
│    └─ Implicitly via Claude API quotas            │
│    └─ Can add explicit limits later                │
└─────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

### Development
```
Local Machine
├─ Python venv
├─ FastAPI server (localhost:8000)
├─ In-memory cache
├─ .env file with API key
└─ SQLite database (optional)
```

### Production
```
Cloud Platform (AWS/GCP/Azure)
├─ Docker container
├─ Load balancer (traffic distribution)
├─ Multiple FastAPI instances
├─ PostgreSQL database (persistence)
├─ Redis cluster (distributed cache)
├─ CloudWatch/DataDog (monitoring)
├─ Secrets manager (API keys)
└─ VPC/Security groups (network isolation)
```

---

## Future Enhancements

### Phase 2: Persistence
- Add PostgreSQL for application storage
- Add Redis for distributed caching
- Implement audit logging

### Phase 3: Authentication
- OAuth 2.0 integration
- JWT token validation
- Role-based access control (RBAC)

### Phase 4: Advanced Features
- Machine learning refinement
- External bureau integration
- Webhook notifications
- Advanced analytics dashboard

### Phase 5: Scaling
- Microservices decomposition
- Agent-specific services
- Message queue (RabbitMQ/Kafka)
- Horizontal auto-scaling

---

## Key Design Decisions

1. **Claude API Integration**: Provides state-of-the-art reasoning without fine-tuning
2. **Agent Separation**: Each agent is independent, reusable, testable
3. **Parallel Execution**: Risk/Credit/Compliance agents run simultaneously for speed
4. **Explainability**: All decisions include agent-level reasoning
5. **FastAPI Choice**: Modern, async, auto-documentation, Pydantic integration
6. **Orchestrator Pattern**: Loose coupling, easy to add/modify agents

---

For implementation details, see code files:
- `main.py` - API endpoints
- `agents.py` - Agent implementations
- `orchestrator.py` - Multi-agent coordination
- `models.py` - Data structures
- `config.py` - Configuration
