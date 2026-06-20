# Testing Guide - Agentic AI Loan Approval System

## Quick Start Testing

### 1. Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your CLAUDE_API_KEY from console.anthropic.com
```

### 2. Run Example Demo

```bash
python example_notebook.py
```

This runs 3 test applications and displays:
- Individual agent analyses
- Final decision and score
- Risk flags and compliance issues
- Summary statistics

**Expected Output Pattern:**
```
🏦 Agentic AI Intelligent Loan Approval System
================================================================================
Initializing multi-agent orchestrator...

📋 Analyzing: Low-Risk Applicant
   Applicant: John Smith
   Loan Amount: $300,000
   Annual Income: $150,000
   Credit Score: 750

================================================================================
APPLICATION ID: <uuid>
================================================================================
FINAL DECISION: APPROVED
Decision Score: 85.0/100
Processing Time: 18.45s

REASONING:
...strong financial profile, excellent credit history, well-documented income...

AGENT ANALYSES:
...detailed analysis from each agent...

📊 ANALYSIS SUMMARY
================================================================================
Total Applications Processed: 3
  ✅ Approved: 1
  ❌ Rejected: 1
  ⏳ Manual Review: 1
```

## API Testing

### 3. Start FastAPI Server

```bash
python main.py
```

Server runs at: `http://localhost:8000`

### 4. Test Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-06-18T14:30:45.123456"
}
```

#### Submit Loan Application
```bash
curl -X POST http://localhost:8000/loans/analyze \
  -H "Content-Type: application/json" \
  -d @sample_application.json
```

Expected response:
```json
{
  "application_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "COMPLETED",
  "decision": "APPROVED",
  "decision_result": {
    "application_id": "550e8400-e29b-41d4-a716-446655440000",
    "final_decision": "APPROVED",
    "decision_score": 82.5,
    "reasoning": "...",
    "agent_analyses": [...],
    "risk_flags": [],
    "compliance_issues": [],
    "created_at": "2026-06-18T14:30:45.123456",
    "processing_time_seconds": 22.34
  },
  "created_at": "2026-06-18T14:30:45.123456",
  "updated_at": "2026-06-18T14:30:48.123456"
}
```

#### Get Application Status
```bash
curl http://localhost:8000/loans/{application_id}
```

Replace `{application_id}` with the ID from the previous response.

#### Get Detailed Analysis
```bash
curl http://localhost:8000/loans/{application_id}/details
```

Returns agent-by-agent breakdown:
```json
{
  "application_id": "...",
  "final_decision": "APPROVED",
  "decision_score": 82.5,
  "reasoning": "...",
  "risk_flags": [...],
  "compliance_issues": [],
  "agent_analyses": [
    {
      "agent_name": "Document Verification Agent",
      "score": 85.0,
      "recommendation": "Approve",
      "analysis": "..."
    },
    ...
  ],
  "processing_time_seconds": 22.34,
  "created_at": "2026-06-18T14:30:45.123456"
}
```

#### List All Applications
```bash
curl http://localhost:8000/loans
```

Returns summary of all analyzed applications:
```json
{
  "total_applications": 3,
  "applications": [
    {
      "application_id": "...",
      "decision": "APPROVED",
      "decision_score": 85.0,
      "processing_time_seconds": 22.34,
      "created_at": "2026-06-18T14:30:45.123456"
    },
    ...
  ]
}
```

### 5. Interactive API Documentation

Visit: `http://localhost:8000/docs`

This opens Swagger UI where you can:
- View all endpoints
- Try out API calls interactively
- See request/response schemas
- Test with the web interface

## Test Cases

### Test Case 1: Low-Risk Approval
**Expected**: APPROVED (score > 75)

```json
{
  "credit_score": 750,
  "annual_income": 150000,
  "loan_amount": 300000,
  "total_debt": 45000,
  "delinquencies_past_30_days": 0,
  "income_verification_confidence": 0.95,
  "employment_verification_confidence": 0.90
}
```

**Verifications**:
- ✅ Credit score well above 600 minimum
- ✅ Debt-to-income ratio low
- ✅ Strong document verification
- ✅ No delinquencies
- ✅ Decision score ≥ 75

### Test Case 2: Manual Review (Medium Risk)
**Expected**: MANUAL_REVIEW (40 < score < 75)

```json
{
  "credit_score": 680,
  "annual_income": 85000,
  "loan_amount": 250000,
  "total_debt": 38000,
  "delinquencies_past_30_days": 0,
  "delinquencies_past_90_days": 1,
  "inquiries_last_6_months": 3,
  "income_verification_confidence": 0.72,
  "employment_verification_confidence": 0.85
}
```

**Verifications**:
- ⚠️ Credit score acceptable but not strong
- ⚠️ Some recent delinquency history
- ⚠️ Multiple recent inquiries
- ⚠️ Income verification just meets threshold
- ⏳ Decision score 40-75 range
- ⏳ Recommendation for human review

### Test Case 3: High-Risk Rejection
**Expected**: REJECTED (score < 40)

```json
{
  "credit_score": 580,
  "annual_income": 55000,
  "loan_amount": 400000,
  "total_debt": 95000,
  "delinquencies_past_30_days": 2,
  "delinquencies_past_90_days": 3,
  "inquiries_last_6_months": 8,
  "bankruptcy_history": "Chapter 7 (2015)",
  "income_verification_confidence": 0.45,
  "employment_verification_confidence": 0.50
}
```

**Verifications**:
- ❌ Credit score below 600 minimum
- ❌ Multiple recent delinquencies
- ❌ Debt exceeds 50% of income
- ❌ Bankruptcy history
- ❌ Poor document verification
- ❌ Decision score < 40
- ❌ Clear REJECTED recommendation

## Test Scenarios

### Scenario A: Boundary Testing
Test edge cases at thresholds:

```python
# Credit score exactly at minimum
credit_score = 600

# Debt-to-income exactly at maximum
debt_to_income = 0.43

# Income verification at minimum threshold
income_verification_confidence = 0.80
```

**Expected**: System should handle boundaries gracefully and may escalate to MANUAL_REVIEW.

### Scenario B: Parallel Execution Validation
Monitor processing times:

- Run same application 3 times
- Record processing times
- Verify times are consistent (± 5 seconds)

**Expected**: Processing time should be deterministic.

### Scenario C: Consistency Testing
Submit identical applications twice:

1. First submission → Get decision
2. Second submission → Should get same decision (or retrieve from cache)

**Expected**: Identical inputs produce identical decisions.

### Scenario D: Stress Testing
Submit multiple applications rapidly:

```bash
for i in {1..10}; do
  curl -X POST http://localhost:8000/loans/analyze \
    -H "Content-Type: application/json" \
    -d @sample_application.json
done
```

**Expected**: All requests complete successfully with proper decisions.

## Validation Checklist

- [ ] Setup completed without errors
- [ ] Example notebook runs successfully
- [ ] All 3 test applications produce expected decisions
- [ ] FastAPI server starts without errors
- [ ] Health check endpoint returns healthy status
- [ ] Can submit loan application via API
- [ ] Application receives unique ID
- [ ] Can retrieve application status
- [ ] Can view detailed agent analysis
- [ ] Can list all applications
- [ ] Decision scores are in range 0-100
- [ ] Processing time is reasonable (< 30s)
- [ ] Risk flags appear for risky applications
- [ ] Compliance issues flagged when relevant
- [ ] Agent recommendations are reasonable
- [ ] Final decision aligns with agent recommendations
- [ ] Low-risk application approved
- [ ] High-risk application rejected
- [ ] Medium-risk application marked for manual review
- [ ] API documentation accessible at /docs
- [ ] Error responses are meaningful

## Debugging Tips

### Issue: CLAUDE_API_KEY not found
**Solution**: 
```bash
cp .env.example .env
# Edit .env and add your actual API key
```

### Issue: ImportError for anthropic
**Solution**:
```bash
pip install --upgrade anthropic
```

### Issue: Processing times very long (> 60s)
**Solution**: Check API rate limits or network latency. May indicate API quota usage.

### Issue: JSON parsing errors in agents
**Solution**: Check that agent prompts are well-formed and agent responses are valid JSON.

### Issue: Can't connect to localhost:8000
**Solution**: 
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill the process if needed and restart
```

## Performance Benchmarks

Expected performance on standard hardware:

| Metric | Value |
|--------|-------|
| Avg processing time | 15-30 seconds |
| Min processing time | 10 seconds |
| Max processing time | 45 seconds |
| Throughput | ~120 apps/hour |
| Memory per request | ~50-100 MB |
| API response latency | < 100ms |

## Success Criteria

✅ **System is ready for production when:**
1. All test cases pass
2. Decision scores correlate with risk profiles
3. Processing time is consistent and reasonable
4. No errors in logs
5. API documentation is accurate
6. Manual review recommendations are appropriate
7. Audit trail is complete and detailed

---

For additional help, see README.md and CLAUDE.md
