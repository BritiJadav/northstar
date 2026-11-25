import time
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1/submissions/ingest"

SAMPLE_BROKER_SUBMISSIONS = [
    {
        "broker_name": "Howden Insurance Brokers India",
        "broker_email": "commercial.property@howdenindia.com",
        "document_filename": "Howden_AutoParts_Proposal.pdf",
        "raw_document_text": """
        INSURED: M/s Precision Gearwheels & Transmissions Pvt Ltd
        ADDRESS: Plot 52, Chakan Industrial Phase II, Pune 410501
        OCCUPANCY: Light Engineering - Automotive Transmission Gears & CNC Milling
        BUILDING SUM INSURED: ₹4,50,00,000
        PLANT & MACHINERY: ₹7,00,00,000
        STOCK SUM INSURED: ₹1,50,00,000
        TOTAL SUM INSURED: ₹13,00,00,000
        CONSTRUCTION: Class 1 PUCCA (RCC Columns, Brickwork, Non-combustible roof)
        FIRE PROTECTION: Dedicated Yard Hydrant System with 2,500 LPM Pump
        PRIOR 3-YEAR CLAIMS: Nil
        """
    },
    {
        "broker_name": "Marsh McLennan India",
        "broker_email": "sme.intake@marshmclennan.co.in",
        "document_filename": "Marsh_Textile_Logistics.pdf",
        "raw_document_text": """
        CLIENT NAME: M/s Western Spun Fabric Warehousing LLP
        RISK LOCATION: Gala 14, Bhiwandi Logistics Corridor, Thane 421302
        OCCUPANCY: Textile Warehouse - Raw Cotton Bales & Synthetic Yarn Storage
        BUILDING SUM INSURED: ₹3,00,00,000
        PLANT AND MACHINERY: ₹50,00,000
        STOCK SUM INSURED: ₹4,50,00,000
        TOTAL SUM INSURED: ₹8,00,00,000
        CONSTRUCTION: Class 1 PUCCA
        FIRE EXTINGUISHERS: Installed as per IS 2190
        """
    },
    {
        "broker_name": "Apex Insurance Intermediaries",
        "broker_email": "triage@apexbrokers.co.in",
        "document_filename": "Apex_Prohibited_Fireworks.pdf",
        "raw_document_text": """
        PROPOSAL FOR: Sivakasi Star Fireworks & Sparkler Manufacturing
        LOCATION: Sivakasi Bypass Road, Virudhunagar 626124
        OCCUPANCY: Manufacturing of Fireworks, Pyrotechnics and Safety Matches
        BUILDING SUM INSURED: ₹1,00,00,000
        PLANT & MACHINERY: ₹50,00,000
        STOCK SUM INSURED: ₹1,00,00,000
        TOTAL SUM INSURED: ₹2,50,00,000
        """
    },
    {
        "broker_name": "Aon India Insurance Brokers",
        "broker_email": "commercial@aon.com",
        "document_filename": "Aon_Duplicate_Filing.pdf",
        "raw_document_text": """
        INSURED ENTITY: Precision Gearwheels and Transmissions Private Limited
        LOCATION: Plot 52, Chakan Phase II, Pune 410501
        OCCUPANCY: Auto Component Manufacturing
        BUILDING SUM INSURED: ₹4,50,00,000
        PLANT & MACHINERY: ₹7,00,00,000
        STOCK SUM INSURED: ₹1,50,00,000
        TOTAL SUM INSURED: ₹13,00,00,000
        """
    }
]

def simulate_email_inbox():
    print("=" * 70)
    print(" NORTHSTAR AUTOMATED EMAIL INGESTION LISTENER (SIMULATING M365 INBOX)")
    print("=" * 70)
    print("Connecting to regional shared mailbox poller...\n")
    
    for idx, sub in enumerate(SAMPLE_BROKER_SUBMISSIONS, 1):
        print(f"[{idx}/4] Inbound Email Received from: {sub['broker_name']} ({sub['broker_email']})")
        print(f"       Attachment Detected: {sub['document_filename']}")
        
        try:
            start_time = time.time()
            response = requests.post(BASE_URL, json=sub, timeout=10)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                triage = data["triage_result"]["status"]
                is_dup = data["clearance_result"]["is_duplicate"]
                
                print(f"       ✔ Ingested & Triaged in {elapsed:.2f}s | Submission ID: {data['submission_id']}")
                print(f"       ✔ Triage Status: {triage}")
                if is_dup:
                    print(f"       ⚠ Clearance Alert: DUPLICATE detected ({data['clearance_result']['similarity_score']*100:.1f}% match with prior broker)")
                if triage == "DECLINED_OUT_OF_APPETITE":
                    print(f"       ✖ Out of Appetite: Auto-draft decline notice created (Pune keying bypassed).")
            else:
                print(f"       ✖ Error: HTTP {response.status_code} - {response.text}")
        except Exception as e:
            print(f"       ✖ Connection Error: {e}")
            
        print("-" * 70)
        time.sleep(1.5)
        
    print("\nBatch Ingestion Complete! Open http://localhost:8000 to view active queue.")

if __name__ == "__main__":
    simulate_email_inbox()
