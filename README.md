# MSME Financial Health Card — Prototype
**IDBI Innovate 2026 | Track 3: Financial Inclusion / Digital Lending / Credit Decisioning**

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

All data is **100% synthetic and fictional** — no real customer, bank, or GST data
is used anywhere in this prototype.

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
