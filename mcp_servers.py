"""
MCP (Model Context Protocol) Servers
Provides standardized agent communication through MCP servers
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn

# ============================================================================
# MCP Server for Document Verification
# ============================================================================

document_app = FastAPI(title="Document Verification MCP Server")

class DocumentRequest(BaseModel):
    applicant_name: str
    documents: List[str]
    income_verification_confidence: float
    employment_verification_confidence: float

@document_app.post("/mcp/document_verify")
async def document_verify(request: DocumentRequest) -> JSONResponse:
    """
    MCP endpoint for document verification.

    Standardized interface for agents to verify documents.
    """
    response = {
        "status": "success",
        "agent": "document_verification",
        "data": {
            "applicant": request.applicant_name,
            "documents_count": len(request.documents),
            "documents": request.documents,
            "income_confidence": request.income_verification_confidence,
            "employment_confidence": request.employment_verification_confidence,
            "verification_complete": True,
            "score": (request.income_verification_confidence + request.employment_verification_confidence) / 2 * 100
        }
    }
    return JSONResponse(response)

# ============================================================================
# MCP Server for Credit Analysis
# ============================================================================

credit_app = FastAPI(title="Credit Analysis MCP Server")

class CreditRequest(BaseModel):
    credit_score: int
    accounts_open: int
    total_debt: float
    delinquencies_30: int
    delinquencies_90: int
    inquiries: int
    bankruptcy_history: str = None

@credit_app.post("/mcp/credit_analyze")
async def credit_analyze(request: CreditRequest) -> JSONResponse:
    """
    MCP endpoint for credit analysis.

    Standardized interface for agents to analyze credit profiles.
    """
    # Simple risk calculation
    risk_score = 0

    # Credit score impact
    if request.credit_score < 600:
        risk_score += 40
    elif request.credit_score < 650:
        risk_score += 20
    elif request.credit_score < 700:
        risk_score += 10

    # Delinquency impact
    risk_score += request.delinquencies_30 * 15
    risk_score += request.delinquencies_90 * 20

    # Recent inquiries impact
    if request.inquiries > 5:
        risk_score += 20
    elif request.inquiries > 2:
        risk_score += 10

    # Bankruptcy impact
    if request.bankruptcy_history:
        risk_score += 30

    # Calculate creditworthiness score (0-100)
    creditworthiness_score = max(0, min(100, 100 - risk_score))

    response = {
        "status": "success",
        "agent": "credit_analysis",
        "data": {
            "credit_score": request.credit_score,
            "accounts_open": request.accounts_open,
            "total_debt": request.total_debt,
            "creditworthiness_score": creditworthiness_score,
            "risk_level": "High" if risk_score > 60 else "Medium" if risk_score > 30 else "Low",
            "delinquencies": {
                "past_30_days": request.delinquencies_30,
                "past_90_days": request.delinquencies_90
            },
            "bankruptcy": request.bankruptcy_history or "None"
        }
    }
    return JSONResponse(response)

# ============================================================================
# MCP Server for Compliance Checking
# ============================================================================

compliance_app = FastAPI(title="Compliance MCP Server")

class ComplianceRequest(BaseModel):
    applicant_name: str
    loan_amount: float
    annual_income: float
    purpose: str

@compliance_app.post("/mcp/compliance_check")
async def compliance_check(request: ComplianceRequest) -> JSONResponse:
    """
    MCP endpoint for compliance checking.

    Standardized interface for agents to check regulatory compliance.
    """
    # Check compliance rules
    compliance_issues = []
    compliance_score = 100

    # Loan amount validation
    if request.loan_amount < 10_000:
        compliance_issues.append("Loan amount below minimum ($10,000)")
        compliance_score -= 20
    elif request.loan_amount > 1_000_000:
        compliance_issues.append("Loan amount above maximum ($1,000,000)")
        compliance_score -= 20

    # Income validation
    if request.annual_income == 0:
        compliance_issues.append("Income not provided")
        compliance_score -= 30

    # Loan-to-income ratio
    loan_to_income = request.loan_amount / request.annual_income if request.annual_income > 0 else 0
    if loan_to_income > 5:
        compliance_issues.append("Loan-to-income ratio exceeds 5:1")
        compliance_score -= 15

    # Purpose validation
    valid_purposes = ["Home", "Auto", "Personal", "Business"]
    if request.purpose not in valid_purposes:
        compliance_issues.append(f"Invalid loan purpose: {request.purpose}")
        compliance_score -= 10

    response = {
        "status": "success",
        "agent": "compliance",
        "data": {
            "applicant": request.applicant_name,
            "loan_amount": request.loan_amount,
            "compliance_score": max(0, compliance_score),
            "issues": compliance_issues,
            "compliant": len(compliance_issues) == 0,
            "checks": {
                "loan_amount": "Pass" if request.loan_amount >= 10_000 and request.loan_amount <= 1_000_000 else "Fail",
                "income_provided": "Pass" if request.annual_income > 0 else "Fail",
                "loan_to_income": "Pass" if loan_to_income <= 5 else "Fail",
                "purpose_valid": "Pass" if request.purpose in valid_purposes else "Fail"
            }
        }
    }
    return JSONResponse(response)

# ============================================================================
# MCP Server Health & Status
# ============================================================================

@document_app.get("/mcp/health")
async def doc_health():
    return {"status": "healthy", "service": "document_verification"}

@credit_app.get("/mcp/health")
async def credit_health():
    return {"status": "healthy", "service": "credit_analysis"}

@compliance_app.get("/mcp/health")
async def compliance_health():
    return {"status": "healthy", "service": "compliance"}

# ============================================================================
# MCP Registry (for agent discovery)
# ============================================================================

mcp_registry_app = FastAPI(title="MCP Registry Server")

@mcp_registry_app.get("/mcp/registry")
async def mcp_registry():
    """
    MCP registry endpoint for agent service discovery.

    Allows agents to discover available MCP services.
    """
    return {
        "services": [
            {
                "name": "document_verification",
                "url": "http://localhost:8502/mcp",
                "description": "Document verification and validation",
                "endpoints": ["/document_verify", "/health"]
            },
            {
                "name": "credit_analysis",
                "url": "http://localhost:8503/mcp",
                "description": "Credit history and analysis",
                "endpoints": ["/credit_analyze", "/health"]
            },
            {
                "name": "compliance",
                "url": "http://localhost:8504/mcp",
                "description": "Regulatory compliance checking",
                "endpoints": ["/compliance_check", "/health"]
            }
        ]
    }

@mcp_registry_app.post("/mcp/register_service")
async def register_service(service_data: Dict[str, Any]):
    """Register a new MCP service"""
    return {
        "status": "registered",
        "service": service_data.get("name"),
        "url": service_data.get("url")
    }

# ============================================================================
# Unified MCP Gateway (optional single endpoint)
# ============================================================================

gateway_app = FastAPI(title="MCP Gateway")

@gateway_app.post("/mcp/document_verify")
async def gateway_document_verify(request: DocumentRequest):
    """Gateway endpoint that routes to document verification service"""
    return await document_verify(request)

@gateway_app.post("/mcp/credit_analyze")
async def gateway_credit_analyze(request: CreditRequest):
    """Gateway endpoint that routes to credit analysis service"""
    return await credit_analyze(request)

@gateway_app.post("/mcp/compliance_check")
async def gateway_compliance_check(request: ComplianceRequest):
    """Gateway endpoint that routes to compliance service"""
    return await compliance_check(request)

@gateway_app.get("/mcp/health")
async def gateway_health():
    """Gateway health check"""
    return {
        "status": "healthy",
        "service": "mcp_gateway",
        "timestamp": str(__import__("datetime").datetime.utcnow())
    }

# ============================================================================
# Run MCP Servers
# ============================================================================

def run_document_server(port=8502):
    """Run Document Verification MCP Server"""
    print(f"Starting Document Verification MCP Server on port {port}...")
    uvicorn.run(document_app, host="0.0.0.0", port=port)

def run_credit_server(port=8503):
    """Run Credit Analysis MCP Server"""
    print(f"Starting Credit Analysis MCP Server on port {port}...")
    uvicorn.run(credit_app, host="0.0.0.0", port=port)

def run_compliance_server(port=8504):
    """Run Compliance MCP Server"""
    print(f"Starting Compliance MCP Server on port {port}...")
    uvicorn.run(compliance_app, host="0.0.0.0", port=port)

def run_registry_server(port=8505):
    """Run MCP Registry Server"""
    print(f"Starting MCP Registry Server on port {port}...")
    uvicorn.run(mcp_registry_app, host="0.0.0.0", port=port)

def run_gateway_server(port=8506):
    """Run MCP Gateway (unified endpoint)"""
    print(f"Starting MCP Gateway on port {port}...")
    uvicorn.run(gateway_app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        server_type = sys.argv[1]

        if server_type == "document":
            run_document_server()
        elif server_type == "credit":
            run_credit_server()
        elif server_type == "compliance":
            run_compliance_server()
        elif server_type == "registry":
            run_registry_server()
        elif server_type == "gateway":
            run_gateway_server()
        else:
            print("Usage: python mcp_servers.py [document|credit|compliance|registry|gateway]")
    else:
        print("Starting all MCP servers...")
        print("Run with argument: python mcp_servers.py [server_type]")
