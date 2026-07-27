"""Add 30 backlog bets (6/30 - 7/26) to tracker."""
import json
from pathlib import Path

TRACKER = Path("/home/user/workspace/bet-tracker/data.json")

# ---------- The 30 new tickets ----------
# Format: dict per bet, ID assigned sequentially starting 1758

new_bets = []

def add(bet):
    new_bets.append(bet)

# ============ GameDayWagers - 18 tickets ============

# --- 7/9 losers ---
add({
    "Date": "2026-07-09",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup / MLB / Tennis parlay",
    "Type": "parlay",
    "Description": "4-leg: ESP + ARG + FRA advance + LAD -1.5",
    "Pick": "ESP, ARG, FRA to advance + LAD -1.5",
    "Opponent": "",
    "Odds": "",
    "Risk": "125",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-09",
    "Notes": "GameDayWagers ticket #425608426_1. 4-leg parlay across WC advance markets and MLB run line."
})
add({
    "Date": "2026-07-09",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + Tennis parlay",
    "Type": "parlay",
    "Description": "4-leg: FRA + ESP + ARG advance + Kostyuk ML",
    "Pick": "FRA, ESP, ARG to advance + Kostyuk ML",
    "Opponent": "",
    "Odds": "",
    "Risk": "250",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-09",
    "Notes": "GameDayWagers ticket #432657300_1. 4-leg parlay across WC advance markets and tennis ML."
})
add({
    "Date": "2026-07-09",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + Tennis parlay",
    "Type": "parlay",
    "Description": "4-leg: FRA advance + Kostyuk ML + Kostyuk games o22.5 + Kostyuk sets +3",
    "Pick": "FRA advance + 3x Kostyuk match props",
    "Opponent": "",
    "Odds": "",
    "Risk": "100",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-09",
    "Notes": "GameDayWagers ticket #432657336_1. 4-leg parlay: FRA to advance plus 3 correlated Kostyuk match props."
})
add({
    "Date": "2026-07-09",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + MLB parlay",
    "Type": "parlay",
    "Description": "2-leg: FRA advance + SEA -1.5",
    "Pick": "FRA advance + SEA -1.5",
    "Opponent": "",
    "Odds": "",
    "Risk": "500",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-09",
    "Notes": "GameDayWagers ticket #432665152_1. 2-leg parlay: FRA to advance + SEA -1.5 run line."
})
# 7/9 WINNER - FRA + DET -1.5 - stake estimated
add({
    "Date": "2026-07-09",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + MLB parlay",
    "Type": "parlay",
    "Description": "2-leg: FRA advance + DET -1.5",
    "Pick": "FRA advance + DET -1.5",
    "Opponent": "",
    "Odds": "",
    "Risk": "570",
    "To Win": "1000",
    "Status": "won",
    "Result Date": "2026-07-09",
    "Notes": "GameDayWagers ticket #432665159_1. 2-leg parlay: FRA to advance + DET -1.5 vs OAK. Stake estimated from typical closing odds (actual GDW stake not recovered); profit +$1,000 confirmed from ticket display."
})
add({
    "Date": "2026-07-09",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + MLB parlay",
    "Type": "parlay",
    "Description": "2-leg: FRA advance + TEX -1.5",
    "Pick": "FRA advance + TEX -1.5",
    "Opponent": "",
    "Odds": "",
    "Risk": "328.05",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-09",
    "Notes": "GameDayWagers ticket #432665169_1. 2-leg parlay: FRA to advance + TEX -1.5 run line."
})

# --- 7/10 GDW ---
add({
    "Date": "2026-07-10",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + MLB parlay",
    "Type": "parlay",
    "Description": "2-leg: ESP advance + ATL -1.5",
    "Pick": "ESP advance + ATL -1.5",
    "Opponent": "",
    "Odds": "",
    "Risk": "250",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-10",
    "Notes": "GameDayWagers ticket #432751020_1. 2-leg parlay: ESP to advance + ATL -1.5 run line."
})
# 7/10 WINNER - ESP + ATL 1H+5 - stake estimated
add({
    "Date": "2026-07-10",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + MLB parlay",
    "Type": "parlay",
    "Description": "2-leg: ESP advance + ATL 1st 5 innings +0.5",
    "Pick": "ESP advance + ATL 1H run line",
    "Opponent": "",
    "Odds": "",
    "Risk": "260",
    "To Win": "352.50",
    "Status": "won",
    "Result Date": "2026-07-10",
    "Notes": "GameDayWagers ticket #432751032_1. 2-leg parlay: ESP to advance + ATL 1st 5 innings run line vs STL. Stake estimated from typical closing odds (actual GDW stake not recovered); profit +$352.50 confirmed from ticket display."
})
add({
    "Date": "2026-07-10",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + MLB parlay",
    "Type": "parlay",
    "Description": "2-leg: ESP advance + PHI ML",
    "Pick": "ESP advance + PHI ML",
    "Opponent": "",
    "Odds": "",
    "Risk": "400",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-10",
    "Notes": "GameDayWagers ticket #432751038_1. 2-leg parlay: ESP to advance + PHI moneyline."
})
# 7/10 WINNER - ESP + TOR ML - stake estimated
add({
    "Date": "2026-07-10",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + MLB parlay",
    "Type": "parlay",
    "Description": "2-leg: ESP advance + TOR ML",
    "Pick": "ESP advance + TOR ML",
    "Opponent": "",
    "Odds": "",
    "Risk": "410",
    "To Win": "612",
    "Status": "won",
    "Result Date": "2026-07-10",
    "Notes": "GameDayWagers ticket #432751122_1. 2-leg parlay: ESP to advance + TOR ML vs SD. Stake estimated from typical closing odds (actual GDW stake not recovered); profit +$612 confirmed from ticket display."
})
add({
    "Date": "2026-07-10",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "MLB + WC + Tennis parlay",
    "Type": "parlay",
    "Description": "4-leg: Clemens Over 1.5 HRR + Sinner ML + ARG advance + MIN ML",
    "Pick": "Clemens O1.5 HRR + Sinner ML + ARG advance + MIN ML",
    "Opponent": "",
    "Odds": "",
    "Risk": "125",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-11",
    "Notes": "GameDayWagers ticket #432805795_1. 4-leg parlay: Clemens hits+runs+RBI prop + Sinner match ML + ARG to advance + MIN ML."
})

# --- 7/11 GDW winners (Sinner + ARG) - stake estimated ---
add({
    "Date": "2026-07-11",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + Wimbledon parlay",
    "Type": "parlay",
    "Description": "2-leg: ARG advance + Sinner ML",
    "Pick": "ARG advance + Sinner match ML",
    "Opponent": "",
    "Odds": "",
    "Risk": "450",
    "To Win": "295",
    "Status": "won",
    "Result Date": "2026-07-11",
    "Notes": "GameDayWagers ticket #432826621_1. 2-leg parlay: ARG to advance + Sinner match ML at Wimbledon. Stake estimated from typical closing odds (actual GDW stake not recovered); profit +$295 confirmed from ticket display."
})
add({
    "Date": "2026-07-11",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + Wimbledon parlay",
    "Type": "parlay",
    "Description": "2-leg: ARG advance + Sinner ML (duplicate ticket)",
    "Pick": "ARG advance + Sinner match ML",
    "Opponent": "",
    "Odds": "",
    "Risk": "450",
    "To Win": "295",
    "Status": "won",
    "Result Date": "2026-07-11",
    "Notes": "GameDayWagers ticket #432826632_1. Duplicate 2-leg parlay: ARG to advance + Sinner match ML. Stake estimated from typical closing odds (actual GDW stake not recovered); profit +$295 confirmed from ticket display."
})

# --- 7/14 GDW ---
add({
    "Date": "2026-07-14",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + MLB parlay",
    "Type": "parlay",
    "Description": "4-leg: FRA advance + FRA/ESP BTTS + ENG advance + ASG 1st inning Draw",
    "Pick": "FRA advance + FRA/ESP BTTS + ENG advance + ASG 1I Draw",
    "Opponent": "",
    "Odds": "",
    "Risk": "125",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-15",
    "Notes": "GameDayWagers ticket #432945417_1. 4-leg parlay: FRA to advance + FRA/ESP BTTS + ENG to advance + MLB All-Star Game 1st inning draw."
})
add({
    "Date": "2026-07-14",
    "Sport": "Soccer",
    "League": "FIFA",
    "Event": "2026 FIFA World Cup",
    "Type": "parlay",
    "Description": "3-leg: FRA advance + FRA/ESP BTTS + ENG advance",
    "Pick": "FRA advance + FRA/ESP BTTS + ENG advance",
    "Opponent": "",
    "Odds": "",
    "Risk": "125",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-15",
    "Notes": "GameDayWagers ticket #432945447_1. 3-leg WC parlay: FRA to advance + FRA/ESP BTTS + ENG to advance."
})

# --- 7/15 GDW ---
add({
    "Date": "2026-07-15",
    "Sport": "Soccer",
    "League": "FIFA",
    "Event": "2026 FIFA World Cup",
    "Type": "parlay",
    "Description": "2-leg: ENG/ARG BTTS + ENG advance",
    "Pick": "ENG/ARG BTTS + ENG advance",
    "Opponent": "",
    "Odds": "",
    "Risk": "200",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-15",
    "Notes": "GameDayWagers ticket #433029533_1. 2-leg WC parlay: ENG/ARG BTTS + ENG to advance."
})

# --- 7/18 GDW ---
add({
    "Date": "2026-07-18",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + MLB parlay",
    "Type": "parlay",
    "Description": "2-leg: ARG lift trophy + SF/SEA 1st inning Draw",
    "Pick": "ARG win WC + SF/SEA 1I Draw",
    "Opponent": "",
    "Odds": "",
    "Risk": "400",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-19",
    "Notes": "GameDayWagers ticket #433205774_1. 2-leg parlay: ARG to win WC + SF/SEA 1st inning draw."
})
add({
    "Date": "2026-07-18",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "2026 FIFA World Cup + MLB parlay",
    "Type": "parlay",
    "Description": "2-leg: ARG lift trophy + SF/SEA 1st inning Draw (duplicate)",
    "Pick": "ARG win WC + SF/SEA 1I Draw",
    "Opponent": "",
    "Odds": "",
    "Risk": "115",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-19",
    "Notes": "GameDayWagers ticket #433205825_1. Duplicate 2-leg parlay: ARG to win WC + SF/SEA 1st inning draw."
})

# ============ Wagerhouse - 12 tickets ============

# --- 6/30 ---
add({
    "Date": "2026-06-30",
    "Sport": "Baseball",
    "League": "MLB",
    "Event": "LAA @ MLB game",
    "Type": "spread",
    "Description": "LAA +0.5 (1st 5 innings) -121",
    "Pick": "LAA +0.5 (1st 5)",
    "Opponent": "",
    "Odds": "-121",
    "Risk": "121",
    "To Win": "100",
    "Status": "won",
    "Result Date": "2026-06-30",
    "Notes": "Wagerhouse ticket #G303196491. 1st-half run line."
})

# --- 7/3 ---
add({
    "Date": "2026-07-03",
    "Sport": "Soccer",
    "League": "FIFA",
    "Event": "2026 FIFA World Cup",
    "Type": "parlay",
    "Description": "5-leg WC advance/BTTS parlay",
    "Pick": "ESP/PRT/HRV/SUI/DZA/ARG mix",
    "Opponent": "",
    "Odds": "",
    "Risk": "150",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-06",
    "Notes": "Wagerhouse ticket #393201042. 5-leg WC parlay across advance markets and BTTS."
})
add({
    "Date": "2026-07-03",
    "Sport": "Soccer",
    "League": "FIFA",
    "Event": "2026 FIFA World Cup",
    "Type": "parlay",
    "Description": "5-leg: SUI/DZA BTTS + FRA/MRC/USA advance",
    "Pick": "SUI/DZA BTTS + FRA/MRC/USA advance",
    "Opponent": "",
    "Odds": "",
    "Risk": "150",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-06",
    "Notes": "Wagerhouse ticket #393270984. 5-leg WC parlay."
})
add({
    "Date": "2026-07-03",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "MLB + WC parlay",
    "Type": "parlay",
    "Description": "5-leg: LAD -1.5 + ARG HT/FT + COL ML + WC BTTS",
    "Pick": "LAD -1.5 + ARG HT/FT + COL ML + BTTS legs",
    "Opponent": "",
    "Odds": "",
    "Risk": "100",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-04",
    "Notes": "Wagerhouse ticket #393316703. 5-leg parlay: LAD -1.5 + ARG HT/FT + COL ML + WC BTTS markets."
})

# --- 7/9 Wagerhouse ---
add({
    "Date": "2026-07-09",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "MLB + WC parlay",
    "Type": "parlay",
    "Description": "3-leg: Eovaldi Over 6.5 Ks + FRA advance + TEX -1.5",
    "Pick": "Eovaldi O6.5 Ks + FRA advance + TEX -1.5",
    "Opponent": "",
    "Odds": "",
    "Risk": "100",
    "To Win": "",
    "Status": "lost",
    "Result Date": "2026-07-09",
    "Notes": "Wagerhouse ticket #393810229. 3-leg parlay: Eovaldi strikeout prop + FRA to advance + TEX run line."
})
# 7/9 Wagerhouse WINNER - Luzardo + FRA + PHI
add({
    "Date": "2026-07-09",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "MLB + WC parlay",
    "Type": "parlay",
    "Description": "3-leg: Luzardo Over 7.5 Ks + FRA advance + PHI ML",
    "Pick": "Luzardo O7.5 Ks + FRA advance + PHI ML",
    "Opponent": "",
    "Odds": "",
    "Risk": "100",
    "To Win": "247",
    "Status": "won",
    "Result Date": "2026-07-09",
    "Notes": "Wagerhouse ticket #393810672. 3-leg parlay: Luzardo strikeout prop + FRA to advance + PHI ML. Stake estimated from typical closing odds (actual Wagerhouse stake not recovered); profit +$247 confirmed from ticket display."
})

# --- 7/10 Wagerhouse WINNER - Rays 1st 5 + Spain ---
add({
    "Date": "2026-07-10",
    "Sport": "Multi",
    "League": "Multi",
    "Event": "MLB + WC parlay",
    "Type": "parlay",
    "Description": "2-leg: TB ML 1st 5 innings -120 + ESP advance",
    "Pick": "TB ML 1st 5 + ESP advance",
    "Opponent": "",
    "Odds": "",
    "Risk": "150",
    "To Win": "213.71",
    "Status": "won",
    "Result Date": "2026-07-10",
    "Notes": "Wagerhouse ticket (unnamed). 2-leg parlay: TB ML 1st 5 innings -120 + ESP to advance. Stake estimated from typical closing odds (actual Wagerhouse stake not recovered); profit +$213.71 confirmed from ticket display."
})

# --- 7/17 Wagerhouse - Spieth ---
add({
    "Date": "2026-07-17",
    "Sport": "Golf",
    "League": "PGA Tour",
    "Event": "2026 Open Championship",
    "Type": "prop",
    "Description": "Jordan Spieth 2nd Round Under 70.5",
    "Pick": "Spieth 2R Under 70.5",
    "Opponent": "",
    "Odds": "-110",
    "Risk": "220",
    "To Win": "200",
    "Status": "lost",
    "Result Date": "2026-07-17",
    "Notes": "Wagerhouse ticket (Spieth 2R prop). Round-2 total strokes prop."
})

# --- 7/19 Wagerhouse ---
add({
    "Date": "2026-07-19",
    "Sport": "Golf",
    "League": "PGA Tour",
    "Event": "2026 Open Championship",
    "Type": "future",
    "Description": "Si Woo Kim to win 2026 Open Championship",
    "Pick": "Si Woo Kim",
    "Opponent": "Field",
    "Odds": "+105",
    "Risk": "500",
    "To Win": "525",
    "Status": "lost",
    "Result Date": "2026-07-20",
    "Notes": "Wagerhouse ticket #G305506219. Open Championship outright. Fox won."
})
add({
    "Date": "2026-07-19",
    "Sport": "Golf",
    "League": "PGA Tour",
    "Event": "2026 Open Championship",
    "Type": "future",
    "Description": "Cameron Young to win 2026 Open Championship",
    "Pick": "Cameron Young",
    "Opponent": "Field",
    "Odds": "+105",
    "Risk": "2000",
    "To Win": "2100",
    "Status": "lost",
    "Result Date": "2026-07-20",
    "Notes": "Wagerhouse ticket #G305520501. Open Championship outright. Fox won."
})
add({
    "Date": "2026-07-19",
    "Sport": "Golf",
    "League": "PGA Tour",
    "Event": "2026 Open Championship",
    "Type": "future",
    "Description": "Ryan Fox to win 2026 Open Championship",
    "Pick": "Ryan Fox",
    "Opponent": "Field",
    "Odds": "+305",
    "Risk": "1500",
    "To Win": "4575",
    "Status": "won",
    "Result Date": "2026-07-20",
    "Notes": "Wagerhouse ticket #G305520772. Open Championship outright. Fox won — biggest cash of the stretch."
})

# --- 7/26 Wagerhouse - Koivun ---
add({
    "Date": "2026-07-26",
    "Sport": "Golf",
    "League": "PGA Tour",
    "Event": "2026 3M Open",
    "Type": "future",
    "Description": "Jackson Koivun to win 3M Open",
    "Pick": "Jackson Koivun",
    "Opponent": "Field",
    "Odds": "-835",
    "Risk": "1500",
    "To Win": "179.64",
    "Status": "won",
    "Result Date": "2026-07-26",
    "Notes": "Wagerhouse ticket #G306282450. Heavy chalk outright at 3M Open — won."
})

# --------- Now write ----------
with open(TRACKER) as f:
    data = json.load(f)

next_id = 1758
for i, b in enumerate(new_bets):
    b["ID"] = str(next_id + i)
    data["bets"].append(b)

with open(TRACKER, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Added {len(new_bets)} bets. IDs {next_id}-{next_id + len(new_bets) - 1}")
print(f"Total bets now: {len(data['bets'])}")
