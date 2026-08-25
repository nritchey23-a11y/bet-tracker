#!/usr/bin/env python3
"""Generate small, plain, server-rendered digest pages that an LLM/search thread
can fetch and reason over without JavaScript.

Source of truth is FALLBACK_BETS inside index.html (same as regen_exports.py).
Outputs (all tiny, all text-first):
  ask.html      - landing page listing the digest URLs
  brief.txt     - one-page headline numbers
  futures.txt   - every open future, grouped by league, with totals
  pending.txt   - every open bet
  stats.txt     - breakdowns by sport/league/type/book/month + streaks + best/worst
plus a .html mirror of each .txt (same text in <pre>) for crawlers that prefer HTML.
"""
import json, re, os, html
from datetime import datetime, timezone
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://nritchey23-a11y.github.io/bet-tracker"

with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as fh:
    doc = fh.read()
m = re.search(r"const FALLBACK_BETS = (\[.*?\]);\s*\n", doc, re.DOTALL)
if not m:
    raise SystemExit("FALLBACK_BETS not found in index.html")
bets = json.loads(m.group(1))

now = datetime.now(timezone.utc)
STAMP = now.strftime("%Y-%m-%d %H:%M UTC")


def f(x):
    try:
        return float(str(x).replace("$", "").replace(",", "").replace("+", "") or 0)
    except Exception:
        return 0.0


def money(x):
    return ("-$" if x < 0 else "$") + f"{abs(x):,.2f}"


def book_of(b):
    n = (b.get("Notes") or "").lower()
    if "wagerhouse" in n:
        return "Wagerhouse"
    if "gamedaywager" in n or "gameday" in n:
        return "GameDayWagers"
    return "Untagged"


SETTLED = ("won", "lost", "push", "half-won", "half-lost")


def st(b):
    return (b.get("Status") or "").strip().lower()


def pnl(b):
    s = st(b)
    if s in ("won", "half-won"):
        return f(b.get("To Win"))
    if s in ("lost", "half-lost"):
        return -f(b.get("Risk"))
    return 0.0


settled = [b for b in bets if st(b) in SETTLED]
pending = [b for b in bets if st(b) == "pending"]
won = [b for b in settled if st(b) in ("won", "half-won")]
lost = [b for b in settled if st(b) in ("lost", "half-lost")]
push = [b for b in settled if st(b) == "push"]

risked = sum(f(b.get("Risk")) for b in settled)
net = sum(pnl(b) for b in settled)
roi = (net / risked * 100) if risked else 0.0
wr = (len(won) / (len(won) + len(lost)) * 100) if (won or lost) else 0.0
pend_risk = sum(f(b.get("Risk")) for b in pending)
pend_max = sum(f(b.get("To Win")) for b in pending)

HDR = (
    "This file is a plain-text digest of Nick Ritchey's personal sports-betting\n"
    "tracker. All figures are precomputed. Conventions: 'To Win' is PROFIT, not\n"
    "total payout (payout = Risk + To Win). Settled excludes pending/refunded.\n"
    f"Generated: {STAMP}\n"
)


def head(title):
    return f"{title}\n{'=' * len(title)}\n\n{HDR}\n"


# ---------------------------------------------------------------- brief.txt
L = [head("BET TRACKER - BRIEF")]
L.append("HEADLINE")
L.append(f"  Total bets logged      : {len(bets)}")
L.append(f"  Settled record         : {len(won)}W-{len(lost)}L-{len(push)}P")
L.append(f"  Win rate (excl. pushes): {wr:.1f}%")
L.append(f"  Total risked (settled) : {money(risked)}")
L.append(f"  Net profit/loss        : {money(net)}")
L.append(f"  ROI                    : {roi:+.2f}%")
L.append(f"  Open bets              : {len(pending)}")
L.append(f"  Open risk (exposure)   : {money(pend_risk)}")
L.append(f"  Open max win           : {money(pend_max)}")
L.append("")

bysport = defaultdict(lambda: {"w": 0, "l": 0, "p": 0, "r": 0.0, "n": 0.0})
for b in settled:
    d = bysport[b.get("Sport") or "Unknown"]
    d["r"] += f(b.get("Risk"))
    d["n"] += pnl(b)
    d["w" if st(b) in ("won", "half-won") else "l" if st(b) in ("lost", "half-lost") else "p"] += 1
L.append("SETTLED BY SPORT (sorted by net P&L)")
L.append(f"  {'Sport':<14}{'Record':<14}{'Risked':>13}{'Net P&L':>13}{'ROI':>9}")
for k, v in sorted(bysport.items(), key=lambda x: -x[1]["n"]):
    r = f"{v['w']}W-{v['l']}L-{v['p']}P"
    ro = (v["n"] / v["r"] * 100) if v["r"] else 0.0
    L.append(f"  {k[:13]:<14}{r:<14}{money(v['r']):>13}{money(v['n']):>13}{ro:>8.1f}%")
L.append("")
L.append("OPEN EXPOSURE BY SPORT")
ps = defaultdict(lambda: [0, 0.0, 0.0])
for b in pending:
    k = b.get("Sport") or "Unknown"
    ps[k][0] += 1
    ps[k][1] += f(b.get("Risk"))
    ps[k][2] += f(b.get("To Win"))
for k, v in sorted(ps.items(), key=lambda x: -x[1][1]):
    unit = "bet " if v[0] == 1 else "bets"
    L.append(f"  {k[:16]:<18}{v[0]:>4} {unit}  risk {money(v[1]):>12}  max win {money(v[2]):>12}")
L.append("")
L.append("MORE DETAIL")
for n in ("futures", "pending", "teams", "stats"):
    L.append(f"  {BASE}/{n}.txt")
brief = "\n".join(L) + "\n"

# ---------------------------------------------------------------- futures.txt
FUT = ("future", "futures", "outright")
pf = [b for b in pending if (b.get("Type") or "").strip().lower() in FUT]
L = [head("BET TRACKER - OPEN FUTURES")]
L.append(f"Open futures: {len(pf)}   Total risk: {money(sum(f(b.get('Risk')) for b in pf))}"
         f"   Max win: {money(sum(f(b.get('To Win')) for b in pf))}")
L.append("")
grp = defaultdict(list)
for b in pf:
    grp[f"{b.get('Sport') or '?'} / {b.get('League') or '?'}"].append(b)
for k in sorted(grp, key=lambda k: -sum(f(b.get("Risk")) for b in grp[k])):
    rows = sorted(grp[k], key=lambda b: -f(b.get("Risk")))
    L.append(f"--- {k}  ({len(rows)} open, risk {money(sum(f(b.get('Risk')) for b in rows))}) ---")
    for b in rows:
        L.append(f"  [{b.get('ID')}] {b.get('Date')} | {b.get('Pick') or b.get('Description')}")
        L.append(f"        {b.get('Description')}")
        L.append(f"        odds {b.get('Odds') or 'n/a':<7} risk {money(f(b.get('Risk'))):<13}"
                 f" to win {money(f(b.get('To Win'))):<13} book {book_of(b)}")
    L.append("")
futures = "\n".join(L) + "\n"

# ---------------------------------------------------------------- pending.txt
L = [head("BET TRACKER - ALL OPEN BETS")]
L.append(f"Open bets: {len(pending)}   Total risk: {money(pend_risk)}   Max win: {money(pend_max)}")
L.append("")
for b in sorted(pending, key=lambda b: -f(b.get("Risk"))):
    L.append(f"[{b.get('ID')}] {b.get('Date')} | {b.get('Sport')}/{b.get('League')} | {b.get('Type')}")
    L.append(f"     {b.get('Description')}")
    L.append(f"     pick {b.get('Pick')} | odds {b.get('Odds') or 'n/a'} | risk {money(f(b.get('Risk')))}"
             f" | to win {money(f(b.get('To Win')))} | book {book_of(b)}")
pend_txt = "\n".join(L) + "\n"

# ---------------------------------------------------------------- teams.txt
# Per-team index of OPEN bets. Exists so a "what do I have on <team>?" question
# resolves from one contiguous block instead of scanning a league-grouped file.
TRAIL = re.compile(
    r"\s+(over|under|o|u)\s*[\d.]+$|\s*[+-]\d+(\.\d+)?$|\s+ml$|\s+moneyline$",
    re.IGNORECASE)


def team_of(b):
    p = (b.get("Pick") or "").strip()
    if not p or len(p) > 60:
        return None
    prev = None
    while prev != p:
        prev = p
        p = TRAIL.sub("", p).strip()
    return p or None


by_team = defaultdict(list)
for b in pending:
    t = team_of(b)
    if t:
        by_team[t].append(b)

L = [head("BET TRACKER - OPEN BETS BY TEAM")]
L.append("Alphabetical index of every team/selection with at least one OPEN bet.")
L.append("To answer 'what do I have on <team>?', find the team heading below and read")
L.append("every line under it. A team may hold several open bets (e.g. a season win")
L.append("total AND a championship future) - report all of them, not just the first.")
L.append("")
L.append(f"Teams with open action: {len(by_team)}")
L.append("")
L.append("QUICK INDEX: " + ", ".join(sorted(by_team)))
L.append("")
for t in sorted(by_team):
    rows = by_team[t]
    tr = sum(f(b.get("Risk")) for b in rows)
    tw = sum(f(b.get("To Win")) for b in rows)
    L.append(f"### {t}  --  {len(rows)} open bet{'s' if len(rows) != 1 else ''},"
             f" risk {money(tr)}, max win {money(tw)}")
    for b in sorted(rows, key=lambda b: -f(b.get("Risk"))):
        L.append(f"    [{b.get('ID')}] {b.get('Date')} | {b.get('Type')}"
                 f" | {b.get('Sport')}/{b.get('League')}")
        L.append(f"        {b.get('Description')}")
        L.append(f"        pick {b.get('Pick')} | odds {b.get('Odds') or 'n/a'}"
                 f" | risk {money(f(b.get('Risk')))} | to win {money(f(b.get('To Win')))}"
                 f" | book {book_of(b)}")
    L.append("")
teams = "\n".join(L) + "\n"

# ---------------------------------------------------------------- stats.txt
L = [head("BET TRACKER - BREAKDOWNS")]


def table(title, keyfn, rows_src=settled):
    d = defaultdict(lambda: {"w": 0, "l": 0, "p": 0, "r": 0.0, "n": 0.0})
    for b in rows_src:
        v = d[keyfn(b)]
        v["r"] += f(b.get("Risk"))
        v["n"] += pnl(b)
        v["w" if st(b) in ("won", "half-won") else "l" if st(b) in ("lost", "half-lost") else "p"] += 1
    L.append(title)
    L.append(f"  {'Key':<28}{'Record':<14}{'Risked':>13}{'Net P&L':>13}{'ROI':>9}")
    for k, v in sorted(d.items(), key=lambda x: -x[1]["n"]):
        r = f"{v['w']}W-{v['l']}L-{v['p']}P"
        ro = (v["n"] / v["r"] * 100) if v["r"] else 0.0
        L.append(f"  {str(k)[:27]:<28}{r:<14}{money(v['r']):>13}{money(v['n']):>13}{ro:>8.1f}%")
    L.append("")


table("BY SPORT", lambda b: b.get("Sport") or "Unknown")
table("BY LEAGUE", lambda b: f"{b.get('Sport')}/{b.get('League')}")
table("BY BET TYPE", lambda b: (b.get("Type") or "unknown").lower())
table("BY BOOK (Notes-derived; most rows untagged)", book_of)
table("BY MONTH PLACED", lambda b: (b.get("Date") or "?")[:7])

# streaks
seq = sorted([b for b in settled if st(b) in ("won", "lost", "half-won", "half-lost")],
             key=lambda b: (b.get("Result Date") or b.get("Date") or "", int(b.get("ID") or 0)))
best = cur = 0
worst = curl = 0
for b in seq:
    if st(b) in ("won", "half-won"):
        cur += 1; curl = 0; best = max(best, cur)
    else:
        curl += 1; cur = 0; worst = max(worst, curl)
tail = "".join("W" if st(b) in ("won", "half-won") else "L" for b in seq[-40:])
L.append("STREAKS (settled, chronological by result date)")
L.append(f"  Longest win streak : {best}")
L.append(f"  Longest loss streak: {worst}")
L.append(f"  Last 40 results    : {tail}")
L.append("")

L.append("TOP 10 WINS (realized profit)")
for b in sorted(won, key=lambda b: -f(b.get("To Win")))[:10]:
    L.append(f"  +{money(f(b.get('To Win'))):<13} [{b.get('ID')}] {b.get('Result Date') or b.get('Date')}"
             f" {b.get('Odds') or '':>7} | {(b.get('Description') or '')[:62]}")
L.append("")
L.append("TOP 10 LOSSES (realized loss)")
for b in sorted(lost, key=lambda b: -f(b.get("Risk")))[:10]:
    L.append(f"  -{money(f(b.get('Risk'))):<13} [{b.get('ID')}] {b.get('Result Date') or b.get('Date')}"
             f" {b.get('Odds') or '':>7} | {(b.get('Description') or '')[:62]}")
L.append("")
stats = "\n".join(L) + "\n"

# ---------------------------------------------------------------- write
files = {"brief.txt": brief, "futures.txt": futures, "pending.txt": pend_txt,
         "teams.txt": teams, "stats.txt": stats}
for name, body in files.items():
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
        fh.write(body)
    # HTML mirror: identical text, wrapped so HTML-preferring fetchers get it too
    stem = name[:-4]
    page = (f"<!doctype html><html lang=en><head><meta charset=utf-8>"
            f"<meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>Bet Tracker - {stem}</title>"
            f"<meta name=description content='Plain-text digest of Nick Ritchey bet tracker: {stem}. Generated {STAMP}.'>"
            f"</head><body><pre style=\"font:13px/1.45 ui-monospace,Menlo,Consolas,monospace;"
            f"white-space:pre-wrap;word-wrap:break-word;margin:16px\">\n"
            f"{html.escape(body)}</pre></body></html>\n")
    with open(os.path.join(ROOT, stem + ".html"), "w", encoding="utf-8") as fh:
        fh.write(page)

rows = "".join(
    f"<li><a href='{s}.txt'>{s}.txt</a> &nbsp;<a href='{s}.html'>(html)</a> &mdash; {d}</li>"
    for s, d in [("brief", "headline record, P&amp;L, ROI, exposure by sport"),
                 ("futures", "every open future, grouped by league"),
                 ("pending", "every open bet with stake and price"),
                 ("teams", "open bets grouped by team &mdash; best for &ldquo;what do I have on X?&rdquo;"),
                 ("stats", "breakdowns by sport/league/type/book/month, streaks, best &amp; worst")])
with open(os.path.join(ROOT, "ask.html"), "w", encoding="utf-8") as fh:
    fh.write(f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Bet Tracker - LLM-readable digests</title>
<meta name=description content="Small plain-text digests of the bet tracker, readable without JavaScript.">
</head><body style="font:15px/1.6 system-ui,sans-serif;max-width:52em;margin:2em auto;padding:0 1em">
<h1>Bet Tracker &mdash; readable digests</h1>
<p>Generated {STAMP}. Static text, no JavaScript, safe to fetch and quote.
{len(bets)} bets &middot; {len(won)}W-{len(lost)}L-{len(push)}P &middot; net {money(net)}
&middot; {len(pending)} open risking {money(pend_risk)}.</p>
<ul>{rows}</ul>
<p><strong>Note:</strong> &ldquo;To Win&rdquo; is profit, not total payout.
Full ledger: <a href="bets.csv">bets.csv</a>. Interactive dashboard:
<a href="./">dashboard</a>.</p>
</body></html>
""")

# ---------------------------------------------------------------- summary.txt appendix
# The "Bet tracking" project restricts web search to summary.txt alone, so a team
# question there cannot reach teams.txt. Append a compact team index (one line per
# bet) to summary.txt so that single allowed file can answer team questions too.
A = []
A.append("")
A.append("=" * 78)
A.append("OPEN BETS BY TEAM  (compact index - every open bet, grouped by team)")
A.append("=" * 78)
A.append("A team may hold SEVERAL open bets (e.g. a win total AND a championship")
A.append("future). Read every line under a heading and report all of them.")
A.append("'win' below is PROFIT, not total payout. Nicknames: map Huskies->Washington,")
A.append("Buckeyes->Ohio State, Ducks->Oregon, etc. No heading = no open bet.")
A.append("")
A.append(f"Teams with open action ({len(by_team)}): " + ", ".join(sorted(by_team)))
A.append("")
for t in sorted(by_team):
    rows = by_team[t]
    tr = sum(f(b.get("Risk")) for b in rows)
    tw = sum(f(b.get("To Win")) for b in rows)
    A.append(f"### {t}  --  {len(rows)} open, risk {money(tr)}, max win {money(tw)}")
    for b in sorted(rows, key=lambda b: -f(b.get("Risk"))):
        A.append(f"    [{b.get('ID')}] {b.get('Date')} {b.get('Type')} "
                 f"{b.get('League')} | {b.get('Pick')} | {b.get('Odds') or 'n/a'} | "
                 f"risk {money(f(b.get('Risk')))} | win {money(f(b.get('To Win')))} | "
                 f"{book_of(b)} | {b.get('Description')}")
A.append("")
A.append("=" * 78)
A.append("SETTLED BY SPORT")
A.append("=" * 78)
A.append(f"  {'Sport':<14}{'Record':<14}{'Risked':>13}{'Net P&L':>13}{'ROI':>9}")
for k, v in sorted(bysport.items(), key=lambda x: -x[1]["n"]):
    r = f"{v['w']}W-{v['l']}L-{v['p']}P"
    ro = (v["n"] / v["r"] * 100) if v["r"] else 0.0
    A.append(f"  {k[:13]:<14}{r:<14}{money(v['r']):>13}{money(v['n']):>13}{ro:>8.1f}%")
A.append("")
A.append("Deeper cuts (breakdowns by league/type/book/month, streaks, biggest wins and")
A.append(f"losses): {BASE}/stats.txt")
A.append("")

summary_path = os.path.join(ROOT, "summary.txt")
with open(summary_path, encoding="utf-8") as fh:
    base_summary = fh.read()
marker = "OPEN BETS BY TEAM"
if marker in base_summary:  # idempotent: drop any prior appendix before re-adding
    base_summary = base_summary[:base_summary.index("=" * 78)].rstrip() + "\n"
with open(summary_path, "w", encoding="utf-8") as fh:
    fh.write(base_summary.rstrip() + "\n" + "\n".join(A))

print(f"OK: digests for {len(bets)} bets ({len(pending)} open).")
print(f"  summary.txt   {os.path.getsize(summary_path) / 1024:6.1f} KB (with team appendix)")
for n in list(files) + ["ask.html"]:
    print(f"  {n:<14}{os.path.getsize(os.path.join(ROOT, n)) / 1024:6.1f} KB")
