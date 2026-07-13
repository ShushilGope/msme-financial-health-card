# MSME Financial Health Card — Prototype
**IDBI Innovate 2026 | Track 3: Financial Inclusion / Digital Lending / Credit Decisioning**

## Status
This is a **Round 1 prototype submission** — a working proof-of-concept, not a
production system. It demonstrates the core scoring logic, explainability
approach, and UX pattern; it is not connected to any live bank, GST, UPI, AA,
or EPFO systems.

## What this is
An explainable, alternate-data credit assessment prototype for New-to-Credit (NTC) and
New-to-Bank (NTB) MSMEs. It aggregates four signal sources — GST, UPI, Account
Aggregator (AA) bank data, and EPFO — into a single Financial Health Score, with:

- **Partial-data resilience**: scores confidently even when 1-2 sources are missing,
  with confidence level adjusted accordingly.
- **Rule-based, fully traceable scoring**: every sub-score is computed from real
  formulas over the input signals — not a black-box model.
- **Explainability panel**: plain-language underwriting rationale generated directly
  from the same signals used for scoring — including red-flag detection for
  suspicious patterns (e.g. circular-transaction / gamed-data signatures) that a
  raw score alone would miss.
- **Consent & audit trail**: simulated AA consent toggle, live score recomputation
  on consent change, and a downloadable audit log of every scoring decision.

All data is **100% synthetic and fictional** — no real customer, bank, or GST data
is used anywhere in this prototype.

## Limitations (honest, by design)
- **Scoring weights are judgment-based, not data-derived.** No real default/repayment
  outcome data was available to train or calibrate weights. Weights reflect
  directional BFSI underwriting logic (GST/UPI weighted highest as hardest-to-fake
  activity signals), not statistical validation.
- **Only one fraud/gaming pattern is detected** (circular-transaction signature via
  UPI volatility + transaction count). Real-world gaming behavior is far more varied.
- **Only 4 data sources.** Utility bill payments, e-way bill data, Udyam registration,
  and trade-reference data are not yet included.
- **No live API integration.** GST, UPI, AA, and EPFO data are simulated; production
  deployment requires real integration with GSTN, NPCI/UPI, Sahamati (AA), and EPFO
  data services, plus ULI/OCEN connectivity.
- **Rule-based, not ML.** Deliberate choice for Round 1 — see Roadmap below.

## Roadmap (Phase 2+)
- Calibrate scoring weights using logistic regression / gradient boosting once real
  historical repayment outcome data is available (via IDBI sandbox access).
- Expand fraud/anomaly detection beyond circular-transaction patterns (e.g. invoice
  mismatch detection, sudden vendor concentration shifts).
- Add utility bill payments, e-way bill data, Udyam registration, and trade-reference
  signals as additional scoring inputs.
- Live integration with GSTN, UPI/NPCI, Sahamati Account Aggregator network, EPFO,
  and IDBI's ULI/OCEN ecosystem.
- Portfolio-level dashboard (risk concentration, expected default distribution
  across a loan book, not just single-applicant scoring).
- Human-in-the-loop review workflow aligned with RBI Digital Lending Guidelines.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `data_gen.py` — synthetic MSME dataset (15 profiles: strong, weak, borderline,
  missing-source, and "trap"/gamed-data cases)
- `scoring.py` — scoring engine + explainability logic
- `app.py` — Streamlit dashboard

## Deploy for free (for submission link)
1. Push this folder to a public GitHub repo.
2. Go to https://share.streamlit.io, sign in with GitHub, click "New app".
3. Select the repo, branch, and set main file path to `app.py`.
4. Deploy — you'll get a public URL to use as your "Project Deployment Link".

## Production integration path
Each ingestion function in `scoring.py` (`score_gst`, `score_upi`, `score_aa`,
`score_epfo`) is written to take a normalized dict as input — designed so that in
production, `data_gen.py`'s synthetic dicts would be replaced by live payloads from
GST/GSTN APIs, UPI transaction feeds, the Account Aggregator consent flow, and EPFO
data services, without changing the scoring logic itself.