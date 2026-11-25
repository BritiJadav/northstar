from app.schemas import (
    AppetiteCheckResult, TriageStatus, OccupancyCategory, PropertyLocationItem
)
from typing import List

class DeterministicAppetiteEngine:
    """
    Evaluates NorthStar Underwriting Guidelines deterministically.
    Adheres strictly to IRDAI File-and-Use filed underwriting guidelines.
    Zero LLM autonomy is allowed in this gate to eliminate hallucinations.
    """
    
    PROHIBITED_OCCUPANCIES = {
        OccupancyCategory.FIREWORKS_EXPLOSIVES: "Prohibited under NorthStar Treaty Exclusion Rule EXCL-04 (Hazardous Pyrotechnics).",
        OccupancyCategory.CHEMICAL_SOLVENT_STORAGE: "Prohibited under NorthStar Solvency & Toxic Storage Guideline EXCL-09."
    }
    
    REFERRAL_OCCUPANCIES = {
        OccupancyCategory.PLASTICS_MANUFACTURING: "High fire load; requires on-site Risk Engineering hydrant inspection.",
        OccupancyCategory.WOOD_TIMBER_STORAGE: "High combustible fuel load; mandatory physical risk inspection."
    }
    
    MAX_AUTOMATIC_SUM_INSURED = 100_000_000.0  # ₹10 Crore threshold for Risk Engg referral
    
    @classmethod
    def evaluate(cls, locations: List[PropertyLocationItem], broker_name: str, insured_name: str) -> AppetiteCheckResult:
        violations = []
        referrals = []
        
        for loc in locations:
            # 1. Prohibited Occupancy Check
            if loc.occupancy_code in cls.PROHIBITED_OCCUPANCIES:
                violations.append(
                    f"Location {loc.location_id} ({loc.address}): Occupancy '{loc.occupancy_code.value}' is strictly OUT OF APPETITE. "
                    f"Reason: {cls.PROHIBITED_OCCUPANCIES[loc.occupancy_code]}"
                )
            
            # 2. Risk Engineering Referral Trigger (PDF p. 19: 12% require risk-engineering)
            if loc.occupancy_code in cls.REFERRAL_OCCUPANCIES:
                referrals.append(
                    f"Location {loc.location_id}: Occupancy '{loc.occupancy_code.value}' requires Risk Engineering survey. "
                    f"Detail: {cls.REFERRAL_OCCUPANCIES[loc.occupancy_code]}"
                )
                
            if loc.total_sum_insured >= cls.MAX_AUTOMATIC_SUM_INSURED:
                referrals.append(
                    f"Location {loc.location_id}: Total Sum Insured ₹{loc.total_sum_insured:,.2f} exceeds automatic underwriting threshold of ₹10.00 Cr. "
                    f"Mandatory Risk Engineering referral required."
                )
        
        # Determine Final Triage Status
        if violations:
            decline_email = (
                f"Subject: Notice of Non-Appetite - Submission for {insured_name}\n\n"
                f"Dear {broker_name},\n\n"
                f"Thank you for sharing the proposal for {insured_name}.\n\n"
                f"After screening against NorthStar General Insurance's Commercial Underwriting Guidelines, "
                f"we regret to inform you that this risk falls outside our current underwriting appetite due to:\n"
                + "\n".join([f"- {v}" for v in violations]) +
                f"\n\nConsequently, we cannot offer terms on this risk. We appreciate our partnership and look forward "
                f"to supporting your eligible commercial risks.\n\n"
                f"Sincerely,\nCommercial Underwriting Operations\nNorthStar General Insurance"
            )
            return AppetiteCheckResult(
                status=TriageStatus.DECLINED_OUT_OF_APPETITE,
                rule_violations=violations,
                requires_risk_engineering=bool(referrals),
                referral_reasons=referrals,
                decline_draft_email=decline_email
            )
        
        if referrals:
            return AppetiteCheckResult(
                status=TriageStatus.REFERRED_RISK_ENGINEERING,
                rule_violations=[],
                requires_risk_engineering=True,
                referral_reasons=referrals
            )
            
        return AppetiteCheckResult(
            status=TriageStatus.ELIGIBLE,
            rule_violations=[],
            requires_risk_engineering=False,
            referral_reasons=[]
        )
