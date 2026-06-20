"""
Agentic AI Intelligent Loan Approval System - Example Usage
Demonstrates the multi-agent system with sample loan applications
"""

import sys
import json
from datetime import datetime
from models import (
    ApplicantInfo, LoanDetails, CreditProfile, DocumentVerification,
    LoanApplication
)
from orchestrator import LoanOrchestrator

def create_sample_application_1():
    """Low-risk approved candidate"""
    return LoanApplication(
        applicant_info=ApplicantInfo(
            first_name="John",
            last_name="Smith",
            email="john.smith@email.com",
            phone="555-0001",
            date_of_birth="1980-05-15",
            ssn_last_4="1234",
            annual_income=150_000,
            employment_status="Employed",
            years_employed=8.5,
            current_employer="Tech Corporation Inc."
        ),
        loan_details=LoanDetails(
            loan_amount=300_000,
            loan_purpose="Home",
            loan_term_months=360,
            interest_rate_requested=6.5
        ),
        credit_profile=CreditProfile(
            credit_score=750,
            accounts_open=5,
            delinquencies_past_30_days=0,
            delinquencies_past_90_days=0,
            total_debt=45_000,
            inquiries_last_6_months=1,
            bankruptcy_history=None
        ),
        document_verification=DocumentVerification(
            income_verification_status="Verified",
            income_verification_confidence=0.95,
            employment_verification_status="Verified",
            employment_verification_confidence=0.90,
            documents_provided=["W2", "Pay stubs (3 months)", "Tax returns (2 years)"]
        ),
        application_date=datetime.utcnow().isoformat()
    )

def create_sample_application_2():
    """Medium-risk manual review candidate"""
    return LoanApplication(
        applicant_info=ApplicantInfo(
            first_name="Sarah",
            last_name="Johnson",
            email="sarah.j@email.com",
            phone="555-0002",
            date_of_birth="1985-08-22",
            ssn_last_4="5678",
            annual_income=85_000,
            employment_status="Self-employed",
            years_employed=3.0,
            current_employer="Johnson Consulting LLC"
        ),
        loan_details=LoanDetails(
            loan_amount=250_000,
            loan_purpose="Home",
            loan_term_months=360,
            interest_rate_requested=7.2
        ),
        credit_profile=CreditProfile(
            credit_score=680,
            accounts_open=3,
            delinquencies_past_30_days=0,
            delinquencies_past_90_days=1,
            total_debt=38_000,
            inquiries_last_6_months=3,
            bankruptcy_history=None
        ),
        document_verification=DocumentVerification(
            income_verification_status="Pending",
            income_verification_confidence=0.72,
            employment_verification_status="Verified",
            employment_verification_confidence=0.85,
            documents_provided=["Tax returns (2 years)", "Bank statements"]
        ),
        application_date=datetime.utcnow().isoformat()
    )

def create_sample_application_3():
    """High-risk rejection candidate"""
    return LoanApplication(
        applicant_info=ApplicantInfo(
            first_name="Michael",
            last_name="Davis",
            email="m.davis@email.com",
            phone="555-0003",
            date_of_birth="1990-12-10",
            ssn_last_4="9012",
            annual_income=55_000,
            employment_status="Employed",
            years_employed=1.5,
            current_employer="Retail Store Inc."
        ),
        loan_details=LoanDetails(
            loan_amount=400_000,
            loan_purpose="Home",
            loan_term_months=360,
            interest_rate_requested=8.5
        ),
        credit_profile=CreditProfile(
            credit_score=580,
            accounts_open=2,
            delinquencies_past_30_days=2,
            delinquencies_past_90_days=3,
            total_debt=95_000,
            inquiries_last_6_months=8,
            bankruptcy_history="Chapter 7 (2015)"
        ),
        document_verification=DocumentVerification(
            income_verification_status="Failed",
            income_verification_confidence=0.45,
            employment_verification_status="Pending",
            employment_verification_confidence=0.50,
            documents_provided=["Pay stub (current)"]
        ),
        application_date=datetime.utcnow().isoformat()
    )

def format_result(decision_result):
    """Pretty print the decision result"""
    print("\n" + "="*80)
    print(f"APPLICATION ID: {decision_result.application_id}")
    print("="*80)
    print(f"FINAL DECISION: {decision_result.final_decision}")
    print(f"Decision Score: {decision_result.decision_score:.1f}/100")
    print(f"Processing Time: {decision_result.processing_time_seconds:.2f}s")
    print("\nREASONING:")
    print("-" * 80)
    print(decision_result.reasoning)
    print("\nAGENT ANALYSES:")
    print("-" * 80)

    for agent in decision_result.agent_analyses:
        print(f"\n{agent.agent_name}:")
        print(f"  Score: {agent.score:.1f}/100")
        print(f"  Recommendation: {agent.recommendation}")
        print(f"  Analysis: {agent.analysis[:150]}...")

    if decision_result.risk_flags:
        print("\nRISK FLAGS:")
        print("-" * 80)
        for flag in decision_result.risk_flags:
            print(f"  • {flag}")

    if decision_result.compliance_issues:
        print("\nCOMPLIANCE ISSUES:")
        print("-" * 80)
        for issue in decision_result.compliance_issues:
            print(f"  • {issue}")

    print("\n" + "="*80)

def main():
    """Run the loan approval system with sample applications"""
    print("🏦 Agentic AI Intelligent Loan Approval System")
    print("=" * 80)
    print("Initializing multi-agent orchestrator...\n")

    orchestrator = LoanOrchestrator()

    # Sample applications
    applications = [
        ("Low-Risk Applicant", create_sample_application_1()),
        ("Medium-Risk Applicant", create_sample_application_2()),
        ("High-Risk Applicant", create_sample_application_3())
    ]

    for description, loan_app in applications:
        print(f"\n📋 Analyzing: {description}")
        print(f"   Applicant: {loan_app.applicant_info.first_name} {loan_app.applicant_info.last_name}")
        print(f"   Loan Amount: ${loan_app.loan_details.loan_amount:,.0f}")
        print(f"   Annual Income: ${loan_app.applicant_info.annual_income:,.0f}")
        print(f"   Credit Score: {loan_app.credit_profile.credit_score}")

        try:
            decision_result = orchestrator.analyze_application(loan_app)
            format_result(decision_result)

        except Exception as e:
            print(f"\n❌ Error analyzing application: {str(e)}")
            continue

    # Summary
    print("\n📊 ANALYSIS SUMMARY")
    print("=" * 80)
    all_results = orchestrator.get_all_results()
    approved_count = sum(1 for r in all_results if r.final_decision.value == "APPROVED")
    rejected_count = sum(1 for r in all_results if r.final_decision.value == "REJECTED")
    review_count = sum(1 for r in all_results if r.final_decision.value == "MANUAL_REVIEW")

    print(f"Total Applications Processed: {len(all_results)}")
    print(f"  ✅ Approved: {approved_count}")
    print(f"  ❌ Rejected: {rejected_count}")
    print(f"  ⏳ Manual Review: {review_count}")

    avg_score = sum(r.decision_score for r in all_results) / len(all_results) if all_results else 0
    avg_time = sum(r.processing_time_seconds for r in all_results) / len(all_results) if all_results else 0

    print(f"\nAverage Decision Score: {avg_score:.1f}/100")
    print(f"Average Processing Time: {avg_time:.2f}s")
    print("=" * 80)

if __name__ == "__main__":
    main()
