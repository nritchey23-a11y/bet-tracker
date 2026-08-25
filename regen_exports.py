#!/usr/bin/env python3
"""Regenerate static exports (summary.txt, bets.csv, data.json, report.html)
from current FALLBACK_BETS in index.html. Run before every deploy."""
import json, re, csv, sys, os
from datetime import datetime, timezone, timedelta
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(ROOT, "index.html")

with open(HTML) as f:
    html = f.read()
m = re.search(r"const FALLBACK_BETS = (\[.*?\]);\s*\n", html, re.DOTALL)
if not m:
    sys.exit("FALLBACK_BETS not found")
bets = json.loads(m.group(1))

# Coerce numeric helpers
def f(x):
    try: return float(str(x).replace(",", "").replace("+", "")) if x not in (None, "") else 0.0
    except: return 0.0

now = datetime.now(timezone.utc)
today_pt = (now - timedelta(hours=7)).date()  # rough PT date

# -------- data.json (raw)
with open(os.path.join(ROOT, "data.json"), "w") as out:
    json.dump({"generated_at": now.isoformat(), "count": len(bets), "bets": bets}, out, indent=1)

# -------- bets.csv (full table)
cols = ["ID","Date","Sport","League","Event","Type","Description","Pick","Opponent","Odds","Risk","To Win","Status","Result Date","Notes"]
with open(os.path.join(ROOT, "bets.csv"), "w", newline="") as out:
    w = csv.DictWriter(out, fieldnames=cols)
    w.writeheader()
    for b in bets: w.writerow({c: b.get(c, "") for c in cols})

# -------- Aggregations
def parse_date(s):
    try: return datetime.strptime(s, "%Y-%m-%d").date()
    except: return None

# Week buckets: Tue-Mon (weekday Tue=1). Find Tue on/before a date.
def week_start(d):
    # Python: Mon=0..Sun=6. Tue=1. We want Tue as week start.
    delta = (d.weekday() - 1) % 7
    return d - timedelta(days=delta)

# Settled P&L per bet
def pnl(b):
    s = b.get("Status","").lower()
    risk = f(b.get("Risk")); tw = f(b.get("To Win"))
    if s == "won": return tw
    if s == "lost": return -risk
    if s == "push": return 0.0
    return None  # pending / void

settled_total = 0.0; won = lost = push = pending = 0
pending_risk = pending_max = 0.0
by_day = defaultdict(lambda: {"won":0,"lost":0,"push":0,"pending":0,"pnl":0.0,"pending_risk":0.0,"pending_max":0.0})
by_week = defaultdict(lambda: {"won":0,"lost":0,"push":0,"pending":0,"pnl":0.0,"pending_risk":0.0,"pending_max":0.0})

for b in bets:
    s = b.get("Status","").lower()
    d = parse_date(b.get("Date",""))
    p = pnl(b)
    if s == "won": won += 1
    elif s == "lost": lost += 1
    elif s == "push": push += 1
    elif s == "pending":
        pending += 1
        pending_risk += f(b.get("Risk"))
        pending_max  += f(b.get("To Win"))
    if p is not None: settled_total += p
    if d:
        bd = by_day[d.isoformat()]
        bw = by_week[week_start(d).isoformat()]
        for bucket in (bd, bw):
            if s in ("won","lost","push","pending"):
                bucket[s] += 1
            if p is not None: bucket["pnl"] += p
            if s == "pending":
                bucket["pending_risk"] += f(b.get("Risk"))
                bucket["pending_max"]  += f(b.get("To Win"))

# Sort bets desc by ID for "recent activity" listing
def id_int(b):
    try: return int(b.get("ID","0"))
    except: return 0
bets_sorted = sorted(bets, key=id_int, reverse=True)

# Recent days/weeks (last 8 days, last 4 weeks)
def fmt_money(x):
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.2f}"

day_keys = sorted(by_day.keys(), reverse=True)[:8]
week_keys = sorted(by_week.keys(), reverse=True)[:4]

# -------- summary.txt
out = []
out.append("BET TRACKER — LIVE SUMMARY")
out.append(f"Generated: {now.isoformat()}")
out.append(f"Total bets in tracker: {len(bets)}")
out.append("")
out.append("OVERALL STATUS")
out.append(f"  Won: {won}  Lost: {lost}  Push: {push}  Pending: {pending}")
out.append(f"  Lifetime settled P&L: {fmt_money(settled_total)}")
out.append(f"  Pending risk: {fmt_money(pending_risk)}   Pending max win: {fmt_money(pending_max)}")
out.append("")
out.append("RECENT DAYS (most recent 8 with activity)")
for k in day_keys:
    v = by_day[k]
    record = f"{v['won']}W-{v['lost']}L"
    if v['push']: record += f"-{v['push']}P"
    pending_str = f"  Pending: {v['pending']} (risk {fmt_money(v['pending_risk'])}, max {fmt_money(v['pending_max'])})" if v['pending'] else ""
    out.append(f"  {k}: {record}  P&L: {fmt_money(v['pnl'])}{pending_str}")
out.append("")
out.append("RECENT WEEKS (Tue–Mon, most recent 4)")
for k in week_keys:
    v = by_week[k]
    wk_start = datetime.strptime(k, "%Y-%m-%d").date()
    wk_end = wk_start + timedelta(days=6)
    record = f"{v['won']}W-{v['lost']}L"
    if v['push']: record += f"-{v['push']}P"
    pending_str = f"  Pending: {v['pending']} (risk {fmt_money(v['pending_risk'])})" if v['pending'] else ""
    out.append(f"  Week {k} → {wk_end.isoformat()}: {record}  P&L: {fmt_money(v['pnl'])}{pending_str}")
out.append("")
out.append("INDIVIDUAL BETS (most recent 80, sorted by ID desc):")
for b in bets_sorted[:80]:
    risk = f(b.get("Risk")); tw = f(b.get("To Win"))
    pnl_str = ""
    p = pnl(b)
    if p is not None: pnl_str = f"  P&L: {fmt_money(p)}"
    notes = b.get("Notes","")
    if notes: notes = "  Notes: " + notes
    out.append(
        f"#{b.get('ID')} | {b.get('Date','')} | {b.get('Sport','')}/{b.get('League','')} | "
        f"{b.get('Description','')} | Pick: {b.get('Pick','')} | Odds: {b.get('Odds','')} | "
        f"Risk ${risk:,.2f} → Win ${tw:,.2f} | Status: {b.get('Status','')}{pnl_str}{notes}"
    )

with open(os.path.join(ROOT, "summary.txt"), "w") as f:
    f.write("\n".join(out) + "\n")

# -------- report.html
rows = []
for b in bets_sorted[:200]:
    rows.append("<tr>" + "".join(f"<td>{(b.get(c,'') or '')}</td>" for c in cols) + "</tr>")
report = f"""<!doctype html><meta charset=utf-8><title>Bet Tracker Report</title>
<style>body{{font-family:system-ui;margin:20px}}table{{border-collapse:collapse;font-size:12px}}td,th{{border:1px solid #ccc;padding:4px 8px}}th{{background:#eee}}</style>
<h1>Bet Tracker — Report</h1>
<p>Generated: {now.isoformat()}<br>Total: {len(bets)} | Won {won} / Lost {lost} / Push {push} / Pending {pending}<br>Settled P&amp;L: {fmt_money(settled_total)} | Pending risk: {fmt_money(pending_risk)}</p>
<table><thead><tr>{''.join(f'<th>{c}</th>' for c in cols)}</tr></thead><tbody>
{''.join(rows)}
</tbody></table>"""
with open(os.path.join(ROOT, "report.html"), "w") as f:
    f.write(report)

print(f"OK: regenerated 4 export files. {len(bets)} bets. {won}W-{lost}L-{push}P, {pending} pending. Settled P&L {fmt_money(settled_total)}.")

# -------- LLM-readable digests (brief/futures/pending/stats + ask.html)
# Keeps the small plain-text pages in sync so search threads never read stale numbers.
import subprocess
_d = subprocess.run([sys.executable, os.path.join(ROOT, "gen_digests.py")],
                    capture_output=True, text=True)
print(_d.stdout.strip() or _d.stderr.strip())
if _d.returncode != 0:
    sys.exit("gen_digests.py failed")
