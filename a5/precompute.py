#!/usr/bin/env python3
"""
precompute.py
Preprocess NYC 311 2024 dataset -> monthly average response times by zipcode.

Output CSV format:
year,month,zipcode,avg_hours,count
2024,1,ALL,36.5,50231
2024,1,11218,40.2,320
...
"""

import csv
from collections import defaultdict
from datetime import datetime

INPUT = "data/NYC_311_2024.csv"      # path to raw trimmed data
OUTPUT = "data/nyc311_monthly.csv"   # precomputed dataset

DATE_FORMATS = (
    "%m/%d/%Y %I:%M:%S %p",  # e.g. 12/31/2024 11:59:38 PM
    "%m/%d/%Y %H:%M",        # fallback
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
)

def parse_dt(s):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None

# Accumulators: (year, month, zipcode) -> [sum_hours, count]
agg = defaultdict(lambda: [0.0, 0])

with open(INPUT, newline="", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for row in r:
        created = parse_dt(row.get("Created Date", ""))
        closed = parse_dt(row.get("Closed Date", ""))
        zipcode = (row.get("Incident Zip") or "").strip()

        # Skip invalid
        if not created or not closed:
            continue
        if closed < created:
            continue
        if not zipcode.isdigit() or len(zipcode) != 5:
            continue

        if created.year != 2024:  # only include 2024-created
            continue

        # Duration in hours
        duration = (closed - created).total_seconds() / 3600.0

        # Group by closed month (FAQ #2)
        year, month = closed.year, closed.month
        agg[(year, month, zipcode)][0] += duration
        agg[(year, month, zipcode)][1] += 1

        # Citywide ALL bucket
        agg[(year, month, "ALL")][0] += duration
        agg[(year, month, "ALL")][1] += 1

# Write precomputed dataset
with open(OUTPUT, "w", newline="", encoding="utf-8") as out:
    w = csv.writer(out)
    w.writerow(["year", "month", "zipcode", "avg_hours", "count"])
    for (year, month, zipcode), (total, count) in sorted(agg.items()):
        avg = total / count if count else 0
        w.writerow([year, month, zipcode, round(avg, 2), count])

print(f"✅ Precomputed data written to {OUTPUT}")
