#!/usr/bin/env python3
"""Add 6/29 GameDayWagers bets: 4 graded straight + 2 pending parlays + 8 pending WC futures.

IDs start at 1689.
"""
import json, re

INDEX_FILE = "/home/user/workspace/bet-tracker/index.html"
NEW_BETS = []

# ===== 6/29 Brazil vs Japan straight bets (graded) =====
NEW_BETS.append({
    "Date": "2026-06-29",
    "Sport": "Soccer",
    "League": "International",
    "Event": "Brazil vs Japan",
    "Type": "1H Total",
    "Description": "Brazil/Japan 1st Half Total - Over 1",
    "Pick": "Over 1 (1H)",
    "Opponent": "",
    "Odds": "+106",
    "Risk": "100",
    "To Win": "106",
    "Status": "push",
    "Result Date": "2026-06-29",
    "Notes": "GameDayWagers ticket #411622273. 1HT total exactly 1 = PUSH.",
})
NEW_BETS.append({
    "Date": "2026-06-29",
    "Sport": "Soccer",
    "League": "International",
    "Event": "Brazil vs Japan",
    "Type": "1H Spread",
    "Description": "Brazil 1st Half Spread -0.5",
    "Pick": "Brazil -0.5 (1H)",
    "Opponent": "Japan",
    "Odds": "+140",
    "Risk": "100",
    "To Win": "140",
    "Status": "lost",
    "Result Date": "2026-06-29",
    "Notes": "GameDayWagers ticket #411622272.",
})
NEW_BETS.append({
    "Date": "2026-06-29",
    "Sport": "Soccer",
    "League": "International",
    "Event": "Brazil vs Japan",
    "Type": "Team Total",
    "Description": "Brazil Team Total - Over 1.5",
    "Pick": "Brazil Over 1.5",
    "Opponent": "",
    "Odds": "-100",
    "Risk": "200",
    "To Win": "200",
    "Status": "won",
    "Result Date": "2026-06-29",
    "Notes": "GameDayWagers ticket #411622271.",
})
NEW_BETS.append({
    "Date": "2026-06-29",
    "Sport": "Soccer",
    "League": "International",
    "Event": "Brazil vs Japan",
    "Type": "ML",
    "Description": "Brazil Game Money Line",
    "Pick": "Brazil ML",
    "Opponent": "Japan",
    "Odds": "-125",
    "Risk": "400",
    "To Win": "320",
    "Status": "won",
    "Result Date": "2026-06-29",
    "Notes": "GameDayWagers ticket #411622270.",
})

# ===== 6/29 5-leg parlays (pending) =====
# Both have same 5 legs: DEU ML (DEU-PAR), BTTS Yes (NED-MRC), NED ML (NED-MRC),
#                       HT/FT BRA/BRA (BRA-JPN), BRA Total Goals Over 2.5 (BRA-JPN)
PARLAY_DESC = "5-leg parlay: DEU ML (DEU-PAR) / BTTS Yes (NED-MRC) / NED ML (NED-MRC) / HT/FT BRA/BRA (BRA-JPN) / BRA Total Goals Over 2.5 (BRA-JPN)"
NEW_BETS.append({
    "Date": "2026-06-29",
    "Sport": "Soccer",
    "League": "International",
    "Event": "5-leg parlay #411622793",
    "Type": "Parlay",
    "Description": PARLAY_DESC,
    "Pick": "5-leg",
    "Opponent": "Various",
    "Odds": "Combo",
    "Risk": "25",
    "To Win": "950",
    "Status": "pending",
    "Result Date": "",
    "Notes": "GameDayWagers ticket #411622793.",
})
NEW_BETS.append({
    "Date": "2026-06-29",
    "Sport": "Soccer",
    "League": "International",
    "Event": "5-leg parlay #411622757",
    "Type": "Parlay",
    "Description": PARLAY_DESC,
    "Pick": "5-leg",
    "Opponent": "Various",
    "Odds": "Combo",
    "Risk": "75",
    "To Win": "2850",
    "Status": "pending",
    "Result Date": "",
    "Notes": "GameDayWagers ticket #411622757. Larger stake on same 5 legs as #411622793.",
})

# ===== 6/29 WC futures - Stage of Elimination props (all pending) =====
# These bet the team gets eliminated AT this stage (i.e., reaches but loses at this round)
def fut(ticket, team, stage, odds, risk, towin, opp=""):
    return {
        "Date": "2026-06-29",
        "Sport": "Soccer",
        "League": "FIFA",
        "Event": "2026 FIFA World Cup - Stage of Elimination",
        "Type": "future",
        "Description": f"{team} eliminated in {stage}",
        "Pick": f"{team} - {stage}",
        "Opponent": opp,
        "Odds": odds,
        "Risk": str(risk),
        "To Win": str(towin),
        "Status": "pending",
        "Result Date": "",
        "Notes": f"GameDayWagers ticket #{ticket}. Stage-of-elimination prop.",
    }

NEW_BETS.append(fut("411621906", "Colombia",      "Quarter finals", "+200",  500, 1000))
NEW_BETS.append(fut("411621905", "Ivory Coast",   "Last 32",        "-185",  925, 500))
NEW_BETS.append(fut("411621904", "United States", "Quarter finals", "+240",  500, 1200))
NEW_BETS.append(fut("411621903", "Argentina",     "Runner up",      "+425",  500, 2125))
NEW_BETS.append(fut("411621902", "Norway",        "Last 16",        "+150",  500, 750))
NEW_BETS.append(fut("411621901", "Netherlands",   "Quarter-Finals", "+275",  400, 1100))
NEW_BETS.append(fut("411621900", "Germany",       "Last 16",        "+110", 1000, 1100))
NEW_BETS.append(fut("411621899", "Portugal",      "Last 16",        "+150", 1000, 1500))

# Assign IDs starting at 1689
START_ID = 1689
for i, b in enumerate(NEW_BETS):
    b["ID"] = str(START_ID + i)

print(f"Prepared {len(NEW_BETS)} bets, IDs {START_ID}-{START_ID + len(NEW_BETS) - 1}")

# Summary
from collections import defaultdict
nets = defaultdict(float)
pending_risk = 0
for b in NEW_BETS:
    risk = float(b["Risk"])
    win = float(b["To Win"])
    if b["Status"] == "won":
        nets[b["Date"]] += win
    elif b["Status"] == "lost":
        nets[b["Date"]] -= risk
    elif b["Status"] == "pending":
        pending_risk += risk
for d in sorted(nets):
    print(f"  {d} graded: {nets[d]:+.2f}")
print(f"  Pending risk exposed: ${pending_risk:.2f}")

# Inject
with open(INDEX_FILE, "r") as f:
    html = f.read()

def format_bet(b):
    lines = ["  {"]
    keys = ["Date", "Sport", "League", "Event", "Type", "Description", "Pick", "Opponent",
            "Odds", "Risk", "To Win", "Status", "Result Date", "Notes", "ID"]
    for i, k in enumerate(keys):
        v_json = json.dumps(b[k], ensure_ascii=False)
        suffix = "" if i == len(keys) - 1 else ","
        lines.append(f'    "{k}": {v_json}{suffix}')
    lines.append("  }")
    return "\n".join(lines)

new_entries = ",\n".join(format_bet(b) for b in NEW_BETS)

# Last ID injected was 1688
old = '"ID": "1688"\n  }\n];'
new = '"ID": "1688"\n  },\n' + new_entries + "\n];"
html2 = html.replace(old, new, 1)
if html2 == html:
    print("REPLACE FAILED")
    raise SystemExit(2)

with open(INDEX_FILE, "w") as f:
    f.write(html2)

print(f"Injected. Last ID: {NEW_BETS[-1]['ID']}")

with open("/home/user/workspace/bet-tracker/new_bets_629.json", "w") as f:
    json.dump(NEW_BETS, f, indent=2)
