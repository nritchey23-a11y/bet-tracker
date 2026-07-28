"""Add 14 new pending futures (10 Wagerhouse + 4 GameDayWagers). Skip Nebraska (dup of ID 1728)."""
import json, re
from pathlib import Path

ROOT = Path("/home/user/workspace/bet-tracker")
HTML = ROOT / "index.html"

new_bets = []

# ============ WAGERHOUSE - 10 futures (image 1) ============
# Date visible via pending page 7/28; use 2026-07-27 as placement date best-guess.
WH_DATE = "2026-07-27"

new_bets.append({
    "Date": WH_DATE, "Sport": "Football", "League": "NCAAF",
    "Event": "2026-27 Regular Season Wins - Texas A&M",
    "Type": "future",
    "Description": "NCAA FB 26/27 - Regular Season Wins - Texas A&M - Under 8.5",
    "Pick": "Texas A&M Under 8.5", "Opponent": "", "Odds": "-115",
    "Risk": "500", "To Win": "434", "Status": "pending", "Result Date": "",
    "Notes": "Wagerhouse pending. Pending end of CFB 2026-27 regular season."
})
new_bets.append({
    "Date": WH_DATE, "Sport": "Football", "League": "NCAAF",
    "Event": "2026-27 Regular Season Wins - Missouri",
    "Type": "future",
    "Description": "NCAA FB 26/27 - Regular Season Wins - Missouri - Under 6.5",
    "Pick": "Missouri Under 6.5", "Opponent": "", "Odds": "-110",
    "Risk": "275", "To Win": "250", "Status": "pending", "Result Date": "",
    "Notes": "Wagerhouse pending. Pending end of CFB 2026-27 regular season."
})
new_bets.append({
    "Date": WH_DATE, "Sport": "Football", "League": "NCAAF",
    "Event": "2026-27 Regular Season Wins - James Madison",
    "Type": "future",
    "Description": "NCAA FB 26/27 - Regular Season Wins - James Madison - Under 8.5",
    "Pick": "James Madison Under 8.5", "Opponent": "", "Odds": "+115",
    "Risk": "250", "To Win": "287", "Status": "pending", "Result Date": "",
    "Notes": "Wagerhouse pending. Pending end of CFB 2026-27 regular season."
})
new_bets.append({
    "Date": WH_DATE, "Sport": "Football", "League": "NCAAF",
    "Event": "2026-27 Big 12 Championship Game",
    "Type": "future",
    "Description": "Odds to win Big 12 Championship Game - BYU",
    "Pick": "BYU", "Opponent": "Field", "Odds": "+750",
    "Risk": "300", "To Win": "2250", "Status": "pending", "Result Date": "",
    "Notes": "Wagerhouse pending. Pending 2026-27 Big 12 Championship Game."
})
new_bets.append({
    "Date": WH_DATE, "Sport": "Football", "League": "NFL",
    "Event": "2026-27 Division of Super Bowl Winner",
    "Type": "future",
    "Description": "Odds to win Division of Super Bowl Winner - NFC West",
    "Pick": "NFC West", "Opponent": "Field", "Odds": "+285",
    "Risk": "1000", "To Win": "2850", "Status": "pending", "Result Date": "",
    "Notes": "Wagerhouse pending. Pending end of Super Bowl LXI (2026-27 NFL season)."
})
new_bets.append({
    "Date": WH_DATE, "Sport": "Football", "League": "NFL",
    "Event": "2026-27 Regular Season Wins - NY Giants",
    "Type": "future",
    "Description": "NFL 26/27 - Regular Season Wins - Giants - Over 7.5",
    "Pick": "NYG Over 7.5", "Opponent": "", "Odds": "-110",
    "Risk": "550", "To Win": "500", "Status": "pending", "Result Date": "",
    "Notes": "Wagerhouse pending. Pending end of NFL 2026-27 regular season."
})
new_bets.append({
    "Date": WH_DATE, "Sport": "Football", "League": "NFL",
    "Event": "2026-27 Regular Season Wins - LA Chargers",
    "Type": "future",
    "Description": "NFL 26/27 - Regular Season Wins - Chargers - Over 10.5",
    "Pick": "LAC Over 10.5", "Opponent": "", "Odds": "+120",
    "Risk": "500", "To Win": "600", "Status": "pending", "Result Date": "",
    "Notes": "Wagerhouse pending. Pending end of NFL 2026-27 regular season."
})
new_bets.append({
    "Date": WH_DATE, "Sport": "Football", "League": "NFL",
    "Event": "2026-27 Regular Season Wins - Jacksonville Jaguars",
    "Type": "future",
    "Description": "NFL 26/27 - Regular Season Wins - Jaguars - Over 9.5",
    "Pick": "JAX Over 9.5", "Opponent": "", "Odds": "+120",
    "Risk": "1000", "To Win": "1200", "Status": "pending", "Result Date": "",
    "Notes": "Wagerhouse pending. Pending end of NFL 2026-27 regular season."
})
new_bets.append({
    "Date": WH_DATE, "Sport": "Football", "League": "NFL",
    "Event": "2026-27 Regular Season Wins - Detroit Lions",
    "Type": "future",
    "Description": "NFL 26/27 - Regular Season Wins - Lions - Over 10.5",
    "Pick": "DET Over 10.5", "Opponent": "", "Odds": "-125",
    "Risk": "1250", "To Win": "1000", "Status": "pending", "Result Date": "",
    "Notes": "Wagerhouse pending. Pending end of NFL 2026-27 regular season."
})
new_bets.append({
    "Date": WH_DATE, "Sport": "Football", "League": "NFL",
    "Event": "2026-27 Regular Season Wins - Dallas Cowboys",
    "Type": "future",
    "Description": "NFL 26/27 - Regular Season Wins - Cowboys - Under 9.5",
    "Pick": "DAL Under 9.5", "Opponent": "", "Odds": "-115",
    "Risk": "1150", "To Win": "1000", "Status": "pending", "Result Date": "",
    "Notes": "Wagerhouse pending. Pending end of NFL 2026-27 regular season."
})

# ============ GAMEDAYWAGERS - 4 futures (image 2) ============
# All ticket-stamped 07/26/2026 17:12
GDW_DATE = "2026-07-26"

new_bets.append({
    "Date": GDW_DATE, "Sport": "Football", "League": "NCAAF",
    "Event": "2026-27 Regular Season Wins - Texas A&M",
    "Type": "future",
    "Description": "NCAA FB 26/27 - Regular Season Wins - Props Texas AM - Under 8.5",
    "Pick": "Texas A&M Under 8.5", "Opponent": "", "Odds": "-120",
    "Risk": "100", "To Win": "83.33", "Status": "pending", "Result Date": "",
    "Notes": "GameDayWagers contest ticket #433700359_1. Pending end of CFB 2026-27 regular season."
})
new_bets.append({
    "Date": GDW_DATE, "Sport": "Football", "League": "NCAAF",
    "Event": "2026-27 Regular Season Wins - Missouri",
    "Type": "future",
    "Description": "NCAA FB 26/27 - Regular Season Wins - Props Missouri - Under 6.5",
    "Pick": "Missouri Under 6.5", "Opponent": "", "Odds": "+105",
    "Risk": "250", "To Win": "262.50", "Status": "pending", "Result Date": "",
    "Notes": "GameDayWagers contest ticket #433700358_1. Pending end of CFB 2026-27 regular season."
})
new_bets.append({
    "Date": GDW_DATE, "Sport": "Football", "League": "NCAAF",
    "Event": "2026-27 Regular Season Wins - James Madison",
    "Type": "future",
    "Description": "NCAA FB 26/27 - Regular Season Wins - Props James Madison - Under 8.5",
    "Pick": "James Madison Under 8.5", "Opponent": "", "Odds": "+125",
    "Risk": "250", "To Win": "312.50", "Status": "pending", "Result Date": "",
    "Notes": "GameDayWagers contest ticket #433700357_1. Pending end of CFB 2026-27 regular season."
})
new_bets.append({
    "Date": GDW_DATE, "Sport": "Football", "League": "NCAAF",
    "Event": "2026-27 Regular Season Wins - UConn",
    "Type": "future",
    "Description": "NCAA FB 26/27 - Regular Season Wins - Props UConn - Under 5.5",
    "Pick": "UConn Under 5.5", "Opponent": "", "Odds": "+115",
    "Risk": "500", "To Win": "575", "Status": "pending", "Result Date": "",
    "Notes": "GameDayWagers contest ticket #433700356_1. Pending end of CFB 2026-27 regular season."
})

# ---------- Write to FALLBACK_BETS ----------
html = HTML.read_text()
m = re.search(r"const FALLBACK_BETS\s*=\s*(\[[\s\S]*?\]);", html)
bets = json.loads(m.group(1))
print(f"Current FALLBACK_BETS count: {len(bets)}")

max_id = max(int(b.get("ID", 0)) for b in bets)
next_id = max_id + 1
print(f"Next ID: {next_id}")

# Assign IDs and dupe-check
existing_tickets = set()
for b in bets:
    for tid in re.findall(r"#([A-Za-z0-9_]+)", b.get("Notes", "")):
        existing_tickets.add(tid)

added = 0
for b in new_bets:
    dupe = False
    for tid in re.findall(r"#([A-Za-z0-9_]+)", b.get("Notes", "")):
        if tid in existing_tickets:
            print(f"  SKIP duplicate ticket #{tid}: {b['Description']}")
            dupe = True
            break
    if dupe:
        continue
    b["ID"] = str(next_id + added)
    bets.append(b)
    added += 1

print(f"Added {added} bets. IDs {next_id}-{next_id + added - 1}")
print(f"New FALLBACK_BETS count: {len(bets)}")

new_json = json.dumps(bets, indent=2, ensure_ascii=False)
new_html = html[:m.start(1)] + new_json + html[m.end(1):]
HTML.write_text(new_html)
print("Wrote index.html")
