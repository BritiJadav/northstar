# NorthStar General Insurance — Architectural & Governance Decision Log
### Mandatory Capstone Submission Deliverable (Virtusa Assessment Pack, Page 2)

**Project:** NorthStar Commercial Lines Intelligent Ingestion & Triage Gateway  
**Lead:** Five-Member Forward Deployed Engineer (FDE) Team  
**Standards:** Architecture Decision Record (ADR) Format

---

## Decision Log Summary Register

| Decision ID | Date | Title / Scope | Decided By | Stakeholders Informed | Business & Technical Rationale | Status |
| :---: | :---: | :--- | :--- | :--- | :--- | :---: |
| **DEC-001** | 2026-11-24 | Deferral of Autonomous Quote Issuance | FDE Lead & CUO | Ashok Menon (Sponsor), Operations Lead | NorthStar AI Policy allows assistive pricing only. Autonomous quotes violate IRDAI File-and-Use rules, threaten 68% loss ratio, and rely on uncertified Excel macro execution. | **APPROVED** |
| **DEC-002** | 2026-11-24 | Preservation of Email-Native Ingestion (No Portal) | FDE Lead & Head of Distribution | Commercial Sponsor, Pune Ops | 2023 broker portal failed with 8% adoption. Head of Distribution promised "no new portals". Forcing portal entry will alienate brokers and destroy submission volume. | **APPROVED** |
| **DEC-003** | 2026-11-24 | Deterministic Appetite Triage vs. LLM Prompts | AI Lead & Security Lead | CUO, Lead Evaluator | LLMs can hallucinate occupancy eligibility and misclassify hazardous chemicals. Deterministic rule evaluation guarantees 100% precision on statutory exclusions and costs zero tokens. | **APPROVED** |
| **DEC-004** | 2026-11-24 | SaaS Batch Staging Payload vs. Direct Quote API | Solution Architect | Core SaaS Vendor Team, Enterprise IT | Core vendor SaaS has quarterly release freezes and a restricted quote API. Exporting a validated staging payload decouples deployment from vendor timelines. | **APPROVED** |
| **DEC-005** | 2026-11-24 | Actuarial Excel Rating Bridge vs. Python Re-write | Solution Architect & Actuarial Lead | Chief Actuary, CUO | Rewriting property rating Excel workbooks into Python requires months of actuarial re-certification. A headless Excel bridge allows rapid rating validation without model risk delays. | **APPROVED** |
| **DEC-006** | 2026-11-24 | Mandatory In-Region India Endpoint (`asia-south1`) | Security Lead & InfoSec | Head of Legal & Compliance | Indian DPDP Act 2023 mandates data residency for sensitive personal and commercial data. All Gemini LLM calls are pinned to Vertex AI in Mumbai. | **APPROVED** |
| **DEC-007** | 2026-11-24 | Conditional Lazy Calling for Third-Party CAT Data | Delivery Lead & Solution Architect | Chief Financial Officer | Third-party catastrophe modeling is billed per API call. Only calling the API for in-appetite risks > ₹5 Cr in coastal/seismic zones eliminates 95% of unnecessary API spend. | **APPROVED** |
| **DEC-008** | 2026-11-24 | RapidFuzz Composite Entity Matching vs. Vector Search | AI Lead & Prototype Lead | Clearance Officers, Pune Ops | Entity clearance requires exact and phonetic matching on Name, PIN, and Sum Insured. RapidFuzz executes in sub-milliseconds with explainable confidence scores. | **APPROVED** |

---

## Detailed Architectural Decision Records (ADRs)

### ADR-001: Deferral of Autonomous Quoting in First Valuable Slice
- **Context:** The sponsor, Ashok Menon, asked for an AI that reads emails and quotes automatically.
- **Decision:** The FDE team unanimously rejected automated quote generation for the MVP, constraining scope to Intake, Triage, Duplicate Clearance, and Pre-filled Underwriting Packaging.
- **Consequences:**
  - *Positive:* Fully complies with NorthStar AI policy (assistive pricing only); completely insulates the 68% property loss ratio from reckless risk selection; guarantees IRDAI compliance.
  - *Trade-off:* Underwriters still spend 15 minutes reviewing and signing off on the Excel rating output.
  - *Approval:* Confirmed by CUO Dr. Rajeshwar Rao; endorsed by Ashok Menon.

### ADR-002: Email-Native Channel Strategy (Rejecting Broker Web Portal)
- **Context:** Distribution has struggled with broker digital adoption since 2023.
- **Decision:** Intake must operate asynchronously behind existing regional shared mailboxes (`commercial.west@northstar.co.in`, etc.). No new logins, web portals, or broker behavior modifications are permitted.
- **Consequences:**
  - *Positive:* 100% broker channel adoption from Day 1; zero change management friction for brokers.
  - *Trade-off:* System must handle unstructured text, arbitrary attachments, and dirty OCR scans.

### ADR-003: Deterministic Rule Engine for Underwriting Appetite
- **Context:** 45% of incoming submissions are outside NorthStar's underwriting appetite.
- **Decision:** Underwriting appetite rules are implemented as pure deterministic Python rules mapped to standard IIB/TAC tariff occupancy codes rather than LLM system prompts.
- **Consequences:**
  - *Positive:* 100% triage accuracy; zero chance of hallucinated eligibility; instantaneous execution (<2ms); zero token expense on junk files.
  - *Trade-off:* New occupancy codes must be configured in JSON/rule tables rather than natural language prompts.

### ADR-004: Vendor SaaS Staging Payload Pattern
- **Context:** NorthStar's commercial lines core system is a vendor SaaS package with quarterly release cycles and limited APIs.
- **Decision:** The system outputs an immutable, schema-compliant Staging Payload (JSON and normalized CSV) that populates the core system's batch staging tables upon underwriter approval.
- **Consequences:**
  - *Positive:* Bypasses the 5-month vendor release window; eliminates vendor dependency risks.
  - *Trade-off:* Requires a daily automated batch sync job into the core policy master.
