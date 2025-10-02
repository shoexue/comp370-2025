#!/usr/bin/env python3
"""
complaint_borough.py
Count complaint types per borough in a creation-date range.

Usage:
  python3 complaint_borough.py -i data/NYC_311_2024.csv -s 2024-01-01 -e 2024-01-31
  python3 complaint_borough.py -i data/NYC_311_2024.csv -s 2024-01-01 -e 2024-01-31 -o out.csv
"""

import argparse, csv, sys
from collections import Counter
from datetime import datetime

DATE_FORMATS = (
    "%m/%d/%Y %I:%M:%S %p",  # e.g., 09/27/2025 01:30:44 AM
    "%m/%d/%Y %H:%M",        # 09/27/2025 01:30
    "%Y-%m-%d %H:%M:%S",     # 2025-09-27 01:30:44
    "%Y-%m-%d",              # 2025-09-27
)

def parse_dt(s: str):
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            continue
    return None

def main():
    p = argparse.ArgumentParser(description="Count complaint types per borough in a date range.")
    p.add_argument("-i", "--input", required=True, help="Input CSV (trimmed to 2024).")
    p.add_argument("-s", "--start", required=True, help="Start date (YYYY-MM-DD)")
    p.add_argument("-e", "--end", required=True, help="End date (YYYY-MM-DD)")
    p.add_argument("-o", "--output", help="Optional output CSV file (default: stdout)")
    args = p.parse_args()

    try:
        start = datetime.fromisoformat(args.start)
        end = datetime.fromisoformat(args.end).replace(hour=23, minute=59, second=59)
    except ValueError:
        sys.exit("Error: start/end must be YYYY-MM-DD")

    counts = Counter()
    with open(args.input, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            d_raw = row.get("Created Date")
            complaint = (row.get("Complaint Type") or "").strip()
            borough = (row.get("Borough") or "").strip()
            if not d_raw or not complaint or not borough:
                continue
            dt = parse_dt(d_raw)
            if dt and start <= dt <= end:
                counts[(complaint, borough)] += 1

    outfh = sys.stdout if not args.output else open(args.output, "w", encoding="utf-8", newline="")
    with outfh:
        w = csv.writer(outfh)
        w.writerow(["complaint type", "borough", "count"])
        for (complaint, borough), c in sorted(counts.items()):
            w.writerow([complaint, borough, c])

if __name__ == "__main__":
    main()
