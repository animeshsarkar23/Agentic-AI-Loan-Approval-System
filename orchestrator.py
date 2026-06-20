import uuid
import time
from datetime import datetime
from models import LoanApplication, LoanDecisionResult, AgentAnalysis
from config import LoanDecision
from agents import (
    document_verification_agent,
    credit_analysis_agent,
    risk_assessment_agent,
    compliance_agent,
    decision_agent
)

class LoanOrchestrator:
    """Orchestrates multi-agent analysis for loan applications."""

    def __init__(self):
        self.results_cache = {}

    def analyze_application(self, loan_app: LoanApplication) -> LoanDecisionResult:
        """
        Orchestrates all agents to analyze a loan application.

        Flow:
        1. Document Verification Agent
        2. Credit Analysis Agent (parallel)
        3. Risk Assessment Agent (parallel)
        4. Compliance Agent (parallel)
        5. Decision Agent (synthesis)
        """

        start_time = time.time()
        application_id = loan_app.id or str(uuid.uuid4())

        try:
            # Phase 1: Document Verification (prerequisite for other agents)
            doc_analysis = document_verification_agent(loan_app)

            # Phase 2: Parallel agent analysis
            credit_analysis = credit_analysis_agent(loan_app)
            risk_analysis = risk_assessment_agent(loan_app)
            compliance_analysis = compliance_agent(loan_app)

            # Collect all analyses
            agent_analyses = [
                doc_analysis,
                credit_analysis,
                risk_analysis,
                compliance_analysis
            ]

            # Phase 3: Decision synthesis
            decision_result_data = decision_agent(loan_app, agent_analyses)

            # Create final decision result
            decision_result = LoanDecisionResult(
                application_id=application_id,
                final_decision=LoanDecision[decision_result_data["decision"]],
                decision_score=decision_result_data["decision_score"],
                reasoning=decision_result_data["reasoning"],
                agent_analyses=agent_analyses,
                risk_flags=decision_result_data.get("risk_flags", []),
                compliance_issues=decision_result_data.get("compliance_issues", []),
                created_at=datetime.utcnow().isoformat(),
                processing_time_seconds=time.time() - start_time
            )

            # Cache the result
            self.results_cache[application_id] = decision_result

            return decision_result

        except Exception as e:
            raise Exception(f"Error analyzing loan application: {str(e)}")

    def get_result(self, application_id: str) -> LoanDecisionResult:
        """Retrieve cached analysis result."""
        return self.results_cache.get(application_id)

    def get_all_results(self) -> list[LoanDecisionResult]:
        """Retrieve all cached analysis results."""
        return list(self.results_cache.values())
