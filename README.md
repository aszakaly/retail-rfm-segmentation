# Retail RFM Segmentation

Customer segmentation for a UK-based online retailer (the *Online Retail II*
dataset), taking raw transaction data through to two decision-ready dashboards.

**▶ Live dashboards:** https://aszakaly.github.io/retail-rfm-segmentation/
(executive overview is the entry page; link through to the operative view).

---

## Purpose

Turn ~1.07M raw sales line-items into a small set of **named, strategy-ready
customer segments** so the business can answer a single question: *which
customers deserve which action, and where is the revenue actually concentrated?*

The headline finding drives everything downstream: **Champions + Loyal Customers
are 36.5% of the customer base but 82.8% of revenue.** Strategy must protect that
core, rescue the high-value lapsers, and nurture newcomers — not spend evenly
across everyone.

---

## Key steps

1. **Data discovery** — profile the raw Excel: 2 sheets (FY2009–10, FY2010–11),
   8 columns, ~1.07M rows; found 20.5% missing Customer IDs, cancellation
   invoices, non-product codes, and a Dec-2010 sheet overlap.
2. **Data cleaning** — `01_clean_data.py` → `retail_clean.csv` (+ a full audit
   of every removed row).
3. **RFM modelling** — `02_rfm_segments.py` → `rfm_segments.csv` (per-customer
   scores + segment), validated with K-Means.
4. **Dashboards** — `build_dashboards.py` → two interactive HTML dashboards
   (executive + operative) powered by the real data.

---

## Key decisions

| Decision | Choice made | Why |
|---|---|---|
| **Cancellations** | Remove all C-invoice lines **and** the matching original purchase when one exists (same Customer + StockCode + Price + Quantity) | A reversed sale was never net revenue, so neither row should count |
| **Orphan cancellations** | Removed (12,327 with no matching original in the data window) | Not real purchases either |
| **Missing Customer IDs** | Dropped (234,437 rows, 22%) | Guests can't be tied to a customer, so can't be segmented |
| **International customers** | **Kept** (41 countries) | Enables cross-border segments; UK still ~92% |
| **Recency snapshot date** | 2011-12-10 (day after the last transaction) | Standard RFM convention; Recency = days since last purchase |
| **Scoring** | Quintile (1–5) on R, F, M; Frequency rank-binned to handle ties; Recency reverse-scored | Equal-sized, comparable score bands |
| **Segment count** | 10 named segments from the standard R × (F+M) grid | Each segment maps to a distinct business action — count is driven by strategy, not tuned |
| **Validation** | K-Means (elbow + silhouette) as a cross-check, not the primary method | Elbow at K=4 confirms the 10 named segments nest within 4 natural macro-clusters |
| **Dashboard format** | Self-contained interactive HTML (data embedded as JSON) | Runs in any browser with no server or install; portable |
| **Visual style** | "Structured craft" brand (cobalt/graphite, sharp drafted cards, mono metrics) | Distinctive, on-brand |

---

## Pipeline

```
online_retail_II.xlsx
        │   01_clean_data.py
        ▼
retail_clean.csv  ───────────────►  cleaning_audit_removed_rows.csv
        │   02_rfm_segments.py
        ▼
rfm_segments.csv
        │   build_dashboards.py  (writes dashboard_data.json)
        ▼
index.html (executive)  +  operative.html
```

Run order:

```bash
python3 01_clean_data.py      # → retail_clean.csv, cleaning_audit_removed_rows.csv
python3 02_rfm_segments.py    # → rfm_segments.csv  (+ K-Means validation printout)
python3 build_dashboards.py   # → dashboard_data.json, index.html, operative.html
```

Requirements: `pandas`, `openpyxl` (cleaning); `numpy`, optional `scikit-learn`
(modelling/validation). Open the dashboards by double-clicking the HTML files —
no server needed (data is embedded; fonts load from Google Fonts when online).

---

## Methodology

**RFM** scores each customer on three behaviours:
- **Recency (R)** — days since last purchase (lower = better).
- **Frequency (F)** — number of distinct invoices.
- **Monetary (M)** — total revenue.

Each is scored 1–5 by quintile. Recency is reverse-scored so 5 = most recent;
Frequency is rank-binned first because many customers share the same low values.
The **R score** and a combined **F+M score** are matched against the standard
segment grid to label each customer as one of: Champions, Loyal Customers,
Potential Loyalists, New Customers, Promising, Need Attention, About to Sleep,
At Risk, Can't Lose Them, Hibernating.

**Hybrid validation:** the named segments are the deliverable (every one carries
an attached strategy), and K-Means clustering on log-scaled R/F/M independently
confirms the structure is real — the elbow lands at K=4, and those four natural
macro-clusters (high-value core / developing / lapsing / dormant) line up with
the named segments rather than contradicting them.

---

## Files

> **Note:** the raw data file `online_retail_II.xlsx` is **not committed** (44 MB).
> Download it from the [UCI Machine Learning Repository — Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
> and place it in the project root, then run the pipeline below.

| File | One-line description |
|---|---|
| `online_retail_II.xlsx` | Raw source data (not committed — download separately) — two sheets of online-retail transactions (FY2009–10, FY2010–11). |
| `01_clean_data.py` | Cleans the raw Excel into tidy transactions and writes a full audit of every removed row. |
| `02_rfm_segments.py` | Computes R/F/M scores, assigns the 10 named segments, and runs the K-Means validation. |
| `build_dashboards.py` | Generates the two interactive HTML dashboards from the modelled data. |
| `retail_clean.csv` | Cleaned line-item transactions (769,968 rows) with an added Revenue column *(generated by `01_clean_data.py` — not committed, 80 MB)*. |
| `cleaning_audit_removed_rows.csv` | Every removed row (297,403) tagged with the step and reason it was dropped *(generated by `01_clean_data.py` — not committed, 43 MB)*. |
| `rfm_segments.csv` | One row per customer: R/F/M values, 1–5 scores, combined score, and assigned segment. |
| `dashboard_data.json` | Aggregated data (segment summaries, monthly trend, country splits, customer list) embedded into the dashboards. |
| `index.html` | Leadership dashboard (GitHub Pages entry page) — KPIs, revenue concentration, customers-vs-revenue imbalance, and seasonal trend, filterable by country; links to the operative view. |
| `operative.html` | Marketing/CRM workspace — per-segment detail, campaign plays, and a searchable, sortable, exportable customer table; links back to the executive view. |
| `README.md` | This file. |
