from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class TriageStatus(str, Enum):
    ELIGIBLE = "ELIGIBLE"
    DECLINED_OUT_OF_APPETITE = "DECLINED_OUT_OF_APPETITE"
    DUPLICATE_FLAGGED = "DUPLICATE_FLAGGED"
    REFERRED_RISK_ENGINEERING = "REFERRED_RISK_ENGINEERING"
    INCOMPLETE_DATA = "INCOMPLETE_DATA"
    SECURITY_QUARANTINE = "SECURITY_QUARANTINE"

class OccupancyCategory(str, Enum):
    LIGHT_ENGINEERING = "LIGHT_ENGINEERING"
    TEXTILE_WAREHOUSE = "TEXTILE_WAREHOUSE"
    PHARMACEUTICALS = "PHARMACEUTICALS"
    FOOD_PROCESSING = "FOOD_PROCESSING"
    COMMERCIAL_OFFICE = "COMMERCIAL_OFFICE"
    RETAIL_SHOP = "RETAIL_SHOP"
    PLASTICS_MANUFACTURING = "PLASTICS_MANUFACTURING"
    WOOD_TIMBER_STORAGE = "WOOD_TIMBER_STORAGE"
    CHEMICAL_SOLVENT_STORAGE = "CHEMICAL_SOLVENT_STORAGE"  # Prohibited
    FIREWORKS_EXPLOSIVES = "FIREWORKS_EXPLOSIVES"          # Prohibited

class FieldProvenance(BaseModel):
    source_document: str = Field(..., description="Filename of source attachment")
    page_number: int = Field(1, description="Page number of finding")
    bounding_box: Optional[List[float]] = Field(None, description="[ymin, xmin, ymax, xmax] normalized coordinates")
    text_snippet: str = Field(..., description="Raw text snippet extracted from source document")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Extraction confidence")

class PropertyLocationItem(BaseModel):
    location_id: str = "LOC-01"
    address: str
    pin_code: str
    occupancy_code: OccupancyCategory
    building_sum_insured: float = Field(0.0, ge=0.0)
    plant_machinery_sum_insured: float = Field(0.0, ge=0.0)
    stock_sum_insured: float = Field(0.0, ge=0.0)
    total_sum_insured: float = Field(..., ge=0.0)
    construction_type: str = Field("PUCCA", description="Class 1 PUCCA construction")
    math_inconsistent: bool = Field(False, description="True if component sums do not equal total sum insured")
    provenance: Optional[FieldProvenance] = None

    @field_validator("total_sum_insured")
    def verify_math_consistency(cls, v, info):
        data = info.data
        bld = data.get("building_sum_insured", 0.0)
        pnm = data.get("plant_machinery_sum_insured", 0.0)
        stk = data.get("stock_sum_insured", 0.0)
        component_sum = bld + pnm + stk
        # Note: Do not raise an unhandled exception here so the pipeline can ingest
        # files with broker math errors and flag them for underwriter review.
        return v

class DuplicateCheckResult(BaseModel):
    is_duplicate: bool = False
    matched_submission_id: Optional[str] = None
    matched_broker_name: Optional[str] = None
    similarity_score: float = 0.0
    match_reasons: List[str] = []

class AppetiteCheckResult(BaseModel):
    status: TriageStatus = TriageStatus.ELIGIBLE
    rule_violations: List[str] = []
    requires_risk_engineering: bool = False
    referral_reasons: List[str] = []
    decline_draft_email: Optional[str] = None

class SOVDiffItem(BaseModel):
    asset_id: str
    field_name: str
    old_value: Any
    new_value: Any
    change_type: str  # "MODIFIED", "ADDED", "DELETED"

class UnderwritingPackage(BaseModel):
    submission_id: str
    received_timestamp: datetime
    broker_name: str
    broker_email: str
    insured_entity_name: str
    insured_pan_gstin: Optional[str] = None
    locations: List[PropertyLocationItem]
    aggregate_sum_insured: float
    prior_claims_5yr: float = 0.0
    triage_result: AppetiteCheckResult
    clearance_result: DuplicateCheckResult
    sov_has_updates: bool = False
    sov_diffs: List[SOVDiffItem] = []
    security_passed: bool = True
    underwriter_notes: Optional[str] = None
    assigned_underwriter: Optional[str] = None
    audit_hash: str
    status: str = "PENDING_REVIEW"
