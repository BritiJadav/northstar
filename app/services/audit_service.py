import sqlite3
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.config import settings

def get_utc_now_iso():
    return datetime.now(timezone.utc).isoformat()

class AuditService:
    """
    Implements IRDAI File-and-Use & Governance audit logging:
    'Every quote must show the data, rate and authority used' (PDF p. 20).
    'The bank/insurer must be able to reconstruct any decision for eight years' (PDF p. 6, 20).
    """
    
    @classmethod
    def init_db(cls):
        conn = sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()
        
        # Submissions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                submission_id TEXT PRIMARY KEY,
                received_timestamp TEXT,
                broker_name TEXT,
                broker_email TEXT,
                insured_entity_name TEXT,
                pin_code TEXT,
                aggregate_sum_insured REAL,
                triage_status TEXT,
                is_duplicate INTEGER,
                package_json TEXT,
                audit_hash TEXT,
                status TEXT
            )
        """)
        
        # Tamper-Evident Audit Event Trail
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_trail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                submission_id TEXT,
                event_type TEXT,
                performed_by TEXT,
                details_json TEXT,
                record_hash TEXT
            )
        """)
        
        conn.commit()
        conn.close()

    @classmethod
    def record_submission(cls, pkg: Dict[str, Any]) -> str:
        cls.init_db()
        conn = sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()
        
        sub_id = pkg["submission_id"]
        ts = pkg.get("received_timestamp", get_utc_now_iso())
        package_str = json.dumps(pkg, default=str)
        audit_hash = hashlib.sha256(package_str.encode()).hexdigest()
        
        pin = pkg["locations"][0]["pin_code"] if pkg.get("locations") else ""
        
        cursor.execute("""
            INSERT OR REPLACE INTO submissions (
                submission_id, received_timestamp, broker_name, broker_email,
                insured_entity_name, pin_code, aggregate_sum_insured,
                triage_status, is_duplicate, package_json, audit_hash, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sub_id, ts, pkg["broker_name"], pkg["broker_email"],
            pkg["insured_entity_name"], pin, pkg["aggregate_sum_insured"],
            pkg["triage_result"]["status"], 1 if pkg["clearance_result"]["is_duplicate"] else 0,
            package_str, audit_hash, pkg.get("status", "PENDING_REVIEW")
        ))
        
        # Log creation event
        cursor.execute("""
            INSERT INTO audit_trail (timestamp, submission_id, event_type, performed_by, details_json, record_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            get_utc_now_iso(), sub_id, "SUBMISSION_INGESTED_AND_TRIAGED",
            "AI_GATEWAY_PIPELINE", json.dumps({"triage": pkg["triage_result"]["status"], "hash": audit_hash}),
            audit_hash
        ))
        
        conn.commit()
        conn.close()
        return audit_hash

    @classmethod
    def get_all_submissions(cls) -> List[Dict[str, Any]]:
        cls.init_db()
        conn = sqlite3.connect(settings.DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM submissions ORDER BY received_timestamp DESC")
        rows = cursor.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["package"] = json.loads(d["package_json"])
            result.append(d)
        conn.close()
        return result

    @classmethod
    def get_submission_by_id(cls, sub_id: str) -> Optional[Dict[str, Any]]:
        cls.init_db()
        conn = sqlite3.connect(settings.DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM submissions WHERE submission_id = ?", (sub_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        d = dict(row)
        d["package"] = json.loads(d["package_json"])
        return d

    @classmethod
    def underwriter_sign_off(cls, sub_id: str, underwriter_id: str, approved_premium: float, notes: str) -> str:
        cls.init_db()
        conn = sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()
        
        ts = get_utc_now_iso()
        audit_payload = {
            "underwriter_id": underwriter_id,
            "approved_premium": approved_premium,
            "notes": notes,
            "timestamp": ts
        }
        event_hash = hashlib.sha256(json.dumps(audit_payload).encode()).hexdigest()
        
        cursor.execute("""
            UPDATE submissions SET status = 'QUOTE_APPROVED', triage_status = 'APPROVED_BY_UW'
            WHERE submission_id = ?
        """, (sub_id,))
        
        cursor.execute("""
            INSERT INTO audit_trail (timestamp, submission_id, event_type, performed_by, details_json, record_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            ts, sub_id, "UNDERWRITER_QUOTE_SIGN_OFF",
            underwriter_id, json.dumps(audit_payload), event_hash
        ))
        
        conn.commit()
        conn.close()
        return event_hash
