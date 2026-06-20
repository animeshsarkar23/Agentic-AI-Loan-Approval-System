from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from config import LoanDecision, ApplicationStatus

class ApplicantInfo(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    date_of_birth: str
    ssn_last_4: str
    annual_income: float = Field(gt=0)
    employment_status: str  # Employed, Self-employed, Retired
    years_employed: float = Field(ge=0)
    current_employer: str

class LoanDetails(BaseModel):
    loan_amount: float = Field(gt=0)
    loan_purpose: str  # Home, Auto, Personal, Business
    loan_term_months: int = Field(gt=0)
    interest_rate_requested: Optional[float] = None

class CreditProfile(BaseModel):
    credit_score: int = Field(ge=300, le=850)
    accounts_open: int
    delinquencies_past_30_days: int
    delinquencies_past_90_days: int
    total_debt: float
    inquiries_last_6_months: int
    bankruptcy_history: Optional[str] = None

class DocumentVerification(BaseModel):
    income_verification_status: str  # Verified, Pending, Failed
    income_verification_confidence: float = Field(ge=0, le=1)
    employment_verification_status: str
    employment_verification_confidence: float = Field(ge=0, le=1)
    documents_provided: List[str] = []  # W2, Pay stubs, Tax returns, etc.

class LoanApplication(BaseModel):
    applicant_info: ApplicantInfo
    loan_details: LoanDetails
    credit_profile: CreditProfile
    document_verification: DocumentVerification
    application_date: Optional[str] = None
    id: Optional[str] = None

class AgentAnalysis(BaseModel):
    agent_name: str
    analysis: str
    score: float = Field(ge=0, le=100)
    recommendation: str  # Approve, Reject, Review

class LoanDecisionResult(BaseModel):
    application_id: str
    final_decision: LoanDecision
    decision_score: float = Field(ge=0, le=100)
    reasoning: str
    agent_analyses: List[AgentAnalysis]
    risk_flags: List[str] = []
    compliance_issues: List[str] = []
    created_at: str
    processing_time_seconds: float

class ApplicationResponse(BaseModel):
    application_id: str
    status: ApplicationStatus
    decision: Optional[LoanDecision] = None
    decision_result: Optional[LoanDecisionResult] = None
    error_message: Optional[str] = None
    created_at: str
    updated_at: str
