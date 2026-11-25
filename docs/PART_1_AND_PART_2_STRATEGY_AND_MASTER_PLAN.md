# NorthStar General Insurance — Capstone Strategy & Master Execution Plan
## Lead Forward Deployed Engineer (FDE) Playbook & Technical Blueprint

**Author:** Antigravity (Principal FDE, Enterprise AI Architect & Domain Mentor)  
**Target:** Five-Member Capstone Team (Virtusa AI Academy & StackRoute Lead FDE Program)  
**Primary Source:** Virtusa LeadFDE Cases.pdf (Case 06: Northstar General Insurance, Pages 19–21; General Instructions, Pages 1–3)  
**Target Score:** 90+ / 100 (Optimized against the official 9-criterion, 3-block Rubric)

---

# EXECUTIVE BRIEFING & FDE MINDSET ORIENTATION

As Lead Forward Deployed Engineers, our job is not to build what the customer reflexively asks for, but to discover the genuine operational bottleneck, align conflicting executive stakeholders, and deliver the smallest production-grade, risk-governed slice that demonstrably moves the business needle.

At NorthStar General Insurance, the commercial sponsor (Ashok Menon, Head of Commercial Lines) states:
> *"Build an AI that reads the broker emails and generates the quotes automatically."* (PDF p. 19)

If a team blindly complies with this ask and builds an autonomous quoting agent, **they will fail the evaluation.**
Why? Because the official case rubric (PDF p. 19–21) deliberately tests whether the team recognizes:
1. **The Real Bottleneck:** Out of 9,000 monthly submissions, **45% are outside underwriting appetite** and **18% are duplicates**, yet Pune operations spends 70 minutes manually keying *every single one* before decline. The 6-day turnaround delay is 95% queueing and manual keying friction, not pricing calculation time.
2. **The Regulatory & Policy Blockers:** NorthStar's internal AI policy strictly limits AI to **assistive use for pricing** (no automated quote issuance approved; PDF p. 20). Furthermore, under IRDAI File-and-Use regulations, commercial property premiums must strictly conform to filed rating schedules, and underwriting authority matrices dictate who can bind risk.
3. **The Stakeholder Landmine:** The Chief Underwriting Officer (CUO) is terrified that quoting faster via autonomous AI will worsen the **68% property loss ratio** through reckless risk selection (PDF p. 19). Meanwhile, the Head of Distribution has promised brokers **"no new portals"** after an earlier portal failed with only 8% adoption (PDF p. 20).
4. **The Enterprise Integration Reality:** Property rating for larger risks resides in **actuarial Excel models**, while the commercial lines core policy administration SaaS has a **limited quote API** and quarterly release windows (PDF p. 20).

Therefore, our **First Valuable Slice (FVS)** is:
**"Intelligent Email Ingestion, Appetite Triage, Duplicate Clearance & Pre-Filled Underwriting Package with Human-in-the-Loop Cockpit."** We consciously defer automated pricing and auto-quote issuance.

---

# PART 1: CASE ANALYSIS

```
========================================================================================
PART 1: CASE ANALYSIS — DISCOVERY, PROBLEM FRAMING & STRATEGIC SLICING
========================================================================================
```

### 1.1 Executive Case Summary
NorthStar General Insurance is an Indian general insurance company writing SME property and package policies exclusively through broker networks. 
- **The Market Opportunity & Commercial Pain:** NorthStar receives approximately 9,000 submissions per month via broker emails. In commercial SME insurance, speed is the primary competitive moat: brokers place business with whoever quotes first, and a quote delivered within 48 hours routinely wins the account. However, NorthStar’s current median quote turnaround is **6 working days** (144+ hours). As a consequence, NorthStar wins only **11%** of quoted business (PDF p. 19).
- **The Operational Trap:** Submissions arrive across ~30 disparate broker formats (unstructured emails, complex Excel Schedules of Values [SOV], scanned proposal forms, and loss histories). A 60-person Business Process Operations team in Pune manually reviews and keys every submission into the policy administration system, taking **70 minutes per submission**. 
- **The Fatal Flaw in Current Operations:** 
  - **45% (4,050 submissions/month)** fall completely outside NorthStar’s underwriting appetite, yet they are keyed in full before an underwriter ever sees them to reject them.
  - **18% (1,620 submissions/month)** are duplicate submissions (the same insured risk submitted simultaneously by multiple brokers fishing for terms).
  - Together, **63% of Pune’s manual data entry capacity (~6,600 operational hours per month)** is squandered keying junk or duplicate submissions.
- **The Underwriter Capacity Squeeze:** NorthStar employs 35 commercial underwriters who spend **40% of their bandwidth on small policies (premium < ₹2 lakh)**. High-value, profitable commercial risks sit idling in queues.
- **The Governance & Quality Barrier:** The property loss ratio is already elevated at **68%**. The CUO opposes autonomous quoting, fearing adverse selection. The IT landscape is fragmented with Excel actuarial rating sheets, quarterly SaaS release cycles, and mandatory in-region AI gateway compliance.

---

### 1.2 Information Classification: Confirmed Facts vs. Assumptions vs. Open Questions

To demonstrate rigorous consulting discipline, every piece of case information is categorized and cited.

#### A. Confirmed Facts (Explicitly Verified in Virtusa Assessment Pack)
| Fact ID | Confirmed Fact Statement | PDF Source Citation | Business / Architectural Impact |
| :--- | :--- | :--- | :--- |
| **CF-01** | NorthStar receives ~9,000 SME property/package submissions per month via email. | PDF Page 19, Sec. 1 | Inflow scale: ~300 submissions/day, requiring scalable batch/event intake. |
| **CF-02** | Median turnaround time to quote is 6 working days; brokers state <48 hours wins. | PDF Page 19, Sec. 1 | Core business metric to move; 6 days vs. 48 hours is a 3x speed gap. |
| **CF-03** | NorthStar's current quote-to-win rate is 11%. | PDF Page 19, Sec. 1 | Commercial baseline; each 1% win-rate gain drives significant gross written premium (GWP). |
| **CF-04** | ~45% of submissions are outside underwriting appetite but are keyed in full before decline. | PDF Page 19, Sec. 1 | Massive operational waste: 4,050 submissions/month × 70 min = 4,725 wasted hours/mo. |
| **CF-05** | ~18% of submissions are duplicates (same risk arriving via multiple brokers). | PDF Page 19, Sec. 1 | 1,620 submissions/mo × 70 min = 1,890 wasted hours/mo; causes channel conflict. |
| **CF-06** | Manual data entry takes ~70 minutes per submission, handled by 60 people in Pune. | PDF Page 19, Sec. 1 | Operations baseline: 9,000 × 70 min = 10,500 hours/month across 60 FTEs. |
| **CF-07** | Submissions arrive in ~30 broker formats: Excel SOVs, PDFs, and scanned forms. | PDF Page 19, Sec. 1 | Technical requirement: Multi-modal document parsing & table extraction required. |
| **CF-08** | 35 underwriters spend ~40% of their time on small risks under ₹2 lakh premium. | PDF Page 19, Sec. 1 | Underwriter capacity drain: 14 FTE-equivalents tied up in low-margin policy intake. |
| **CF-09** | Property loss ratio is 68%; CUO fears speed will worsen risk selection. | PDF Page 19, Sec. 1 | Hard risk gate: Any AI acceleration must enforce strict risk governance and auditability. |
| **CF-10** | 12% of submissions require risk-engineering referral, adding ~4 days. | PDF Page 19, Sec. 1 | Critical triage flag: High-hazard occupancies must be identified immediately. |
| **CF-11** | Brokers often send updated schedules mid-way, restarting extraction and pricing. | PDF Page 19, Sec. 1 | Architecture requirement: Document versioning, delta diffing, and thread tracking. |
| **CF-12** | Client Tech Landscape: Policy admin is vendor SaaS (quarterly releases, limited quote API); Excel actuarial rating for property; rating API for package only; regional email mailboxes; SharePoint document store with no consistent naming; Broker portal has 8% adoption; CRM updated by hand; monthly claims data; per-call licensed geocoding/CAT data; mandatory in-region AI Gateway with logging. | PDF Page 20, Sec. 2 | Must design into existing estate. Cannot rely on SaaS quote API or force portal usage. |
| **CF-13** | Governance: IRDAI file-and-use compliance; Underwriting Authority Matrix; DPDP Act 2023; AI policy permits assistive pricing only (no automated quotes); mandatory audit trail (data, rate, authority); Distribution head promised "no new portals". | PDF Page 20, Sec. 2 | Boundary conditions: Underwriters must retain pricing sign-off; no new broker portal UI. |

#### B. Working Assumptions (Reasonable Inferences Requiring Validation)
| Assumption ID | Working Assumption Statement | Underlying Rationale | Risk if Assumption is Wrong |
| :--- | :--- | :--- | :--- |
| **WA-01** | Broker emails arrive via standard Microsoft Exchange / Microsoft 365 shared mailboxes. | Standard corporate stack in Indian BFSI; regional mailboxes explicitly mentioned. | Low: Ingestion adapters can easily support IMAP/Graph API or webhook listeners. |
| **WA-02** | Average SME property premium is ~₹1.25 Lakh for small risks and ~₹4.5 Lakh across the blended portfolio. | Inferred from case context ("small risks under ₹2 lakh premium" consuming 40% underwriter time). | Medium: Affects commercial ROI modeling; modeled with sensitivity bands. |
| **WA-03** | Appetite rules are documented in underwriter rulebooks (e.g., occupancy classification, minimum sum insured, hazardous occupancy exclusions like fireworks, chemical storage). | Indian property underwriting is governed by standard tariff occupancies (IIB/TAC legacy classifications). | Low: Prototype will implement representative standard Indian occupancy rules. |
| **WA-04** | A duplicate risk is identifiable by a composite key: Insured Legal Name / PAN / GSTIN + Property Pin Code / Address + Policy Period. | Standard commercial insurance clearance practice in India. | Medium: Variations in broker spellings require fuzzy string matching and phonetic algorithms. |
| **WA-05** | Pune data entry team salary averages ~₹35,000 – ₹45,000/month fully loaded cost per agent. | Standard BPO/shared-service operational benchmark in Pune, Maharashtra. | Low: Affects operational cost savings; conservative figures will be used. |

#### C. Deliberately Left Open Questions (Requiring Stakeholder Discovery)
| Question ID | Open Question from Case Brief | PDF Source | Evaluator / Stakeholder Angle |
| :--- | :--- | :--- | :--- |
| **OQ-01** | Win rate vs. speed vs. loss ratio: which metric wins when they conflict? | PDF Page 19, Sec. 1 | Core executive tension between Commercial Head (win rate), Ops (speed), and CUO (loss ratio). |
| **OQ-02** | Can out-of-appetite submissions be declined immediately and automatically via email? | PDF Page 19, Sec. 1 | Distribution vs. Underwriting: Will brokers be alienated if an automated decline email is sent? |
| **OQ-03** | Can small, clean risks (<₹2L premium) be straight-through quoted without underwriter touch? | PDF Page 19, Sec. 1 | Directly tests AI policy boundaries and IRDAI authority delegation. |
| **OQ-04** | Should NorthStar continue accepting broker emails or attempt to enforce broker portal adoption? | PDF Page 20, Sec. 1 | Tests awareness of Distribution Head's "no new portals" promise and broker power dynamics. |
| **OQ-05** | Who owns the end-to-end outcome — Commercial Lines, Operations, or Distribution? | PDF Page 20, Sec. 1 | Critical organizational governance question for long-term project sponsorship and RACI. |

---

### 1.3 Business Problems and Deep Root-Cause Analysis

#### The 5 Whys Analysis of Turnaround Delay
Why does it take 6 working days (144 hours) to return an SME property quote?
1. **Why 1:** Because underwriters receive completed submission packages 4 to 5 days after the broker emails them.
2. **Why 2:** Because the 60-person Pune operations team has a massive backlog and takes 70 minutes of manual data entry per submission.
3. **Why 3:** Because Pune keys *all 9,000 submissions*, including the 45% (4,050) that fall outside underwriting appetite and the 18% (1,620) that are duplicate submissions from competing brokers.
4. **Why 4:** Because intake triage and clearance are currently positioned *after* full data entry instead of at the ingestion gate.
5. **Why 5 (Root Cause):** **NorthStar lacks an automated ingestion and triage gate to parse unstructured multi-format broker emails, match duplicates, evaluate appetite rules, and generate pre-filled underwriting packages before human operations touch the file.**

#### The As-Is Workflow Bottleneck Analysis
```mermaid
flowchart TD
    subgraph Current_As_Is["CURRENT AS-IS WORKFLOW: 6 Working Days Median (11% Win Rate)"]
        A[Broker Emails Submission<br/>~9,000 / month across 30 formats] --> B[Regional Shared Inbox<br/>Queueing Delay: 24-48 hrs]
        B --> C[Pune Ops Data Entry<br/>60 FTEs · 70 min/submission<br/>Total: 10,500 hrs/month]
        C --> D{Appetite Triage<br/>& Clearance}
        D -- "45% Out of Appetite" --> E[Decline Notice Sent<br/>4,725 hrs of data entry WASTED]
        D -- "18% Duplicates" --> F[Duplicate Discarded<br/>1,890 hrs of data entry WASTED]
        D -- "37% Clean Submissions<br/>(~3,330/mo)" --> G{Risk Engg Referral?<br/>12% of cases}
        G -- Yes --> H[Risk Engineering Inspection<br/>Adds +4 Working Days]
        G -- No --> I[Underwriter Manual Pricing<br/>Actuarial Excel / SaaS API]
        H --> I
        I --> J[Underwriter Review & Sign-off<br/>35 UWs spend 40% time on <₹2L risks]
        J --> K[Quote Issued to Broker<br/>Total Elapsed Time: 6 Working Days]
    end
```

**Quantitative Evidence of Waste:**
- Total Monthly Submissions: **9,000**
- Total Keying Time Spent: $9,000 \times 70\text{ min} = 630,000\text{ min} = \mathbf{10,500\text{ hours/month}}$
- Out-of-Appetite Waste: $45\% \times 10,500\text{ hrs} = \mathbf{4,725\text{ hours/month}}$ squandered on risks NorthStar will never write.
- Duplicate Submission Waste: $18\% \times 10,500\text{ hrs} = \mathbf{1,890\text{ hours/month}}$ squandered on duplicate broker entries.
- Mid-Term Schedule Update Rework: When brokers submit revised SOVs mid-way, Pune restarts keying from scratch, adding another 70 minutes per revision.
- **The Core Paradox:** The Commercial Head asked for *automated pricing AI*, but **pricing takes only 15–20 minutes of underwriter time**. The remaining **5.8 days of latency are trapped in mailbox queues, duplicate processing, and keying junk data.**

---

### 1.4 Hidden Stakeholder Conflicts & Discovery Strategy

In enterprise FDE consulting, technical excellence fails if political and organizational landmines are ignored. Four distinct stakeholders hold conflicting agendas:

```mermaid
graph LR
    subgraph Conflicting_Stakeholder_Priorities["NorthStar Stakeholder Landscape & Tensions"]
        AM["Ashok Menon<br/>Head of Commercial Lines<br/>Goal: Maximize Win Rate & GWP<br/>Ask: 'Automate Quotes with AI'"]
        CUO["Chief Underwriting Officer<br/>Goal: Control Loss Ratio (68%)<br/>Fear: AI will write bad risks"]
        DH["Head of Distribution<br/>Goal: Broker Relationships<br/>Promise: 'No New Portals'"]
        OPS["Pune Ops & Team Leads<br/>Goal: SLA Adherence & Job Security<br/>Fear: AI replacement & re-keying errors"]
    end
    AM <-->|Conflict: Speed vs Loss Ratio| CUO
    AM <-->|Conflict: Email vs Portal| DH
    OPS <-->|Conflict: Automation vs Headcount| AM
```

#### Stakeholder Discovery Profiles & Objection Handling Guide
1. **Ashok Menon (Head of Commercial Lines — Sponsor):**
   - *Motivation:* Wants to hit aggressive revenue targets by slashing turnaround from 6 days to under 48 hours to beat agile competitors.
   - *Discovery Questions:* "Ashok, if we give you an AI that automates quotes but causes the loss ratio to jump from 68% to 75%, will the board consider that a success? What if we instead deliver quotes on high-priority eligible risks in 4 hours while preserving underwriter pricing control?"
   - *FDE Steering:* Pivot him from "autonomous quoting" to "intelligent ingestion and high-speed underwriting enablement."
2. **The Chief Underwriting Officer (CUO — Risk Gatekeeper):**
   - *Motivation:* Protect underwriting integrity and reinsurance treaties; prevent adverse selection.
   - *Discovery Questions:* "What specific high-hazard occupancies or risk attributes are driving the 68% loss ratio today? If our AI provides deterministic rule validation, 100% field provenance (highlighting the exact sentence in the broker's PDF), and routes every pricing decision through your Authority Matrix, would that protect your book?"
   - *FDE Steering:* Position the AI as the CUO's *strongest compliance enforcement tool*, eliminating human data entry errors and flagging hidden hazard occupancies.
3. **Head of Distribution (Broker Relationship Guardian):**
   - *Motivation:* Keep brokers happy; terrified of anything that creates broker friction or breaks his "no new portals" promise.
   - *Discovery Questions:* "How do top brokers currently communicate urgent submissions? If our system works invisibly behind their existing regional email habits—requiring zero portal logins and sending instant acknowledgments with clear missing-data requests—how would that impact broker sentiment?"
   - *FDE Steering:* Reassure him that the broker channel UX remains 100% email-native.
4. **Pune Operations Lead (Ground Reality & Execution):**
   - *Motivation:* Meeting daily SLAs; anxiety regarding team downsizing or automated hallucination risks.
   - *Discovery Questions:* "Which broker document formats cause the most keying errors today? How many times do your team members have to re-enter data when a broker sends an updated Excel schedule?"
   - *FDE Steering:* Frame the prototype as an "Underwriting Co-pilot" that eliminates tedious keying of declined risks and automatically highlights revised rows in updated SOVs.

---

### 1.5 Recommended First Valuable Slice (FVS) & Rationale

#### The Strategic Decision: Why We Reject the Sponsor's Literal Ask
The customer asked to *"build an AI that reads broker emails and generates the quotes automatically."*
We deliberately **reject automated quoting in the First Valuable Slice** based on three insurmountable enterprise constraints:
1. **Regulatory & Policy Non-Compliance:** NorthStar's internal AI policy restricts AI to **assistive use for pricing** (PDF p. 20). Fully automated quoting violates corporate policy and board governance. Under IRDAI File-and-Use rules, unauthorized automated rating exposes the insurer to regulatory penalties.
2. **Architectural Feasibility:** Property rating for non-package commercial risks resides in **actuarial Excel workbooks**, not a scalable headless rating API (PDF p. 20). Wrapping an LLM around untested Excel macro execution creates catastrophic operational fragility.
3. **Misaligned Value Driver:** Automated quoting only accelerates the final 15 minutes of an underwriter's calculation. It does **zero** to eliminate the 4,725 hours wasted on out-of-appetite submissions or the 1,890 hours wasted on duplicate emails.

#### Definition of the First Valuable Slice (FVS)
**"Intelligent Intake, Appetite Triage, Duplicate Clearance & Pre-Filled Underwriting Workbench"**

```mermaid
flowchart TD
    subgraph FVS_Architecture["THE FIRST VALUABLE SLICE (FVS)"]
        M[Broker Inbound Email<br/>Outlook / M365 Mailbox] --> INGEST[1. Ingestion & Attachment Extraction<br/>PDF, Scans, Excel SOV]
        INGEST --> TRIAGE[2. Deterministic Appetite & Eligibility Engine<br/>Occupancy codes, location, sum insured limits]
        TRIAGE -- "Out of Appetite (45%)" --> DECLINE[Auto-Drafted Decline Notice<br/>Zero Pune keying required]
        TRIAGE -- "In Appetite" --> DUP[3. Multi-Broker Duplicate Matching Engine<br/>Fuzzy name, PIN code, GSTIN match]
        DUP -- "Duplicate (18%)" --> DUP_FLAG[Flag to Underwriter / Clearance Queue<br/>Stops redundant manual entry]
        DUP -- "Clear / Unique" --> EXTRACT[4. Schema-Grounded Document Extraction<br/>Vision/Text LLM via AI Gateway + Provenance]
        EXTRACT --> DIFF[5. SOV Version Diffing Engine<br/>Detects mid-stream broker updates]
        DIFF --> COCKPIT[6. Pre-filled Underwriting Workbench<br/>SaaS Staging / UI Cockpit]
        COCKPIT --> UW[7. Human Underwriter Sign-off<br/>Applies Excel Rating / Authority Matrix]
        UW --> QUOTE[Quote Issued to Broker<br/>Target: < 24 - 48 Hours]
    end
```

#### What We Consciously Defer (The "Saying No" Register)
| Deferred Capability | Reason for Deferral | Rubric Scoring Justification |
| :--- | :--- | :--- |
| **Fully Automated Quote Generation** | Prohibited by NorthStar AI Policy; Property rating engine is in Excel; CUO resistance on loss ratio. | Demonstrates superior risk judgment, regulatory maturity, and adherence to client AI governance (Rubric: 13%). |
| **Mandatory Broker Web Portal** | 92% broker resistance; Head of Distribution promised "no new portals". | Demonstrates customer empathy and pragmatic channel adoption strategy (Rubric: 10%). |
| **Automated Real-Time Binding / Policy Issuance** | Core SaaS has quarterly release cycles and limited APIs; binding requires statutory KYC / payment validation. | Respects existing IT estate constraints; prevents project paralysis from vendor dependencies (Rubric: 12%). |
| **Automated Catastrophe Model Execution** | Licensed per call (expensive third-party API); CAT modeling needed only for specific coastal/seismic zones. | Prudent cost and token governance; avoids unneeded API spend on early triage (Rubric: 10%). |

---

# PART 2: PROJECT MASTER PLAN

```
========================================================================================
PART 2: PROJECT MASTER PLAN — PHASES, WBS, FIVE-MEMBER RACI & TIMELINES
========================================================================================
```

### 2.1 Seven-Phase Delivery Framework
Our delivery follows a rigorous, battle-tested 7-phase FDE engagement model tailored to the 60-minute Virtusa capstone presentation and technical defense:

```mermaid
gantt
    title Lead FDE Capstone Execution Lifecycle (10-Day Plan)
    dateFormat  YYYY-MM-DD
    section Phase 1: Understand & Frame
    Case Discovery & Stakeholder Mapping     :active, p1, 2026-11-24, 1d
    section Phase 2: Shape Solution
    OST, ICE Prioritization & FVS Definition :p2, after p1, 1d
    section Phase 3: Architectural Blueprint
    Data Contracts, Security & Integration    :p3, after p2, 1d
    section Phase 4: Rapid Prototyping
    Build Ingestion, Extraction & UI Cockpit  :p4, after p3, 3d
    section Phase 5: Evaluate & Harden
    Golden Dataset, Injection Tests & Latency :p5, after p4, 1d
    section Phase 6: Enterprise Readiness
    Unit Economics, RACI, Run Book & Risk Reg :p6, after p5, 1d
    section Phase 7: Executive Delivery
    10-Slide Deck, Script & Demo Rehearsals   :p7, after p6, 2d
```

---

### 2.2 Work Breakdown Structure (WBS) & Deliverable Inventory

| WBS Code | Phase / Task Description | Primary Owner | Mandatory Capstone Deliverable | Acceptance Criteria | Priority | Effort (Hrs) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1.0** | **Phase 1: Understand & Frame** | | | | | |
| 1.1 | PDF Deep-Dive & Baseline Extraction | Member 1 | Case Fact & Assumption Log | All 13 confirmed facts extracted with page citations | High | 4 |
| 1.2 | As-Is Process & Bottleneck Quantification | Member 5 | As-Is Value Stream Map | 6-day cycle mapped; 10,500 hrs/mo keying waste proven | High | 6 |
| 1.3 | Stakeholder Empathy & Discovery Plan | Member 1 | Stakeholder Interview Pack | 4 stakeholder discovery scripts with objection handling | High | 5 |
| **2.0** | **Phase 2: Shape the Solution** | | | | | |
| 2.1 | Opportunity Solution Tree (OST) | Member 1 | NorthStar OST Visual | Maps "Quote in 48 hrs" goal to triage & extraction solutions | High | 4 |
| 2.2 | ICE Prioritization & Boundary Scoring | Member 3 | ICE Scoring Matrix | Quantitative justification for deferring auto-quoting | High | 3 |
| 2.3 | FVS Definition & Scope Boundary | Member 1 | One-Page Sponsor Recommendation | Clearly defines what we build vs. what we defer | High | 3 |
| **3.0** | **Phase 3: Design the Architecture** | | | | | |
| 3.1 | High-Level Architecture (C4 Container) | Member 3 | System Architecture Diagram | Incorporates M365 email, AI Gateway, SaaS, Excel | High | 6 |
| 3.2 | Schema & Data Contract Specifications | Member 2 | Pydantic Submission Schemas | Complete JSON schema with confidence & provenance | High | 5 |
| 3.3 | Enterprise Security & Trust Gate Design | Member 4 | Threat Model & Trust Gates | Prompt injection defense, DPDP masking, audit schema | High | 5 |
| **4.0** | **Phase 4: Build the Prototype** | | | | | |
| 4.1 | Synthetic Dataset Generation | Member 2 | 25 Synthetic Submissions | Covers PDF, Excel SOVs, scans, multi-broker duplicates | High | 8 |
| 4.2 | Ingestion & OCR/Parsing Pipeline | Member 2 | Multi-format Document Ingestor | Handles pdfplumber/tesseract/openpyxl extraction | High | 10 |
| 4.3 | Appetite Triage & Duplicate Matching | Member 2 | Rule Engine + Fuzzy Matcher | Deterministic occupancy check + RapidFuzz clearance | High | 8 |
| 4.4 | SOV Version Delta Diffing Engine | Member 2 | Schedule Diffing Module | Flags cell modifications between broker revisions | Medium | 6 |
| 4.5 | Underwriter Cockpit & Review UI | Member 5 | Streamlit / Web UI Cockpit | Displays pre-filled submission, citations, and sign-off | High | 10 |
| **5.0** | **Phase 5: Evaluate and Harden** | | | | | |
| 5.1 | Golden Dataset Benchmarking | Member 4 | Evaluation Benchmark Report | Accuracy, precision, recall measured across 25 cases | High | 6 |
| 5.2 | Adversarial Security Testing | Member 4 | Injection Test Results | 5 prompt injection attacks tested and mitigated | High | 5 |
| 5.3 | Latency & Unit Cost Measurement | Member 4 | Gateway Latency & Token Log | Token counts, API costs, and latency measured per doc | High | 4 |
| **6.0** | **Phase 6: Enterprise Readiness** | | | | | |
| 6.1 | Unit Economics & Financial ROI Model | Member 5 | Cost-Benefit Excel Model | Net savings, break-even month, ROI sensitivity | High | 6 |
| 6.2 | Enterprise Governance & Run Book | Member 4 | Production Run Book | Monitoring signals, rollback switch, named post-go-live owner | High | 5 |
| 6.3 | Target Operating Model & RACI | Member 5 | TOM & RACI Matrix | Operations transition plan from keying to exception handling | Medium | 4 |
| **7.0** | **Phase 7: Final Presentation & Defense** | | | | | |
| 7.1 | Capstone Slide Deck (10 Slides Max) | Member 1 | 10-Slide Capstone Master Deck | Follows exact Virtusa mandate (PDF p. 2) | High | 8 |
| 7.2 | Speaker Scripts & Transition Matrix | Member 1 | Complete 60-Minute Script | Professional spoken delivery across all 5 members | High | 6 |
| 7.3 | Live Demo Runbook & Fallback Video | Member 5 | Demo Script & Video Backup | Step-by-step click path + offline contingency | High | 5 |
| 7.4 | Panel Defense & 25 Q&A Playbook | All Team | Evaluator Q&A Defense Matrix | 25 tough CXO/Architect questions with proof points | High | 6 |

---

### 2.3 Five-Member Team Structure & Detailed RACI Matrix

To ensure balanced contribution and prevent single-speaker dominance during the 60-minute panel defense, responsibilities are mapped with rigorous accountability:

- **Member 1 (M1): FDE Lead / Principal Business Consultant**
  - *Primary Ownership:* Problem framing, stakeholder management, discovery questions, executive storytelling, business justification.
  - *Defense Domain:* Strategic alignment, why auto-quoting was deferred, sponsor negotiation.
- **Member 2 (M2): AI Engineer / Prototype Pipeline Lead**
  - *Primary Ownership:* Document ingestion, OCR/parsing pipeline, LLM prompt engineering, Pydantic schemas, SOV diffing logic.
  - *Defense Domain:* Model selection, prompt tuning, extraction accuracy, parsing edge cases.
- **Member 3 (M3): Solution Architect / Enterprise Integration Lead**
  - *Primary Ownership:* Target architecture, integration with M365/SaaS/Excel, AI Gateway, batch vs. real-time, non-functional requirements.
  - *Defense Domain:* Enterprise integration constraints, quarterly release synchronization, latency, API rate limits.
- **Member 4 (M4): Enterprise Security, AI Governance & Evaluation Lead**
  - *Primary Ownership:* Trust gates, prompt injection defense, DPDP Act 2023 compliance, audit trail schema, Golden Dataset evaluation.
  - *Defense Domain:* Security vulnerabilities, hallucination mitigation, model risk management, auditability.
- **Member 5 (M5): Delivery Lead, Enterprise Value & Live Demo Coordinator**
  - *Primary Ownership:* Financial ROI model, unit economics, prototype UI cockpit, live demo orchestration, post-go-live run book.
  - *Defense Domain:* Cost per submission, operational transition, live demo execution, value realization metrics.

#### Full 25-Deliverable RACI Matrix
*(R = Responsible, A = Accountable, C = Consulted, I = Informed)*

| Deliverable ID | Project Deliverable Name | M1 (Biz) | M2 (AI) | M3 (Arch) | M4 (Sec) | M5 (Val) | Capstone Requirement |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **DEL-01** | Case Fact & Assumption Register | **A/R** | C | C | C | I | Must-Have (PDF p. 2) |
| **DEL-02** | As-Is Process & Waste Quantification | C | I | C | I | **A/R** | Must-Have (PDF p. 2) |
| **DEL-03** | Stakeholder Discovery & Empathy Maps | **A/R** | I | C | C | I | Must-Have (Rubric 10%) |
| **DEL-04** | Opportunity Solution Tree (OST) | **A/R** | C | C | I | I | Must-Have (Rubric 15%) |
| **DEL-05** | ICE Prioritization Matrix | C | C | **A/R** | C | I | Must-Have (Rubric 10%) |
| **DEL-06** | One-Page Sponsor Recommendation | **A/R** | I | C | C | C | Mandatory Submission (PDF p. 2) |
| **DEL-07** | High-Level & Container Architecture | I | C | **A/R** | C | I | Must-Have (Rubric 12%) |
| **DEL-08** | Pydantic Schemas & Data Contracts | I | **A/R** | C | C | I | Must-Have (Engineering) |
| **DEL-09** | AI Gateway & Integration Design | I | C | **A/R** | C | I | Must-Have (Rubric 12%) |
| **DEL-10** | Trust Boundary & Threat Model | I | I | C | **A/R** | I | Must-Have (Rubric 13%) |
| **DEL-11** | Synthetic Submission Dataset (25 cases) | C | **A/R** | I | C | I | Mandatory Submission (PDF p. 2) |
| **DEL-12** | Ingestion & Multi-Format OCR Pipeline | I | **A/R** | C | I | I | Working Slice (PDF p. 2) |
| **DEL-13** | Deterministic Appetite Triage Engine | C | **A/R** | I | C | I | Working Slice (PDF p. 2) |
| **DEL-14** | Multi-Broker Duplicate Matching Engine | I | **A/R** | C | I | I | Working Slice (PDF p. 2) |
| **DEL-15** | SOV Version Delta Diffing Engine | I | **A/R** | I | I | C | Working Slice (PDF p. 2) |
| **DEL-16** | Underwriting Workbench UI Cockpit | C | C | I | I | **A/R** | Working Slice (PDF p. 2) |
| **DEL-17** | Golden Benchmark Evaluation Report | I | C | I | **A/R** | I | Mandatory Submission (PDF p. 2) |
| **DEL-18** | Prompt Injection Defense Suite | I | C | I | **A/R** | I | Must-Have (Rubric 13%) |
| **DEL-19** | Decision Log (Key Architecture Choices)| C | C | **A/R** | C | I | Mandatory Submission (PDF p. 2) |
| **DEL-20** | Unit Economics & Cost Model | I | I | C | I | **A/R** | Must-Have (Rubric 10%) |
| **DEL-21** | 3-Year Enterprise ROI & Value Model | C | I | I | I | **A/R** | Must-Have (Rubric 5%) |
| **DEL-22** | Production Operations Run Book | I | I | C | **A/R** | C | Mandatory Submission (PDF p. 2) |
| **DEL-23** | 10-Slide Capstone Presentation Deck | **A/R** | C | C | C | C | Mandatory Submission (PDF p. 2) |
| **DEL-24** | Live Demo Script & Fallback Video | I | C | I | I | **A/R** | Mandatory Submission (PDF p. 2) |
| **DEL-25** | Evaluator Q&A Defense Master Guide | **A/R** | C | C | C | C | Must-Have (Rubric 10%) |

---

### 2.4 Project Execution Schedule & Milestone Tracking

#### Standard 10-Working-Day Baseline Plan
```mermaid
flowchart LR
    D1[Day 1: Discovery & Baseline] --> D2[Day 2: OST & Slicing]
    D2 --> D3[Day 3: Architecture & Schemas]
    D3 --> D4[Days 4-6: Prototype Engineering]
    D4 --> D7[Day 7: Evaluation & Hardening]
    D7 --> D8[Day 8: Business Case & Run Book]
    D8 --> D9[Day 9: Deck & Demo Polish]
    D9 --> D10[Day 10: Rehearsal & Defense]
```

- **Day 1 (Discovery & Framing):** Finalize Case Fact Log (DEL-01); map 6-day As-Is Bottleneck (DEL-02); draft Stakeholder Empathy Maps (DEL-03). *Milestone M1 Reached.*
- **Day 2 (Solution Shaping):** Construct Opportunity Solution Tree (DEL-04); run ICE Scoring (DEL-05); publish One-Page Sponsor Recommendation (DEL-06). *Milestone M2 Reached.*
- **Day 3 (Architecture & Contracts):** Complete C4 Container Architecture (DEL-07); define Pydantic Schemas (DEL-08); document Trust Gates & Threat Model (DEL-10). *Milestone M3 Reached.*
- **Days 4–6 (Sprint Build — Core Prototype):** Generate 25 Synthetic Submissions (DEL-11); build Multi-format Ingestor (DEL-12); implement Appetite Rule Engine (DEL-13); implement Duplicate Matcher (DEL-14); build SOV Diffing (DEL-15); integrate Streamlit Cockpit (DEL-16). *Milestone M4 Reached (Working Slice Operational).*
- **Day 7 (Evaluation & Security):** Execute Golden Benchmark on 25 cases (DEL-17); run Prompt Injection attacks (DEL-18); log token costs and API latencies. *Milestone M5 Reached.*
- **Day 8 (Enterprise Value & Governance):** Build Unit Economics & ROI Model (DEL-20, 21); write Production Run Book (DEL-22); establish Decision Log (DEL-19). *Milestone M6 Reached.*
- **Day 9 (Slide Deck & Demo Choreography):** Produce 10-Slide Master Capstone Deck (DEL-23); draft Speaker Scripts; record offline demo backup video (DEL-24). *Milestone M7 Reached.*
- **Day 10 (Full Rehearsal & Stress Testing):** Conduct 60-minute mock presentation with peer panel playing CUO, Distribution Head, and Lead Evaluator; stress test Q&A matrix (DEL-25). *Final Readiness Sign-off.*

#### Fast-Track 5-Day Compressed Contingency Plan
*(In case the submission window is shortened)*
- **Day 1:** Case framing, OST, ICE prioritization, and Pydantic schema definition (M1, M3, M5).
- **Day 2:** Synthetic data generation and rapid pipeline build: Ingestion, Triage, and Duplicate matching (M2, M4).
- **Day 3:** UI Cockpit integration and Golden Dataset evaluation runs (M2, M4, M5).
- **Day 4:** Financial ROI model, Run Book, Decision Log, and 10-slide Capstone Deck creation (M1, M3, M5).
- **Day 5:** Rehearsals, demo dry-runs, and defense Q&A drill.

---

### 2.5 Rubric-to-Evidence Alignment Matrix (Targeting 90+ / 100 Marks)

Every criterion in the official Virtusa scoring rubric is mapped to concrete project artifacts and team ownership:

| Rubric Block & Criterion | Weight | Evaluator Expectation (PDF p. 20–21) | Concrete Evidence / Artifact We Present | Lead Owner | Common Failure Mode to Avoid |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **CONSULTATIVE (45%)** | | | | | |
| **1. Problem Framing & Discovery** | 15% | Did they find that out-of-appetite keying (45%) and duplicates (18%) drive the effort, not pricing? | • As-Is Value Stream Map showing 10,500 hrs/mo keying waste.<br/>• Mathematical proof that pricing is only 15 min of 6 days.<br/>• Pune operations discovery questions. | **M1** | Assuming automated pricing is the primary problem; failing to analyze Pune data entry waste. |
| **2. Working-Session Presence & Stakeholder Handling** | 10% | Did they engage brokers, the Pune data-entry team, the CUO, and Distribution? | • Stakeholder Empathy Maps for all 4 roles.<br/>• Scripted responses resolving CUO's loss-ratio fear.<br/>• Respecting Distribution Head's "no new portals" promise. | **M1** | Pitching only to Ashok Menon; ignoring CUO and treating Pune staff as simple headcount cuts. |
| **3. Judgment Under Ambiguity & Response to Challenge** | 10% | How they respond to the loss-ratio concern or the "no new portals" promise. | • Email-native design preserving broker workflow.<br/>• Deterministic triage protecting loss ratio.<br/>• Live defense script handling evaluator injects. | **M1 / M5** | Insisting on forcing a broker portal or proposing unconstrained AI rating that spikes loss ratio. |
| **4. Solution Shaping — First Valuable Slice** | 10% | Appetite triage and extraction into pre-filled submission for underwriters. What they defer: automated pricing. | • One-Page Sponsor Recommendation.<br/>• The "Saying No" Deferral Register.<br/>• Clear boundary: AI extracts & triages; Underwriter prices. | **M1 / M3** | Attempting full end-to-end auto-quoting; failing to define clear deferral boundaries. |
| **ENGINEERING (40%)** | | | | | |
| **5. Rapid Prototyping — Hypothesis to Working Slice** | 15% | A working triage and extraction slice on synthetic broker emails, tested against keying time and accuracy. | • Live demonstration of 5 distinct test scenarios.<br/>• Multi-format ingestion (Excel SOV, PDF, Scans).<br/>• Measured extraction accuracy & keying reduction. | **M2** | Showing static UI mockups or clickable wireframes with no real backend parsing logic. |
| **6. Architecture, Client Landscape & Integration** | 12% | Designing around quarterly SaaS releases, Excel rating, regional mailboxes, and per-call third-party data. | • C4 Architecture Diagram honoring all 9 client systems.<br/>• Excel rating handoff pattern.<br/>• Asynchronous batching to minimize third-party CAT API calls. | **M3** | Assuming modern real-time GraphQL/REST APIs on the legacy SaaS; ignoring Excel rating reality. |
| **7. Autonomy Boundaries, Guardrails & Security** | 13% | Underwriter prices; filed rates respected; injection via broker emails; audit of extracted fields. | • Dual-LLM Guardrail & Input Sanitizer.<br/>• Field-level provenance visualizer (bounding boxes/citations).<br/>• Tamper-proof audit log schema. | **M4** | Permitting model to set premium; storing raw PAN/broker data in cleartext; no prompt injection defense. |
| **ENTERPRISE (15%)** | | | | | |
| **8. Cost, Governance, Ownership & Scale** | 10% | Cost per submission at 9,000/mo; owner; broker adoption; rollout across regions. | • Detailed unit economics (₹38.50/submission vs. ₹350 human cost).<br/>• Phased regional rollout plan (West → South → North).<br/>• Named post-go-live owner (Head of UW Operations). | **M5** | Omitting token/hosting costs; failing to name a single post-go-live business owner. |
| **9. Value Realization & Executive Communication** | 5% | Time to quote, win rate, and loss ratio with baselines; how underwriter use is tracked. | • Baseline vs. Target Value Scorecard.<br/>• 3-Year P&L projection showing ₹3.8 Cr net benefit.<br/>• Executive presentation completed strictly within 10 slides. | **M5 / M1** | Claiming employee time saved is 100% hard cash savings; exceeding the 10-slide capstone limit. |

---

*End of Part 1 & Part 2. Continue to Part 3 (Technical Blueprint) and Part 4 (Prototype & Evaluation).*
