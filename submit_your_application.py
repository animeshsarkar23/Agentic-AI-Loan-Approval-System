#!/usr/bin/env python3
"""
Submit YOUR Application - Based on your parameters
"""

import json
from models import (
    ApplicantInfo, LoanDetails, CreditProfile, DocumentVerification,
    LoanApplication
)
from orchestrator import LoanOrchestrator
from datetime import datetime, UTC

print("\n" + "="*80)
print("🏦 SUBMITTING YOUR APPLICATION TO THE SYSTEM")
print("="*80 + "\n")

# Your Parameters (from the questionnaire)
print("📝 YOUR PARAMETERS:")
print("-" * 80)

applicant_data = {
    "first_name": "User",
    "last_name": "Application",
    "email": "user@application.com",
    "phone": "555-0001",
    "date_of_birth": "1990-05-15",
    "ssn_last_4": "1234",
    "annual_income": 150000,  # $150,000+
    "employment_status": "Employed",
    "years_employed": 5,  # 3-7 years
    "current_employer": "Professional Services"
}

loan_data = {
    "loan_amount": 250000,  # $200,000-$300,000 (middle)
    "loan_purpose": "Home",
    "loan_term_months": 180,  # 10-15 years (middle: 15 years)
    "interest_rate_requested": 6.5
}

credit_data = {
    "credit_score": 620,  # 600-650 range
    "accounts_open": 4,
    "delinquencies_past_30_days": 0,
    "delinquencies_past_90_days": 2,  # Multiple past 90 days
    "total_debt": 20000,  # Under $25,000
    "inquiries_last_6_months": 2,
    "bankruptcy_history": None
}

doc_data = {
    "income_verification_status": "Verified",
    "income_verification_confidence": 0.85,
    "employment_verification_status": "Verified",
    "employment_verification_confidence": 0.80,
    "documents_provided": ["Pay stubs", "W2", "Employment Letter"]
}

# Display Summary
print(f"💰 Annual Income:        ${applicant_data['annual_income']:,}")
print(f"👔 Employment Status:    {applicant_data['employment_status']}")
print(f"⏱️  Years Employed:       {applicant_data['years_employed']} years")
print(f"📊 Credit Score:         {credit_data['credit_score']}")
print(f"💳 Existing Debt:        ${credit_data['total_debt']:,}")
print(f"⚠️  Delinquencies (90d):  {credit_data['delinquencies_past_90_days']}")
print(f"🏠 Loan Amount:          ${loan_data['loan_amount']:,}")
print(f"📅 Loan Term:            {loan_data['loan_term_months']} months ({loan_data['loan_term_months']//12} years)")
print(f"📍 Bankruptcy:           None")

print("\n" + "="*80)
print("📤 SUBMITTING APPLICATION...")
print("="*80 + "\n")

# Create Application
loan_app = LoanApplication(
    applicant_info=ApplicantInfo(
        first_name=applicant_data["first_name"],
        last_name=applicant_data["last_name"],
        email=applicant_data["email"],
        phone=applicant_data["phone"],
        date_of_birth=applicant_data["date_of_birth"],
        ssn_last_4=applicant_data["ssn_last_4"],
        annual_income=applicant_data["annual_income"],
        employment_status=applicant_data["employment_status"],
        years_employed=applicant_data["years_employed"],
        current_employer=applicant_data["current_employer"]
    ),
    loan_details=LoanDetails(
        loan_amount=loan_data["loan_amount"],
        loan_purpose=loan_data["loan_purpose"],
        loan_term_months=loan_data["loan_term_months"],
        interest_rate_requested=loan_data["interest_rate_requested"]
    ),
    credit_profile=CreditProfile(
        credit_score=credit_data["credit_score"],
        accounts_open=credit_data["accounts_open"],
        delinquencies_past_30_days=credit_data["delinquencies_past_30_days"],
        delinquencies_past_90_days=credit_data["delinquencies_past_90_days"],
        total_debt=credit_data["total_debt"],
        inquiries_last_6_months=credit_data["inquiries_last_6_months"],
        bankruptcy_history=credit_data["bankruptcy_history"]
    ),
    document_verification=DocumentVerification(
        income_verification_status=doc_data["income_verification_status"],
        income_verification_confidence=doc_data["income_verification_confidence"],
        employment_verification_status=doc_data["employment_verification_status"],
        employment_verification_confidence=doc_data["employment_verification_confidence"],
        documents_provided=doc_data["documents_provided"]
    ),
    application_date=datetime.now(UTC).isoformat()
)

# Analyze
try:
    orchestrator = LoanOrchestrator()
    decision_result = orchestrator.analyze_application(loan_app)
    
    print("\n" + "="*80)
    print("✅ APPLICATION ANALYZED SUCCESSFULLY!")
    print("="*80 + "\n")
    
    print(f"📋 Application ID:        {decision_result.application_id}")
    print(f"🎯 Final Decision:        {decision_result.final_decision.value}")
    print(f"📊 Decision Score:        {decision_result.decision_score:.1f}/100")
    print(f"⏱️  Processing Time:       {decision_result.processing_time_seconds:.2f} seconds")
    
    print("\n" + "-"*80)
    print("📝 DECISION REASONING:")
    print("-"*80)
    print(decision_result.reasoning)
    
    print("\n" + "-"*80)
    print("🤖 AGENT ANALYSES:")
    print("-"*80)
    for agent in decision_result.agent_analyses:
        print(f"\n{agent.agent_name}:")
        print(f"  Score: {agent.score:.1f}/100")
        print(f"  Recommendation: {agent.recommendation}")
        print(f"  Analysis: {agent.analysis[:200]}...")
    
    if decision_result.risk_flags:
        print("\n" + "-"*80)
        print("⚠️  RISK FLAGS:")
        print("-"*80)
        for flag in decision_result.risk_flags:
            print(f"  • {flag}")
    
    if decision_result.compliance_issues:
        print("\n" + "-"*80)
        print("🚫 COMPLIANCE ISSUES:")
        print("-"*80)
        for issue in decision_result.compliance_issues:
            print(f"  • {issue}")
    
    print("\n" + "="*80)
    print("✨ APPLICATION PROCESSING COMPLETE!")
    print("="*80 + "\n")
    
    # Display Decision in Large Format
    if decision_result.final_decision.value == "APPROVED":
        print("╔════════════════════════════════════════╗")
        print("║  ✅  APPLICATION APPROVED  ✅         ║")
        print("╚════════════════════════════════════════╝")
    elif decision_result.final_decision.value == "REJECTED":
        print("╔════════════════════════════════════════╗")
        print("║  ❌  APPLICATION REJECTED  ❌         ║")
        print("╚════════════════════════════════════════╝")
    else:
        print("╔════════════════════════════════════════╗")
        print("║  ⏳  MANUAL REVIEW REQUIRED  ⏳       ║")
        print("╚════════════════════════════════════════╝")
    
    print()
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

