# 🌐 Web UI Input Guide - How to Use the Loan Approval System

## Quick Start

### Access the Web UI
1. Open your browser
2. Go to: **http://localhost:8501**
3. You'll see the Streamlit interface with navigation on the left sidebar

---

## 📋 Step-by-Step: Submit Your First Loan Application

### Step 1: Navigate to "Submit Application"
- Look at the left sidebar
- Click on **"📋 Submit Application"**
- You'll see a form with default values already filled in

### Step 2: Review Default Values
The form comes pre-filled with test data:

```
👤 APPLICANT INFORMATION
├─ First Name: John
├─ Last Name: Doe
├─ Email: john@example.com
├─ Phone: 555-0001
├─ Date of Birth: 1980-05-15
├─ SSN (Last 4): 1234
├─ Annual Income: $150,000
├─ Employment Status: Employed
├─ Years Employed: 8.5
└─ Current Employer: Tech Corporation Inc.

💰 LOAN DETAILS
├─ Loan Amount: $300,000
├─ Loan Purpose: Home
├─ Loan Term: 360 months
└─ Interest Rate: 6.5%

📊 CREDIT PROFILE
├─ Credit Score: 750
├─ Accounts Open: 5
├─ Delinquencies (30 days): 0
├─ Delinquencies (90 days): 0
├─ Total Debt: $45,000
├─ Recent Inquiries: 1
└─ Bankruptcy History: None

📄 DOCUMENT VERIFICATION
├─ Income Verification Status: Verified
├─ Income Confidence: 95%
├─ Employment Verification: Verified
├─ Employment Confidence: 90%
└─ Documents: W2, Pay stubs (3 months), Tax returns (2 years)
```

### Step 3: Modify Values (Optional)
You can change any field:

**For Low-Risk Application (Should be APPROVED):**
- Credit Score: Keep at 750 or higher
- Annual Income: Keep at $150,000+
- Total Debt: Keep at $45,000 or lower
- Employment Years: Keep at 5+

**For Medium-Risk Application (Should be MANUAL_REVIEW):**
- Credit Score: Change to 680
- Annual Income: Change to $85,000
- Total Debt: Change to $38,000
- Delinquencies (90 days): Change to 1

**For High-Risk Application (Should be REJECTED):**
- Credit Score: Change to 580
- Annual Income: Change to $55,000
- Total Debt: Change to $95,000
- Delinquencies (30 days): Change to 2
- Delinquencies (90 days): Change to 3

### Step 4: Submit Application
1. Scroll down to bottom of form
2. Click the **"🚀 Submit Application & Analyze"** button (large blue button)
3. You'll see a spinner: "Analyzing application... This may take 20-30 seconds"

### Step 5: View Results
After 15-30 seconds, the results appear:

```
DECISION PANEL
├─ Decision: ✅ APPROVED (or ❌ REJECTED or ⏳ MANUAL_REVIEW)
├─ Score: XX.X/100
├─ Processing Time: XX.XX seconds
└─ Application ID: [UUID]

REASONING
└─ Detailed text explanation from the AI

AGENT ANALYSES
├─ Document Verification Agent
│  ├─ Score: XX.0/100
│  ├─ Recommendation: Approve/Reject/Review
│  └─ Analysis: [Detailed explanation]
├─ Credit Analysis Agent
├─ Risk Assessment Agent
├─ Compliance Agent
└─ Decision Agent

RISK FLAGS (if any)
└─ • Flag 1
   • Flag 2

COMPLIANCE ISSUES (if any)
└─ • Issue 1
   • Issue 2
```

---

## 🔄 Different Input Scenarios

### Scenario 1: Perfect Applicant (Should be APPROVED)
```
Applicant Information:
├─ First Name: Sarah
├─ Last Name: Williams
├─ Email: sarah@example.com
├─ Phone: 555-0101
├─ Annual Income: $200,000
└─ Years Employed: 12

Credit Profile:
├─ Credit Score: 800
├─ Accounts Open: 6
├─ Delinquencies (30 days): 0
├─ Delinquencies (90 days): 0
├─ Total Debt: $30,000
└─ Recent Inquiries: 0

Document Verification:
├─ Income Confidence: 95%
├─ Employment Confidence: 95%
└─ Documents: W2, Pay stubs, Tax returns

Loan Details:
├─ Loan Amount: $250,000
├─ Purpose: Home
└─ Term: 360 months
```

**Expected Result:** ✅ **APPROVED** (Score: 85-95)

---

### Scenario 2: Borderline Applicant (Should be MANUAL_REVIEW)
```
Applicant Information:
├─ First Name: Michael
├─ Last Name: Brown
├─ Email: michael@example.com
├─ Phone: 555-0202
├─ Annual Income: $85,000
└─ Years Employed: 3

Credit Profile:
├─ Credit Score: 680
├─ Accounts Open: 3
├─ Delinquencies (30 days): 0
├─ Delinquencies (90 days): 1
├─ Total Debt: $38,000
└─ Recent Inquiries: 3

Document Verification:
├─ Income Confidence: 72%
├─ Employment Confidence: 85%
└─ Documents: Pay stubs, Bank statements

Loan Details:
├─ Loan Amount: $250,000
├─ Purpose: Home
└─ Term: 360 months
```

**Expected Result:** ⏳ **MANUAL_REVIEW** (Score: 45-65)

---

### Scenario 3: Risky Applicant (Should be REJECTED)
```
Applicant Information:
├─ First Name: James
├─ Last Name: Davis
├─ Email: james@example.com
├─ Phone: 555-0303
├─ Annual Income: $55,000
└─ Years Employed: 1

Credit Profile:
├─ Credit Score: 580
├─ Accounts Open: 2
├─ Delinquencies (30 days): 2
├─ Delinquencies (90 days): 3
├─ Total Debt: $95,000
├─ Bankruptcy History: Chapter 7 (2015)
└─ Recent Inquiries: 8

Document Verification:
├─ Income Confidence: 45%
├─ Employment Confidence: 50%
└─ Documents: Pay stub only

Loan Details:
├─ Loan Amount: $400,000
├─ Purpose: Home
└─ Term: 360 months
```

**Expected Result:** ❌ **REJECTED** (Score: 25-35)

---

## 📊 View Application History

### After Submitting Multiple Applications

1. Click **"📈 Application History"** in sidebar
2. See summary statistics:
   - Total Applications
   - Approved count
   - Rejected count
   - Manual Review count
3. See decision breakdown chart (pie chart)
4. See all applications in a table:
   ```
   Application ID | Applicant | Decision | Score | Timestamp
   ```

---

## 🔧 System Status Page

### To View System Configuration

1. Click **"🔧 System Status"** in sidebar
2. See three sections:

**Status Indicators:**
```
System Status:      🟢 Operational
API Model:          Claude 3.5 Sonnet
Agents Active:      5
```

**Agent List:**
```
Agent Name | Responsibility | Status
Document Verification | Validates documents | ✅
Credit Analysis | Evaluates credit history | ✅
Risk Assessment | Analyzes loan risk | ✅
Compliance Check | Checks compliance | ✅
Decision Synthesis | Makes final decision | ✅
```

**Decision Thresholds:**
```
Parameter | Value
Approval Threshold | ≥ 75
Rejection Threshold | < 40
Manual Review Range | 40-75
Min Credit Score | 600
Max Debt-to-Income | 43%
Min Income Verification | 80%
Min Employment Verification | 70%
```

---

## 🔌 Understanding the Decision

### What Each Agent Score Means

**Document Verification Agent (0-100):**
- 90-100: Excellent document quality and verification
- 75-89: Good verification with minor concerns
- 60-74: Acceptable but some documents weak
- Below 60: Documentation issues

**Credit Analysis Agent (0-100):**
- 90-100: Excellent credit history
- 75-89: Good credit, few issues
- 60-74: Acceptable credit with concerns
- Below 60: Poor credit history

**Risk Assessment Agent (0-100):**
- 90-100: Low risk, excellent financials
- 75-89: Low-medium risk
- 60-74: Medium risk with concerns
- Below 60: High risk profile

**Compliance Agent (0-100):**
- 90-100: Fully compliant
- 75-89: Compliant with minor flags
- 60-74: Some compliance concerns
- Below 60: Significant compliance issues

---

## 💡 Tips for Using the UI

### Best Practices

1. **Start with defaults** - Click submit with default values to see how it works
2. **Modify one field at a time** - Change credit score, see how decision changes
3. **Try edge cases** - Very high income, very low credit score, etc.
4. **Check history** - See how different inputs produce different decisions
5. **Review reasoning** - Read the AI explanations to understand decisions

### Common Field Changes

| Field | Min | Default | Max | Notes |
|-------|-----|---------|-----|-------|
| Credit Score | 300 | 750 | 850 | Major impact on decision |
| Annual Income | $10k | $150k | $1M | Affects DTI ratio |
| Total Debt | $0 | $45k | $500k | Combined with income = DTI |
| Loan Amount | $10k | $300k | $1M | Must be realistic for income |
| Years Employed | 0 | 8.5 | 50 | Stability indicator |
| Employment Status | - | Employed | - | Options: Employed, Self-employed, Retired |

---

## 🎯 Exploration Ideas

### Try These Input Combinations

1. **High Income, Low Debt:**
   - Annual Income: $300,000
   - Total Debt: $20,000
   - **Result**: Likely APPROVED

2. **Excellent Credit, Moderate Income:**
   - Credit Score: 800
   - Annual Income: $100,000
   - **Result**: Likely APPROVED

3. **Recent Delinquency:**
   - Delinquencies (30 days): 1
   - Recent Inquiries: 5
   - **Result**: Likely MANUAL_REVIEW

4. **Borderline Numbers:**
   - Credit Score: 600 (exactly minimum)
   - Debt-to-Income: 43% (exactly maximum)
   - **Result**: Likely MANUAL_REVIEW

5. **Below Minimums:**
   - Credit Score: 550
   - Annual Income: $40,000
   - Loan Amount: $300,000
   - **Result**: Likely REJECTED

---

## ⌨️ Keyboard Shortcuts

In Streamlit UI:

| Shortcut | Action |
|----------|--------|
| `Tab` | Navigate between form fields |
| `Enter` | Submit form (when submit button focused) |
| `Esc` | Close any open dialogs |
| `Ctrl+L` | Clear browser console |

---

## 🐛 Troubleshooting Input Issues

### Issue: Form not responding
**Solution**: Refresh browser (F5)

### Issue: Can't see all form fields
**Solution**: Scroll down, browser window might be too small

### Issue: Error when submitting
**Solution**: Check all required fields are filled (they should have asterisks *)

### Issue: Takes too long to process
**Solution**: Normal! API calls take 15-30 seconds due to Claude AI processing

### Issue: Application not saved in history
**Solution**: Refresh page, it will be there

---

## 📝 Recording a Demo

### What to Show While Recording

1. **Show Form** (30 seconds)
   - Scroll through all fields
   - Point out default values

2. **Modify Values** (1 minute)
   - Change credit score to 680
   - Change income to $85,000
   - Show it's customizable

3. **Submit** (2 seconds)
   - Click submit button

4. **Wait for Analysis** (20-30 seconds)
   - Show loading indicator
   - Explain what's happening

5. **View Results** (1 minute)
   - Show decision
   - Expand agent sections
   - Point out reasoning

6. **Explore More** (remaining time)
   - Show history
   - Show API docs
   - Submit another application

---

## 🎓 Learning Outcomes

After using the Web UI, you'll understand:

✓ How multi-agent AI systems work
✓ How loan approval decisions are made
✓ What factors influence lending decisions
✓ How to interpret AI agent analysis
✓ How to use REST APIs (via docs)
✓ How to manage application lifecycle

---

## 📞 Getting Help

For issues:
- Check RECORDING_GUIDE.md for recording help
- Check README.md for feature documentation
- Check ARCHITECTURE.md for system design
- Check GETTING_STARTED.md for setup help

---

**Ready to use the Web UI? Visit: http://localhost:8501** 🚀
