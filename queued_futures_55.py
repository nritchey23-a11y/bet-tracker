#!/usr/bin/env python3
"""Load all 55 queued futures from the 6/17 screenshots.

Breakdown:
- 25 Action Network futures (placed Apr-Jun 2026)
- 30 Wagerhouse contest futures (placed Apr-Jun 2026)
- Auto-settle WC futures that already resolved at group stage:
    WON: USA Group D, Mexico Group A
  All other WC tournament-progression and all non-WC season-long bets = pending.
  (Norway/Colombia/Netherlands R16 and Senegal Top African still live per user.)
"""
import json, re

INDEX_FILE = "/home/user/workspace/bet-tracker/index.html"
NEW_BETS = []

def b(date, sport, league, event, btype, desc, pick, opp, odds, risk, towin,
      status="pending", result_date="", notes="", ticket=""):
    note_full = (f"Wagerhouse contest ticket #{ticket}. " if ticket else "") + notes
    return {
        "Date": date, "Sport": sport, "League": league, "Event": event,
        "Type": btype, "Description": desc, "Pick": pick, "Opponent": opp,
        "Odds": odds, "Risk": str(risk), "To Win": str(towin),
        "Status": status, "Result Date": result_date, "Notes": note_full.strip(),
    }

# =========================================================================
# ACTION NETWORK FUTURES (25 bets) — placed at various 2026 dates
# =========================================================================

# --- Non-WC (8) ---
NEW_BETS.append(b("2026-06-16", "Football", "NCAAF", "Big 12 Championship", "future",
                  "Odds to win Big 12 Championship Game", "BYU", "Field", "+750", 300, 2250,
                  notes="Action Network. Pending end-of-CFB-season 2026-27."))
NEW_BETS.append(b("2026-05-31", "Football", "NCAAF", "Big Ten Championship", "future",
                  "Odds to win Big Ten Championship Game", "Washington", "Field", "+3000", 500, 15000,
                  notes="Action Network. Pending end-of-CFB-season 2026-27."))
NEW_BETS.append(b("2026-06-04", "Football", "NFL", "NFC West Division Super Bowl Winner", "future",
                  "Odds to win Div of Super Bowl Winner - NFC West", "NFC West", "Field", "+285", 1000, 2850,
                  notes="Action Network. Pending end of 2026-27 NFL season."))
NEW_BETS.append(b("2026-06-04", "Football", "NFL", "Regular Season Wins - NYG", "future",
                  "NY Giants Regular Season Wins O 7.5", "NYG Over 7.5", "", "-110", 550, 500,
                  notes="Action Network. Pending 2026-27 NFL season."))
NEW_BETS.append(b("2026-06-04", "Football", "NFL", "Regular Season Wins - LAC", "future",
                  "LA Chargers Regular Season Wins O 10.5", "LAC Over 10.5", "", "+120", 500, 600,
                  notes="Action Network. Pending 2026-27 NFL season."))
NEW_BETS.append(b("2026-06-04", "Football", "NFL", "Regular Season Wins - JAX", "future",
                  "JAX Jaguars Regular Season Wins O 9.5", "JAX Over 9.5", "", "+120", 1000, 1200,
                  notes="Action Network. Pending 2026-27 NFL season."))
NEW_BETS.append(b("2026-06-04", "Football", "NFL", "Regular Season Wins - DET", "future",
                  "Detroit Lions Regular Season Wins O 10.5", "DET Over 10.5", "", "-125", 1250, 1000,
                  notes="Action Network. Pending 2026-27 NFL season."))
NEW_BETS.append(b("2026-06-04", "Football", "NFL", "Regular Season Wins - DAL", "future",
                  "Dallas Cowboys Regular Season Wins U 9.5", "DAL Under 9.5", "", "-115", 1150, 1000,
                  notes="Action Network. Pending 2026-27 NFL season."))

# --- Action Network WC (17) ---
def an_wc(event_label, pick, odds, risk, towin, status="pending", result_date="", notes=""):
    return b("2026-06-04", "Soccer", "FIFA", f"2026 FIFA World Cup - {event_label}", "future",
             f"{event_label} - {pick}", pick, "Field", odds, risk, towin,
             status=status, result_date=result_date, notes=("Action Network. " + notes).strip())

NEW_BETS.append(an_wc("UEFA Top Finish",            "Germany",       "+900",  100, 900))
NEW_BETS.append(an_wc("CONCACAF Top Finish",        "Mexico",        "+160", 1000, 1600))
NEW_BETS.append(an_wc("Tournament Winner",          "Germany",       "+1500", 500, 7500))
NEW_BETS.append(an_wc("Reach Semi Finals",          "Norway",        "+500",  200, 1000))
NEW_BETS.append(an_wc("Reach Semi Finals",          "Netherlands",   "+450",  200, 900))
NEW_BETS.append(an_wc("Reach Semi Finals",          "Germany",       "+325",  500, 1625))
NEW_BETS.append(an_wc("Reach Semi Finals",          "Portugal",      "+250",  600, 1500))
NEW_BETS.append(an_wc("Reach Final",                "Germany",       "+550",  500, 2750))
NEW_BETS.append(an_wc("Reach Final",                "Portugal",      "+450",  550, 2475))
NEW_BETS.append(an_wc("Reach Quarter Finals",       "Norway",        "+200",  400, 800))
NEW_BETS.append(an_wc("Reach Quarter Finals",       "Netherlands",   "+160",  450, 720))
NEW_BETS.append(an_wc("Reach Quarter Finals",       "Germany",       "+150",  500, 750))
NEW_BETS.append(an_wc("Reach Quarter Finals",       "Portugal",      "+125",  600, 750))
NEW_BETS.append(an_wc("Reach Round of 16",          "Uruguay",       "+130",  600, 780,
                       notes="Group stage status uncertain - mark pending pending user confirmation."))
NEW_BETS.append(an_wc("Reach Round of 16",          "Colombia",      "+120",  650, 780,
                       notes="Group stage in progress / R16 not yet clinched."))
NEW_BETS.append(an_wc("Reach Round of 16",          "Norway",        "-150", 1500, 1000,
                       notes="Group stage in progress / R16 not yet clinched."))
NEW_BETS.append(an_wc("Reach Round of 16",          "Netherlands",   "-150", 1500, 1000,
                       notes="Group stage in progress / R16 not yet clinched."))

# =========================================================================
# WAGERHOUSE CONTEST FUTURES (30 bets)
# =========================================================================

# --- CFB Reg Season Wins (12 bets, dated 6/9) ---
def wh_cfb(team, line, side, odds, risk, towin, ticket):
    pick = f"{team} {side} {line}"
    return b("2026-06-09", "Football", "NCAAF", f"2026-27 Regular Season Wins - {team}",
             "future", f"NCAA FB 26/27 - Regular Season Wins - Props {team} - {side} {line}",
             pick, "", odds, risk, towin, ticket=ticket,
             notes="Pending end of CFB 2026-27 regular season.")

NEW_BETS.append(wh_cfb("Nebraska",       "6.5",  "Over",  "+105",   500,   525, "410645406"))
NEW_BETS.append(wh_cfb("Virginia Tech",  "6.5",  "Under", "+120",   500,   600, "410645405"))
NEW_BETS.append(wh_cfb("Northwestern",   "5.5",  "Under", "-130",   650,   500, "410645404"))
NEW_BETS.append(wh_cfb("Kansas State",   "8.5",  "Over",  "+105",   750, 787.50, "410645375"))
NEW_BETS.append(wh_cfb("Washington",     "7.5",  "Over",  "-170",  1000, 588.24, "410645374"))
NEW_BETS.append(wh_cfb("Iowa State",     "5.5",  "Over",  "+105",   750, 787.50, "410645373"))
NEW_BETS.append(wh_cfb("NC State",       "7.5",  "Over",  "+100",  1000,  1000, "410645372"))
NEW_BETS.append(wh_cfb("Michigan",       "8.5",  "Over",  "+135",   750, 1012.50, "410645371"))
NEW_BETS.append(wh_cfb("South Carolina", "6.5",  "Over",  "+115",  1000,  1150, "410645370"))
NEW_BETS.append(wh_cfb("Georgia",        "9.5",  "Under", "+150",   750,  1125, "410645369"))
NEW_BETS.append(wh_cfb("Oregon",        "10.5",  "Over",  "+100",  1000,  1000, "410645368"))
NEW_BETS.append(wh_cfb("Ohio State",     "9.5",  "Over",  "-165",  1650,  1000, "410645367"))

# --- NFL Reg Season Wins (5 bets, dated 6/4) ---
def wh_nfl_wins(team, line, side, odds, risk, towin, ticket):
    pick = f"{team} {side} {line}"
    return b("2026-06-04", "Football", "NFL", f"2026-27 Regular Season Wins - {team}",
             "future", f"NFL 26/27 - Regular Season Wins - Props {team} - {side} {line}",
             pick, "", odds, risk, towin, ticket=ticket,
             notes="Pending end of NFL 2026-27 regular season.")

NEW_BETS.append(wh_nfl_wins("NY Jets",       "5.5", "Under", "-105", 1050, 1000, "410449428"))
NEW_BETS.append(wh_nfl_wins("BUF Bills",    "10.5", "Over",  "-120",  900,  750, "410449427"))
NEW_BETS.append(wh_nfl_wins("JAX Jaguars",   "8.5", "Over",  "-130", 1300, 1000, "410449426"))
NEW_BETS.append(wh_nfl_wins("LA Chargers",   "9.5", "Over",  "-130", 1300, 1000, "410449425"))
NEW_BETS.append(wh_nfl_wins("CIN Bengals",  "10.5", "Over",  "+115",  500,  575, "410449424"))

# --- Wagerhouse Contest WC Futures (5 bets) ---
def wh_wc(event_label, pick, odds, risk, towin, status="pending", result_date="", notes="", ticket=""):
    return b("2026-06-04", "Soccer", "FIFA", f"2026 FIFA World Cup - {event_label}",
             "future", f"FIFA World Cup 2026 - {event_label} - {pick}", pick, "Field",
             odds, risk, towin, status=status, result_date=result_date, ticket=ticket, notes=notes)

NEW_BETS.append(wh_wc("Tournament Winner", "Portugal",      "+1100", 500, 5500,
                       ticket="410446173"))
NEW_BETS.append(wh_wc("Group D Winner",    "USA",            "+140", 1000, 1400,
                       status="won", result_date="2026-06-26",
                       ticket="410446172", notes="USA won Group D outright."))
NEW_BETS.append(wh_wc("Group A Winner",    "Mexico",         "-125", 1000,  800,
                       status="won", result_date="2026-06-26",
                       ticket="410446171", notes="Mexico won Group A outright."))
NEW_BETS.append(wh_wc("Top North American Team", "United States", "+140", 725, 1015,
                       ticket="410446170",
                       notes="Tournament-progression prop. USA leads NA region after group stage."))
NEW_BETS.append(wh_wc("Top African Team",  "Senegal",        "+450",  150,  675,
                       ticket="410446169", notes="Senegal still alive in tournament."))

# --- MLB Division (1 bet, dated 5/27) ---
NEW_BETS.append(b("2026-05-27", "Baseball", "MLB", "2026 AL West Division Winner", "future",
                  "MLB 2026 Division Winner - American League West - Seattle Mariners",
                  "Seattle Mariners", "Field", "+110", 1000, 1100,
                  notes="Wagerhouse contest ticket #409988351. Pending end of 2026 MLB regular season."))

# --- NFL Division Winners (6 bets, dated 4/30) ---
def wh_nfl_div(div, team, odds, risk, towin, ticket):
    return b("2026-04-30", "Football", "NFL", f"2026-27 {div} Division Winner", "future",
             f"NFL 26/27 Division Winner - Props {div} - {team}", team, "Field",
             odds, risk, towin, ticket=ticket,
             notes="Pending NFL 2026-27 season.")

NEW_BETS.append(wh_nfl_div("NFC North", "CHI Bears",     "+320", 375, 1200, "300552460"))
NEW_BETS.append(wh_nfl_div("NFC East",  "WAS Commanders","+500", 250, 1250, "300552459"))
NEW_BETS.append(wh_nfl_div("NFC South", "ATL Falcons",   "+450", 250, 1125, "300552458"))
NEW_BETS.append(wh_nfl_div("AFC North", "CIN Bengals",   "+210", 500, 1050, "300552457"))
NEW_BETS.append(wh_nfl_div("AFC West",  "KC Chiefs",     "+170", 500,  850, "300552456"))
NEW_BETS.append(wh_nfl_div("NFC West",  "SF 49ers",      "+260", 375,  975, "300552455"))

# --- NFL Reg Season Wins (1 more, dated 4/29) ---
NEW_BETS.append(b("2026-04-29", "Football", "NFL", "2026-27 Regular Season Wins - SEA Seahawks",
                  "future", "NFL 26/27 - Regular Season Wins - Props SEA Seahawks - Over 10.5",
                  "SEA Over 10.5", "", "-130", 1300, 1000,
                  notes="Wagerhouse contest ticket #300514464. Pending NFL 2026-27 season."))

# Verify total
print(f"Total bets prepared: {len(NEW_BETS)}")
assert len(NEW_BETS) == 55, f"Expected 55, got {len(NEW_BETS)}"

# Assign IDs starting at 1703
START_ID = 1703
for i, bet in enumerate(NEW_BETS):
    bet["ID"] = str(START_ID + i)

# Summary
from collections import defaultdict
status_count = defaultdict(int)
profit = 0
pending_risk = 0
for bet in NEW_BETS:
    s = bet["Status"]
    status_count[s] += 1
    if s == "won":
        profit += float(bet["To Win"])
    elif s == "lost":
        profit -= float(bet["Risk"])
    elif s == "pending":
        pending_risk += float(bet["Risk"])

print(f"Status: {dict(status_count)}")
print(f"Settled profit from auto-settled WC bets: ${profit:+.2f}")
print(f"Pending risk: ${pending_risk:.2f}")

# Inject into index.html
with open(INDEX_FILE, "r") as f:
    html = f.read()

def format_bet(bb):
    lines = ["  {"]
    keys = ["Date", "Sport", "League", "Event", "Type", "Description", "Pick", "Opponent",
            "Odds", "Risk", "To Win", "Status", "Result Date", "Notes", "ID"]
    for i, k in enumerate(keys):
        v_json = json.dumps(bb[k], ensure_ascii=False)
        suffix = "" if i == len(keys) - 1 else ","
        lines.append(f'    "{k}": {v_json}{suffix}')
    lines.append("  }")
    return "\n".join(lines)

new_entries = ",\n".join(format_bet(bb) for bb in NEW_BETS)

old = '"ID": "1702"\n  }\n];'
new = '"ID": "1702"\n  },\n' + new_entries + "\n];"
html2 = html.replace(old, new, 1)
if html2 == html:
    print("REPLACE FAILED")
    raise SystemExit(2)

with open(INDEX_FILE, "w") as f:
    f.write(html2)

print(f"Injected. Last ID: {NEW_BETS[-1]['ID']}")

with open("/home/user/workspace/bet-tracker/queued_futures_55.json", "w") as f:
    json.dump(NEW_BETS, f, indent=2)
