# SKBank Fraud Detection Dashboard

Chinese version: [README_zh.md](./README_zh.md)

A multi-page Dash application for abnormal transaction detection workflows, combining:
- Transaction and balance visualization
- Industry distribution analysis
- Risk alarm inspection
- AI model risk segmentation
- Alert notification email list management

## Tech Stack

- Python 3.9-3.11 recommended
- Dash 2.x
- Plotly
- Pandas
- Gunicorn (deployment)

## Project Structure

```text
.
├── app.py                            # Dash entrypoint (use_pages=True)
├── Procfile                          # web: gunicorn app:server
├── requirements.txt
├── Data/
│   ├── CFMASTER.csv
│   ├── CFMASTER_SAR.csv
│   ├── SAMASTER_SAR.csv
│   └── SATXNREC_SAR.csv
├── model_prediction/
│   ├── 20230930.csv
│   └── 20231001.csv
├── pages/
│   ├── home.py
│   ├── transaction.py
│   ├── industry_risk.py
│   ├── risk_alarm.py
│   ├── model_prediction.py
│   └── alert_notification/
│       ├── alert_notification.py
│       └── emails.json
├── images/
└── html/
```

## Local Setup

1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Start the app

```bash
python3 app.py
```

4. Open in browser

```text
http://127.0.0.1:8050
```

## Deployment

The `Procfile` is already configured:

```text
web: gunicorn app:server
```

You can deploy to platforms supporting Procfile-style startup.

## Pages

- `/`: Home and system overview
- `/ai_model`: Model metrics and risk-level distribution
- `/alert_notification`: Add/remove alert emails
- `Transaction Data Dashboard`: Transaction and balance chart by account
- `Industry distribution`: Industry counts for SAR vs non-SAR accounts
- `風險警示平台`: Treemap for risk signal flags by account and date

## Data Requirements

- CSV files under `Data/` and `model_prediction/` are required runtime inputs.
- If you replace datasets, keep column names consistent with current code.

## Notes

- `pages/alert_notification/emails.json` is a local state file and will be overwritten by UI actions.
- Some dropdowns use hardcoded defaults; charts may render empty initially if the default value is not present in your data.
- For production, disable debug mode (`app.py` currently uses `app.run(debug=True)`).

## Quick Check

Run a basic syntax check:

```bash
python3 -m compileall -q app.py pages
```
