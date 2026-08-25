#!/usr/bin/env python3
"""Add 32 new bets from 2026-08-24 intake:
   - 25 Wagerhouse CFB 26/27 Regular Season Wins + ACC futures
   - 4 Wagerhouse other futures (F1 x2, Mariners x2)
   - 1 Wagerhouse NFL Seahawks Alt Reg Season Wins
   - 1 Wagerhouse NFL 4-team ML parlay (Seahawks/Rams/Lions/Eagles)
   - 2 GameDayWagers CFB futures (Buffalo, Miami ACC) — 08/22 tickets
   Duplicate check completed against 1,807 existing bets; the three GDW 07/26
   tickets (Texas AM/Missouri/James Madison) were already in tracker (IDs
   1798-1800) and are NOT re-added.
"""
import json, re, os, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(ROOT, "index.html")

with open(HTML) as f:
    html = f.read()
m = re.search(r"const FALLBACK_BETS = (\[.*?\]);\s*\n", html, re.DOTALL)
bets = json.loads(m.group(1))
start_id = max(int(b["ID"]) for b in bets) + 1
print(f"Starting new IDs at {start_id}")

INTAKE_DATE = "2026-08-24"  # date these were provided in chat

new = []

# --- Wagerhouse CFB Regular Season Wins futures (23) ---
cfb_wh = [
    # (Team, side, line, odds, risk, to_win)
    ("Western Michigan", "Under", "7.5", "-165", 825, 500),
    ("Massachusetts",   "Over",  "2.5", "-200", 1000, 500),
    ("Connecticut",     "Under", "5.5", "-130", 650, 500),
    ("UCLA",            "Over",  "6.5", "-105", 525, 500),
    ("Tulsa",           "Over",  "5.5", "-130", 650, 500),
    ("Texas State",     "Over",  "6.5", "+125", 500, 625),
    ("Southern Miss",   "Under", "3.5", "+100", 500, 500),
    ("Sacramento State","Under", "4.5", "-110", 550, 500),
    ("North Texas",     "Over",  "5.5", "-115", 575, 500),
    ("Navy",            "Under", "7.5", "+150", 400, 600),
    ("Michigan State",  "Under", "4",   "-120", 500, 416),
    ("Iowa",            "Under", "7.5", "+115", 500, 575),
    ("Georgia Tech",    "Under", "6.5", "-135", 675, 500),
    ("Florida Atlantic","Over",  "5.5", "-160", 800, 500),
    ("Fresno State",    "Under", "7.5", "-165", 825, 500),
    ("Colorado",        "Over",  "4.5", "+130", 500, 650),
    ("Colorado State",  "Over",  "3.5", "-145", 725, 500),
    ("Clemson",         "Under", "7.5", "+125", 500, 625),
    ("Boise State",     "Over",  "8",   "-130", 650, 500),
    ("Baylor",          "Under", "6.5", "-160", 800, 500),
    ("Auburn",          "Over",  "6.5", "-125", 625, 500),
    ("Army",            "Under", "7.5", "+110", 500, 550),
    ("Southern Miss",   "Under", "3.5", "+105", 500, 525),  # 2nd ticket, different price
]
for team, side, line, odds, risk, tw in cfb_wh:
    new.append({
        "Date": INTAKE_DATE,
        "Sport": "Football",
        "League": "NCAAF",
        "Event": "NCAA FB 26/27 Regular Season Wins",
        "Type": "future",
        "Description": f"NCAA FB 26/27 - Regular Season Wins - Props {team} - {side} {line}",
        "Pick": f"{team} {side} {line}",
        "Opponent": "",
        "Odds": odds,
        "Risk": str(risk),
        "To Win": str(tw),
        "Status": "pending",
        "Result Date": "",
        "Notes": "Wagerhouse pending. Pending end of CFB 2026-27 regular season.",
    })

# --- Wagerhouse ACC Championship future ---
new.append({
    "Date": INTAKE_DATE,
    "Sport": "Football",
    "League": "NCAAF",
    "Event": "NCAA FB 26/27 ACC Championship",
    "Type": "future",
    "Description": "NCAA FB 26/27 - Conference Championship Winner - ACC - Miami (FL)",
    "Pick": "Miami (FL)",
    "Opponent": "field",
    "Odds": "-165",
    "Risk": "825",
    "To Win": "500",
    "Status": "pending",
    "Result Date": "",
    "Notes": "Wagerhouse pending. Pending 2026 ACC Championship Game.",
})

# --- Wagerhouse F1 futures (2) ---
new.append({
    "Date": INTAKE_DATE,
    "Sport": "Auto Racing",
    "League": "F1",
    "Event": "F1 2026 Drivers Championship",
    "Type": "future",
    "Description": "F1 2026 Drivers Championship - George Russell",
    "Pick": "George Russell",
    "Opponent": "field",
    "Odds": "+2000",
    "Risk": "250",
    "To Win": "5000",
    "Status": "pending",
    "Result Date": "",
    "Notes": "Wagerhouse pending. Pending end of 2026 F1 season.",
})
new.append({
    "Date": INTAKE_DATE,
    "Sport": "Auto Racing",
    "League": "F1",
    "Event": "F1 2026 Drivers Championship",
    "Type": "future",
    "Description": "F1 2026 Drivers Championship - Kimi Antonelli",
    "Pick": "Kimi Antonelli",
    "Opponent": "field",
    "Odds": "-450",
    "Risk": "4500",
    "To Win": "1000",
    "Status": "pending",
    "Result Date": "",
    "Notes": "Wagerhouse pending. Pending end of 2026 F1 season.",
})

# --- Wagerhouse Mariners futures (2) ---
new.append({
    "Date": INTAKE_DATE,
    "Sport": "Baseball",
    "League": "MLB",
    "Event": "MLB 2026 World Series",
    "Type": "future",
    "Description": "MLB 2026 World Series Winner - Seattle Mariners",
    "Pick": "Seattle Mariners",
    "Opponent": "field",
    "Odds": "+3500",
    "Risk": "250",
    "To Win": "8750",
    "Status": "pending",
    "Result Date": "",
    "Notes": "Wagerhouse pending. Pending 2026 World Series.",
})
new.append({
    "Date": INTAKE_DATE,
    "Sport": "Baseball",
    "League": "MLB",
    "Event": "MLB 2026 AL Pennant",
    "Type": "future",
    "Description": "MLB 2026 AL Pennant Winner - Seattle Mariners",
    "Pick": "Seattle Mariners",
    "Opponent": "field",
    "Odds": "+1200",
    "Risk": "250",
    "To Win": "3000",
    "Status": "pending",
    "Result Date": "",
    "Notes": "Wagerhouse pending. Pending 2026 ALCS.",
})

# --- Wagerhouse Seahawks Alt Reg Season Wins ---
new.append({
    "Date": INTAKE_DATE,
    "Sport": "Football",
    "League": "NFL",
    "Event": "NFL 26/27 Regular Season Wins",
    "Type": "future",
    "Description": "NFL 26/27 - Regular Season Wins - Props SEA Seahawks - Over 11.5 (Alt)",
    "Pick": "Seattle Seahawks Over 11.5 Alt",
    "Opponent": "",
    "Odds": "+150",
    "Risk": "500",
    "To Win": "750",
    "Status": "pending",
    "Result Date": "",
    "Notes": "Wagerhouse pending. Alternate line — separate ticket from Over 10.5 -130 position. Pending end of NFL 2026-27 regular season.",
})

# --- Wagerhouse NFL 4-team ML parlay ---
new.append({
    "Date": INTAKE_DATE,
    "Sport": "Football",
    "League": "NFL",
    "Event": "NFL Week 1 2026 - 4-team ML parlay",
    "Type": "parlay",
    "Description": "4-leg parlay: SEA ML -195 + LAR ML -195 + DET ML -330 + PHI ML -220",
    "Pick": "Seahawks ML + Rams ML + Lions ML + Eagles ML",
    "Opponent": "",
    "Odds": "+234",
    "Risk": "500",
    "To Win": "1168",
    "Status": "pending",
    "Result Date": "",
    "Notes": "Wagerhouse pending. 4-team NFL ML parlay: SEA -195, LAR -195, DET -330, PHI -220. Total return $1,668 (profit $1,168). Combined odds ~+234 back-calculated from stake/return.",
})

# --- GameDayWagers 08/22 tickets (2) ---
new.append({
    "Date": "2026-08-22",
    "Sport": "Football",
    "League": "NCAAF",
    "Event": "NCAA FB 26/27 Regular Season Wins",
    "Type": "future",
    "Description": "NCAA FB 26/27 - Regular Season Wins - Props Buffalo - Under 6.5",
    "Pick": "Buffalo Under 6.5",
    "Opponent": "",
    "Odds": "-200",
    "Risk": "1000",
    "To Win": "500",
    "Status": "pending",
    "Result Date": "",
    "Notes": "GameDayWagers contest ticket #435424278-1. Placed 08/22/2026 16:25. Pending end of CFB 2026-27 regular season.",
})
new.append({
    "Date": "2026-08-22",
    "Sport": "Football",
    "League": "NCAAF",
    "Event": "NCAA FB 26/27 ACC Championship",
    "Type": "future",
    "Description": "NCAA FB 26/27 - Conference Championship Winner - ACC - Miami Hurricanes",
    "Pick": "Miami Hurricanes",
    "Opponent": "field",
    "Odds": "-149",
    "Risk": "745",
    "To Win": "500",
    "Status": "pending",
    "Result Date": "",
    "Notes": "GameDayWagers contest ticket #435423893-1. Placed 08/22/2026 16:15. Pending 2026 ACC Championship Game.",
})

# Assign IDs
for i, b in enumerate(new):
    b["ID"] = str(start_id + i)

print(f"Adding {len(new)} new bets, IDs {new[0]['ID']}-{new[-1]['ID']}")

# Compute totals for sanity
total_risk = sum(float(b["Risk"]) for b in new)
total_win = sum(float(b["To Win"]) for b in new)
print(f"Total risk: ${total_risk:,.2f}")
print(f"Total to-win: ${total_win:,.2f}")

# Rebuild FALLBACK_BETS with a stable field order matching existing rows.
# Existing rows use these keys — preserve order for readable diffs.
FIELDS = ["ID","Date","Sport","League","Event","Type","Description","Pick",
          "Opponent","Odds","Risk","To Win","Status","Result Date","Notes"]

bets_out = bets + [{k: b.get(k, "") for k in FIELDS} for b in new]

# Serialize back into index.html preserving formatting style of existing block.
# Existing serialization uses json.dumps with indent-2? Let's inspect.
new_json = json.dumps(bets_out, indent=1)
new_html = html[:m.start(1)] + new_json + html[m.end(1):]

with open(HTML, "w") as f:
    f.write(new_html)
print(f"index.html updated. New bet count: {len(bets_out)}")
