#!/usr/bin/env python3
"""
01_clean_data.py
================
Clean the raw Online Retail II dataset for RFM segmentation.

Input : online_retail_II.xlsx   (sheets: 'Year 2009-2010', 'Year 2010-2011')
Output: retail_clean.csv                  -- cleaned line-item transactions
        cleaning_audit_removed_rows.csv   -- every removed row + reason

Cleaning steps (order matters):
  1. Combine both sheets.
  2. Drop exact duplicate rows (Dec-2010 sheet overlap + repeated lines).
  3. Cancellation pairing: remove ALL cancellation (C-prefix) lines. Where a
     cancellation matches an original positive purchase
     (same Customer + StockCode + Price + Quantity), remove that original too
     -- the sale was reversed, so it was never real revenue.
  4. Drop rows with no Customer ID (guests cannot be segmented).
  5. Filter non-product StockCodes (POST, M, ADJUST, BANK CHARGES, TEST, ...).
  6. Drop zero/negative price and non-positive quantity.
  7. Cast Customer ID to int and add a Revenue column.

International transactions are KEPT (no country filter).

Requires: pandas, openpyxl
"""
import pandas as pd
from collections import defaultdict

RAW_FILE   = 'online_retail_II.xlsx'
CLEAN_FILE = 'retail_clean.csv'
AUDIT_FILE = 'cleaning_audit_removed_rows.csv'
ORIG_COLS  = ['Invoice', 'StockCode', 'Description', 'Quantity',
              'InvoiceDate', 'Price', 'Customer ID', 'Country']


def main():
    # ---- Step 0: load & combine ----
    df1 = pd.read_excel(RAW_FILE, sheet_name='Year 2009-2010')
    df2 = pd.read_excel(RAW_FILE, sheet_name='Year 2010-2011')
    raw_total = len(df1) + len(df2)
    df = pd.concat([df1, df2], ignore_index=True)
    df['Invoice']   = df['Invoice'].astype(str)
    df['StockCode'] = df['StockCode'].astype(str)

    removed_frames = []
    audit_log = []

    def capture(rows, step, reason):
        r = rows[ORIG_COLS].copy()
        r.insert(0, 'RemovalStep', step)
        r['RemovalReason'] = reason
        removed_frames.append(r)

    def log(step, note):
        audit_log.append((step, len(df), df['Customer ID'].nunique(), note))

    log('0. Raw combined (both sheets)', '')

    # ---- Step 1: exact duplicates ----
    dup_mask = df.duplicated(keep='first')
    capture(df[dup_mask], 1,
            'Exact duplicate row (Dec-2010 sheet overlap or repeated line)')
    df = df[~dup_mask]
    log('1. Drop exact duplicate rows', f'-{int(dup_mask.sum()):,}')

    # ---- Step 2: cancellation pairing ----
    is_cancel = df['Invoice'].str.startswith('C')
    canc = df[is_cancel].copy()
    pos  = df[~is_cancel & (df['Quantity'] > 0)].copy()

    # queue of positive-purchase row indices per (customer, stock, price, qty)
    pos_groups = defaultdict(list)
    for idx, cust, stock, price, qty in zip(
            pos.index, pos['Customer ID'], pos['StockCode'],
            pos['Price'], pos['Quantity']):
        pos_groups[(cust, stock, price, qty)].append(idx)

    matched_canc_idx, orphan_canc_idx, matched_pos_idx = [], [], []
    for idx, cust, stock, price, qty in zip(
            canc.index, canc['Customer ID'], canc['StockCode'],
            canc['Price'], canc['Quantity']):
        bucket = pos_groups.get((cust, stock, price, abs(qty)))
        if bucket:                       # found the original purchase
            matched_pos_idx.append(bucket.pop())
            matched_canc_idx.append(idx)
        else:                            # no original in the data window
            orphan_canc_idx.append(idx)

    capture(df.loc[matched_canc_idx], 2,
            'Cancellation line - matched to an original purchase (sale reversed)')
    capture(df.loc[orphan_canc_idx], 2,
            'Cancellation line - orphan (no matching original in data window)')
    capture(df.loc[matched_pos_idx], 2,
            'Original purchase reversed by a matching cancellation')
    df = df.drop(index=set(canc.index) | set(matched_pos_idx))
    log('2. Cancellation pairing removal',
        f'-{len(canc):,} C-rows ({len(matched_canc_idx):,} paired/'
        f'{len(orphan_canc_idx):,} orphan), -{len(matched_pos_idx):,} originals')

    # ---- Step 3: null Customer ID ----
    mask = df['Customer ID'].isna()
    capture(df[mask], 3,
            'Missing Customer ID (guest/unregistered - cannot be segmented)')
    df = df[~mask]
    log('3. Drop null Customer ID (guest)', f'-{int(mask.sum()):,}')

    # ---- Step 4: non-product StockCodes ----
    mask = ~df['StockCode'].str.match(r'^\d')   # product codes start with a digit
    capture(df[mask], 4,
            'Non-product StockCode (admin/fee: POST, M, C2, ADJUST, '
            'BANK CHARGES, DOT, TEST, etc.)')
    df = df[~mask]
    log('4. Filter non-product StockCodes', f'-{int(mask.sum()):,}')

    # ---- Step 5: zero/negative price & non-positive quantity ----
    mask = df['Price'] <= 0
    capture(df[mask], 5, 'Zero or negative unit price (free item / data error)')
    df = df[~mask]
    log('5. Drop zero/negative price', f'-{int(mask.sum()):,}')

    mask = df['Quantity'] <= 0
    capture(df[mask], 5, 'Non-positive quantity')
    df = df[~mask]
    log('5b. Drop non-positive quantity', f'-{int(mask.sum()):,}')

    # ---- Step 6: finalise ----
    df['Customer ID'] = df['Customer ID'].astype(int)
    df['Revenue'] = df['Quantity'] * df['Price']
    log('6. Cast ID->int, add Revenue', 'international INCLUDED')

    # ---- Save outputs ----
    df.to_csv(CLEAN_FILE, index=False)
    audit = pd.concat(removed_frames, ignore_index=True)
    audit = audit.sort_values(['RemovalStep', 'Invoice']).reset_index(drop=True)
    audit.to_csv(AUDIT_FILE, index=False)

    # ---- Report ----
    print('=' * 70)
    print('CLEANING AUDIT TRAIL')
    print('=' * 70)
    print(f"{'Step':<40}{'Rows':>12}{'Cust':>9}   Note")
    print('-' * 70)
    for step, rows, custs, note in audit_log:
        print(f'{step:<40}{rows:>12,}{custs:>9,}   {note}')

    assert len(df) + len(audit) == raw_total, 'Row reconciliation MISMATCH!'
    print('\nReconciliation OK: '
          f'{len(df):,} kept + {len(audit):,} removed = {raw_total:,} raw rows')
    print(f"Clean dataset : {len(df):,} rows | {df['Customer ID'].nunique():,} customers "
          f"| {df['Country'].nunique()} countries | £{df['Revenue'].sum():,.0f}")
    print(f'Wrote {CLEAN_FILE} and {AUDIT_FILE}')


if __name__ == '__main__':
    main()
