import re
from typing import Tuple, Dict, List

class SecurityGuardrail:
    """
    Enforces Trust Boundary 1 and Trust Boundary 3:
    - Indirect Prompt Injection Defense
    - DPDP Act 2023 PII Sanitization
    - Input Validation
    """
    
    INJECTION_PATTERNS = [
        r"ignore\s+(?:all\s+)?previous\s+instructions",
        r"system\s+prompt\s+override",
        r"you\s+are\s+now\s+(?:in\s+)?maintenance\s+mode",
        r"forget\s+all\s+(?:prior\s+)?rules",
        r"set\s+risk_category\s*=",
        r"quote_premium\s*=",
        r"bypass\s+underwriting",
        r"auto-quote\s+approved",
        r"disregard\s+guidelines"
    ]
    
    PAN_REGEX = r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b"
    PHONE_REGEX = r"\b(?:\+91[\-\s]?)?[6789]\d{9}\b"
    AADHAAR_REGEX = r"\b\d{4}\s?\d{4}\s?\d{4}\b"
    
    @classmethod
    def scan_for_prompt_injection(cls, text: str) -> Tuple[bool, List[str]]:
        """
        Scans untrusted broker text (from emails, PDFs, OCR) for adversarial prompt injection tokens.
        Returns: (is_malicious, matched_patterns)
        """
        if not text:
            return False, []
            
        detected = []
        for pattern in cls.INJECTION_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detected.append(pattern)
                
        return (len(detected) > 0, detected)
        
    @classmethod
    def mask_dpdp_pii(cls, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Complies with DPDP Act 2023 data minimization mandate.
        Masks personal identifiers before sending payload to AI Gateway.
        Returns: (masked_text, token_mapping)
        """
        if not text:
            return "", {}
            
        token_map = {}
        masked_text = text
        
        # 1. Mask Phone Numbers
        def replace_phone(match):
            val = match.group(0)
            token = f"[MASKED_PHONE_{len(token_map)+1}]"
            token_map[token] = val
            return token
            
        masked_text = re.sub(cls.PHONE_REGEX, replace_phone, masked_text)
        
        # 2. Mask Aadhaar
        def replace_aadhaar(match):
            val = match.group(0)
            token = f"[MASKED_AADHAAR_{len(token_map)+1}]"
            token_map[token] = val
            return token
            
        masked_text = re.sub(cls.AADHAAR_REGEX, replace_aadhaar, masked_text)
        
        return masked_text, token_map

    @classmethod
    def sanitize_untrusted_input(cls, raw_content: str) -> Tuple[str, bool, List[str]]:
        """Runs full sanitization and returns (clean_text, injection_detected, detected_threats)"""
        is_injected, threats = cls.scan_for_prompt_injection(raw_content)
        if is_injected:
            # Strip injected instructions while preserving document data
            clean_text = raw_content
            for p in cls.INJECTION_PATTERNS:
                clean_text = re.sub(p, "[SECURITY_STRIPPED_CONTENT]", clean_text, flags=re.IGNORECASE)
            return clean_text, True, threats
        return raw_content, False, []
