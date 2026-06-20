import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
MODEL = "global.anthropic.claude-haiku-4-5-20251001-v1:0"
API_TIMEOUT = 30

class LoanDecision(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    MANUAL_REVIEW = "MANUAL_REVIEW"

class ApplicationStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    ANALYZING = "ANALYZING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"

# Risk thresholds
MIN_CREDIT_SCORE = 600
MAX_DEBT_TO_INCOME = 0.43
MIN_INCOME_VERIFICATION_CONFIDENCE = 0.8
MIN_EMPLOYMENT_VERIFICATION_CONFIDENCE = 0.7

# Compliance rules
MAX_LOAN_AMOUNT = 1_000_000
MIN_LOAN_AMOUNT = 10_000
