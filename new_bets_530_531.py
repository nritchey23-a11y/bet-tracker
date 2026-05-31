"""Add 5/30 settled bets (1485-1492) + 5/31 pending bets (1493-1501) to both
the Google Sheet and the dashboard's FALLBACK_BETS."""
import json, re

# Schema: ID Date Sport League Event Type Description Pick Opponent Odds Risk To Win Status Result Date Notes
new_bets = [
    # ===== 5/30 SETTLED =====
    {
        "ID": "1485", "Date": "2026-05-30", "Sport": "Mixed", "League": "NBA+MLB",
        "Event": "5-team Round Robin (2s/3s/4s/5s)",
        "Type": "Round Robin",
        "Description": "5-leg RR: SAS ML +130 / PIT ML 1st 5 -142 / ARI ML +137 / WAS ML 1st 5 +100 / COL-SF Over 11 +100",
        "Pick": "26 parlays @ $25 each",
        "Opponent": "Various",
        "Odds": "Mixed",
        "Risk": "353.91",
        "To Win": "0",
        "Status": "lost",
        "Result Date": "2026-05-30",
        "Notes": "Original $650 stake (26x$25). Results: SAS WON, PIT 1st5 WON, ARI LOST, WAS 1st5 LOST, COL/SF O11 PUSH (total exactly 11). 4 winning parlays returned $296.09: SAS+PIT 2L=$97.99, SAS+(push reduced)=$57.50, PIT+(push reduced)=$42.61, SAS+PIT+(push reduced)=$97.99. Net realized -$353.91."
    },
    {
        "ID": "1486", "Date": "2026-05-30", "Sport": "Baseball", "League": "MLB",
        "Event": "WAS @ SD", "Type": "1st 5 Run Line",
        "Description": "Nationals +0.5 1st 5",
        "Pick": "WAS +0.5", "Opponent": "SD", "Odds": "-135",
        "Risk": "135", "To Win": "100", "Status": "lost", "Result Date": "2026-05-30",
        "Notes": "1st 5: SD 3, WAS 1. WAS lost 1st 5 by 2."
    },
    {
        "ID": "1487", "Date": "2026-05-30", "Sport": "Baseball", "League": "MLB",
        "Event": "WAS @ SD", "Type": "1st 5 Money Line",
        "Description": "Nationals ML 1st 5",
        "Pick": "WAS", "Opponent": "SD", "Odds": "+105",
        "Risk": "100", "To Win": "105", "Status": "lost", "Result Date": "2026-05-30",
        "Notes": "1st 5: SD 3, WAS 1"
    },
    {
        "ID": "1488", "Date": "2026-05-30", "Sport": "Basketball", "League": "NBA",
        "Event": "SAS @ OKC (WCF Game 7)", "Type": "Money Line",
        "Description": "Spurs ML",
        "Pick": "SAS", "Opponent": "OKC", "Odds": "+130",
        "Risk": "200", "To Win": "260", "Status": "won", "Result Date": "2026-05-30",
        "Notes": "SAS 111-103 OKC. Wembanyama 22pts/7reb."
    },
    {
        "ID": "1489", "Date": "2026-05-30", "Sport": "Baseball", "League": "MLB",
        "Event": "PHI @ LAD", "Type": "Money Line",
        "Description": "Phillies ML",
        "Pick": "PHI", "Opponent": "LAD", "Odds": "+112",
        "Risk": "200", "To Win": "224", "Status": "won", "Result Date": "2026-05-30",
        "Notes": "PHI 4-3 LAD"
    },
    {
        "ID": "1490", "Date": "2026-05-30", "Sport": "Baseball", "League": "MLB",
        "Event": "SF @ COL", "Type": "Total",
        "Description": "Giants/Rockies Over 11",
        "Pick": "Over 11", "Opponent": "—", "Odds": "-105",
        "Risk": "210", "To Win": "200", "Status": "push", "Result Date": "2026-05-30",
        "Notes": "COL 8, SF 3 = exactly 11 total. PUSH."
    },
    {
        "ID": "1491", "Date": "2026-05-30", "Sport": "Baseball", "League": "MLB",
        "Event": "MIN @ PIT", "Type": "1st 5 Run Line",
        "Description": "Pirates -0.5 1st 5",
        "Pick": "PIT -0.5", "Opponent": "MIN", "Odds": "+105",
        "Risk": "200", "To Win": "210", "Status": "won", "Result Date": "2026-05-30",
        "Notes": "1st 5: PIT 8, MIN 7 (Game 2 of DH)"
    },
    {
        "ID": "1492", "Date": "2026-05-30", "Sport": "Baseball", "League": "MLB",
        "Event": "ARI @ SEA", "Type": "Parlay",
        "Description": "Bryan Woo Over 5.5K + SEA 1st 5 ML",
        "Pick": "Woo O5.5K + SEA 1st 5", "Opponent": "ARI", "Odds": "+212",
        "Risk": "150", "To Win": "318", "Status": "won", "Result Date": "2026-05-30",
        "Notes": "Woo 9 K's (over 5.5). SEA 4-0 in 1st 5. Ticket 1448663729-1."
    },
    # ===== 5/31 PENDING =====
    {
        "ID": "1493", "Date": "2026-05-31", "Sport": "Baseball", "League": "MLB",
        "Event": "5-team Round Robin (2s/3s/4s/5s)", "Type": "Round Robin",
        "Description": "ATL -1.5 +120 / PIT -1.5 +135 / NYY -1.5 +103 / MIL -1.5 -105 / TB -1.5 +115",
        "Pick": "26 parlays @ $25 each", "Opponent": "Various",
        "Odds": "Mixed", "Risk": "650", "To Win": "6609.91", "Status": "pending",
        "Result Date": "", "Notes": "Ticket 410213014. All 5 are full-game -1.5 spreads."
    },
    {
        "ID": "1494", "Date": "2026-05-31", "Sport": "Baseball", "League": "MLB",
        "Event": "OAK @ NYY", "Type": "Run Line",
        "Description": "Yankees -1.5 (game)",
        "Pick": "NYY -1.5", "Opponent": "OAK", "Odds": "+103",
        "Risk": "150", "To Win": "154.50", "Status": "pending", "Result Date": "",
        "Notes": "Ticket 410213045"
    },
    {
        "ID": "1495", "Date": "2026-05-31", "Sport": "Baseball", "League": "MLB",
        "Event": "OAK @ NYY", "Type": "Money Line",
        "Description": "Yankees ML (game)",
        "Pick": "NYY", "Opponent": "OAK", "Odds": "-149",
        "Risk": "223.50", "To Win": "150", "Status": "pending", "Result Date": "",
        "Notes": "Ticket 410213046"
    },
    {
        "ID": "1496", "Date": "2026-05-31", "Sport": "Baseball", "League": "MLB",
        "Event": "TOR @ BAL", "Type": "1st 5 Run Line",
        "Description": "Orioles -0.5 1st 5",
        "Pick": "BAL -0.5", "Opponent": "TOR", "Odds": "+100",
        "Risk": "125", "To Win": "125", "Status": "pending", "Result Date": "",
        "Notes": "Ticket 410213113. Bradish vs Miles."
    },
    {
        "ID": "1497", "Date": "2026-05-31", "Sport": "Baseball", "League": "MLB",
        "Event": "TB @ LAA", "Type": "1st 5 Run Line",
        "Description": "Rays -0.5 1st 5",
        "Pick": "TB -0.5", "Opponent": "LAA", "Odds": "-135",
        "Risk": "168.75", "To Win": "125", "Status": "pending", "Result Date": "",
        "Notes": "Ticket 410213112. Kochanowicz vs McClanahan."
    },
    {
        "ID": "1498", "Date": "2026-05-31", "Sport": "Baseball", "League": "MLB",
        "Event": "SF @ COL", "Type": "1st 5 Run Line",
        "Description": "Giants -0.5 1st 5",
        "Pick": "SF -0.5", "Opponent": "COL", "Odds": "+107",
        "Risk": "125", "To Win": "133.75", "Status": "pending", "Result Date": "",
        "Notes": "Ticket 410213111. Ray vs Gordon."
    },
    {
        "ID": "1499", "Date": "2026-05-31", "Sport": "Baseball", "League": "MLB",
        "Event": "ATL @ CIN", "Type": "1st 5 Run Line",
        "Description": "Braves -0.5 1st 5",
        "Pick": "ATL -0.5", "Opponent": "CIN", "Odds": "+118",
        "Risk": "125", "To Win": "147.50", "Status": "pending", "Result Date": "",
        "Notes": "Ticket 410213110. Strider vs Lodolo."
    },
    {
        "ID": "1500", "Date": "2026-05-31", "Sport": "Baseball", "League": "MLB",
        "Event": "MIN @ PIT", "Type": "1st 5 Run Line",
        "Description": "Pirates -0.5 1st 5",
        "Pick": "PIT -0.5", "Opponent": "MIN", "Odds": "-120",
        "Risk": "300", "To Win": "250", "Status": "pending", "Result Date": "",
        "Notes": "Ticket 410213095. Matthews vs Ashcraft."
    },
    {
        "ID": "1501", "Date": "2026-05-31", "Sport": "Baseball", "League": "MLB",
        "Event": "HOU @ MIL", "Type": "1st 5 Run Line",
        "Description": "Brewers -0.5 1st 5",
        "Pick": "MIL -0.5", "Opponent": "HOU", "Odds": "-125",
        "Risk": "312.50", "To Win": "250", "Status": "pending", "Result Date": "",
        "Notes": "Ticket 410213094. Misiorowski vs Imai."
    },
]

# ===== APPEND TO FALLBACK_BETS =====
PATH = 'index.html'
html = open(PATH).read()
m = re.search(r'const FALLBACK_BETS = (\[.*?\]);\s*\n', html, re.DOTALL)
existing = json.loads(m.group(1))
existing.extend(new_bets)
new_arr = json.dumps(existing, separators=(", ", ": "))
new_html = html[:m.start(1)] + new_arr + html[m.end(1):]
open(PATH, 'w').write(new_html)
print(f"Added {len(new_bets)} bets to FALLBACK_BETS. New total: {len(existing)}")

# Save rows array for sheet upload
cols = ["ID","Date","Sport","League","Event","Type","Description","Pick","Opponent","Odds","Risk","To Win","Status","Result Date","Notes"]
sheet_rows = [[b.get(c,"") for c in cols] for b in new_bets]
open("/tmp/sheet_rows.json","w").write(json.dumps(sheet_rows))
print("Saved sheet_rows.json")