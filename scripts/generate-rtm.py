#!/usr/bin/env python3
"""
Generate a simple Requirements Traceability Matrix (CSV) by scanning docs/specs and docs/adr
for IDs like PRD-XXX, DESIGN-XXX, ADR-XXX, TEST-XXX and mapping to file paths.
"""
import os, re, csv

root = "docs"
rows = []
for dirpath, _, files in os.walk(root):
    for n in files:
        if not n.endswith(".md"): 
            continue
        path = os.path.join(dirpath, n)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        ids = re.findall(r"\b(PRD|DESIGN|ADR|TEST)-\d{3}\b", txt)
        for i in set(ids):
            rows.append([i, path])

os.makedirs("out", exist_ok=True)
with open("out/rtm.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ID","File"])
    w.writerows(sorted(rows))

print("Wrote out/rtm.csv")
