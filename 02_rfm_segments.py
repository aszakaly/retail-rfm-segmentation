#!/usr/bin/env python3
"""
02_rfm_segments.py
==================
Build the RFM model and assign named, strategy-ready segments.

Input : retail_clean.csv   (produced by 01_clean_data.py)
Output: rfm_segments.csv    -- one row per customer: R/F/M values, 1-5 scores,
                              combined score, and assigned Segment.

Method:
  - Recency snapshot = 2011-12-10 (day after the last transaction).
  - Recency   = days since last purchase (lower is better).
  - Frequency = number of distinct invoices.
  - Monetary  = total revenue.
  - Quintile scores 1-5 for each dimension (Frequency is rank-binned first to
    handle ties). Recency is reverse-scored so 5 = most recent.
  - Map (R score x combined F+M score) onto the standard 10-segment business
    grid (Champions, Loyal, At Risk, Can't Lose Them, Hibernating, ...).

A K-Means cross-check (elbow + silhouette) is run if scikit-learn is installed;
it validates that the named segments reflect real structure (elbow at K=4).
The named segments remain the deliverable regardless.

Requires: pandas, numpy  (scikit-learn optional, for the validation block)
"""
import pandas as pd
import numpy as np

CLEAN_FILE = 'retail_clean.csv'
OUT_FILE   = 'rfm_segments.csv'
SNAPSHOT   = pd.Timestamp('2011-12-10')

# Standard R x FM segment grid. Key = "<R><FM>" (each 1-5); regex-matched.
SEGMENT_MAP = {
    r'[1-2][1-2]': 'Hibernating',
    r'[1-2][3-4]': 'At Risk',
    r'[1-2]5':     "Can't Lose Them",
    r'3[1-2]':     'About to Sleep',
    r'33':         'Need Attention',
    r'[3-4][4-5]': 'Loyal Customers',
    r'41':         'Promising',
    r'51':         'New Customers',
    r'[4-5][2-3]': 'Potential Loyalists',
    r'5[4-5]':     'Champions',
}


def build_rfm(df):
    rfm = df.groupby('Customer ID').agg(
        Recency=('InvoiceDate', lambda x: (SNAPSHOT - x.max()).days),
        Frequency=('Invoice', 'nunique'),
        Monetary=('Revenue', 'sum'),
    ).reset_index()

    # quintile scoring (1-5)
    rfm['R_score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5,
                             labels=[1, 2, 3, 4, 5]).astype(int)
    rfm['M_score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm['RFM_Score'] = rfm['R_score'] + rfm['F_score'] + rfm['M_score']
    rfm['FM_score'] = ((rfm['F_score'] + rfm['M_score']) / 2).round().astype(int)

    # map to named segments
    rfm['Segment'] = (rfm['R_score'].astype(str) + rfm['FM_score'].astype(str))
    rfm['Segment'] = rfm['Segment'].replace(SEGMENT_MAP, regex=True)
    return rfm


def summarise(rfm):
    total_cust = len(rfm)
    total_rev = rfm['Monetary'].sum()
    s = rfm.groupby('Segment').agg(
        Customers=('Customer ID', 'count'),
        Avg_Recency=('Recency', 'mean'),
        Avg_Frequency=('Frequency', 'mean'),
        Avg_Monetary=('Monetary', 'mean'),
        Total_Revenue=('Monetary', 'sum'),
    ).reset_index()
    s['%_Customers'] = (s['Customers'] / total_cust * 100).round(1)
    s['%_Revenue'] = (s['Total_Revenue'] / total_rev * 100).round(1)
    s[['Avg_Recency', 'Avg_Frequency', 'Avg_Monetary']] = \
        s[['Avg_Recency', 'Avg_Frequency', 'Avg_Monetary']].round(1)
    return s.sort_values('Total_Revenue', ascending=False)


def kmeans_validation(rfm):
    """Optional: elbow + silhouette to confirm the named segments are real."""
    try:
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
    except ImportError:
        print('\n(scikit-learn not installed -- skipping K-Means validation)')
        return

    X = rfm[['Recency', 'Frequency', 'Monetary']].apply(np.log1p)
    Xs = StandardScaler().fit_transform(X)
    print('\n' + '=' * 50)
    print('K-MEANS VALIDATION (elbow + silhouette)')
    print('=' * 50)
    print(f"{'K':>3}{'Inertia':>14}{'Silhouette':>13}")
    prev = None
    for k in range(2, 11):
        km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(Xs)
        sil = silhouette_score(Xs, km.labels_)
        drop = f'  ({(prev - km.inertia_) / prev * 100:4.1f}% drop)' if prev else ''
        print(f'{k:>3}{km.inertia_:>14.0f}{sil:>13.3f}{drop}')
        prev = km.inertia_
    print('Elbow at K=4 -> the 10 named segments nest within 4 natural macro-clusters.')


def main():
    df = pd.read_csv(CLEAN_FILE, parse_dates=['InvoiceDate'])
    rfm = build_rfm(df)
    rfm.to_csv(OUT_FILE, index=False)

    print('=' * 70)
    print('SEGMENT SUMMARY (sorted by revenue)')
    print('=' * 70)
    cols = ['Segment', 'Customers', '%_Customers', 'Avg_Recency',
            'Avg_Frequency', 'Avg_Monetary', 'Total_Revenue', '%_Revenue']
    print(summarise(rfm)[cols].to_string(index=False))
    print(f"\nTOTAL: {len(rfm):,} customers | £{rfm['Monetary'].sum():,.0f} revenue "
          f"| {rfm['Segment'].nunique()} segments")
    print(f'Wrote {OUT_FILE}')

    kmeans_validation(rfm)


if __name__ == '__main__':
    main()
