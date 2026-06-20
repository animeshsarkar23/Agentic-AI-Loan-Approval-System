from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import (
    LoanApplication, ApplicationResponse, LoanDecisionResult
)
from config import ApplicationStatus
from orchestrator import LoanOrchestrator
from datetime import datetime
import uuid

app = FastAPI(
    title="Agentic AI Loan Approval System",
    description="Multi-agent AI system for intelligent loan approval decisions",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = LoanOrchestrator()
application_status = {}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/loans/analyze")
async def analyze_loan(loan_app: LoanApplication) -> ApplicationResponse:
    """
    Submit a loan application for multi-agent analysis.

    Returns:
        ApplicationResponse with application_id and initial status
    """
    try:
        application_id = loan_app.id or str(uuid.uuid4())
        loan_app.id = application_id

        # Set initial status
        now = datetime.utcnow().isoformat()
        application_status[application_id] = {
            "status": ApplicationStatus.ANALYZING,
            "created_at": now,
            "updated_at": now
        }

        # Run orchestrated analysis
        decision_result = orchestrator.analyze_application(loan_app)

        # Update status
        application_status[application_id] = {
            "status": ApplicationStatus.COMPLETED,
            "created_at": now,
            "updated_at": datetime.utcnow().isoformat(),
            "decision": decision_result.final_decision
        }

        return ApplicationResponse(
            application_id=application_id,
            status=ApplicationStatus.COMPLETED,
            decision=decision_result.final_decision,
            decision_result=decision_result,
            created_at=now,
            updated_at=datetime.utcnow().isoformat()
        )

    except Exception as e:
        error_msg = str(e)
        application_status[application_id] = {
            "status": ApplicationStatus.ERROR,
            "error": error_msg,
            "created_at": now,
            "updated_at": datetime.utcnow().isoformat()
        }
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/loans/{application_id}")
async def get_loan_status(application_id: str) -> ApplicationResponse:
    """
    Get the status and decision for a loan application.

    Args:
        application_id: The unique identifier of the loan application
    """
    try:
        decision_result = orchestrator.get_result(application_id)
        status_info = application_status.get(application_id)

        if not decision_result or not status_info:
            raise HTTPException(status_code=404, detail="Application not found")

        return ApplicationResponse(
            application_id=application_id,
            status=status_info["status"],
            decision=decision_result.final_decision,
            decision_result=decision_result,
            created_at=status_info["created_at"],
            updated_at=status_info["updated_at"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/loans")
async def list_applications() -> dict:
    """
    List all loan applications and their decisions.
    """
    try:
        results = orchestrator.get_all_results()
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
        return {
            "total_applications": len(decisions_summary),
            "applications": decisions_summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/loans/{application_id}/details")
async def get_detailed_analysis(application_id: str) -> dict:
    """
    Get detailed agent-by-agent analysis for a loan application.
    """
    try:
        decision_result = orchestrator.get_result(application_id)

        if not decision_result:
            raise HTTPException(status_code=404, detail="Application not found")

        agent_details = [
            {
                "agent_name": a.agent_name,
                "score": a.score,
                "recommendation": a.recommendation,
                "analysis": a.analysis
            }
            for a in decision_result.agent_analyses
        ]

        return {
            "application_id": application_id,
            "final_decision": decision_result.final_decision,
            "decision_score": decision_result.decision_score,
            "reasoning": decision_result.reasoning,
            "risk_flags": decision_result.risk_flags,
            "compliance_issues": decision_result.compliance_issues,
            "agent_analyses": agent_details,
            "processing_time_seconds": decision_result.processing_time_seconds,
            "created_at": decision_result.created_at
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
