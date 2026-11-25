# NorthStar General Insurance — Production Operations Run Book
### Mandatory Capstone Submission Deliverable (Virtusa Assessment Pack, Page 2)

**System Name:** NorthStar Intelligent Ingestion, Triage & Clearance Gateway  
**Environment:** Google Cloud Platform (Cloud Run, `asia-south1` Mumbai)  
**Public Evaluation URL:** `https://development-appeared-throughout-gentleman.trycloudflare.com`  
**Direct GCP Cloud Run URL:** `https://northstar-intake-service-230261472273.asia-south1.run.app`  
**Container Image:** `asia-south1-docker.pkg.dev/slabspro-slabsuser41/cloud-run-source-deploy/northstar-intake-service:v1`  
**Active Revision:** `northstar-intake-service-00001-kfc` (100% traffic)  
**Classification:** Mission-Critical Commercial Underwriting Support System (Assistive Tier 1)  
**Document Owner:** Member 4 (Security, Risk & Governance Lead) & Member 5 (Delivery Lead)

---

## 1. Named Post-Go-Live Operational Ownership

In accordance with enterprise governance requirements (PDF p. 2), the system has single-point named post-go-live accountability:

| Operational Role | Named Owner | Corporate Title & Department | Contact / Escalation Channel | Primary Responsibilities |
| :--- | :--- | :--- | :--- | :--- |
| **Business Outcome Owner** | **Ashok Menon** | Head of Commercial Lines | `ashok.menon@northstar.co.in` | Overall GWP growth, commercial win rate, broker SLA satisfaction, pilot expansion sign-off. |
| **Operational Process Owner**| **Sunil Kulkarni** | Head of Underwriting Operations (Pune) | `sunil.kulkarni@northstar.co.in`| Pune exception queue SLAs, staff transition & upskilling, daily clearance conflict resolution. |
| **Underwriting Risk Gatekeeper**| **Dr. Rajeshwar Rao**| Chief Underwriting Officer (CUO) | `cuo.desk@northstar.co.in` | Board-approved appetite rules, tariff occupancy codes, Authority Matrix enforcement, loss ratio audit. |
| **Platform & Security Owner**| **Ananya Sharma** | Head of Enterprise Architecture & AI Gateway | `ananya.sharma@northstar.co.in` | In-region gateway uptime (`asia-south1`), Secret Manager keys, prompt version control, DPDP compliance. |

---

## 2. Operational Controls & Safety Kill Switches

The platform enforces three hardware and software kill switches:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        NORTHSTAR OPERATIONAL CONTROL GATES                             │
├──────────────────────────┬─────────────────────────────┬───────────────────────────────┤
│ Control Gate 1:          │ Control Gate 2:             │ Control Gate 3:               │
│ PIPELINE EMERGENCY KILL  │ GATEWAY FALLBACK BREAKER    │ AUTHORITY MATRIX HARD STOP    │
│ Instantly halts auto-    │ Trips after 3 failed LLM    │ Prevents staging quotes where │
│ processing; all inbound  │ calls; auto-routes files to │ premium > underwriter limit   │
│ files divert to Pune Ops │ Assisted Manual Queue with  │ without dual senior approval  │
│ manual mailboxes.        │ raw attachments intact.     │ (L2 / CUO sign-off enforced). │
└──────────────────────────┴─────────────────────────────┴───────────────────────────────┘
```

### Emergency Kill Switch Activation
- **Trigger Condition:** Severe model drift, extraction hallucinations, or active adversarial security campaign.
- **Execution:** Set environment variable in Cloud Run or secret manager:
  ```bash
  gcloud run services update northstar-intake-service \
    --region=asia-south1 \
    --update-env-vars=EMERGENCY_PIPELINE_BYPASS=true
  ```
- **Fallback Behavior:** All incoming emails are routed directly to Pune operations regional Outlook queues with zero automated decline emails sent.

---

## 3. Monitoring Signals & Telemetry Alerts

The system exports OpenTelemetry metrics and structured logs to **Google Cloud Monitoring** in Mumbai:

| Telemetry Signal | Metric / Log Query | Healthy Baseline | Warning Threshold | Critical Incident Action |
| :--- | :--- | :---: | :---: | :--- |
| **Extraction Confidence** | `avg(provenance.confidence_score)` | $\ge 94\%$ | $< 85\%$ | Investigate dirty OCR scan or novel broker format. |
| **End-to-End Latency** | `p95(intake_duration_seconds)` | $< 25\text{ s}$ | $> 45\text{ s}$ | Scale Cloud Run container concurrency; check gateway throttling. |
| **Out-of-Appetite Rate** | `ratio(status == 'DECLINED')` | $42\% - 48\%$ | $> 55\%$ | Potential rule misconfiguration; audit recent tariff updates. |
| **Duplicate Clearance Rate** | `ratio(is_duplicate == true)` | $15\% - 20\%$ | $> 30\%$ | Check for broker spam campaign or entity normalization bug. |
| **Prompt Injection Detections** | `count(SECURITY_QUARANTINE)` | $0\text{ / day}$ | $\ge 1\text{ / day}$ | Security alert sent to InfoSec; IP and broker email blacklisted. |
| **Underwriter Override Rate** | `ratio(field_overridden_by_uw)` | $< 8\%$ | $> 15\%$ | Indicates prompt degradation or formatting change; retrain extractor. |

---

## 4. Production Rollout & Transition Steps

Our enterprise rollout follows a 3-stage phased gate:

### Phase 1: Western Region Shadow Pilot (Weeks 1 to 8)
1. **Target:** Pune and Mumbai regional shared mailboxes (~3,500 submissions/month).
2. **Mode:** Shadow execution. Pipeline runs in parallel with Pune human data entry.
3. **Exit Gate:** 30 consecutive days of zero false declines on appetite triage; extraction precision $\ge 95\%$; underwriter satisfaction score $\ge 85\%$.

### Phase 2: Southern Region Expansion (Weeks 9 to 14)
1. **Target:** Bangalore, Chennai, and Hyderabad regional mailboxes (~3,000 submissions/month).
2. **Mode:** Active assistive execution. Pune staff transition from keying to exception handling.
3. **Exit Gate:** Turnaround time cuts from 6 days to $< 48$ hours on 90% of eligible files.

### Phase 3: Northern & Eastern Enterprise Scale (Weeks 15 to 20)
1. **Target:** Full national volume across all 9,000 monthly submissions.
2. **Mode:** Full enterprise scale. Formal quarterly review by CUO and Actuarial committee.

---

## 5. Standard Operating Procedures (SOPs) for Incident Response

### SOP-01: AI Gateway Outage / 503 Throttling
1. Cloud Run circuit breaker trips after 3 consecutive 503 errors.
2. Status set to `GATEWAY_FALLBACK`.
3. Notifications dispatched to Pune Ops Team Lead and Platform Owner.
4. Raw submissions queued in Cloud Storage; processing resumes automatically when gateway recovers.

### SOP-02: Multi-Broker Clearance Dispute
1. When Broker B submits a risk already quoted to Broker A within 15 days, status triggers `DUPLICATE_FLAGGED`.
2. Assigned Tier 2 Pune clearance coordinator reviews submission timestamps.
3. As per NorthStar commercial policy: first broker with completed submission package retains exclusive quoting rights for 7 business days. Broker B is notified with polite hold letter.
