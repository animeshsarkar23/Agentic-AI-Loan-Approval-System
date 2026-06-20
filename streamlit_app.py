"""
Streamlit Chatbot UI for Agentic AI Loan Approval System
Provides an interactive interface for loan application submission and decision display
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
from models import (
    ApplicantInfo, LoanDetails, CreditProfile, DocumentVerification,
    LoanApplication
)
from orchestrator import LoanOrchestrator
import uuid

# Page configuration
st.set_page_config(
    page_title="🏦 Loan Approval System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = LoanOrchestrator()

if "applications_history" not in st.session_state:
    st.session_state.applications_history = []

if "current_decision" not in st.session_state:
    st.session_state.current_decision = None

# Sidebar
with st.sidebar:
    st.title("📋 Navigation")
    page = st.radio("Select Page", [
        "Submit Application",
        "View Results",
        "Application History",
        "System Status"
    ])

    st.divider()

    st.subheader("ℹ️ About")
    st.info("""
    **Agentic AI Loan Approval System**

    Multi-agent system analyzing loan applications using:
    - Document Verification
    - Credit Analysis
    - Risk Assessment
    - Compliance Check
    - Decision Synthesis

    **Processing Time**: ~20-30 seconds per application
    """)

# Main content
if page == "Submit Application":
    st.title("🏦 Loan Application Submission")

    with st.expander("ℹ️ System Information", expanded=False):
        st.markdown("""
        This system analyzes loan applications using 5 AI agents:

        1. **Document Verification Agent** - Validates income/employment docs
        2. **Credit Analysis Agent** - Evaluates credit history
        3. **Risk Assessment Agent** - Analyzes debt-to-income ratio
        4. **Compliance Agent** - Checks regulatory compliance
        5. **Decision Agent** - Synthesizes all findings

        **Decisions**: APPROVED ✅ | REJECTED ❌ | MANUAL_REVIEW ⏳
        """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👤 Applicant Information")

        first_name = st.text_input("First Name", value="John")
        last_name = st.text_input("Last Name", value="Doe")
        email = st.text_input("Email", value="john@example.com")
        phone = st.text_input("Phone", value="555-0001")
        date_of_birth = st.date_input("Date of Birth", value=datetime(1980, 5, 15))
        ssn_last_4 = st.text_input("SSN (Last 4 digits)", value="1234", max_chars=4)
        annual_income = st.number_input("Annual Income ($)", value=150000, min_value=10000)
        employment_status = st.selectbox(
            "Employment Status",
            ["Employed", "Self-employed", "Retired", "Unemployed"]
        )
        years_employed = st.slider("Years Employed", 0.0, 50.0, 8.5)
        current_employer = st.text_input("Current Employer", value="Tech Corporation Inc.")

    with col2:
        st.subheader("💰 Loan Details")

        loan_amount = st.number_input("Loan Amount ($)", value=300000, min_value=10000)
        loan_purpose = st.selectbox(
            "Loan Purpose",
            ["Home", "Auto", "Personal", "Business"]
        )
        loan_term = st.slider("Loan Term (months)", 12, 360, 360)
        interest_rate = st.number_input("Interest Rate (%)", value=6.5, min_value=0.0)

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📊 Credit Profile")

        credit_score = st.slider("Credit Score", 300, 850, 750)
        accounts_open = st.number_input("Accounts Open", value=5, min_value=0)
        delinq_30 = st.number_input("Delinquencies (30 days)", value=0, min_value=0)
        delinq_90 = st.number_input("Delinquencies (90 days)", value=0, min_value=0)
        total_debt = st.number_input("Total Debt ($)", value=45000, min_value=0)
        inquiries = st.number_input("Recent Inquiries (6m)", value=1, min_value=0)
        bankruptcy = st.selectbox(
            "Bankruptcy History",
            ["None", "Chapter 7 (Current)", "Chapter 7 (Past 7 years)", "Chapter 13 (Current)", "Chapter 13 (Past 7 years)"]
        )

    with col4:
        st.subheader("📄 Document Verification")

        income_status = st.selectbox(
            "Income Verification",
            ["Verified", "Pending", "Failed"]
        )
        income_confidence = st.slider("Income Verification Confidence (%)", 0, 100, 95) / 100

        employment_status_doc = st.selectbox(
            "Employment Verification",
            ["Verified", "Pending", "Failed"]
        )
        employment_confidence = st.slider("Employment Verification Confidence (%)", 0, 100, 90) / 100

        documents = st.multiselect(
            "Documents Provided",
            ["W2", "Pay stubs (1 month)", "Pay stubs (3 months)", "Pay stubs (6 months)",
             "Tax returns (1 year)", "Tax returns (2 years)", "Bank statements", "Employment letter"],
            default=["W2", "Pay stubs (3 months)", "Tax returns (2 years)"]
        )

    st.divider()

    if st.button("🚀 Submit Application & Analyze", use_container_width=True, type="primary"):
        with st.spinner("Analyzing application... This may take 20-30 seconds"):
            try:
                # Create loan application object
                loan_app = LoanApplication(
                    id=str(uuid.uuid4()),
                    applicant_info=ApplicantInfo(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone,
                        date_of_birth=date_of_birth.isoformat(),
                        ssn_last_4=ssn_last_4,
                        annual_income=annual_income,
                        employment_status=employment_status,
                        years_employed=years_employed,
                        current_employer=current_employer
                    ),
                    loan_details=LoanDetails(
                        loan_amount=loan_amount,
                        loan_purpose=loan_purpose,
                        loan_term_months=loan_term,
                        interest_rate_requested=interest_rate
                    ),
                    credit_profile=CreditProfile(
                        credit_score=credit_score,
                        accounts_open=accounts_open,
                        delinquencies_past_30_days=delinq_30,
                        delinquencies_past_90_days=delinq_90,
                        total_debt=total_debt,
                        inquiries_last_6_months=inquiries,
                        bankruptcy_history=None if bankruptcy == "None" else bankruptcy
                    ),
                    document_verification=DocumentVerification(
                        income_verification_status=income_status,
                        income_verification_confidence=income_confidence,
                        employment_verification_status=employment_status_doc,
                        employment_verification_confidence=employment_confidence,
                        documents_provided=documents
                    ),
                    application_date=datetime.utcnow().isoformat()
                )

                # Analyze application
                decision_result = st.session_state.orchestrator.analyze_application(loan_app)

                # Store in session
                st.session_state.current_decision = decision_result
                st.session_state.applications_history.append({
                    "application_id": decision_result.application_id,
                    "applicant": f"{first_name} {last_name}",
                    "decision": decision_result.final_decision.value,
                    "score": decision_result.decision_score,
                    "timestamp": decision_result.created_at
                })

                st.success("✅ Application analyzed successfully!")

                # Display results
                st.divider()
                st.subheader("📋 Decision Results")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    if decision_result.final_decision.value == "APPROVED":
                        st.metric("Decision", "✅ APPROVED", delta="Positive")
                    elif decision_result.final_decision.value == "REJECTED":
                        st.metric("Decision", "❌ REJECTED", delta="Negative")
                    else:
                        st.metric("Decision", "⏳ MANUAL REVIEW", delta="Pending")

                with col2:
                    st.metric("Score", f"{decision_result.decision_score:.1f}/100")

                with col3:
                    st.metric("Processing Time", f"{decision_result.processing_time_seconds:.1f}s")

                with col4:
                    st.metric("Application ID", decision_result.application_id[:8] + "...")

                st.markdown(f"**Reasoning:**\n{decision_result.reasoning}")

                # Agent Analyses
                st.subheader("🤖 Agent Analyses")

                for agent in decision_result.agent_analyses:
                    with st.expander(f"{agent.agent_name} (Score: {agent.score:.0f}/100)"):
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.metric("Score", f"{agent.score:.1f}")
                            st.metric("Recommendation", agent.recommendation)
                        with col2:
                            st.write(agent.analysis)

                # Risk Flags
                if decision_result.risk_flags:
                    st.warning(f"⚠️ **Risk Flags:**\n" + "\n".join([f"- {f}" for f in decision_result.risk_flags]))

                # Compliance Issues
                if decision_result.compliance_issues:
                    st.error(f"🚫 **Compliance Issues:**\n" + "\n".join([f"- {f}" for f in decision_result.compliance_issues]))

            except Exception as e:
                st.error(f"Error analyzing application: {str(e)}")

elif page == "View Results":
    st.title("📊 View Application Results")

    if st.session_state.current_decision:
        decision = st.session_state.current_decision

        st.subheader(f"Application: {decision.application_id[:8]}...")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Final Decision", decision.final_decision.value)
        with col2:
            st.metric("Score", f"{decision.decision_score:.1f}/100")
        with col3:
            st.metric("Time", f"{decision.processing_time_seconds:.1f}s")

        st.markdown("### Decision Reasoning")
        st.write(decision.reasoning)

        st.markdown("### Agent Analyses")
        df_agents = pd.DataFrame([
            {
                "Agent": a.agent_name,
                "Score": f"{a.score:.0f}",
                "Recommendation": a.recommendation
            }
            for a in decision.agent_analyses
        ])
        st.dataframe(df_agents, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            if decision.risk_flags:
                st.error("⚠️ Risk Flags:")
                for flag in decision.risk_flags:
                    st.write(f"- {flag}")

        with col2:
            if decision.compliance_issues:
                st.error("🚫 Compliance Issues:")
                for issue in decision.compliance_issues:
                    st.write(f"- {issue}")

    else:
        st.info("No application analyzed yet. Submit one from the 'Submit Application' page.")

elif page == "Application History":
    st.title("📈 Application History")

    if st.session_state.applications_history:
        df_history = pd.DataFrame(st.session_state.applications_history)

        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Applications", len(df_history))

        with col2:
            approved = len(df_history[df_history["decision"] == "APPROVED"])
            st.metric("Approved", approved)

        with col3:
            rejected = len(df_history[df_history["decision"] == "REJECTED"])
            st.metric("Rejected", rejected)

        with col4:
            manual = len(df_history[df_history["decision"] == "MANUAL_REVIEW"])
            st.metric("Manual Review", manual)

        st.divider()

        # Decision breakdown chart
        decision_counts = df_history["decision"].value_counts()
        st.bar_chart(decision_counts)

        # Applications table
        st.subheader("All Applications")
        st.dataframe(df_history, use_container_width=True)

    else:
        st.info("No applications submitted yet.")

elif page == "System Status":
    st.title("🔧 System Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("System Status", "🟢 Operational")

    with col2:
        st.metric("API Model", "Claude 3.5 Sonnet")

    with col3:
        st.metric("Agents Active", "5")

    st.divider()

    st.subheader("📋 System Configuration")

    config_data = {
        "Component": [
            "Orchestrator",
            "FastAPI Server",
            "Streamlit UI",
            "LangGraph Engine",
            "MCP Framework"
        ],
        "Status": ["✅ Ready", "✅ Ready", "✅ Running", "✅ Ready", "✅ Ready"],
        "Port/Location": ["Local", "8000", "8501", "Local", "8502"]
    }

    st.dataframe(pd.DataFrame(config_data), use_container_width=True)

    st.divider()

    st.subheader("🤖 Active Agents")

    agents_info = {
        "Agent Name": [
            "Document Verification",
            "Credit Analysis",
            "Risk Assessment",
            "Compliance Check",
            "Decision Synthesis"
        ],
        "Responsibility": [
            "Validates documents",
            "Evaluates credit history",
            "Analyzes loan risk",
            "Checks compliance",
            "Synthesizes decisions"
        ],
        "Status": ["✅", "✅", "✅", "✅", "✅"]
    }

    st.dataframe(pd.DataFrame(agents_info), use_container_width=True)

    st.divider()

    st.subheader("📊 Decision Thresholds")

    threshold_data = {
        "Parameter": [
            "Approval Threshold",
            "Rejection Threshold",
            "Manual Review Range",
            "Min Credit Score",
            "Max Debt-to-Income",
            "Min Income Verification",
            "Min Employment Verification"
        ],
        "Value": [
            "≥ 75",
            "< 40",
            "40-75",
            "600",
            "43%",
            "80%",
            "70%"
        ]
    }

    st.dataframe(pd.DataFrame(threshold_data), use_container_width=True)

    st.divider()

    st.subheader("📚 Documentation")

    st.markdown("""
    - **README.md** - Complete feature overview
    - **ARCHITECTURE.md** - System design and data flows
    - **TESTING.md** - Testing guide and validation
    - **GETTING_STARTED.md** - Quick start guide
    - **CLAUDE.md** - Project documentation
    """)

# Footer
st.divider()
st.markdown(
    "Built with ❤️ using Streamlit, FastAPI, Claude AI, and LangGraph | "
    "[GitHub](https://github.com) | [Docs](https://example.com)"
)
