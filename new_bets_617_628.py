#!/usr/bin/env python3
"""Add 22 bets covering 6/17-6/28 to FALLBACK_BETS.

Date breakdown:
- 6/17: 1 bet (3-team parlay LOST)
- 6/19: 6 bets (9-leg parlay + 5-tier RR all DRAW picks, ALL LOST)
- 6/21: 3 bets (Golf - Travelers, all WON)
- 6/24: 2 bets (2nd-half soccer markets)
- 6/25: 1 bet (9-leg parlay LOST)
- 6/27: 6 bets (3x 9-leg parlays + 3-tier RR partial win)
- 6/28: 3 bets (3x 9-leg parlays, 2 WON / 1 LOST, net +$1,803)
"""
import json, re

INDEX_FILE = "/home/user/workspace/bet-tracker/index.html"

# Each bet as dict matching FALLBACK_BETS schema. ID assigned sequentially starting at 1667.
NEW_BETS = []

# ----- 6/17 -----
NEW_BETS.append({
    "Date": "2026-06-17",
    "Sport": "Soccer",
    "League": "International",
    "Event": "3-team parlay POR/GHA/ENG",
    "Type": "Parlay",
    "Description": "Portugal ML -385 (L) / Ghana PK,-0.5 +100 (W) / England -0.5 -145 (W)",
    "Pick": "3-leg",
    "Opponent": "Various",
    "Odds": "Combo",
    "Risk": "150",
    "To Win": "0",
    "Status": "lost",
    "Result Date": "2026-06-17",
    "Notes": "Wagerhouse ticket. Portugal ML loss broke the parlay.",
})

# ----- 6/19 -----
NEW_BETS.append({
    "Date": "2026-06-19",
    "Sport": "Soccer",
    "League": "International",
    "Event": "9-leg parlay #392066176",
    "Type": "Parlay",
    "Description": "9-leg parlay: USA ML / BRA HT/FT / BTTS SCO-MOR / BTTS USA-AUS / DEU ML + 4 more",
    "Pick": "9-leg",
    "Opponent": "Various",
    "Odds": "Combo",
    "Risk": "125",
    "To Win": "0",
    "Status": "lost",
    "Result Date": "2026-06-19",
    "Notes": "Wagerhouse ticket #392066176. Risk corrected from prior $145 reading to $125 per user.",
})

# 6/19 - 5-leg RR all DRAW picks: Mor/Sco +280, Par/Tur +235, Alg/Jor +320, Aus/USA +325, Swe/Ned +290 - ALL LOST
RR_PICKS_619 = "Mor/Sco +280 / Par/Tur +235 / Alg/Jor +320 / Aus/USA +325 / Swe/Ned +290 - all DRAW picks"
NEW_BETS.append({
    "Date": "2026-06-19",
    "Sport": "Soccer",
    "League": "International",
    "Event": "5-leg RR (DRAW picks) - 1-way singles",
    "Type": "Round Robin",
    "Description": f"5 singles @ $1 each ({RR_PICKS_619})",
    "Pick": "5 singles @ $1",
    "Opponent": "Various",
    "Odds": "Mixed",
    "Risk": "5",
    "To Win": "0",
    "Status": "lost",
    "Result Date": "2026-06-19",
    "Notes": "Wagerhouse 5-leg all-DRAW RR. 1-way tier: 5 singles x $1 = $5. ALL DRAW picks lost.",
})
NEW_BETS.append({
    "Date": "2026-06-19",
    "Sport": "Soccer",
    "League": "International",
    "Event": "5-leg RR (DRAW picks) - 2-way combos",
    "Type": "Round Robin",
    "Description": f"10 2-team parlays @ $20 each ({RR_PICKS_619})",
    "Pick": "10 parlays @ $20",
    "Opponent": "Various",
    "Odds": "Mixed",
    "Risk": "200",
    "To Win": "0",
    "Status": "lost",
    "Result Date": "2026-06-19",
    "Notes": "Wagerhouse 5-leg all-DRAW RR. 2-way tier: 10 combos x $20 = $200. ALL DRAW picks lost.",
})
NEW_BETS.append({
    "Date": "2026-06-19",
    "Sport": "Soccer",
    "League": "International",
    "Event": "5-leg RR (DRAW picks) - 3-way combos",
    "Type": "Round Robin",
    "Description": f"10 3-team parlays @ $10 each ({RR_PICKS_619})",
    "Pick": "10 parlays @ $10",
    "Opponent": "Various",
    "Odds": "Mixed",
    "Risk": "100",
    "To Win": "0",
    "Status": "lost",
    "Result Date": "2026-06-19",
    "Notes": "Wagerhouse 5-leg all-DRAW RR. 3-way tier: 10 combos x $10 = $100. ALL DRAW picks lost.",
})
NEW_BETS.append({
    "Date": "2026-06-19",
    "Sport": "Soccer",
    "League": "International",
    "Event": "5-leg RR (DRAW picks) - 4-way combos",
    "Type": "Round Robin",
    "Description": f"5 4-team parlays @ $5 each ({RR_PICKS_619})",
    "Pick": "5 parlays @ $5",
    "Opponent": "Various",
    "Odds": "Mixed",
    "Risk": "25",
    "To Win": "0",
    "Status": "lost",
    "Result Date": "2026-06-19",
    "Notes": "Wagerhouse 5-leg all-DRAW RR. 4-way tier: 5 combos x $5 = $25. ALL DRAW picks lost.",
})
NEW_BETS.append({
    "Date": "2026-06-19",
    "Sport": "Soccer",
    "League": "International",
    "Event": "5-leg RR (DRAW picks) - 5-way combo",
    "Type": "Round Robin",
    "Description": f"1 5-team parlay @ $5 ({RR_PICKS_619})",
    "Pick": "1 parlay @ $5",
    "Opponent": "Various",
    "Odds": "Mixed",
    "Risk": "5",
    "To Win": "0",
    "Status": "lost",
    "Result Date": "2026-06-19",
    "Notes": "Wagerhouse 5-leg all-DRAW RR. 5-way tier: 1 combo x $5 = $5. ALL DRAW picks lost.",
})

# ----- 6/21 Golf - Travelers Championship, all WON -----
NEW_BETS.append({
    "Date": "2026-06-21",
    "Sport": "Golf",
    "League": "PGA Tour",
    "Event": "2026 Travelers Championship",
    "Type": "top20",
    "Description": "Scottie Scheffler Top 20 finish",
    "Pick": "Scottie Scheffler T20",
    "Opponent": "Field",
    "Odds": "-175",
    "Risk": "759.50",
    "To Win": "434",
    "Status": "won",
    "Result Date": "2026-06-22",
    "Notes": "Wagerhouse ticket G301537113.",
})
NEW_BETS.append({
    "Date": "2026-06-21",
    "Sport": "Golf",
    "League": "PGA Tour",
    "Event": "2026 Travelers Championship",
    "Type": "Outright Winner",
    "Description": "Wyndham Clark to win Travelers (in-event price)",
    "Pick": "Wyndham Clark",
    "Opponent": "Field",
    "Odds": "-320",
    "Risk": "640",
    "To Win": "200",
    "Status": "won",
    "Result Date": "2026-06-22",
    "Notes": "Wagerhouse ticket G302013831.",
})
NEW_BETS.append({
    "Date": "2026-06-21",
    "Sport": "Golf",
    "League": "PGA Tour",
    "Event": "2026 Travelers Championship",
    "Type": "Outright Winner",
    "Description": "Wyndham Clark to win Travelers (in-event price)",
    "Pick": "Wyndham Clark",
    "Opponent": "Field",
    "Odds": "-320",
    "Risk": "80",
    "To Win": "25",
    "Status": "won",
    "Result Date": "2026-06-22",
    "Notes": "Wagerhouse ticket G302013967.",
})

# ----- 6/24 -----
NEW_BETS.append({
    "Date": "2026-06-24",
    "Sport": "Soccer",
    "League": "International",
    "Event": "Switzerland match (2H)",
    "Type": "2H ML",
    "Description": "Switzerland 2nd Half ML",
    "Pick": "Switzerland 2H ML",
    "Opponent": "",
    "Odds": "+180",
    "Risk": "100",
    "To Win": "180",
    "Status": "won",
    "Result Date": "2026-06-24",
    "Notes": "Wagerhouse 2nd-half market.",
})
NEW_BETS.append({
    "Date": "2026-06-24",
    "Sport": "Soccer",
    "League": "International",
    "Event": "Qatar vs Bosnia (2H)",
    "Type": "2H DRAW",
    "Description": "Qatar/Bosnia 2nd Half DRAW",
    "Pick": "DRAW",
    "Opponent": "Various",
    "Odds": "+175",
    "Risk": "100",
    "To Win": "175",
    "Status": "lost",
    "Result Date": "2026-06-24",
    "Notes": "Wagerhouse 2nd-half market.",
})

# ----- 6/25 -----
NEW_BETS.append({
    "Date": "2026-06-25",
    "Sport": "Soccer",
    "League": "International",
    "Event": "9-leg parlay #392650228",
    "Type": "Parlay",
    "Description": "9-leg parlay: BTTS TUR-USA / HT/FT NED-NED / BTTS NOR-FRA / Over 2.5 JPN-SWE + 5 more",
    "Pick": "9-leg",
    "Opponent": "Various",
    "Odds": "Combo",
    "Risk": "121",
    "To Win": "0",
    "Status": "lost",
    "Result Date": "2026-06-25",
    "Notes": "Wagerhouse ticket #392650228.",
})

# ----- 6/27 -----
NEW_BETS.append({
    "Date": "2026-06-27",
    "Sport": "Soccer",
    "League": "International",
    "Event": "9-leg parlay #392652491",
    "Type": "Parlay",
    "Description": "9-leg parlay: NED ML / BTTS TUR-USA / DRAW EGY-IRN / BTTS NOR-FRA / BTTS COL-PRT / PRT ML + 3 more",
    "Pick": "9-leg",
    "Opponent": "Various",
    "Odds": "Combo",
    "Risk": "100",
    "To Win": "0",
    "Status": "lost",
    "Result Date": "2026-06-27",
    "Notes": "Wagerhouse ticket #392652491.",
})
NEW_BETS.append({
    "Date": "2026-06-27",
    "Sport": "Soccer",
    "League": "International",
    "Event": "9-leg parlay #392751940",
    "Type": "Parlay",
    "Description": "9-leg parlay: DC EGY-IRN / BTTS COL-PRT / PRT ML / BTTS URU-ESP + 5 more",
    "Pick": "9-leg",
    "Opponent": "Various",
    "Odds": "Combo",
    "Risk": "200",
    "To Win": "0",
    "Status": "lost",
    "Result Date": "2026-06-27",
    "Notes": "Wagerhouse ticket #392751940.",
})
NEW_BETS.append({
    "Date": "2026-06-27",
    "Sport": "Mixed",
    "League": "Mixed",
    "Event": "9-leg parlay #392802134",
    "Type": "Parlay",
    "Description": "9-leg parlay: ENG ML PAN-ENG / ARG ML JOR-ARG / COD ML COD-UZB / 1st Inning DRAW CIN@PIT / 1st Inning DRAW SEA@CLE + 4 more",
    "Pick": "9-leg",
    "Opponent": "Various",
    "Odds": "Combo",
    "Risk": "250",
    "To Win": "0",
    "Status": "lost",
    "Result Date": "2026-06-27",
    "Notes": "Wagerhouse ticket #392802134. Cross-sport (Soccer + MLB 1st innings).",
})

# 6/27 RR - 5 picks: Aus/Par DRAW +135 (W), Iran/Egy DRAW +165 (W),
#                  Ghana/Cro DRAW +225 (L), Portugal ML -120 (L), Austria/Alg DRAW +120 (W)
RR_PICKS_627 = "Aus/Par DRAW +135 (W) / Iran/Egy DRAW +165 (W) / Gha/Cro DRAW +225 (L) / Portugal ML -120 (L) / Austria/Alg DRAW +120 (W)"

# 2-way: 10 combos x $15 = $150. Winning pairs (need both W): (Aus/Par + Iran/Egy), (Aus/Par + Aus/Alg), (Iran/Egy + Aus/Alg)
# Payouts (decimal): +135=2.35, +165=2.65, +120=2.20
#   (Aus/Par + Iran/Egy): 2.35*2.65 = 6.2275 -> $15 -> $93.41 return, +$78.41
#   (Aus/Par + Aus/Alg):  2.35*2.20 = 5.17   -> $15 -> $77.55 return, +$62.55
#   (Iran/Egy + Aus/Alg): 2.65*2.20 = 5.83   -> $15 -> $87.45 return, +$72.45
# 2-way net: -$15*7 + $78.41 + $62.55 + $72.45 = -$105 + $213.41 = +$108.41
NEW_BETS.append({
    "Date": "2026-06-27",
    "Sport": "Soccer",
    "League": "International",
    "Event": "5-leg RR - 2-way combos",
    "Type": "Round Robin",
    "Description": f"10 2-team parlays @ $15 each ({RR_PICKS_627})",
    "Pick": "10 parlays @ $15",
    "Opponent": "Various",
    "Odds": "Mixed",
    "Risk": "0",
    "To Win": "108.41",
    "Status": "won",
    "Result Date": "2026-06-27",
    "Notes": "Wagerhouse 5-leg RR. 2-way tier: 10 combos x $15 = $150 stake. 3 winning combos: Aus/Par+Iran/Egy ($78.41), Aus/Par+Aus/Alg ($62.55), Iran/Egy+Aus/Alg ($72.45). Net +$108.41.",
})

# 3-way: 10 combos x $15 = $150. Only 1 winner: (Aus/Par + Iran/Egy + Aus/Alg)
#   Decimal: 2.35*2.65*2.20 = 13.7005 -> $15 -> $205.51 return, +$190.51
# 3-way net: -$15*9 + $190.51 = -$135 + $190.51 = +$55.51
NEW_BETS.append({
    "Date": "2026-06-27",
    "Sport": "Soccer",
    "League": "International",
    "Event": "5-leg RR - 3-way combos",
    "Type": "Round Robin",
    "Description": f"10 3-team parlays @ $15 each ({RR_PICKS_627})",
    "Pick": "10 parlays @ $15",
    "Opponent": "Various",
    "Odds": "Mixed",
    "Risk": "0",
    "To Win": "55.51",
    "Status": "won",
    "Result Date": "2026-06-27",
    "Notes": "Wagerhouse 5-leg RR. 3-way tier: 10 combos x $15 = $150 stake. 1 winning combo: Aus/Par+Iran/Egy+Aus/Alg paid $205.51. Net +$55.51.",
})

# 4-way: 5 combos x $10 = $50. Need 4 W; only have 3 W -> all combos lose.
NEW_BETS.append({
    "Date": "2026-06-27",
    "Sport": "Soccer",
    "League": "International",
    "Event": "5-leg RR - 4-way combos",
    "Type": "Round Robin",
    "Description": f"5 4-team parlays @ $10 each ({RR_PICKS_627})",
    "Pick": "5 parlays @ $10",
    "Opponent": "Various",
    "Odds": "Mixed",
    "Risk": "50",
    "To Win": "0",
    "Status": "lost",
    "Result Date": "2026-06-27",
    "Notes": "Wagerhouse 5-leg RR. 4-way tier: 5 combos x $10 = $50 stake. Every 4-way requires 4 winners but only 3 picks hit. All combos lost.",
})

# ----- 6/28 -----
NEW_BETS.append({
    "Date": "2026-06-28",
    "Sport": "Mixed",
    "League": "Mixed",
    "Event": "9-leg parlay #392802361",
    "Type": "Parlay",
    "Description": "9-leg parlay: ENG ML PAN-ENG / ARG ML JOR-ARG / DC COL/DRAW COL-PRT / COD ML COD-UZB + 5 more",
    "Pick": "9-leg",
    "Opponent": "Various",
    "Odds": "Combo",
    "Risk": "350",
    "To Win": "1120",
    "Status": "won",
    "Result Date": "2026-06-28",
    "Notes": "Wagerhouse ticket #392802361. Won +$1,120.",
})
NEW_BETS.append({
    "Date": "2026-06-28",
    "Sport": "Mixed",
    "League": "Mixed",
    "Event": "9-leg parlay #392819170",
    "Type": "Parlay",
    "Description": "9-leg parlay: COD ML COD-UZB / ARG ML JOR-ARG / 1st Inning DRAW SEA@CLE + 6 more",
    "Pick": "9-leg",
    "Opponent": "Various",
    "Odds": "Combo",
    "Risk": "350",
    "To Win": "833",
    "Status": "won",
    "Result Date": "2026-06-28",
    "Notes": "Wagerhouse ticket #392819170. Won +$833. Cross-sport (Soccer + MLB 1st inning).",
})
NEW_BETS.append({
    "Date": "2026-06-28",
    "Sport": "Soccer",
    "League": "International",
    "Event": "9-leg parlay #392841418",
    "Type": "Parlay",
    "Description": "9-leg parlay: DC JOR/DRAW JOR-ARG / O0.5 JOR JOR-ARG / FRA ML FRA-SWE / USA ML USA-BIH / DEU ML DEU-PAR / BRA ML BRA-JPN + 3 more",
    "Pick": "9-leg",
    "Opponent": "Various",
    "Odds": "Combo",
    "Risk": "150",
    "To Win": "0",
    "Status": "lost",
    "Result Date": "2026-06-28",
    "Notes": "Wagerhouse ticket #392841418.",
})

# Assign IDs starting at 1667
START_ID = 1667
for i, b in enumerate(NEW_BETS):
    b["ID"] = str(START_ID + i)

print(f"Prepared {len(NEW_BETS)} bets, IDs {START_ID}-{START_ID + len(NEW_BETS) - 1}")

# Day-net validation
from collections import defaultdict
nets = defaultdict(float)
for b in NEW_BETS:
    risk = float(b["Risk"])
    win = float(b["To Win"])
    if b["Status"] == "won":
        nets[b["Date"]] += win  # if Risk=0 use To Win directly; if Risk>0 use To Win
    elif b["Status"] == "lost":
        nets[b["Date"]] -= risk
for d in sorted(nets):
    print(f"  {d}: {nets[d]:+.2f}")

# ---- Inject into index.html ----
with open(INDEX_FILE, "r") as f:
    html = f.read()

# Find the FALLBACK_BETS closing "];" position
# Strategy: find the entry with "ID": "1666", then locate the next "}\n];"
marker = '"ID": "1666"\n  }\n];'
if marker not in html:
    # Try variants
    print("Marker not found, dumping context near 'ID: 1666'")
    raise SystemExit(1)

# Build new bet entries as JSON-formatted blocks matching the indentation
def format_bet(b):
    lines = ["  {"]
    keys = ["Date", "Sport", "League", "Event", "Type", "Description", "Pick", "Opponent",
            "Odds", "Risk", "To Win", "Status", "Result Date", "Notes", "ID"]
    for i, k in enumerate(keys):
        val = b[k]
        v_json = json.dumps(val, ensure_ascii=False)
        suffix = "" if i == len(keys) - 1 else ","
        lines.append(f'    "{k}": {v_json}{suffix}')
    lines.append("  }")
    return "\n".join(lines)

new_entries = ",\n".join(format_bet(b) for b in NEW_BETS)

# Replace marker with marker minus closing "];" + new entries + "];"
old = '"ID": "1666"\n  }\n];'
new = '"ID": "1666"\n  },\n' + new_entries + "\n];"
html2 = html.replace(old, new, 1)
if html2 == html:
    print("REPLACE FAILED")
    raise SystemExit(2)

with open(INDEX_FILE, "w") as f:
    f.write(html2)

print(f"\nInjected {len(NEW_BETS)} bets into {INDEX_FILE}")
print(f"Last ID: {NEW_BETS[-1]['ID']}")

# Save new bets to JSON for sheet sync
with open("/home/user/workspace/bet-tracker/new_bets_617_628.json", "w") as f:
    json.dump(NEW_BETS, f, indent=2)
print("Saved to new_bets_617_628.json")
