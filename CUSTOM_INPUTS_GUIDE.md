# 📝 Custom Inputs Guide - Your Application Parameters

## Your Input Parameters

Based on what you specified, here's how to enter YOUR data into the system:

### Required Input Fields

```
• Applicant ID              - Unique identifier
• Applicant Profile
  ├─ Age                    - Date of birth
  ├─ Income                 - Annual income
  └─ Employment Type        - Employed/Self-employed/etc
• Credit Score              - 300-850
• Loan Amount & Tenure      - Amount & months
• Existing Liabilities      - Total debt
• Location                  - City/State/ZIP
• Application Timestamp     - Auto-generated
```

---

## How to Enter YOUR Data into the System

### Option 1: Use Web UI (Easiest)

**Step 1:** Open http://localhost:8501

**Step 2:** Click "📋 Submit Application"

**Step 3:** Fill in YOUR values:

```
👤 APPLICANT INFORMATION
├─ Applicant ID:       [Your ID or leave blank]
├─ First Name:         [Your first name]
├─ Last Name:          [Your last name]
├─ Email:              [Your email]
├─ Phone:              [Your phone]
├─ Date of Birth:      [Your age/DOB]
├─ SSN (Last 4):       [Last 4 digits]
├─ Annual Income:      [Your income]
├─ Employment Type:    [Select: Employed/Self-employed/etc]
├─ Years Employed:     [Your years]
└─ Current Employer:   [Your employer name]

💰 LOAN DETAILS
├─ Loan Amount:        [Your loan amount]
├─ Tenure (months):    [Your loan term]
├─ Purpose:            [Home/Auto/Personal/Business]
└─ Interest Rate:      [Requested rate - optional]

📊 CREDIT PROFILE
├─ Credit Score:       [Your credit score]
├─ Total Debt:         [Your total liabilities]
├─ Accounts Open:      [Number of accounts]
└─ Delinquencies:      [Any delinquencies?]

📍 LOCATION
└─ Location:           [You can add as employer info]

⏰ APPLICATION TIMESTAMP
└─ Auto-generated      [System fills this automatically]
```

**Step 4:** Click "🚀 Submit Application & Analyze"

**Step 5:** Wait 15-30 seconds

**Step 6:** See YOUR results!

---

## Example: How to Fill in YOUR Specific Data

### Example 1: Employee with Good Credit

```
Applicant Profile:
  Name:           Alice Johnson
  Age:            35 years old (DOB: 1989-06-15)
  Income:         $120,000 per year
  Employment:     Employed at Tech Company
  Years Employed: 7 years

Credit Profile:
  Credit Score:   745
  Total Debt:     $35,000
  Accounts:       5
  Delinquencies:  None

Loan Details:
  Loan Amount:    $250,000
  Tenure:         360 months (30 years)
  Purpose:        Home purchase
  Location:       San Francisco, CA

Timestamp:        Auto-generated (today's date)
```

**In the Web Form:**
- First Name: Alice
- Last Name: Johnson
- Annual Income: 120000
- Employment Type: Employed
- Years Employed: 7
- Credit Score: 745
- Total Debt: 35000
- Loan Amount: 250000
- Loan Term: 360 months
- Loan Purpose: Home

---

### Example 2: Self-Employed with Moderate Credit

```
Applicant Profile:
  Name:           Bob Smith
  Age:            42 years old
  Income:         $95,000 per year
  Employment:     Self-employed (Consultant)
  Years Employed: 8 years

Credit Profile:
  Credit Score:   680
  Total Debt:     $42,000
  Accounts:       4
  Delinquencies:  1 (past 90 days)

Loan Details:
  Loan Amount:    $200,000
  Tenure:         360 months
  Purpose:        Home purchase
  Location:       Austin, TX
```

**In the Web Form:**
- First Name: Bob
- Last Name: Smith
- Annual Income: 95000
- Employment Type: Self-employed
- Years Employed: 8
- Current Employer: Self-employed Consultant
- Credit Score: 680
- Total Debt: 42000
- Loan Amount: 200000

---

## Mapping Your Input Fields to Web Form

| Your Parameter | Web Form Field | Notes |
|---|---|---|
| Applicant ID | (Auto-generated) | System creates ID automatically |
| Age | Date of Birth | Pick date from calendar |
| Income | Annual Income | Enter as number (e.g., 120000) |
| Employment Type | Employment Status | Select from dropdown |
| Credit Score | Credit Score | Enter 300-850 |
| Loan Amount | Loan Amount | Enter as number |
| Tenure/Months | Loan Term (months) | Slider or text input |
| Existing Liabilities | Total Debt | Enter your total debt |
| Location | Current Employer info | Can add location context here |
| Timestamp | (Auto-generated) | System fills with current date/time |

---

## How to Submit Multiple Applications with Different Data

**Scenario:** You want to test how different income levels affect decisions

1. First Application:
   ```
   Income: $150,000
   Credit: 750
   Debt: $45,000
   ```
   - Submit → See results → Should be APPROVED

2. Second Application:
   ```
   Income: $85,000
   Credit: 750 (same)
   Debt: $45,000 (same)
   ```
   - Submit → See results → Different decision due to income change
   - Notice how lower income changes the decision

3. Third Application:
   ```
   Income: $85,000
   Credit: 680 (lower)
   Debt: $45,000
   ```
   - Submit → See results → Even more conservative decision

**In the Web UI:**
1. Fill Application 1 → Submit → View Results
2. Click "📋 Submit Application" again
3. Fill Application 2 → Submit → View Results
4. Go to "📈 Application History" to see all 3 decisions side-by-side

---

## Batch Testing Your Scenarios

### Test Plan Template

Create a test plan with YOUR specific data:

```
TEST SCENARIO 1: Current Situation
├─ Income:           $________
├─ Credit Score:     _________
├─ Total Debt:       $________
├─ Employment:       _______________
├─ Years Employed:   _________
├─ Loan Amount:      $________
├─ Loan Term:        _____ months
└─ Expected Result:  __________________

TEST SCENARIO 2: Improvement Scenario
├─ Income:           $________ (increased)
├─ Credit Score:     _________ (improved)
├─ Total Debt:       $________ (reduced)
└─ Expected Result:  __________________

TEST SCENARIO 3: Worst Case
├─ Income:           $________ (decreased)
├─ Credit Score:     _________ (lowered)
├─ Total Debt:       $________ (increased)
└─ Expected Result:  __________________
```

---

## Data Entry Tips

### Best Practices

1. **Income Field**
   - Enter as whole number (no commas)
   - Example: 150000 (not 150,000)
   - Annual income only

2. **Credit Score**
   - Must be 300-850
   - Typically valid range: 600-800

3. **Debt Field**
   - Enter as whole number
   - Include all liabilities (credit cards, loans, mortgages)
   - Example: 45000 (not $45,000)

4. **Loan Term**
   - Standard mortgage: 360 months (30 years)
   - Short term: 180 months (15 years)
   - Auto loan: 36-72 months

5. **Employment Years**
   - Enter decimal if needed (e.g., 8.5)
   - 0 = newly employed
   - 5+ = demonstrates stability

6. **Date of Birth**
   - Click calendar icon
   - System calculates age from DOB

---

## Recording Your Test with Custom Data

### Step-by-Step Demo

1. Start recording: `./auto_record_ffmpeg.sh`
2. Open http://localhost:8501
3. Enter YOUR data in the form
4. Submit
5. Show results
6. Enter different data
7. Show how different inputs = different decisions
8. Press 'q' to save video

---

## Import from CSV or File

### If you have multiple applicants:

**Option A:** Create test data file

```
Create: applicants.csv

Format:
Name, Income, CreditScore, Debt, LoanAmount, Employment
Alice, 120000, 745, 35000, 250000, Employed
Bob, 95000, 680, 42000, 200000, Self-employed
Charlie, 75000, 620, 50000, 200000, Employed
```

Then submit each one manually via the web UI.

**Option B:** Use Python script

```python
import csv
from models import LoanApplication, ApplicantInfo
from orchestrator import LoanOrchestrator

orchestrator = LoanOrchestrator()

with open('applicants.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Create application from row
        app = LoanApplication(
            applicant_info=ApplicantInfo(
                first_name=row['Name'].split()[0],
                last_name=row['Name'].split()[1],
                annual_income=float(row['Income']),
                # ... other fields
            ),
            # ... other details
        )
        # Analyze
        result = orchestrator.analyze_application(app)
        print(f"{row['Name']}: {result.final_decision}")
```

---

## Viewing Your Results

### After Submission:

1. **Immediate View**
   - Decision score
   - Decision type (APPROVED/REJECTED/MANUAL_REVIEW)
   - Agent reasoning

2. **Go to "📊 View Results"**
   - See your latest application
   - Full agent analysis

3. **Go to "📈 Application History"**
   - See ALL your submissions
   - Compare decisions
   - View statistics

---

## Understanding YOUR Decision

When you submit YOUR data, you'll get:

```
DECISION:
  ✅ APPROVED      = Your application meets all criteria
  ❌ REJECTED      = Your application has critical issues
  ⏳ MANUAL_REVIEW = Your application needs human review

SCORE: 0-100
  90-100 = Excellent
  75-89  = Good approval
  60-74  = Medium concern
  40-59  = Likely rejection
  0-39   = Strong rejection

FACTORS CONSIDERED:
  • Your credit score vs threshold (600)
  • Your debt-to-income ratio vs limit (43%)
  • Your income stability (years employed)
  • Your document verification
  • Your compliance status
  • Recent delinquencies
```

---

## Troubleshooting Your Data Entry

### Problem: "Invalid entry"
**Solution:** Check format
- Income: Number only (e.g., 120000)
- Credit: 300-850
- Debt: Number only (e.g., 35000)

### Problem: "Required field missing"
**Solution:** Fill all fields with asterisk (*)
- Fields marked with * are required
- Use 0 for "none" if needed

### Problem: "Can't see all form fields"
**Solution:** Scroll down
- Form is long
- Scroll to see all sections

### Problem: Different result than expected
**Solution:** Check calculations
- Your DTI = Total Debt ÷ Annual Income
- If DTI > 43%, expect challenges
- If Credit < 600, expect rejection

---

## Next Steps

1. **Prepare YOUR Data**
   - Gather your financial information
   - Write down your numbers

2. **Open Web UI**
   - Go to http://localhost:8501
   - Click "📋 Submit Application"

3. **Enter YOUR Data**
   - Fill in each field
   - Double-check values

4. **Submit**
   - Click "🚀 Submit Application & Analyze"

5. **Review Results**
   - See YOUR decision
   - Understand the reasoning

6. **Test Scenarios** (Optional)
   - Submit different variations
   - See how changes affect decisions
   - Build intuition

---

## Quick Checklist for YOUR Data

Before clicking Submit:

- [ ] First Name: _____________
- [ ] Last Name: _____________
- [ ] Email: _____________
- [ ] Annual Income: $__________
- [ ] Employment Type: __________
- [ ] Years Employed: __________
- [ ] Credit Score: ___________
- [ ] Total Debt: $__________
- [ ] Loan Amount: $__________
- [ ] Loan Term: _____ months
- [ ] All fields filled? ✓

---

**Ready to enter YOUR data? Visit: http://localhost:8501** 🚀
