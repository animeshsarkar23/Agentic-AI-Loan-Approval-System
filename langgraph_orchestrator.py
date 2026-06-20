"""
LangGraph-based Multi-Agent Orchestration Engine
Coordinates agent workflows using LangGraph for complex state management
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import json
from langgraph.graph import StateGraph, START, END
from langgraph.graph.graph import CompiledGraph
from pydantic import BaseModel
from models import LoanApplication, LoanDecisionResult, AgentAnalysis
from config import LoanDecision
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-3-5-sonnet-20241022"

class WorkflowState(BaseModel):
    """State object for LangGraph workflow"""
    application_id: str
    loan_application: LoanApplication
    document_verification_result: Optional[AgentAnalysis] = None
    credit_analysis_result: Optional[AgentAnalysis] = None
    risk_assessment_result: Optional[AgentAnalysis] = None
    compliance_result: Optional[AgentAnalysis] = None
    all_analyses: List[AgentAnalysis] = []
    final_decision: Optional[LoanDecisionResult] = None
    error: Optional[str] = None
    start_time: float = 0.0

class LangGraphOrchestrator:
    """
    LangGraph-based orchestrator for multi-agent loan approval workflow.

    Provides:
    - Complex state management
    - Conditional branching
    - Retry logic
    - Error recovery
    - Parallel and sequential execution
    """

    def __init__(self):
        self.graph: Optional[CompiledGraph] = None
        self.build_workflow()

    def build_workflow(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(dict)

        # Add nodes
        workflow.add_node("document_verification", self._document_verification)
        workflow.add_node("credit_analysis", self._credit_analysis)
        workflow.add_node("risk_assessment", self._risk_assessment)
        workflow.add_node("compliance_check", self._compliance_check)
        workflow.add_node("decision_synthesis", self._decision_synthesis)
        workflow.add_node("error_handler", self._error_handler)

        # Add edges
        workflow.add_edge(START, "document_verification")
        workflow.add_conditional_edges(
            "document_verification",
            self._should_continue,
            {
                True: "credit_analysis",
                False: "error_handler"
            }
        )

        # Parallel execution: credit, risk, compliance
        workflow.add_edge("credit_analysis", "risk_assessment")
        workflow.add_edge("risk_assessment", "compliance_check")
        workflow.add_edge("compliance_check", "decision_synthesis")

        workflow.add_edge("decision_synthesis", END)
        workflow.add_edge("error_handler", END)

        self.graph = workflow.compile()

    def _should_continue(self, state: Dict[str, Any]) -> bool:
        """Determine if workflow should continue"""
        return state.get("error") is None

    def _document_verification(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Document verification node"""
        try:
            loan_app = state["loan_application"]
            doc_verification = loan_app.document_verification

            prompt = f"""
            You are a Document Verification Agent for a loan approval system.

            Analyze the following applicant documents and verification status:

            Applicant: {loan_app.applicant_info.first_name} {loan_app.applicant_info.last_name}
            Income: ${loan_app.applicant_info.annual_income:,.2f}
            Employment: {loan_app.applicant_info.employment_status}

            Document Status:
            - Income Verification: {doc_verification.income_verification_status} ({doc_verification.income_verification_confidence*100:.0f}%)
            - Employment Verification: {doc_verification.employment_verification_status} ({doc_verification.employment_verification_confidence*100:.0f}%)
            - Documents: {', '.join(doc_verification.documents_provided)}

            Provide analysis in JSON format with: analysis, score (0-100), recommendation.
            """

            message = client.messages.create(
                model=MODEL,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            response_data = json.loads(message.content[0].text)

            result = AgentAnalysis(
                agent_name="Document Verification Agent",
                analysis=response_data["analysis"],
                score=response_data["score"],
                recommendation=response_data["recommendation"]
            )

            state["document_verification_result"] = result
            state["all_analyses"].append(result)

        except Exception as e:
            state["error"] = f"Document verification failed: {str(e)}"

        return state

    def _credit_analysis(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Credit analysis node"""
        try:
            loan_app = state["loan_application"]
            credit = loan_app.credit_profile

            prompt = f"""
            You are a Credit Analysis Agent.

            Analyze credit profile:
            - Score: {credit.credit_score}
            - Accounts: {credit.accounts_open}
            - Delinquencies (30d): {credit.delinquencies_past_30_days}
            - Delinquencies (90d): {credit.delinquencies_past_90_days}
            - Total Debt: ${credit.total_debt:,.2f}
            - Recent Inquiries: {credit.inquiries_last_6_months}
            - Bankruptcy: {credit.bankruptcy_history or 'None'}

            Provide analysis in JSON format.
            """

            message = client.messages.create(
                model=MODEL,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            response_data = json.loads(message.content[0].text)

            result = AgentAnalysis(
                agent_name="Credit Analysis Agent",
                analysis=response_data["analysis"],
                score=response_data["score"],
                recommendation=response_data["recommendation"]
            )

            state["credit_analysis_result"] = result
            state["all_analyses"].append(result)

        except Exception as e:
            state["error"] = f"Credit analysis failed: {str(e)}"

        return state

    def _risk_assessment(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Risk assessment node"""
        try:
            loan_app = state["loan_application"]
            applicant = loan_app.applicant_info
            loan = loan_app.loan_details
            credit = loan_app.credit_profile

            debt_to_income = (credit.total_debt / applicant.annual_income) if applicant.annual_income > 0 else 0

            prompt = f"""
            You are a Risk Assessment Agent.

            Risk Indicators:
            - Loan Amount: ${loan.loan_amount:,.2f}
            - Annual Income: ${applicant.annual_income:,.2f}
            - Debt-to-Income: {debt_to_income*100:.1f}%
            - Employment: {applicant.employment_status} ({applicant.years_employed} years)
            - Loan Purpose: {loan.loan_purpose}

            Provide analysis in JSON format.
            """

            message = client.messages.create(
                model=MODEL,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            response_data = json.loads(message.content[0].text)

            result = AgentAnalysis(
                agent_name="Risk Assessment Agent",
                analysis=response_data["analysis"],
                score=response_data["score"],
                recommendation=response_data["recommendation"]
            )

            state["risk_assessment_result"] = result
            state["all_analyses"].append(result)

        except Exception as e:
            state["error"] = f"Risk assessment failed: {str(e)}"

        return state

    def _compliance_check(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Compliance check node"""
        try:
            loan_app = state["loan_application"]
            applicant = loan_app.applicant_info
            loan = loan_app.loan_details

            prompt = f"""
            You are a Compliance Agent.

            Check compliance for:
            - Applicant: {applicant.first_name} {applicant.last_name}
            - Loan Amount: ${loan.loan_amount:,.2f}
            - Purpose: {loan.loan_purpose}
            - Income: ${applicant.annual_income:,.2f}

            Check for regulatory compliance, AML, KYC requirements.
            Provide analysis in JSON format.
            """

            message = client.messages.create(
                model=MODEL,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            response_data = json.loads(message.content[0].text)

            result = AgentAnalysis(
                agent_name="Compliance Agent",
                analysis=response_data["analysis"],
                score=response_data["score"],
                recommendation=response_data["recommendation"]
            )

            state["compliance_result"] = result
            state["all_analyses"].append(result)

        except Exception as e:
            state["error"] = f"Compliance check failed: {str(e)}"

        return state

    def _decision_synthesis(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Decision synthesis node"""
        try:
            analyses_text = "\n".join([
                f"- {a.agent_name}: Score={a.score}, Rec={a.recommendation}"
                for a in state["all_analyses"]
            ])

            prompt = f"""
            You are the Decision Agent. Synthesize findings:

            {analyses_text}

            Decide: APPROVED (score >= 75), REJECTED (score < 40), or MANUAL_REVIEW.
            Provide decision_score (0-100), reasoning, risk_flags, compliance_issues.
            Response in JSON format.
            """

            message = client.messages.create(
                model=MODEL,
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )

            response_data = json.loads(message.content[0].text)

            import time
            processing_time = time.time() - state.get("start_time", 0)

            decision_result = LoanDecisionResult(
                application_id=state["application_id"],
                final_decision=LoanDecision[response_data["decision"]],
                decision_score=response_data["decision_score"],
                reasoning=response_data["reasoning"],
                agent_analyses=state["all_analyses"],
                risk_flags=response_data.get("risk_flags", []),
                compliance_issues=response_data.get("compliance_issues", []),
                created_at=datetime.utcnow().isoformat(),
                processing_time_seconds=processing_time
            )

            state["final_decision"] = decision_result

        except Exception as e:
            state["error"] = f"Decision synthesis failed: {str(e)}"

        return state

    def _error_handler(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Error handler node"""
        error_msg = state.get("error", "Unknown error occurred")
        print(f"Workflow error: {error_msg}")
        return state

    def execute(self, application_id: str, loan_app: LoanApplication) -> LoanDecisionResult:
        """Execute the workflow"""
        import time

        initial_state = {
            "application_id": application_id,
            "loan_application": loan_app,
            "all_analyses": [],
            "start_time": time.time()
        }

        result = self.graph.invoke(initial_state)

        if result.get("error"):
            raise Exception(result["error"])

        return result["final_decision"]
