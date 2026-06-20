import anthropic
import json
from config import (
    CLAUDE_API_KEY, MODEL,
    MIN_CREDIT_SCORE, MAX_DEBT_TO_INCOME,
    MIN_INCOME_VERIFICATION_CONFIDENCE, MIN_EMPLOYMENT_VERIFICATION_CONFIDENCE,
    MAX_LOAN_AMOUNT, MIN_LOAN_AMOUNT
)
from models import LoanApplication, AgentAnalysis

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def call_claude_api(prompt: str, max_tokens: int = 500) -> dict:
    """Helper function to call Claude API and parse JSON response."""
    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )

        if not message.content or not message.content[0].text:
            raise ValueError(f"Empty response from API. Message: {message}")

        response_text = message.content[0].text.strip()

        # Handle markdown code block wrapping
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            json_lines = []
            in_json = False
            for line in lines:
                if line.startswith("```json"):
                    in_json = True
                    continue
                elif line.startswith("```"):
                    break
                elif in_json:
                    json_lines.append(line)
            response_text = "\n".join(json_lines).strip()

        return json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Response was: {message.content[0].text if message.content else 'No content'}")
        raise

def document_verification_agent(loan_app: LoanApplication) -> AgentAnalysis:
    """Verifies applicant documents and validates their authenticity."""

    doc_verification = loan_app.document_verification
    applicant = loan_app.applicant_info

    prompt = f"""
    You are a Document Verification Agent for a loan approval system.

    Analyze the following applicant documents and verification status:

    Applicant: {applicant.first_name} {applicant.last_name}
    Annual Income: ${applicant.annual_income:,.2f}
    Employment Status: {applicant.employment_status}
    Years Employed: {applicant.years_employed}

    Document Verification Details:
    - Income Verification Status: {doc_verification.income_verification_status}
    - Income Verification Confidence: {doc_verification.income_verification_confidence * 100:.1f}%
    - Employment Verification Status: {doc_verification.employment_verification_status}
    - Employment Verification Confidence: {doc_verification.employment_verification_confidence * 100:.1f}%
    - Documents Provided: {', '.join(doc_verification.documents_provided)}

    Minimum Thresholds:
    - Income Verification Confidence Required: {MIN_INCOME_VERIFICATION_CONFIDENCE * 100:.0f}%
    - Employment Verification Confidence Required: {MIN_EMPLOYMENT_VERIFICATION_CONFIDENCE * 100:.0f}%

    Based on this information:
    1. Assess the quality and completeness of document verification
    2. Identify any red flags or inconsistencies
    3. Provide a confidence score (0-100) for document authenticity
    4. Recommend: Approve, Reject, or Review

    Respond in JSON format:
    {{
        "analysis": "your detailed analysis",
        "score": <0-100>,
        "recommendation": "Approve|Reject|Review",
        "red_flags": ["flag1", "flag2"]
    }}
    """

    response_data = call_claude_api(prompt)

    return AgentAnalysis(
        agent_name="Document Verification Agent",
        analysis=response_data["analysis"],
        score=response_data["score"],
        recommendation=response_data["recommendation"]
    )

def credit_analysis_agent(loan_app: LoanApplication) -> AgentAnalysis:
    """Analyzes credit history, credit score, and payment patterns."""

    credit = loan_app.credit_profile

    prompt = f"""
    You are a Credit Analysis Agent for a loan approval system.

    Analyze the following credit profile:

    Credit Score: {credit.credit_score}
    Accounts Open: {credit.accounts_open}
    Delinquencies (Past 30 days): {credit.delinquencies_past_30_days}
    Delinquencies (Past 90 days): {credit.delinquencies_past_90_days}
    Total Debt: ${credit.total_debt:,.2f}
    Inquiries (Last 6 months): {credit.inquiries_last_6_months}
    Bankruptcy History: {credit.bankruptcy_history or 'None'}

    Minimum Credit Score Required: {MIN_CREDIT_SCORE}

    Based on this information:
    1. Evaluate credit worthiness
    2. Assess payment history and patterns
    3. Calculate credit risk level
    4. Provide a credit score (0-100)
    5. Recommend: Approve, Reject, or Review

    Respond in JSON format:
    {{
        "analysis": "your detailed credit analysis",
        "score": <0-100>,
        "recommendation": "Approve|Reject|Review",
        "risk_assessment": "Low|Medium|High"
    }}
    """

    response_data = call_claude_api(prompt)

    return AgentAnalysis(
        agent_name="Credit Analysis Agent",
        analysis=response_data["analysis"],
        score=response_data["score"],
        recommendation=response_data["recommendation"]
    )

def risk_assessment_agent(loan_app: LoanApplication) -> AgentAnalysis:
    """Evaluates risk indicators: debt-to-income ratio, industry, loan-to-value."""

    applicant = loan_app.applicant_info
    loan = loan_app.loan_details
    credit = loan_app.credit_profile

    debt_to_income = credit.total_debt / applicant.annual_income if applicant.annual_income > 0 else 0
    monthly_payment_estimate = (loan.loan_amount * (0.06 / 12)) / (1 - (1 + 0.06/12)**(-loan.loan_term_months))
    debt_to_income_with_new_loan = (credit.total_debt + (monthly_payment_estimate * 12)) / applicant.annual_income

    prompt = f"""
    You are a Risk Assessment Agent for a loan approval system.

    Analyze the following risk indicators:

    Loan Amount: ${loan.loan_amount:,.2f}
    Loan Purpose: {loan.loan_purpose}
    Loan Term: {loan.loan_term_months} months
    Annual Income: ${applicant.annual_income:,.2f}
    Employment Status: {applicant.employment_status}
    Years Employed: {applicant.years_employed}

    Risk Metrics:
    - Current Debt-to-Income Ratio: {debt_to_income * 100:.1f}%
    - Projected Debt-to-Income (with new loan): {debt_to_income_with_new_loan * 100:.1f}%
    - Maximum Allowed Debt-to-Income: {MAX_DEBT_TO_INCOME * 100:.1f}%
    - Loan Amount Range: ${MIN_LOAN_AMOUNT:,.0f} - ${MAX_LOAN_AMOUNT:,.0f}

    Based on this information:
    1. Assess overall risk level (Low, Medium, High)
    2. Identify key risk factors
    3. Evaluate loan amount appropriateness
    4. Provide a risk score (0-100, where 100 is highest risk)
    5. Recommend: Approve, Reject, or Review

    Respond in JSON format:
    {{
        "analysis": "your detailed risk assessment",
        "score": <0-100>,
        "recommendation": "Approve|Reject|Review",
        "risk_flags": ["flag1", "flag2"]
    }}
    """

    response_data = call_claude_api(prompt)

    return AgentAnalysis(
        agent_name="Risk Assessment Agent",
        analysis=response_data["analysis"],
        score=response_data["score"],
        recommendation=response_data["recommendation"]
    )

def compliance_agent(loan_app: LoanApplication) -> AgentAnalysis:
    """Checks regulatory compliance and anti-fraud rules."""

    applicant = loan_app.applicant_info
    loan = loan_app.loan_details

    prompt = f"""
    You are a Compliance Agent for a loan approval system.

    Analyze the following application for compliance and fraud:

    Applicant: {applicant.first_name} {applicant.last_name}
    Annual Income: ${applicant.annual_income:,.2f}
    Loan Amount: ${loan.loan_amount:,.2f}
    Loan Purpose: {loan.loan_purpose}

    Regulatory Constraints:
    - Maximum Loan Amount: ${MAX_LOAN_AMOUNT:,.0f}
    - Minimum Loan Amount: ${MIN_LOAN_AMOUNT:,.0f}
    - Loan-to-Income Ratio Should Not Exceed: 5:1

    Check for:
    1. Regulatory compliance violations
    2. Anti-money laundering (AML) concerns
    3. Know Your Customer (KYC) requirements
    4. Potential fraud indicators
    5. Loan amount reasonableness relative to income
    6. Purpose validity

    Provide a compliance score (0-100, where 100 is fully compliant).
    Recommend: Approve, Reject, or Review

    Respond in JSON format:
    {{
        "analysis": "your detailed compliance analysis",
        "score": <0-100>,
        "recommendation": "Approve|Reject|Review",
        "compliance_issues": ["issue1", "issue2"]
    }}
    """

    response_data = call_claude_api(prompt)

    return AgentAnalysis(
        agent_name="Compliance Agent",
        analysis=response_data["analysis"],
        score=response_data["score"],
        recommendation=response_data["recommendation"]
    )

def decision_agent(loan_app: LoanApplication, agent_analyses: list[AgentAnalysis]) -> dict:
    """Synthesizes all agent findings and makes the final decision."""

    analyses_text = "\n".join([
        f"- {a.agent_name}: Score={a.score}, Recommendation={a.recommendation}\n  {a.analysis}"
        for a in agent_analyses
    ])

    applicant = loan_app.applicant_info
    loan = loan_app.loan_details
    credit = loan_app.credit_profile

    prompt = f"""
    You are the Decision Agent for a loan approval system. Your job is to synthesize findings from all specialist agents and make a final decision.

    Applicant Summary:
    - Name: {applicant.first_name} {applicant.last_name}
    - Annual Income: ${applicant.annual_income:,.2f}
    - Credit Score: {credit.credit_score}
    - Loan Amount Requested: ${loan.loan_amount:,.2f}
    - Loan Purpose: {loan.loan_purpose}

    Agent Analysis Results:
    {analyses_text}

    Decision Rules:
    1. APPROVED: All agents recommend Approve AND decision_score >= 75
    2. REJECTED: Any agent recommends Reject OR decision_score < 40
    3. MANUAL_REVIEW: Mixed recommendations OR 40 <= decision_score < 75

    Based on the agent analyses above:
    1. Calculate an overall decision score (0-100)
    2. Determine final decision: APPROVED, REJECTED, or MANUAL_REVIEW
    3. Provide clear reasoning for the decision
    4. List all risk flags and compliance issues

    Respond in JSON format:
    {{
        "decision": "APPROVED|REJECTED|MANUAL_REVIEW",
        "decision_score": <0-100>,
        "reasoning": "your detailed reasoning",
        "risk_flags": ["flag1", "flag2"],
        "compliance_issues": []
    }}
    """

    return call_claude_api(prompt, max_tokens=800)
