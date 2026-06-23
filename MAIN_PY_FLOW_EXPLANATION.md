# Main.py - FastAPI Application Flow Explanation

## Overview

`main.py` is the entry point for the FastAPI backend server. It sets up the REST API endpoints that clients (web UI, external systems) use to submit and retrieve loan applications.

---

## Complete Program Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      MAIN.PY PROGRAM EXECUTION                          │
└─────────────────────────────────────────────────────────────────────────┘

STEP 1: IMPORTS & INITIALIZATION (Lines 1-9)
═════════════════════════════════════════════════════════════════════════

from fastapi import FastAPI, HTTPException
    ↓
    Import FastAPI framework for building REST APIs
    Import HTTPException for error handling

from fastapi.middleware.cors import CORSMiddleware
    ↓
    Import CORS middleware (allows cross-origin requests)

from models import LoanApplication, ApplicationResponse, LoanDecisionResult
    ↓
    Import Pydantic data models for validation

from config import ApplicationStatus
    ↓
    Import status enums (ANALYZING, COMPLETED, ERROR)

from orchestrator import LoanOrchestrator
    ↓
    Import the orchestrator that runs 5 AI agents

from datetime import datetime
import uuid
    ↓
    Import utilities for timestamps and unique IDs


STEP 2: CREATE FASTAPI APP (Lines 11-15)
═════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="Agentic AI Loan Approval System",
    description="Multi-agent AI system...",
    version="1.0.0"
)
    ↓
    ✅ Creates FastAPI application instance
    ✅ Sets metadata for API documentation
    ✅ This app will be served on http://localhost:8000


STEP 3: CONFIGURE CORS MIDDLEWARE (Lines 18-24)
═════════════════════════════════════════════════════════════════════════

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           ← Accept requests from any domain
    allow_credentials=True,        ← Allow cookies/credentials
    allow_methods=["*"],           ← Allow all HTTP methods
    allow_headers=["*"]            ← Allow all headers
)
    ↓
    ✅ Enables cross-origin requests
    ✅ Allows web UI (http://localhost:8501) to call API
    ✅ Production note: Change ["*"] to specific domains


STEP 4: INITIALIZE GLOBAL OBJECTS (Lines 26-27)
═════════════════════════════════════════════════════════════════════════

orchestrator = LoanOrchestrator()
    ↓
    ✅ Creates single orchestrator instance
    ✅ Loaded once when app starts
    ✅ Reused for all requests

application_status = {}
    ↓
    ✅ In-memory dictionary to track application statuses
    ✅ Key: application_id
    ✅ Value: {status, created_at, updated_at, decision}
    ✅ Note: Lost on app restart (would use database in production)


STEP 5-9: DEFINE API ENDPOINTS (Lines 29-177)
═════════════════════════════════════════════════════════════════════════

```

---

## Detailed Endpoint Flows

### ENDPOINT 1: Health Check

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    GET /health (Lines 29-35)                            │
└─────────────────────────────────────────────────────────────────────────┘

REQUEST:
  GET /health

FLOW:
  1. Client sends GET request to /health
  2. FastAPI routes to health_check() function
  3. Function returns JSON:
     {
       "status": "healthy",
       "timestamp": "2026-06-23T10:30:15.123456"
     }

RESPONSE:
  200 OK
  {
    "status": "healthy",
    "timestamp": "2026-06-23T10:30:15.123456"
  }

PURPOSE:
  ✅ Verify API is running
  ✅ Container orchestration (Kubernetes) uses this for liveness checks
  ✅ Monitoring systems use this for health monitoring
```

---

### ENDPOINT 2: Analyze Loan Application (Main Endpoint)

```
┌─────────────────────────────────────────────────────────────────────────┐
│              POST /loans/analyze (Lines 37-85)                          │
│                   THE MOST IMPORTANT ENDPOINT                           │
└─────────────────────────────────────────────────────────────────────────┘

REQUEST:
  POST /loans/analyze
  Content-Type: application/json
  
  {
    "id": null,  (optional, will be auto-generated if null)
    "applicant_info": {...},
    "loan_details": {...},
    "credit_profile": {...},
    "document_verification": {...}
  }

DETAILED FLOW:
═════════════════════════════════════════════════════════════════════════

PHASE 1: RECEIVE REQUEST (Lines 38-45)
───────────────────────────────────────

async def analyze_loan(loan_app: LoanApplication) -> ApplicationResponse:

Action 1: FastAPI automatically validates JSON input
    ✅ Checks all required fields present
    ✅ Validates data types
    ✅ Raises 422 Unprocessable Entity if invalid

Action 2: FastAPI creates LoanApplication object from JSON
    ✅ Deserializes JSON to Python object
    ✅ All fields type-checked by Pydantic


PHASE 2: GENERATE APPLICATION ID (Lines 46-47)
───────────────────────────────────────────────

application_id = loan_app.id or str(uuid.uuid4())
loan_app.id = application_id

Action: If no ID provided, generate unique ID
    ✅ uuid.uuid4() creates random unique identifier
    ✅ Example: "a03adccc-7bcf-4e0a-8ff9-fd7ac2e62989"
    ✅ Set this ID on the loan application object


PHASE 3: SET INITIAL STATUS (Lines 50-55)
──────────────────────────────────────────

now = datetime.utcnow().isoformat()
application_status[application_id] = {
    "status": ApplicationStatus.ANALYZING,
    "created_at": now,
    "updated_at": now
}

Action: Track application state in memory dictionary
    ✅ Status: "ANALYZING" (processing started)
    ✅ Timestamps for tracking
    ✅ Dictionary key: application_id


PHASE 4: RUN MULTI-AGENT ANALYSIS (Line 58) ⭐ CRITICAL
────────────────────────────────────────────

decision_result = orchestrator.analyze_application(loan_app)

Action: Pass to orchestrator which:
    1. Spawns 5 agents in parallel
    2. Each agent analyzes aspect of application
    3. All agents run simultaneously
    4. Wait for all to complete (~7-15 seconds)
    5. Return LoanDecisionResult with:
       ├─ final_decision (APPROVED/REJECTED/MANUAL_REVIEW)
       ├─ decision_score (0-100)
       ├─ reasoning (why this decision)
       ├─ agent_analyses (each agent's score)
       ├─ risk_flags (identified concerns)
       └─ compliance_issues (compliance notes)

Flow into orchestrator.py:
    ┌─────────────────────────────────────┐
    │ LoanOrchestrator.analyze_application │
    │ (See orchestrator.py for details)    │
    └──────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┬─────────┬──────────┐
        │          │          │         │          │
        ▼          ▼          ▼         ▼          ▼
      Agent1    Agent2      Agent3    Agent4     Agent5
      (Doc)     (Credit)    (Risk)   (Compl)    (Decision)
       
       All run in PARALLEL
       Wait for all to finish
       Return combined result


PHASE 5: UPDATE SUCCESS STATUS (Lines 61-66)
─────────────────────────────────────────────

application_status[application_id] = {
    "status": ApplicationStatus.COMPLETED,
    "created_at": now,
    "updated_at": datetime.utcnow().isoformat(),
    "decision": decision_result.final_decision
}

Action: Mark application as done
    ✅ Status: "COMPLETED"
    ✅ Updated timestamp
    ✅ Store final decision


PHASE 6: BUILD RESPONSE (Lines 68-75)
──────────────────────────────────────

return ApplicationResponse(
    application_id=application_id,
    status=ApplicationStatus.COMPLETED,
    decision=decision_result.final_decision,
    decision_result=decision_result,
    created_at=now,
    updated_at=datetime.utcnow().isoformat()
)

Action: Create response object
    ✅ ApplicationResponse is Pydantic model
    ✅ FastAPI serializes to JSON
    ✅ Return to client with 200 OK


PHASE 7: ERROR HANDLING (Lines 77-85)
──────────────────────────────────────

except Exception as e:
    error_msg = str(e)
    application_status[application_id] = {
        "status": ApplicationStatus.ERROR,
        "error": error_msg,
        "created_at": now,
        "updated_at": datetime.utcnow().isoformat()
    }
    raise HTTPException(status_code=500, detail=error_msg)

Action: Catch any errors and respond gracefully
    ✅ Mark status as ERROR
    ✅ Log error message
    ✅ Return HTTP 500 error to client
    ✅ Error includes error message


COMPLETE RESPONSE EXAMPLE:
═════════════════════════════════════════════════════════════════════════

HTTP/1.1 200 OK
Content-Type: application/json

{
  "application_id": "a03adccc-7bcf-4e0a-8ff9-fd7ac2e62989",
  "status": "COMPLETED",
  "decision": "MANUAL_REVIEW",
  "decision_result": {
    "application_id": "a03adccc-...",
    "final_decision": "MANUAL_REVIEW",
    "decision_score": 56.0,
    "reasoning": "The application presents mixed signals...",
    "agent_analyses": [
      {
        "agent_name": "Document Verification Agent",
        "score": 84.0,
        "recommendation": "Approve",
        "analysis": "..."
      },
      ...
    ],
    "risk_flags": [...],
    "compliance_issues": [...],
    "processing_time_seconds": 15.4,
    "created_at": "2026-06-23T10:30:15Z"
  },
  "created_at": "2026-06-23T10:30:15Z",
  "updated_at": "2026-06-23T10:30:30Z"
}
```

---

### ENDPOINT 3: Get Application Status

```
┌─────────────────────────────────────────────────────────────────────────┐
│            GET /loans/{application_id} (Lines 87-114)                   │
└─────────────────────────────────────────────────────────────────────────┘

REQUEST:
  GET /loans/a03adccc-7bcf-4e0a-8ff9-fd7ac2e62989

FLOW:
═════════════════════════════════════════════════════════════════════════

1. RECEIVE REQUEST (Line 88)
   ├─ Extract application_id from URL path
   └─ FastAPI automatically routes based on path parameter

2. FETCH FROM ORCHESTRATOR (Line 96)
   decision_result = orchestrator.get_result(application_id)
   ├─ Queries storage for this application's result
   └─ Returns LoanDecisionResult or None

3. FETCH STATUS FROM MEMORY (Line 97)
   status_info = application_status.get(application_id)
   ├─ Looks up in-memory dictionary
   └─ Returns status object or None

4. CHECK IF EXISTS (Lines 99-100)
   if not decision_result or not status_info:
       raise HTTPException(status_code=404, ...)
   ├─ If either is missing, application not found
   └─ Return 404 error

5. BUILD RESPONSE (Lines 102-109)
   return ApplicationResponse(...)
   ├─ Combine decision result and status info
   └─ Return complete information

6. ERROR HANDLING (Lines 111-114)
   ├─ Catch HTTPException and re-raise
   └─ Catch other errors and return 500


RESPONSE:
  200 OK
  {
    "application_id": "a03adccc-...",
    "status": "COMPLETED",
    "decision": "MANUAL_REVIEW",
    "decision_result": {...},
    "created_at": "2026-06-23T10:30:15Z",
    "updated_at": "2026-06-23T10:30:30Z"
  }

OR 404 if not found:
  {
    "detail": "Application not found"
  }
```

---

### ENDPOINT 4: List All Applications

```
┌─────────────────────────────────────────────────────────────────────────┐
│               GET /loans (Lines 116-139)                                │
└─────────────────────────────────────────────────────────────────────────┘

REQUEST:
  GET /loans

FLOW:
═════════════════════════════════════════════════════════════════════════

1. FETCH ALL RESULTS (Line 122)
   results = orchestrator.get_all_results()
   └─ Returns list of all LoanDecisionResult objects

2. BUILD SUMMARY (Lines 123-132)
   decisions_summary = [
       {
           "application_id": r.application_id,
           "decision": r.final_decision,
           "decision_score": r.decision_score,
           "processing_time_seconds": r.processing_time_seconds,
           "created_at": r.created_at
       }
       for r in results
   ]
   ├─ Extract key info from each result
   └─ Create list of summaries (not full details)

3. RETURN RESPONSE (Lines 133-136)
   return {
       "total_applications": len(decisions_summary),
       "applications": decisions_summary
   }
   └─ Return count and summary list

4. ERROR HANDLING (Lines 138-139)
   ├─ Catch errors
   └─ Return 500 error

RESPONSE:
  200 OK
  {
    "total_applications": 3,
    "applications": [
      {
        "application_id": "a03adccc-...",
        "decision": "MANUAL_REVIEW",
        "decision_score": 56.0,
        "processing_time_seconds": 15.4,
        "created_at": "2026-06-23T10:30:15Z"
      },
      {
        "application_id": "b14bddd-...",
        "decision": "APPROVED",
        "decision_score": 85.0,
        "processing_time_seconds": 12.1,
        "created_at": "2026-06-23T10:35:20Z"
      },
      ...
    ]
  }
```

---

### ENDPOINT 5: Get Detailed Analysis

```
┌─────────────────────────────────────────────────────────────────────────┐
│      GET /loans/{application_id}/details (Lines 141-177)                │
└─────────────────────────────────────────────────────────────────────────┘

REQUEST:
  GET /loans/a03adccc-7bcf-4e0a-8ff9-fd7ac2e62989/details

FLOW:
═════════════════════════════════════════════════════════════════════════

1. FETCH RESULT (Line 147)
   decision_result = orchestrator.get_result(application_id)

2. VALIDATE EXISTS (Lines 149-150)
   if not decision_result:
       raise HTTPException(status_code=404, ...)

3. EXTRACT AGENT DETAILS (Lines 152-160)
   agent_details = [
       {
           "agent_name": a.agent_name,
           "score": a.score,
           "recommendation": a.recommendation,
           "analysis": a.analysis
       }
       for a in decision_result.agent_analyses
   ]
   └─ Build detailed array of each agent's analysis

4. BUILD RESPONSE (Lines 162-172)
   return {
       "application_id": application_id,
       "final_decision": decision_result.final_decision,
       "decision_score": decision_result.decision_score,
       "reasoning": decision_result.reasoning,
       "risk_flags": decision_result.risk_flags,
       "compliance_issues": decision_result.compliance_issues,
       "agent_analyses": agent_details,  ← Detailed info
       "processing_time_seconds": decision_result.processing_time_seconds,
       "created_at": decision_result.created_at
   }

RESPONSE:
  200 OK
  {
    "application_id": "a03adccc-...",
    "final_decision": "MANUAL_REVIEW",
    "decision_score": 56.0,
    "reasoning": "The application presents mixed signals...",
    "risk_flags": [
      "Recent delinquencies (90 days)",
      "Credit score at minimum threshold",
      ...
    ],
    "compliance_issues": [
      "Incomplete KYC documentation",
      ...
    ],
    "agent_analyses": [
      {
        "agent_name": "Document Verification Agent",
        "score": 84.0,
        "recommendation": "Approve",
        "analysis": "..."
      },
      {
        "agent_name": "Credit Analysis Agent",
        "score": 52.0,
        "recommendation": "Review",
        "analysis": "..."
      },
      ...
    ],
    "processing_time_seconds": 15.4,
    "created_at": "2026-06-23T10:30:15Z"
  }
```

---

## Server Startup

```
┌─────────────────────────────────────────────────────────────────────────┐
│              SERVER STARTUP (Lines 179-181)                             │
└─────────────────────────────────────────────────────────────────────────┘

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

WHEN YOU RUN: python main.py

1. Check if this file is main script
   └─ __name__ == "__main__" is True

2. Import uvicorn
   └─ ASGI server for FastAPI

3. Start server
   uvicorn.run(
       app,                    ← FastAPI app to serve
       host="0.0.0.0",        ← Listen on all interfaces
       port=8000              ← Port 8000
   )

4. Server becomes available
   ✅ http://localhost:8000
   ✅ http://<your-ip>:8000
   ✅ API Docs: http://localhost:8000/docs
   ✅ ReDoc: http://localhost:8000/redoc

5. Server waits for requests
   └─ Handles requests as they come in
```

---

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         COMPLETE DATA FLOW                               │
└──────────────────────────────────────────────────────────────────────────┘

CLIENT (Web UI or API Call)
     │
     ├─ HTTP POST /loans/analyze
     │  JSON body: {applicant_info, loan_details, ...}
     │
     ▼
FastAPI Request Validation
     │
     ├─ Validate JSON structure
     ├─ Type check all fields
     └─ Deserialize to LoanApplication
     │
     ▼
main.py - analyze_loan() function
     │
     ├─ Generate application_id
     ├─ Set status to "ANALYZING"
     │
     ▼
Call orchestrator.analyze_application()
     │
     ├─ Spawn 5 AI agents in parallel
     │  ├─ Document Verification Agent
     │  ├─ Credit Analysis Agent
     │  ├─ Risk Assessment Agent
     │  ├─ Compliance Agent
     │  └─ Decision Agent
     │
     ├─ Each agent calls Claude API
     ├─ Wait for all to complete (~7-15 seconds)
     │
     ▼
Return LoanDecisionResult
     │
     ├─ final_decision (APPROVED/REJECTED/MANUAL_REVIEW)
     ├─ decision_score (0-100)
     ├─ reasoning
     ├─ agent_analyses (list of each agent's result)
     ├─ risk_flags
     └─ compliance_issues
     │
     ▼
Update application_status to "COMPLETED"
     │
     ▼
Build ApplicationResponse
     │
     ├─ application_id
     ├─ status
     ├─ decision
     ├─ decision_result (full details)
     ├─ created_at
     └─ updated_at
     │
     ▼
FastAPI Response Serialization
     │
     ├─ Convert to JSON
     ├─ Set HTTP 200 OK
     └─ Add headers
     │
     ▼
Send HTTP Response to Client
     │
     └─ {full response JSON}


If Error Occurs:
     │
     ├─ Catch exception
     ├─ Set status to "ERROR"
     ├─ Log error message
     │
     ▼
Return HTTP 500 Error
     │
     └─ {"detail": error message}
```

---

## Key Concepts

### 1. Async Functions
```python
async def analyze_loan(loan_app: LoanApplication):
    
✅ "async" allows non-blocking I/O
✅ Server can handle multiple requests simultaneously
✅ Doesn't block on long operations (API calls)
✅ Scalable to thousands of concurrent requests
```

### 2. Pydantic Models
```python
loan_app: LoanApplication

✅ Automatic JSON deserialization
✅ Type validation
✅ Auto-generates API documentation
✅ Raises 422 on invalid input
```

### 3. HTTP Exceptions
```python
raise HTTPException(status_code=404, detail="...")

✅ Convert Python exceptions to HTTP responses
✅ Returns proper status codes
✅ Sends error messages to client
```

### 4. In-Memory Storage
```python
application_status = {}

⚠️ Data lost on app restart
✅ Good for demo/testing
❌ Not suitable for production
→ Would use database in production
```

### 5. CORS Middleware
```python
app.add_middleware(CORSMiddleware, allow_origins=["*"])

✅ Allows web UI to call API from different origin
✅ Production: restrict to specific origins
```

---

## Execution Summary

| Step | Action | Time | Status |
|------|--------|------|--------|
| 1 | Request arrives at /loans/analyze | 0s | Received |
| 2 | Validate input JSON | 0.1s | Processing |
| 3 | Generate application_id | 0.1s | Processing |
| 4 | Set status to ANALYZING | 0.2s | Processing |
| 5 | Call orchestrator.analyze_application() | 0.2s | Processing |
| 6 | 5 agents run in parallel | 7-15s | Analyzing |
| 7 | Decision Engine synthesizes result | 8-16s | Analyzing |
| 8 | Update status to COMPLETED | 16s | Completed |
| 9 | Build response object | 16s | Completed |
| 10 | Serialize to JSON & send to client | 16s | Response sent |

**Total time: 15-30 seconds**

---

## Production Considerations

### Current Issues (Demo/Dev)
- ❌ In-memory status tracking (lost on restart)
- ❌ No database persistence
- ❌ CORS allows all origins
- ❌ No authentication/authorization
- ❌ No request rate limiting
- ❌ No logging/monitoring

### Production Improvements Needed
- ✅ Database for persistent storage
- ✅ Restrict CORS to known origins
- ✅ Add API authentication (API keys or OAuth)
- ✅ Implement rate limiting
- ✅ Add comprehensive logging
- ✅ Add monitoring/alerting
- ✅ Add request validation logging
- ✅ Add error tracking (Sentry)
- ✅ Use connection pooling for DB
- ✅ Add request timeout handling

---

## Files This Depends On

```
main.py
├─ models.py
│  ├─ LoanApplication
│  ├─ ApplicationResponse
│  └─ LoanDecisionResult
│
├─ config.py
│  └─ ApplicationStatus (enum)
│
└─ orchestrator.py
   ├─ LoanOrchestrator class
   ├─ analyze_application()
   ├─ get_result()
   └─ get_all_results()
       │
       └─ agents.py
          ├─ Document Verification Agent
          ├─ Credit Analysis Agent
          ├─ Risk Assessment Agent
          ├─ Compliance Agent
          └─ Decision Agent
```

---

**End of Main.py Flow Explanation**

This document explains every line of code and the complete execution flow of the FastAPI application.
