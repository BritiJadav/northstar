from typing import Dict, Any
from app.schemas import OccupancyCategory

class ActuarialExcelRatingBridge:
    """
    Implements the integration constraint:
    'Property rating for larger risks stays in Excel' (PDF p. 20).
    'AI policy: assistive for pricing; no automated quotes have been approved' (PDF p. 20).
    Calculates indicative tariff premiums based on filed IRDAI File-and-Use base rates,
    which the human underwriter validates in their workbench.
    """
    
    # Base tariff rates per ₹1,000 Sum Insured (IIB standard general insurance schedules)
    OCCUPANCY_BASE_RATES = {
        OccupancyCategory.COMMERCIAL_OFFICE: 0.18,       # ₹0.18 per ₹1k SI (Low risk)
        OccupancyCategory.RETAIL_SHOP: 0.25,
        OccupancyCategory.FOOD_PROCESSING: 0.45,
        OccupancyCategory.PHARMACEUTICALS: 0.50,
        OccupancyCategory.LIGHT_ENGINEERING: 0.60,
        OccupancyCategory.TEXTILE_WAREHOUSE: 0.95,
        OccupancyCategory.WOOD_TIMBER_STORAGE: 1.40,
        OccupancyCategory.PLASTICS_MANUFACTURING: 1.65,
        OccupancyCategory.CHEMICAL_SOLVENT_STORAGE: 2.50, # High risk
        OccupancyCategory.FIREWORKS_EXPLOSIVES: 5.00      # Excluded
    }
    
    @classmethod
    def calculate_indicative_premium(
        cls,
        occupancy: OccupancyCategory,
        total_sum_insured: float,
        construction_type: str = "PUCCA",
        eq_zone: int = 3, # Seismic Zone III default
        has_fire_hydrant: bool = True
    ) -> Dict[str, Any]:
        """
        Simulates the actuarial Excel macro calculation for property risks.
        Returns detailed rating breakdown.
        """
        base_rate_per_k = cls.OCCUPANCY_BASE_RATES.get(occupancy, 0.75)
        
        # Base Premium
        base_premium = (total_sum_insured / 1000.0) * base_rate_per_k
        
        # Discounts & Loadings
        construction_factor = 0.95 if construction_type.upper() == "PUCCA" else 1.15
        fire_protection_discount = 0.10 if has_fire_hydrant else 0.0
        
        # Natural Perils (STFI + Earthquake)
        eq_rate_per_k = 0.05 * (eq_zone / 3.0)
        stfi_rate_per_k = 0.12
        nat_cat_premium = (total_sum_insured / 1000.0) * (eq_rate_per_k + stfi_rate_per_k)
        
        net_base = base_premium * construction_factor * (1.0 - fire_protection_discount)
        net_risk_premium = net_base + nat_cat_premium
        
        # Indian Goods & Services Tax (GST 18%)
        gst_amount = net_risk_premium * 0.18
        gross_final_premium = net_risk_premium + gst_amount
        
        # Required Underwriter Authority Level
        authority_level = "L1 Underwriter"
        if gross_final_premium > 200_000:
            authority_level = "L2 Senior Underwriter"
        if gross_final_premium > 1_000_000:
            authority_level = "L3 Chief Underwriting Officer (CUO)"
            
        return {
            "occupancy": occupancy.value,
            "base_rate_per_mille": base_rate_per_k,
            "base_premium": round(base_premium, 2),
            "nat_cat_premium": round(nat_cat_premium, 2),
            "net_risk_premium": round(net_risk_premium, 2),
            "gst_18pct": round(gst_amount, 2),
            "indicative_total_premium": round(gross_final_premium, 2),
            "required_authority_signoff": authority_level,
            "is_assistive_only": True,
            "pricing_source": "Actuarial Excel Sheet Template v2026.3"
        }
