"""
Scoring engine for the MSME Financial Health Card.
Rule-based, transparent, and traceable — every number in the explanation is
directly computed from the input signals (no LLM narration layer), so the
'explainability' is real, not decorative.
"""

def score_gst(gst):
    if not gst.get("available"):
        return None, []
    notes = []
    turnover_score = min(100, gst["monthly_turnover_lakhs"] * 3)
    filing_score = gst["filing_on_time_pct"]
    growth = gst["turnover_growth_yoy_pct"]
    growth_score = max(0, min(100, 50 + growth * 2))
    sub = round((turnover_score * 0.4 + filing_score * 0.35 + growth_score * 0.25), 1)
    if gst["filing_on_time_pct"] < 70:
        notes.append(f"GST filing consistency is low ({gst['filing_on_time_pct']}% on-time) — a compliance risk signal.")
    if growth < 0:
        notes.append(f"YoY turnover declined {abs(growth)}% — revenue trend is negative.")
    if growth > 25 and gst["monthly_turnover_lakhs"] > 15:
        notes.append(f"Turnover growth of {growth}% combined with high absolute turnover is unusually steep — worth independent verification.")
    return sub, notes

def score_upi(upi):
    if not upi.get("available"):
        return None, []
    notes = []
    inflow_score = min(100, upi["monthly_inflow_lakhs"] * 4)
    volatility = upi["inflow_volatility_pct"]
    stability_score = max(0, 100 - volatility * 1.5)
    txn_density_score = min(100, upi["txn_count_monthly"] / 8)
    sub = round((inflow_score * 0.4 + stability_score * 0.35 + txn_density_score * 0.25), 1)
    if volatility > 40:
        notes.append(f"Cash inflow volatility is high ({volatility}%) — irregular revenue pattern.")
    if volatility < 5 and upi["txn_count_monthly"] > 800:
        notes.append(f"Extremely low volatility ({volatility}%) paired with very high transaction count ({upi['txn_count_monthly']}/mo) resembles a circular-transaction pattern rather than organic business activity — flagged for manual review.")
    return sub, notes

def score_aa(aa):
    if not aa.get("available"):
        return None, []
    notes = []
    balance_score = min(100, aa["avg_bank_balance_lakhs"] * 15)
    bounce_penalty = aa["bounced_payments_6m"] * 12
    bounce_score = max(0, 100 - bounce_penalty)
    repayment_score = aa["existing_loan_repayment_score"]
    sub = round((balance_score * 0.3 + bounce_score * 0.35 + repayment_score * 0.35), 1)
    if aa["bounced_payments_6m"] > 2:
        notes.append(f"{aa['bounced_payments_6m']} bounced payments in the last 6 months — repayment reliability concern.")
    if aa["avg_bank_balance_lakhs"] < 0.5 and aa["existing_loan_repayment_score"] > 55:
        notes.append(f"Average bank balance is thin (₹{aa['avg_bank_balance_lakhs']}L) despite healthy repayment history — limited cash buffer for shocks.")
    return sub, notes

def score_epfo(epfo):
    if not epfo.get("available"):
        return None, []
    notes = []
    headcount_score = min(100, epfo["employee_count"] * 6)
    consistency_score = epfo["contribution_consistency_pct"]
    trend_bonus = {"growing": 15, "stable": 0, "flat": -5, "declining": -20}.get(epfo["headcount_trend"], 0)
    sub = round(max(0, min(100, (headcount_score * 0.4 + consistency_score * 0.6) + trend_bonus)), 1)
    if epfo["contribution_consistency_pct"] < 65:
        notes.append(f"EPFO contribution consistency is low ({epfo['contribution_consistency_pct']}%) — payroll instability signal.")
    if epfo["headcount_trend"] == "declining":
        notes.append("Employee headcount is declining — an early stress signal that often precedes revenue softness.")
    return sub, notes


SUB_SCORE_LABELS = {
    "gst": "Compliance & Revenue Trend (GST)",
    "upi": "Cash Flow Stability (UPI)",
    "aa": "Repayment & Liquidity (AA)",
    "epfo": "Payroll Stability (EPFO)",
}

WEIGHTS = {"gst": 0.30, "upi": 0.30, "aa": 0.25, "epfo": 0.15}


def compute_health_card(business):
    scores = {}
    notes = {}
    for key, fn in [("gst", score_gst), ("upi", score_upi), ("aa", score_aa), ("epfo", score_epfo)]:
        s, n = fn(business[key])
        scores[key] = s
        notes[key] = n

    available = {k: v for k, v in scores.items() if v is not None}
    if not available:
        return {"final_score": None, "confidence": "None", "sub_scores": scores, "notes": notes}

    # Redistribute weight proportionally across available sources
    total_weight = sum(WEIGHTS[k] for k in available)
    final_score = sum(available[k] * (WEIGHTS[k] / total_weight) for k in available)
    final_score = round(final_score, 1)

    n_sources = len(available)
    confidence = {4: "High", 3: "Medium", 2: "Low-Medium", 1: "Low"}.get(n_sources, "Very Low")

    missing = [k for k in scores if scores[k] is None]

    return {
        "final_score": final_score,
        "confidence": confidence,
        "sources_used": n_sources,
        "missing_sources": missing,
        "sub_scores": scores,
        "notes": notes,
    }


def risk_band(score):
    if score is None:
        return "Insufficient Data"
    if score >= 75:
        return "Low Risk"
    if score >= 55:
        return "Moderate Risk"
    if score >= 35:
        return "Elevated Risk"
    return "High Risk"
