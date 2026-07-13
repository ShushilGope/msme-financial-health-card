"""
Synthetic MSME dataset generator for the Financial Health Card prototype.
Generates 15 fictional MSME profiles with GST, UPI, AA (bank statement), and EPFO
signals — with deliberate variance: strong, weak, borderline, missing-data, and
'trap' (gamed-data) cases. No real customer data is used anywhere.
"""
import random

random.seed(42)

BUSINESS_TYPES = ["Trader", "Manufacturer", "Service Provider", "Retailer", "Exporter"]

def gen_business(name, profile_type):
    """profile_type in: strong, weak, borderline, missing_epfo, missing_aa, trap"""
    b = {"name": name, "type": random.choice(BUSINESS_TYPES), "profile_note": profile_type}

    if profile_type == "strong":
        b["gst"] = {"available": True, "monthly_turnover_lakhs": round(random.uniform(15, 40), 1),
                    "filing_on_time_pct": random.randint(90, 100), "turnover_growth_yoy_pct": random.randint(10, 25)}
        b["upi"] = {"available": True, "monthly_inflow_lakhs": round(random.uniform(12, 35), 1),
                    "inflow_volatility_pct": random.randint(5, 15), "txn_count_monthly": random.randint(300, 800)}
        b["aa"] = {"available": True, "avg_bank_balance_lakhs": round(random.uniform(3, 10), 1),
                   "bounced_payments_6m": 0, "existing_loan_repayment_score": random.randint(85, 100)}
        b["epfo"] = {"available": True, "employee_count": random.randint(8, 25),
                     "contribution_consistency_pct": random.randint(90, 100), "headcount_trend": "growing"}

    elif profile_type == "weak":
        b["gst"] = {"available": True, "monthly_turnover_lakhs": round(random.uniform(2, 6), 1),
                    "filing_on_time_pct": random.randint(40, 65), "turnover_growth_yoy_pct": random.randint(-15, 0)}
        b["upi"] = {"available": True, "monthly_inflow_lakhs": round(random.uniform(1, 5), 1),
                    "inflow_volatility_pct": random.randint(40, 70), "txn_count_monthly": random.randint(30, 100)}
        b["aa"] = {"available": True, "avg_bank_balance_lakhs": round(random.uniform(0.1, 1), 1),
                   "bounced_payments_6m": random.randint(3, 8), "existing_loan_repayment_score": random.randint(30, 55)}
        b["epfo"] = {"available": True, "employee_count": random.randint(1, 3),
                     "contribution_consistency_pct": random.randint(30, 60), "headcount_trend": "declining"}

    elif profile_type == "borderline":
        b["gst"] = {"available": True, "monthly_turnover_lakhs": round(random.uniform(6, 14), 1),
                    "filing_on_time_pct": random.randint(65, 85), "turnover_growth_yoy_pct": random.randint(-5, 10)}
        b["upi"] = {"available": True, "monthly_inflow_lakhs": round(random.uniform(5, 12), 1),
                    "inflow_volatility_pct": random.randint(20, 40), "txn_count_monthly": random.randint(100, 300)}
        b["aa"] = {"available": True, "avg_bank_balance_lakhs": round(random.uniform(0.5, 3), 1),
                   "bounced_payments_6m": random.randint(0, 2), "existing_loan_repayment_score": random.randint(55, 75)}
        b["epfo"] = {"available": True, "employee_count": random.randint(3, 8),
                     "contribution_consistency_pct": random.randint(60, 85), "headcount_trend": "stable"}

    elif profile_type == "missing_epfo":
        b["gst"] = {"available": True, "monthly_turnover_lakhs": round(random.uniform(8, 20), 1),
                    "filing_on_time_pct": random.randint(75, 95), "turnover_growth_yoy_pct": random.randint(5, 18)}
        b["upi"] = {"available": True, "monthly_inflow_lakhs": round(random.uniform(6, 18), 1),
                    "inflow_volatility_pct": random.randint(15, 30), "txn_count_monthly": random.randint(150, 400)}
        b["aa"] = {"available": True, "avg_bank_balance_lakhs": round(random.uniform(1, 5), 1),
                   "bounced_payments_6m": random.randint(0, 1), "existing_loan_repayment_score": random.randint(70, 90)}
        b["epfo"] = {"available": False}  # no employees / not registered — common for sole proprietors

    elif profile_type == "missing_aa":
        b["gst"] = {"available": True, "monthly_turnover_lakhs": round(random.uniform(5, 15), 1),
                    "filing_on_time_pct": random.randint(70, 90), "turnover_growth_yoy_pct": random.randint(0, 15)}
        b["upi"] = {"available": True, "monthly_inflow_lakhs": round(random.uniform(4, 14), 1),
                    "inflow_volatility_pct": random.randint(20, 35), "txn_count_monthly": random.randint(100, 350)}
        b["aa"] = {"available": False}  # AA consent not yet given
        b["epfo"] = {"available": True, "employee_count": random.randint(2, 6),
                     "contribution_consistency_pct": random.randint(65, 88), "headcount_trend": "stable"}

    elif profile_type == "trap":
        # Looks strong on GST turnover, but UPI shows classic circular-transaction /
        # layering pattern (very high txn count, near-zero net balance growth, no volatility)
        b["gst"] = {"available": True, "monthly_turnover_lakhs": round(random.uniform(20, 35), 1),
                    "filing_on_time_pct": random.randint(85, 100), "turnover_growth_yoy_pct": random.randint(30, 50)}
        b["upi"] = {"available": True, "monthly_inflow_lakhs": round(random.uniform(20, 35), 1),
                    "inflow_volatility_pct": random.randint(1, 4), "txn_count_monthly": random.randint(900, 1500)}
        b["aa"] = {"available": True, "avg_bank_balance_lakhs": round(random.uniform(0.05, 0.3), 1),
                   "bounced_payments_6m": 0, "existing_loan_repayment_score": random.randint(60, 75)}
        b["epfo"] = {"available": True, "employee_count": random.randint(1, 2),
                     "contribution_consistency_pct": random.randint(40, 60), "headcount_trend": "flat"}

    return b


PROFILES = [
    ("Shree Ganesh Traders", "strong"),
    ("Vikas Auto Components Pvt Ltd", "strong"),
    ("Radha Textiles", "borderline"),
    ("Kumar Electricals", "borderline"),
    ("Sunrise Food Processing", "weak"),
    ("Lakshmi General Store", "weak"),
    ("Precision Tools Manufacturing", "missing_epfo"),
    ("Bharat Logistics Solutions", "missing_epfo"),
    ("New Age Digital Services", "missing_aa"),
    ("Om Sai Enterprises", "missing_aa"),
    ("Global Exports Co", "trap"),
    ("Metro Trading House", "trap"),
    ("Annapurna Caterers", "borderline"),
    ("Sharma Hardware Mart", "weak"),
    ("Innovative Plastics Ltd", "strong"),
]

def get_dataset():
    return [gen_business(name, ptype) for name, ptype in PROFILES]
