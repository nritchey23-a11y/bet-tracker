#!/usr/bin/env python3
"""One-way sync: dashboard FALLBACK_BETS (source of truth) -> Google Sheet 'Bets'.

index.html is READ ONLY here. This script never writes to it.

Replaces the old sync_sheet.py, which was a one-off migration helper: it had
hardcoded /home/user/workspace/bet-tracker paths, a hardcoded MISSING id list,
depended on a stale sheet_full.json snapshot, and (dangerously) rewrote
index.html. None of that is appropriate for a routine sheet refresh.

Emits chunked JSON payloads for `gws sheets spreadsheets values update` so no
single shell argument gets near ARG_MAX.

Usage:
    python sync_sheet_from_dashboard.py            # write payloads to /tmp/syncchunks
    python sync_sheet_from_dashboard.py --stats    # report only, no files
"""
import json, re, os, sys, math

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import horizon as HZ

COLS = ["ID", "Date", "Sport", "League", "Event", "Type", "Description", "Pick",
        "Opponent", "Odds", "Risk", "To Win", "Status", "Result Date", "Notes",
        "Event Date"]

VOCAB = {"won", "lost", "push", "pending", "half-won", "half-lost", "refunded"}

CHUNK = 300
OUTDIR = "/tmp/syncchunks"


def load_bets():
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as fh:
        html = fh.read()
    m = re.search(r"const FALLBACK_BETS = (\[.*?\]);\s*\n", html, re.S)
    if not m:
        sys.exit("FALLBACK_BETS not found in index.html")
    return json.loads(m.group(1))


def id_key(b):
    v = str(b.get("ID", "")).strip()
    return int(v) if v.isdigit() else 10 ** 9


def main():
    bets = load_bets()
    HZ.enrich(bets)                      # adds 'Event Date' + 'Horizon' in memory
    bets = sorted(bets, key=id_key)

    recased = 0
    unknown = {}
    for b in bets:
        raw = (b.get("Status") or "").strip()
        low = raw.lower()
        if low not in VOCAB:
            unknown[raw] = unknown.get(raw, 0) + 1
        if raw != low:
            recased += 1
        b["Status"] = low

    values = [COLS]
    for b in bets:
        values.append([str(b.get(c, "") or "") for c in COLS])

    payload_bytes = len(json.dumps({"values": values}))
    print(f"rows           : {len(values)} (1 header + {len(bets)} bets)")
    print(f"status recased : {recased}")
    print(f"event date set : {sum(1 for b in bets if b.get('Event Date'))}/{len(bets)}")
    if unknown:
        print(f"!! statuses outside grading vocabulary: {unknown}")
    print(f"payload        : {payload_bytes/1e6:.2f} MB total")

    if "--stats" in sys.argv:
        return

    os.makedirs(OUTDIR, exist_ok=True)
    for f in os.listdir(OUTDIR):
        os.remove(os.path.join(OUTDIR, f))

    n = 0
    # row 1 = header; data rows start at sheet row 2
    for i in range(0, len(values), CHUNK):
        block = values[i:i + CHUNK]
        start_row = i + 1                      # 1-based sheet row
        end_row = start_row + len(block) - 1
        rng = f"Bets!A{start_row}:P{end_row}"
        with open(os.path.join(OUTDIR, f"chunk_{n:03d}.json"), "w") as fh:
            json.dump({"values": block}, fh)
        with open(os.path.join(OUTDIR, f"chunk_{n:03d}.range"), "w") as fh:
            fh.write(rng)
        n += 1
    print(f"wrote {n} chunk(s) to {OUTDIR} (<= {CHUNK} rows each)")
    print(f"last row written: {len(values)}")


if __name__ == "__main__":
    main()
