# NorthStar General Insurance — Score Maximization & Next Actions
## Parts 7 & 8: 100-Point Rubric Guide, Risk Mitigation & Immediate Execution Checklist

**Author:** Antigravity (Principal FDE, Enterprise AI Architect & Presentation Coach)  
**Target:** Five-Member Capstone Team (Virtusa AI Academy & StackRoute Lead FDE Program)  
**Primary Source:** Virtusa LeadFDE Cases.pdf (Case 06: Northstar General Insurance, Pages 19–21; Scoring Rubric, Pages 1–3)  
**Target Score:** 90+ / 100 Marks across all 9 Official Evaluation Criteria

---

# PART 7: SCORE MAXIMIZATION (TARGETING 90+ / 100)

```
========================================================================================
PART 7: SCORE MAXIMIZATION — RUBRIC MAPPING, PITFALLS & REHEARSAL CHECKLIST
========================================================================================
```

### 7.1 Detailed Rubric Mapping Across All 9 Criteria (100 Marks)

The official Virtusa Lead FDE evaluation rubric (PDF p. 20–21) divides 100 marks into three distinct evaluation blocks:
- **Block 1: Consultative — 45%** (Scored by Lead FDE / Principal Consultant Scorer)
- **Block 2: Engineering — 40%** (Scored by Chief AI Architect / Technical Lead Scorer)
- **Block 3: Enterprise — 15%** (Scored by Delivery Director / Enterprise Program Scorer)

---

#### BLOCK 1: CONSULTATIVE (45 MARKS)

#### 1. Problem Framing & Discovery (15% Weight)
- **Evaluator Question (PDF p. 20):** *"Did they find that out-of-appetite keying (45%) and duplicates (18%) drive the effort, not pricing? Quality of questions to checkers and team leads."*
- **What Earns Full Marks (13–15 Marks):**
  - Demonstrating that the 6-day turnaround delay is **95% queue and manual keying friction**, not pricing calculation time.
  - Mathematical proof showing that out of 10,500 hours/month spent in Pune, **6,615 hours (63%)** are completely wasted keying files that are declined or duplicate.
  - Presenting concrete discovery questions that engage frontline Pune operations and underwriters rather than treating them as an abstract headcount number.
- **Common Mistakes That Lose Marks:**
  - Blindly accepting Ashok Menon’s initial ask: *"We built an AI pricing bot because the sponsor asked for automated quotes."* (Instant failure on problem framing).
  - Focusing only on the underwriter's desk while ignoring the 60-person Pune data-entry bottleneck.

#### 2. Working-Session Presence & Stakeholder Handling (10% Weight)
- **Evaluator Question (PDF p. 20):** *"Did they engage brokers, the Pune data-entry team, the CUO and Distribution?"*
- **What Earns Full Marks (9–10 Marks):**
  - Explicitly presenting the conflicting agendas of all four stakeholders: Ashok Menon (growth/speed), CUO (loss ratio control), Distribution Head (broker relationships / "no new portals"), and Pune Ops (job security / accuracy).
  - Demonstrating consultative empathy: explaining how the solution protects the CUO's book, preserves the Distribution Head's promise, and upskills Pune operations.
- **Common Mistakes That Lose Marks:**
  - Pitching only to the commercial sponsor (Ashok Menon) and ignoring the risk gatekeepers.
  - Proposing that AI will replace the Pune staff (causes severe organizational resistance and fails stakeholder handling).

#### 3. Judgment Under Ambiguity & Response to Challenge (10% Weight)
- **Evaluator Question (PDF p. 21):** *"How they respond to the loss-ratio concern or the 'no new portals' promise."*
- **What Earns Full Marks (9–10 Marks):**
  - When the evaluator injects: *"The CUO refuses to sign off because the loss ratio is 68%"*, the team calmly responds: *"Our system does not allow AI to quote or bind; it enforces your Underwriting Appetite deterministically before an underwriter ever prices the file."*
  - When told *"Brokers hate portals"*, the team demonstrates that the solution is 100% email-native with zero broker behavior change.
  - Re-framing challenges as design requirements without getting defensive or abandoning the core business value.
- **Common Mistakes That Lose Marks:**
  - Digging in: *"We think the CUO is too conservative and should trust the AI."*
  - Collapsing: *"If the CUO says no, we will scrap the project."*

#### 4. Solution Shaping — The First Valuable Slice (10% Weight)
- **Evaluator Question (PDF p. 21):** *"For example: appetite triage and extraction into a pre-filled submission for underwriters. What they defer: automated pricing."*
- **What Earns Full Marks (9–10 Marks):**
  - Clearly articulating the First Valuable Slice: **Intelligent Intake, Appetite Triage, Duplicate Clearance, and Pre-filled Underwriting Packaging.**
  - Presenting a formal **"Saying No" Deferral Register**: explicitly deferring autonomous quoting, mandatory broker portals, live policy binding, and automated CAT API execution.
  - Explaining the business trade-off: moving the needle on the 6-day backlog today while deferring high-risk, low-feasibility components.
- **Common Mistakes That Lose Marks:**
  - Attempting to boil the ocean: trying to demo automated quoting, automated binding, and broker portals all at once.
  - Failing to explain *why* automated pricing was deferred.

---

#### BLOCK 2: ENGINEERING (40 MARKS)

#### 5. Rapid Prototyping — Hypothesis to Working Slice (15% Weight)
- **Evaluator Question (PDF p. 21):** *"A working triage and extraction slice on synthetic broker emails, tested against keying time and accuracy."*
- **What Earns Full Marks (13–15 Marks):**
  - Running a real, responsive, functional prototype (not Figma mockups or static wireframes).
  - Executing live test scenarios: clean intake, prohibited fireworks triage, duplicate broker clearance, mid-stream SOV delta diffing, and prompt injection defense.
  - Proving real data parsing: extracting multi-line tables, calculating sums, and validating Pydantic schemas.
- **Common Mistakes That Lose Marks:**
  - Showing video recordings without having the code running locally.
  - Prototype crashing when an unexpected input or edge case is entered.

#### 6. Architecture, Client Landscape & Integration (12% Weight)
- **Evaluator Question (PDF p. 21):** *"Designing around quarterly SaaS releases, Excel rating, regional mailboxes and per-call third-party data."*
- **What Earns Full Marks (11–12 Marks):**
  - Explicitly designing into all nine systems in NorthStar's estate (PDF p. 20).
  - Bypassing the quarterly SaaS release lock via a validated Staging Payload.
  - Integrating the Actuarial Excel Rating Bridge rather than pretending Excel can be rewritten in Python overnight.
  - Demonstrating **Conditional Lazy Calling** on third-party CAT data to control per-call costs.
- **Common Mistakes That Lose Marks:**
  - Designing a greenfield architecture assuming modern REST/GraphQL APIs on legacy systems.
  - Forgetting the "in-region India" requirement for the AI Gateway.

#### 7. Autonomy Boundaries, Guardrails & Security (13% Weight)
- **Evaluator Question (PDF p. 21):** *"Underwriter prices; filed rates respected; injection via broker emails; audit of extracted fields."*
- **What Earns Full Marks (12–13 Marks):**
  - Strict separation of control and data planes: the LLM extracts text; deterministic rules decide eligibility; humans price.
  - Demonstrating live defense against indirect prompt injection embedded in broker PDFs.
  - DPDP Act 2023 compliance: masking personal PANs and phone numbers before AI gateway transit.
  - IRDAI-compliant tamper-proof audit trail storing SHA-256 hashes for 8-year decision reconstruction.
- **Common Mistakes That Lose Marks:**
  - Giving an LLM tool access to generate quotes or bind policies.
  - Storing raw unencrypted customer PII in cloud logs or SQLite databases.

---

#### BLOCK 3: ENTERPRISE (15 MARKS)

#### 8. Cost, Governance, Ownership & Scale (10% Weight)
- **Evaluator Question (PDF p. 21):** *"Cost per submission at 9,000 a month; owner; broker adoption; rollout across regions."*
- **What Earns Full Marks (9–10 Marks):**
  - Clear unit economics: **₹24.11 per submission** vs. **₹266.67 human baseline** (91% reduction).
  - Naming specific post-go-live owners across Commercial Lines, Underwriting Operations, Risk, and IT.
  - Phased regional rollout plan: West (Pilot/Shadow) → South → North/East.
- **Common Mistakes That Lose Marks:**
  - Omitting token and hosting costs; claiming the solution is "free".
  - Failing to name a single post-go-live business owner.

#### 9. Value Realization & Executive Communication (5% Weight)
- **Evaluator Question (PDF p. 21):** *"Time to quote, win rate and loss ratio with baselines; how underwriter use is tracked."*
- **What Earns Full Marks (4–5 Marks):**
  - Baseline vs. Target scorecard linking TAT (<48 hrs) to win-rate expansion (11% → 18%).
  - Tracking underwriter adoption via Suggestion Acceptance Rate ($\ge 92\%$).
  - Delivering a concise, polished 10-slide executive presentation strictly within time limits.
- **Common Mistakes That Lose Marks:**
  - Claiming 100% of employee hours saved are cash salary cuts.
  - Going over the 10-slide capstone limit or running out of time during the presentation.

---

### 7.2 High-Risk Traps & Pitfalls to Avoid

| Risk ID | Dangerous Trap / Evaluator Landmine | How to Defend & Mitigate |
| :--- | :--- | :--- |
| **TRAP-01** | **The Autonomous Quoting Trap:** Building an end-to-end bot that calculates premiums and sends quotes to brokers without human touch. | **Mitigation:** Emphasize that autonomous quoting violates NorthStar AI policy (assistive pricing only), violates IRDAI File-and-Use rules, and threatens the 68% loss ratio. |
| **TRAP-02** | **The Broker Portal Mandate:** Proposing a new web portal for brokers to enter data. | **Mitigation:** Reiterate the 2023 portal failure (8% adoption) and the Head of Distribution's "no new portals" promise. Keep broker intake 100% email-native. |
| **TRAP-03** | **The Direct Headcount Slashing Trap:** Claiming that 60 people in Pune will be fired to save ₹2.88 Crore. | **Mitigation:** Frame as capacity liberation: Pune staff upskilled into Underwriting Support Specialists managing exceptions, VIP broker service, and renewals. |
| **TRAP-04** | **The Greenfield API Assumption:** Assuming the core policy admin SaaS has open real-time REST APIs. | **Mitigation:** Acknowledge the quarterly release constraint and demonstrate the Staging Payload export pattern that bypasses release freezes. |
| **TRAP-05** | **The Single-Speaker Trap:** Member 1 doing all the talking while other members remain silent. | **Mitigation:** Enforce the strict 5-speaker distribution table. Every member presents their assigned domain and answers relevant defense questions. |

---

### 7.3 Final Capstone Rehearsal Checklist

- [ ] **Timing Discipline:** Presentation + Live Demo completes strictly in **under 32 minutes**, leaving a full 28 minutes for panel defense.
- [ ] **Slide Constraint:** Capstone deck has **exactly 10 slides or fewer** (strictly per PDF p. 2 mandate).
- [ ] **Local Demo Reliability:** FastAPI server starts cleanly with `uvicorn app.main:app --port 8000` and displays all scenario buttons.
- [ ] **Offline Video Backup:** A 3-minute screen recording of the working UI is stored locally in case localhost networking glitches.
- [ ] **Speaker Transitions:** Every presenter introduces the next speaker by name and topic (no awkward pauses).
- [ ] **Q&A Protocol:** Member 1 directs incoming panel questions to the designated subject matter owner.
- [ ] **Evaluator Injects:** The team is prepared for evaluators playing the CUO, Distribution Head, or Head of Ops.

---

# PART 8: IMMEDIATE NEXT ACTIONS

```
========================================================================================
PART 8: IMMEDIATE NEXT ACTIONS — TEAM ASSIGNMENTS & FIRST MILESTONE
========================================================================================
```

### 8.1 Team Action Items for Today

| Team Member | Role | Action Items for Today | Immediate Deliverable |
| :--- | :--- | :--- | :--- |
| **Member 1** | FDE Lead & Business Consultant | • Review Slide 1–3 scripts and rehearse the opening 60-second hook.<br/>• Finalize Stakeholder Empathy Maps and objection handling. | Opening Narrative & Sponsor One-Pager (DEL-06) |
| **Member 2** | AI Engineer & Prototype Lead | • Verify the 8 test scenarios in the live UI (`http://localhost:8000`).<br/>• Review Pydantic schemas and OCR bounding box provenance code. | Live Demo Rehearsal & Provenance Check (DEL-16) |
| **Member 3** | Solution Architect & Integration Lead | • Review Slide 4–5 scripts on C4 Container Architecture.<br/>• Master defense points on SaaS quarterly releases and Excel rating bridge. | C4 Target Architecture Narrative (DEL-07) |
| **Member 4** | Security, Governance & Evaluation Lead | • Review Slide 7–8 scripts on Prompt Injection and DPDP Act 2023.<br/>• Validate Golden Benchmark test results across all 25 cases. | Security Defense Suite & Benchmark Report (DEL-17, 18) |
| **Member 5** | Enterprise Value & Demo Coordinator | • Review Slide 6 & 9 scripts on Unit Economics (₹24.11 vs ₹266.67).<br/>• Coordinate live demo click path and record offline backup video. | Live Demo Choreography & Video Backup (DEL-24) |

---

### 8.2 First Milestone: End-to-End Dry Run
- **Target Deadline:** Today, within 4 hours.
- **Objective:** Execute a complete 30-minute dry-run presentation followed by a 15-minute simulated evaluator cross-examination.
- **Success Criteria:** Zero slide stumbles, seamless handoffs between all 5 members, error-free prototype demonstration, and flawless defense of the First Valuable Slice.
