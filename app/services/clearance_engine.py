import re
import difflib
from typing import List, Dict, Optional
from app.schemas import DuplicateCheckResult

def normalize_text(text: str) -> str:
    """Normalize company name: lowercase, strip punctuation, remove legal corporate suffixes."""
    if not text:
        return ""
    text = text.lower().strip()
    # Strip common corporate abbreviations in India
    suffixes = [
        r"\bpvt\b", r"\bltd\b", r"\bprivate\b", r"\blimited\b",
        r"\bllp\b", r"\benterprises\b", r"\bindustries\b", r"\bcorp\b",
        r"\btechnologies\b", r"\bcorporation\b"
    ]
    for s in suffixes:
        text = re.sub(s, "", text)
    text = re.sub(r"[^\w\s]", "", text)
    return " ".join(text.split())

def string_similarity(s1: str, s2: str) -> float:
    """Compute string similarity using SequenceMatcher ratio."""
    norm1 = normalize_text(s1)
    norm2 = normalize_text(s2)
    if not norm1 or not norm2:
        return 0.0
    if norm1 == norm2:
        return 1.0
    # Also check token set similarity
    tokens1 = set(norm1.split())
    tokens2 = set(norm2.split())
    token_overlap = len(tokens1.intersection(tokens2)) / max(len(tokens1.union(tokens2)), 1)
    seq_ratio = difflib.SequenceMatcher(None, norm1, norm2).ratio()
    return max(seq_ratio, token_overlap)

class MultiBrokerClearanceEngine:
    """
    Solves the 18% duplicate submission problem (PDF p. 19).
    Detects when competing brokers submit the identical corporate risk to NorthStar.
    """
    
    @classmethod
    def check_duplicate(
        cls,
        new_insured_name: str,
        new_pin_code: str,
        new_sum_insured: float,
        new_broker_name: str,
        existing_submissions: List[Dict]
    ) -> DuplicateCheckResult:
        
        highest_score = 0.0
        matched_sub = None
        match_reasons = []
        
        for sub in existing_submissions:
            # Skip checking against the same broker's revision (handled by thread diff)
            if sub.get("broker_name", "").lower() == new_broker_name.lower():
                continue
                
            existing_name = sub.get("insured_entity_name", "")
            existing_pin = sub.get("pin_code", "")
            existing_si = float(sub.get("aggregate_sum_insured", 0.0))
            
            name_sim = string_similarity(new_insured_name, existing_name)
            pin_match = (new_pin_code.strip() == existing_pin.strip()) if (new_pin_code and existing_pin) else False
            
            # Sum insured closeness (within 15% tolerance)
            si_diff_pct = abs(new_sum_insured - existing_si) / max(existing_si, 1.0)
            si_close = (si_diff_pct <= 0.15) if (new_sum_insured > 0 and existing_si > 0) else False
            
            # Composite Scoring:
            # If PIN matches and Name similarity is > 75%, or Name similarity > 90%
            composite_score = 0.0
            reasons = []
            
            if pin_match:
                composite_score = (name_sim * 0.7) + 0.3
                reasons.append(f"Matching Property PIN Code: {new_pin_code}")
            else:
                composite_score = name_sim
                
            if si_close:
                composite_score = min(composite_score + 0.1, 1.0)
                reasons.append(f"Comparable Sum Insured (₹{new_sum_insured:,.0f} vs ₹{existing_si:,.0f})")
                
            if name_sim >= 0.70:
                reasons.append(f"Entity Name Match ({name_sim*100:.1f}%): '{new_insured_name}' vs '{existing_name}'")
                
            if composite_score > highest_score and composite_score >= 0.80:
                highest_score = composite_score
                matched_sub = sub
                match_reasons = reasons

        if matched_sub and highest_score >= 0.80:
            return DuplicateCheckResult(
                is_duplicate=True,
                matched_submission_id=matched_sub.get("submission_id"),
                matched_broker_name=matched_sub.get("broker_name"),
                similarity_score=round(highest_score, 3),
                match_reasons=match_reasons
            )
            
        return DuplicateCheckResult(
            is_duplicate=False,
            similarity_score=round(highest_score, 3),
            match_reasons=[]
        )
