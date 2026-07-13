import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from data_gen import get_dataset
from scoring import compute_health_card, risk_band, SUB_SCORE_LABELS

st.set_page_config(page_title="MSME Financial Health Card", layout="wide")

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

st.title("🏦 MSME Financial Health Card")
st.caption("AI-powered alternate-data credit assessment for New-to-Credit / New-to-Bank MSMEs — Prototype for IDBI Innovate 2026, Track 3")

st.warning("⚠️ All data shown is synthetic and fictional, generated for demonstration purposes only. No real customer or bank data is used.", icon="⚠️")

dataset = get_dataset()
names = [b["name"] for b in dataset]

col_select, col_info = st.columns([1, 2])
with col_select:
    selected_name = st.selectbox("Select an MSME profile", names)

business = next(b for b in dataset if b["name"] == selected_name)

with col_info:
    aa_consent = st.toggle("AA Data Consent Given (simulated)", value=business["aa"].get("available", False))

# Apply simulated consent toggle — revoking consent removes AA data from scoring, live
business_eval = dict(business)
business_eval["aa"] = dict(business["aa"])
business_eval["aa"]["available"] = aa_consent and business["aa"].get("available", False)

result = compute_health_card(business_eval)

st.session_state.audit_log.append({
    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Business": business["name"],
    "AA Consent": "Given" if aa_consent else "Revoked/Not Given",
    "Sources Used": result["sources_used"],
    "Score": result["final_score"] if result["final_score"] is not None else "N/A",
    "Confidence": result["confidence"],
    "Risk Band": risk_band(result["final_score"]),
})

st.divider()

# ---- Header: Score + Confidence ----
c1, c2, c3 = st.columns([1, 1, 2])

with c1:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=result["final_score"] if result["final_score"] is not None else 0,
        title={"text": "Financial Health Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#1f77b4"},
            "steps": [
                {"range": [0, 35], "color": "#f8d7da"},
                {"range": [35, 55], "color": "#fff3cd"},
                {"range": [55, 75], "color": "#d1ecf1"},
                {"range": [75, 100], "color": "#d4edda"},
            ],
        }
    ))
    fig.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.metric("Risk Band", risk_band(result["final_score"]))
    st.metric("Confidence Level", result["confidence"])
    st.metric("Data Sources Used", f"{result['sources_used']} / 4")

with c3:
    st.subheader("Business Snapshot")
    st.write(f"**Name:** {business['name']}")
    st.write(f"**Type:** {business['type']}")
    if result["missing_sources"]:
        missing_labels = ", ".join(SUB_SCORE_LABELS[k] for k in result["missing_sources"])
        st.info(f"ℹ️ Score computed on **{result['sources_used']} of 4** data sources. "
                f"Missing: {missing_labels}. Confidence reduced accordingly — this is a deliberate "
                f"design choice, not a data gap being hidden.")
    else:
        st.success("✅ All 4 data sources available — full confidence assessment.")

st.divider()

# ---- Sub-scores ----
st.subheader("Sub-Score Breakdown")
sub_cols = st.columns(4)
for i, key in enumerate(["gst", "upi", "aa", "epfo"]):
    with sub_cols[i]:
        val = result["sub_scores"][key]
        st.metric(SUB_SCORE_LABELS[key], f"{val}/100" if val is not None else "N/A")
        if val is not None:
            st.progress(val / 100)
        else:
            st.caption("Source unavailable")

st.divider()

# ---- Explainability Panel ----
st.subheader("📋 Underwriting Rationale (Explainability Panel)")
st.caption("Every line below is generated directly from the computed signals — not a generic LLM summary.")

any_notes = False
for key in ["gst", "upi", "aa", "epfo"]:
    notes = result["notes"][key]
    if notes:
        any_notes = True
        for n in notes:
            icon = "🚩" if ("review" in n.lower() or "unusual" in n.lower() or "flagged" in n.lower()) else "•"
            st.write(f"{icon} **[{SUB_SCORE_LABELS[key].split('(')[1].rstrip(')')}]** {n}")

if not any_notes:
    st.write("✅ No risk flags raised — all signals within normal ranges for this profile.")

st.divider()

# ---- Audit Trail ----
st.subheader("🔒 Consent & Audit Trail")
st.caption("Every scoring decision is logged with the consent state and data sources used at that moment — "
           "supports RBI Digital Lending Guidelines requirements for traceable, human-reviewable decisions.")

log_df = pd.DataFrame(st.session_state.audit_log)
csv = log_df.to_csv(index=False).encode("utf-8")  # build CSV from original types first
log_df_display = log_df.astype(str)  # force uniform string dtype — avoids pyarrow crash on mixed None/float columns
try:
    st.dataframe(log_df_display, use_container_width=True, hide_index=True)
except Exception:
    st.table(log_df_display)

st.download_button("Download Audit Log (CSV)", csv, "audit_log.csv", "text/csv")

if st.button("Clear Audit Log"):
    st.session_state.audit_log = []
    st.rerun()

st.divider()
st.caption("Prototype built with a rule-based, fully traceable scoring engine (no black-box model) — "
           "designed to map onto IDBI's ULI / OCEN / Account Aggregator ecosystem for production deployment. "
           "Consent-based data access and human-in-the-loop underwriting are core design assumptions, "
           "consistent with RBI Digital Lending Guidelines.")