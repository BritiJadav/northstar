# NorthStar General Insurance | Commercial Lines Intake & Triage Gateway
### Lead Forward Deployed Engineer (FDE) Production Capstone (Case 06)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.6+-e92063.svg)](https://docs.pydantic.dev/)
[![GCP Cloud Run](https://img.shields.io/badge/GCP-Cloud_Run_(asia--south1)-4285F4.svg)](https://cloud.google.com/run)
[![Tests Passing](https://img.shields.io/badge/tests-7%20passed-brightgreen.svg)]()

---

## 1. Executive Problem & Solution Summary
- **The Problem:** NorthStar receives ~9,000 broker submissions/month for SME property policies. Median quote turnaround is **6 working days**, leading to a low **11% win rate**. A 60-person team in Pune spends 70 minutes manually keying *every* file, even though **45% are outside appetite** and **18% are duplicate submissions**.
- **The Misdirected Customer Ask:** *"Build an AI that reads broker emails and generates the quotes automatically."*
- **The Lead FDE First Valuable Slice (FVS):** We consciously **reject automated quoting** due to IRDAI File-and-Use compliance, client AI policy restrictions (assistive pricing only), Excel actuarial rating models, and CUO loss-ratio concerns. Instead, our First Valuable Slice automates **Email Ingestion, Deterministic Appetite Triage, Multi-Broker Clearance, SOV Version Diffing, and Pre-filled Underwriting Cockpit staging**, while underwriters retain pricing sign-off.

---

## 2. Architecture & Estate Mapping
The system designs into NorthStar's nine existing systems (PDF p. 20):
1. **Regional Inboxes:** Non-intrusive asynchronous email ingestion via Graph/IMAP.
2. **SharePoint Document Store:** Standardized UUID folder taxonomy.
3. **Vendor SaaS Policy Admin:** Pre-filled staging payload exports (bypasses quarterly release windows).
4. **Actuarial Excel Rating:** Macro parameter bridge for property risks.
5. **AI Gateway:** In-region India LLM endpoint (`asia-south1`) with audit logging.
6. **Security & Governance:** Indirect prompt injection scanner and DPDP Act 2023 PII maskers.

---

## 3. Quickstart Guide (Local Development in VS Code)

### Prerequisites
- Python 3.11 or higher
- Git
- VS Code (Recommended extensions: Python, Pylance, Thunder Client)

### Installation
```bash
# 1. Clone repository & navigate to project root
cd C:\Users\v69-labuser449619\Desktop\Northstar

# 2. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run automated test suite
python -m pytest tests/test_pipeline.py -v
```

### Running the Application
```bash
# Start FastAPI server with live reloading
uvicorn app.main:app --reload --port 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser to access the **Interactive Underwriting Cockpit**.

---

## 4. Evaluator Scenario Demonstrations
In the web cockpit, use the quick scenario buttons to test:
1. **Clean Eligible Risk:** Light Engineering SME risk triaged and routed for underwriting sign-off.
2. **Prohibited Occupancy:** Fireworks & explosives flagged immediately; auto-drafts decline email; saves 70 min Pune keying.
3. **Multi-Broker Duplicate:** Competing broker submits same unit; detected via composite entity clearance.
4. **Prompt Injection Attack:** Adversarial instructions embedded in broker PDF neutralized and quarantined.
5. **Mid-Stream SOV Diff:** Revised Excel schedule analyzed; visual diff highlights updated rows.
6. **Risk Engineering Referral:** High-hazard plastics manufacturing auto-referred (reflecting the 12% case cohort).

---

## 5. Google Cloud Platform (GCP) Deployment

### Target Architecture in GCP
- **Cloud Run:** Serverless container hosting the FastAPI intake service.
- **Vertex AI:** `asia-south1` (Mumbai) Gemini endpoint for in-region compliance.
- **Cloud Storage:** Secure bucket for broker attachments with CMEK encryption.
- **Cloud Build:** Automated CI/CD pipeline executing unit tests before container deployment.

### Deploying via Cloud Build
```bash
# Set your GCP Project ID
gcloud config set project <YOUR_GCP_PROJECT_ID>
gcloud config set run/region asia-south1

# Submit build and deploy to Cloud Run
gcloud builds submit --config=deploy/cloudbuild.yaml .
```
