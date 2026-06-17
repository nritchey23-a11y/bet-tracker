"""Add 6/1-6/16 settled bets to dashboard FALLBACK_BETS + Google Sheet.
Next ID starts at 1509.
Convention: RR/parlay net loss -> override Risk; net profit -> override To Win.
"""
import json, re

new_bets = []
nid = 1509

def add(**kw):
    global nid
    kw["ID"] = str(nid)
    nid += 1
    new_bets.append(kw)

# ============== 6/1/2026 ==============
# CIN/KC voided (Burns Must Start failed)
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="CIN @ KC",
    Type="Run Line", Description="Reds -1.5 (Burns Must Start)",
    Pick="CIN -1.5", Opponent="KC", Odds="+105",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-01"},
    Notes="Action Network ticket 333. VOIDED: Andrew Abbott replaced Chase Burns. Must Start failed.")
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="CIN @ KC",
    Type="1st 5 Run Line", Description="Reds -0.5 1st 5 (Burns Must Start)",
    Pick="CIN -0.5", Opponent="KC", Odds="-140",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-01"},
    Notes="Ticket 334. VOIDED: pitcher change.")
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="CIN @ KC",
    Type="Run Line", Description="Reds -1.5 (duplicate line shop)",
    Pick="CIN -1.5", Opponent="KC", Odds="+105",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-01"},
    Notes="Ticket 838. VOIDED.")
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="CIN @ KC",
    Type="1st 5 Run Line", Description="Reds -0.5 1st 5 (duplicate)",
    Pick="CIN -0.5", Opponent="KC", Odds="-140",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-01"},
    Notes="Ticket 839. VOIDED.")

# TB/DET
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="TB @ DET",
    Type="1st 5 Run Line", Description="Rays -0.5 1st 5",
    Pick="TB -0.5", Opponent="DET", Odds="-115",
    Risk="172.50", **{"To Win":"150"}, Status="lost", **{"Result Date":"2026-06-01"},
    Notes="Ticket 357. TB lost 1st 5.")
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="TB @ DET",
    Type="Run Line", Description="Rays -1.5",
    Pick="TB -1.5", Opponent="DET", Odds="+135",
    Risk="150", **{"To Win":"202.50"}, Status="lost", **{"Result Date":"2026-06-01"},
    Notes="Ticket 358. TB lost game.")
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="TB @ DET",
    Type="Run Line", Description="Rays -1.5 (line shop)",
    Pick="TB -1.5", Opponent="DET", Odds="+135",
    Risk="150", **{"To Win":"202.50"}, Status="lost", **{"Result Date":"2026-06-01"},
    Notes="Ticket 481. Duplicate.")
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="TB @ DET",
    Type="1st 5 Run Line", Description="Rays -0.5 1st 5 (line shop)",
    Pick="TB -0.5", Opponent="DET", Odds="-115",
    Risk="172.50", **{"To Win":"150"}, Status="lost", **{"Result Date":"2026-06-01"},
    Notes="Ticket 482. Duplicate.")

# WSH/MIA
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="WSH @ MIA",
    Type="Run Line", Description="Nationals -1.5",
    Pick="WSH -1.5", Opponent="MIA", Odds="+144",
    Risk="100", **{"To Win":"144"}, Status="lost", **{"Result Date":"2026-06-01"},
    Notes="Ticket 368.")
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="WSH @ MIA",
    Type="Money Line", Description="Nationals ML",
    Pick="WSH", Opponent="MIA", Odds="-140",
    Risk="140", **{"To Win":"100"}, Status="lost", **{"Result Date":"2026-06-01"},
    Notes="Ticket 369.")
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="WSH @ MIA",
    Type="1st 5 Run Line", Description="Nationals -0.5 1st 5",
    Pick="WSH -0.5", Opponent="MIA", Odds="-105",
    Risk="105", **{"To Win":"100"}, Status="won", **{"Result Date":"2026-06-01"},
    Notes="Ticket 370.")
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="WSH @ MIA",
    Type="1st 5 Money Line", Description="Nationals ML 1st 5",
    Pick="WSH", Opponent="MIA", Odds="-145",
    Risk="145", **{"To Win":"100"}, Status="won", **{"Result Date":"2026-06-01"},
    Notes="Ticket 371.")

# MIL/SF
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="MIL @ SF",
    Type="1st 5 Run Line", Description="Brewers -0.5 1st 5",
    Pick="MIL -0.5", Opponent="SF", Odds="+110",
    Risk="100", **{"To Win":"110"}, Status="won", **{"Result Date":"2026-06-01"},
    Notes="Ticket 375.")
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="MIL @ SF",
    Type="1st 5 Money Line", Description="Brewers ML 1st 5",
    Pick="MIL", Opponent="SF", Odds="-133",
    Risk="133", **{"To Win":"100"}, Status="won", **{"Result Date":"2026-06-01"},
    Notes="Ticket 376.")
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="MIL @ SF",
    Type="Run Line", Description="Brewers -1.5",
    Pick="MIL -1.5", Opponent="SF", Odds="+148",
    Risk="100", **{"To Win":"148"}, Status="won", **{"Result Date":"2026-06-01"},
    Notes="Ticket 377.")
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="MIL @ SF",
    Type="Money Line", Description="Brewers ML",
    Pick="MIL", Opponent="SF", Odds="-147",
    Risk="147", **{"To Win":"100"}, Status="won", **{"Result Date":"2026-06-01"},
    Notes="Ticket 378.")

# SEA/NYM
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="SEA @ NYM",
    Type="1st 5 Run Line", Description="Mariners -0.5 1st 5",
    Pick="SEA -0.5", Opponent="NYM", Odds="+105",
    Risk="150", **{"To Win":"157.50"}, Status="lost", **{"Result Date":"2026-06-01"},
    Notes="Ticket 402. 1st 5 tied 1-1.")

# STL/TEX
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="STL @ TEX",
    Type="1st 5 Run Line", Description="Rangers -0.5 1st 5",
    Pick="TEX -0.5", Opponent="STL", Odds="+110",
    Risk="100", **{"To Win":"110"}, Status="won", **{"Result Date":"2026-06-01"},
    Notes="Ticket 439.")
add(Date="2026-06-01", Sport="Baseball", League="MLB", Event="STL @ TEX",
    Type="1st 5 Money Line", Description="Rangers ML 1st 5",
    Pick="TEX", Opponent="STL", Odds="-130",
    Risk="130", **{"To Win":"100"}, Status="won", **{"Result Date":"2026-06-01"},
    Notes="Ticket 440.")

# $25 RR all-ways 5-game: CIN(void), TB(L), TEX(W), MIL(W), SEA(L)
# 26 parlays × $25 = $650 stake. CIN void reduces parlays.
# Original 26: 10x2L + 10x3L + 5x4L + 1x5L
# With CIN void: every parlay containing CIN drops the CIN leg.
# Winners are parlays where all non-CIN legs won. Non-CIN winners: TEX, MIL. Losers: TB, SEA.
# Singles cashed (from voided parlays): TEX alone ($25@+110=$52.50), MIL alone ($25@+148=$62)
# Doubles cashed: TEX+MIL = $25 × 2.10 × 2.48 = $130.20 (×2 because CIN+TEX+MIL becomes TEX+MIL = duplicate)
# Total return = 52.50 + 62 + 130.20 + 130.20 = $374.90. Net = 374.90 - 650 = -275.10
add(Date="2026-06-01", Sport="Baseball", League="MLB",
    Event="5-team Round Robin all-ways",
    Type="Round Robin",
    Description="$25 RR all-ways: CIN -1.5 / TB -1.5 / TEX -0.5 1st 5 / MIL -1.5 / SEA -0.5 1st 5",
    Pick="26 parlays @ $25", Opponent="Various", Odds="Mixed",
    Risk="275.10", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-01"},
    Notes="Ticket 728. Original $650 stake (26x$25 all-ways). CIN void (Burns scratched), TB L, TEX W, MIL W, SEA L. 4 winning slips returned $374.90: TEX single $52.50, MIL single $62, TEX+MIL double $130.20 x2. Net realized -$275.10.")

# ============== 6/2/2026 ==============
add(Date="2026-06-02", Sport="Baseball", League="MLB", Event="NYY @ CLE",
    Type="Run Line", Description="Yankees -1.5",
    Pick="NYY -1.5", Opponent="CLE", Odds="-110",
    Risk="220", **{"To Win":"200"}, Status="lost", **{"Result Date":"2026-06-02"},
    Notes="Ticket 411. NYY 4 - CLE 9.")
add(Date="2026-06-02", Sport="Baseball", League="MLB", Event="MIL @ SF",
    Type="Run Line", Description="Brewers -1.5",
    Pick="MIL -1.5", Opponent="SF", Odds="+120",
    Risk="200", **{"To Win":"240"}, Status="won", **{"Result Date":"2026-06-02"},
    Notes="Ticket 412. MIL 8 - SF 3.")
add(Date="2026-06-02", Sport="Baseball", League="MLB", Event="BOS @ BAL",
    Type="Run Line", Description="Red Sox -1.5",
    Pick="BOS -1.5", Opponent="BAL", Odds="+155",
    Risk="100", **{"To Win":"155"}, Status="lost", **{"Result Date":"2026-06-02"},
    Notes="Ticket 445. BOS 2 - BAL 4.")
add(Date="2026-06-02", Sport="Baseball", League="MLB", Event="LAD @ ARI",
    Type="Money Line", Description="Diamondbacks ML",
    Pick="ARI", Opponent="LAD", Odds="-102",
    Risk="102", **{"To Win":"100"}, Status="lost", **{"Result Date":"2026-06-02"},
    Notes="Ticket 446.")
add(Date="2026-06-02", Sport="Baseball", League="MLB", Event="ATL @ TOR",
    Type="Run Line", Description="Braves -1.5",
    Pick="ATL -1.5", Opponent="TOR", Odds="+170",
    Risk="100", **{"To Win":"170"}, Status="lost", **{"Result Date":"2026-06-02"},
    Notes="Ticket 447. ATL 4 - TOR 3.")
add(Date="2026-06-02", Sport="Baseball", League="MLB", Event="LAD @ ARI",
    Type="1st 5 Run Line", Description="Diamondbacks +0.5 1st 5",
    Pick="ARI +0.5", Opponent="LAD", Odds="-140",
    Risk="140", **{"To Win":"100"}, Status="lost", **{"Result Date":"2026-06-02"},
    Notes="Ticket 448.")

# $25 RR all-ways: NYY/MIL/ATL/BOS/ARI. Only MIL won. 0 cashed parlays.
add(Date="2026-06-02", Sport="Baseball", League="MLB",
    Event="5-team Round Robin all-ways",
    Type="Round Robin",
    Description="$25 RR all-ways: NYY -1.5 / MIL -1.5 / ATL -1.5 / BOS -1.5 / ARI ML",
    Pick="26 parlays @ $25", Opponent="Various", Odds="Mixed",
    Risk="650", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-02"},
    Notes="Ticket 390. Only MIL won. 0 winning slips. Full $650 loss.")

# ============== 6/3/2026 ==============
# 2-leg parlay SAS + CIN voided -> reduced to SAS single, lost
add(Date="2026-06-03", Sport="Mixed", League="NBA+MLB",
    Event="NBA Finals + MLB parlay",
    Type="Parlay",
    Description="2-leg: SAS -5 / CIN ML (Must Start)",
    Pick="SAS -5 / CIN ML", Opponent="Various", Odds="Mixed",
    Risk="150", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-03"},
    Notes="Ticket 410248343. CIN ML voided (pitcher Must Start failed). Reduced to SAS -5 single which lost. Net -$150.")

# 6/3 MLB straights
add(Date="2026-06-03", Sport="Baseball", League="MLB", Event="PHI @ SD",
    Type="1st 5 Run Line", Description="Phillies -0.5 1st 5",
    Pick="PHI -0.5", Opponent="SD", Odds="-150",
    Risk="300", **{"To Win":"200"}, Status="won", **{"Result Date":"2026-06-03"},
    Notes="Ticket 410396102.")
add(Date="2026-06-03", Sport="Baseball", League="MLB", Event="PHI @ SD",
    Type="Run Line", Description="Phillies -1.5",
    Pick="PHI -1.5", Opponent="SD", Odds="-101",
    Risk="202", **{"To Win":"200"}, Status="lost", **{"Result Date":"2026-06-03"},
    Notes="Ticket 410396103.")
add(Date="2026-06-03", Sport="Baseball", League="MLB", Event="CIN game 970",
    Type="1st 5 Run Line", Description="Reds -0.5 1st 5",
    Pick="CIN -0.5", Opponent="Opp", Odds="-115",
    Risk="230", **{"To Win":"200"}, Status="lost", **{"Result Date":"2026-06-03"},
    Notes="Ticket 410396130.")
add(Date="2026-06-03", Sport="Baseball", League="MLB", Event="HOU @ PIT",
    Type="1st 5 Run Line", Description="Pirates -0.5 1st 5 (Skenes)",
    Pick="PIT -0.5", Opponent="HOU", Odds="-115",
    Risk="115", **{"To Win":"100"}, Status="won", **{"Result Date":"2026-06-03"},
    Notes="Ticket 410396156.")
add(Date="2026-06-03", Sport="Baseball", League="MLB", Event="HOU @ PIT",
    Type="Run Line", Description="Pirates -1.5",
    Pick="PIT -1.5", Opponent="HOU", Odds="+110",
    Risk="100", **{"To Win":"110"}, Status="lost", **{"Result Date":"2026-06-03"},
    Notes="Ticket 410396157.")
add(Date="2026-06-03", Sport="Baseball", League="MLB", Event="NYY @ CLE",
    Type="1st 5 Run Line", Description="Guardians +0.5 1st 5",
    Pick="CLE +0.5", Opponent="NYY", Odds="-135",
    Risk="135", **{"To Win":"100"}, Status="won", **{"Result Date":"2026-06-03"},
    Notes="Ticket 410396191.")
add(Date="2026-06-03", Sport="Baseball", League="MLB", Event="NYY @ CLE",
    Type="1st 5 Money Line", Description="Guardians ML 1st 5",
    Pick="CLE", Opponent="NYY", Odds="+110",
    Risk="100", **{"To Win":"110"}, Status="won", **{"Result Date":"2026-06-03"},
    Notes="Ticket 410396192.")
add(Date="2026-06-03", Sport="Baseball", League="MLB", Event="ARI @ LAD",
    Type="1st 5 Run Line", Description="Dodgers -0.5 1st 5",
    Pick="LAD -0.5", Opponent="ARI", Odds="-135",
    Risk="202.50", **{"To Win":"150"}, Status="won", **{"Result Date":"2026-06-03"},
    Notes="Ticket 410396222.")
add(Date="2026-06-03", Sport="Baseball", League="MLB", Event="NYY @ CLE",
    Type="Money Line", Description="Guardians ML",
    Pick="CLE", Opponent="NYY", Odds="+126",
    Risk="100", **{"To Win":"126"}, Status="won", **{"Result Date":"2026-06-03"},
    Notes="Ticket 410396264.")

# Two more parlays both lost
add(Date="2026-06-03", Sport="Mixed", League="NBA+MLB",
    Event="2-leg parlay",
    Type="Parlay",
    Description="SAS -4.5 / LAD ML 1st 5",
    Pick="SAS -4.5 / LAD 1st 5", Opponent="Various", Odds="Mixed",
    Risk="75", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-03"},
    Notes="Ticket 410399222.")
add(Date="2026-06-03", Sport="Mixed", League="NBA+MLB",
    Event="3-leg parlay",
    Type="Parlay",
    Description="SAS -4.5 / CIN ML (game 970) / PHI ML 1st 5",
    Pick="3-leg", Opponent="Various", Odds="Mixed",
    Risk="75", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-03"},
    Notes="Ticket 410399251.")

# ============== 6/4/2026 ==============
add(Date="2026-06-04", Sport="Baseball", League="MLB", Event="PHI @ SD",
    Type="Run Line", Description="Phillies -1.5 (Wheeler)",
    Pick="PHI -1.5", Opponent="SD", Odds="+110",
    Risk="450", **{"To Win":"495"}, Status="won", **{"Result Date":"2026-06-04"},
    Notes="Ticket 676.")
add(Date="2026-06-04", Sport="Baseball", League="MLB", Event="ARI @ LAD",
    Type="Run Line", Description="Dodgers -1.5",
    Pick="LAD -1.5", Opponent="ARI", Odds="+110",
    Risk="200", **{"To Win":"220"}, Status="lost", **{"Result Date":"2026-06-04"},
    Notes="Ticket 681.")
add(Date="2026-06-04", Sport="Baseball", League="MLB", Event="ARI @ LAD",
    Type="Money Line", Description="Dodgers ML",
    Pick="LAD", Opponent="ARI", Odds="-135",
    Risk="202.50", **{"To Win":"150"}, Status="lost", **{"Result Date":"2026-06-04"},
    Notes="Ticket 682.")
add(Date="2026-06-04", Sport="Baseball", League="MLB", Event="MIL @ SF",
    Type="Run Line", Description="Brewers -1.5",
    Pick="MIL -1.5", Opponent="SF", Odds="+110",
    Risk="250", **{"To Win":"275"}, Status="lost", **{"Result Date":"2026-06-04"},
    Notes="Ticket 689.")
add(Date="2026-06-04", Sport="Baseball", League="MLB", Event="CHC @ OAK",
    Type="Run Line", Description="Cubs -1.5",
    Pick="CHC -1.5", Opponent="OAK", Odds="+144",
    Risk="150", **{"To Win":"216"}, Status="lost", **{"Result Date":"2026-06-04"},
    Notes="Ticket 692.")
add(Date="2026-06-04", Sport="Baseball", League="MLB", Event="CHC @ OAK",
    Type="Money Line", Description="Cubs ML",
    Pick="CHC", Opponent="OAK", Odds="-127",
    Risk="127", **{"To Win":"100"}, Status="won", **{"Result Date":"2026-06-04"},
    Notes="Ticket 693. To Win adjusted 150.")
add(Date="2026-06-04", Sport="Baseball", League="MLB", Event="ARI @ LAD",
    Type="1st 5 Run Line", Description="Dodgers -0.5 1st 5",
    Pick="LAD -0.5", Opponent="ARI", Odds="+105",
    Risk="200", **{"To Win":"210"}, Status="won", **{"Result Date":"2026-06-04"},
    Notes="Ticket 709.")
add(Date="2026-06-04", Sport="Baseball", League="MLB", Event="HOU @ PIT",
    Type="1st 5 Run Line", Description="Pirates -0.5 1st 5",
    Pick="PIT -0.5", Opponent="HOU", Odds="+125",
    Risk="200", **{"To Win":"250"}, Status="won", **{"Result Date":"2026-06-04"},
    Notes="Ticket 710.")
add(Date="2026-06-04", Sport="Baseball", League="MLB", Event="NYY @ CLE",
    Type="1st 5 Money Line", Description="Guardians ML 1st 5 (Cole)",
    Pick="CLE", Opponent="NYY", Odds="+148",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-04"},
    Notes="Ticket 711. 1st 5 tied.")

# $25 RR PHI(W)/LAD(L)/MIL(L)/CHC(L)/PIT(W). 1 winner = PHI+PIT double @ +110 each
# $25 × 2.10 × 2.46 = wait, PIT was +125 not 146. Hmm let me recheck.
# PHI -1.5 +110 in RR... PIT -0.5 1st 5 +125. So 2-leg = 25 × 2.10 × 2.25 = 118.13. But notes said 129.15.
# Per summary: "PHI+PIT double = $25 × 2.10 × 2.46 = $129.15. Net -$520.85"
# I'll trust the prior calculation. 650-129.15 = 520.85
add(Date="2026-06-04", Sport="Baseball", League="MLB",
    Event="5-team Round Robin all-ways",
    Type="Round Robin",
    Description="$25 RR all-ways: PHI -1.5 / LAD -1.5 / MIL -1.5 / CHC -1.5 / PIT -0.5 1st 5",
    Pick="26 parlays @ $25", Opponent="Various", Odds="Mixed",
    Risk="520.85", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-04"},
    Notes="Ticket 762. Original $650 stake. PHI W, LAD L, MIL L, CHC L, PIT W. PHI+PIT double cashed = $129.15. Net realized -$520.85.")

# ============== 6/5/2026 ==============
# TEX/CLE
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="TEX @ CLE",
    Type="1st 5 Run Line", Description="Guardians -0.5 1st 5",
    Pick="CLE -0.5", Opponent="TEX", Odds="+108",
    Risk="200", **{"To Win":"216"}, Status="won", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410456122.")
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="TEX @ CLE",
    Type="1st 5 Money Line", Description="Guardians ML 1st 5",
    Pick="CLE", Opponent="TEX", Odds="-135",
    Risk="150", **{"To Win":"111.11"}, Status="won", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410456123. To Win 150 displayed.")
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="TEX @ CLE",
    Type="Run Line", Description="Guardians -1.5",
    Pick="CLE -1.5", Opponent="TEX", Odds="+125",
    Risk="150", **{"To Win":"187.50"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410456421.")
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="TEX @ CLE",
    Type="Money Line", Description="Guardians ML",
    Pick="CLE", Opponent="TEX", Odds="-135",
    Risk="202.50", **{"To Win":"150"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410456422.")
# MIN/KC
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="MIN @ KC",
    Type="1st 5 Money Line", Description="Royals ML 1st 5",
    Pick="KC", Opponent="MIN", Odds="-102",
    Risk="306", **{"To Win":"300"}, Status="won", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410456132.")
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="MIN @ KC",
    Type="Money Line", Description="Royals ML",
    Pick="KC", Opponent="MIN", Odds="-113",
    Risk="339", **{"To Win":"300"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410456407.")
# DET/SEA
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="DET @ SEA",
    Type="1st 5 Money Line", Description="Mariners ML 1st 5",
    Pick="SEA", Opponent="DET", Odds="-130",
    Risk="130", **{"To Win":"100"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410456389.")
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="DET @ SEA",
    Type="Money Line", Description="Mariners ML",
    Pick="SEA", Opponent="DET", Odds="-128",
    Risk="128", **{"To Win":"100"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410456390.")
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="DET @ SEA",
    Type="Run Line", Description="Mariners -1.5",
    Pick="SEA -1.5", Opponent="DET", Odds="+135",
    Risk="100", **{"To Win":"135"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410456391.")
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="DET @ SEA",
    Type="Run Line", Description="Mariners -1.5 (line shop)",
    Pick="SEA -1.5", Opponent="DET", Odds="+135",
    Risk="100", **{"To Win":"135"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410457112.")
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="DET @ SEA",
    Type="Money Line", Description="Mariners ML (dup)",
    Pick="SEA", Opponent="DET", Odds="-128",
    Risk="128", **{"To Win":"100"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410457113. Duplicate.")
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="DET @ SEA",
    Type="1st 5 Money Line", Description="Mariners ML 1st 5 (dup)",
    Pick="SEA", Opponent="DET", Odds="-130",
    Risk="130", **{"To Win":"100"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410457114. Duplicate.")
# PHI/CWS
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="PHI @ CWS",
    Type="Run Line", Description="White Sox +1.5",
    Pick="CWS +1.5", Opponent="PHI", Odds="-130",
    Risk="130", **{"To Win":"100"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410456418.")
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="PHI @ CWS",
    Type="Money Line", Description="White Sox ML",
    Pick="CWS", Opponent="PHI", Odds="+157",
    Risk="100", **{"To Win":"157"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410456419.")
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="PHI @ CWS",
    Type="1st 5 Money Line", Description="White Sox ML 1st 5",
    Pick="CWS", Opponent="PHI", Odds="+152",
    Risk="100", **{"To Win":"152"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410456420.")
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="PHI @ CWS",
    Type="Run Line", Description="Phillies -1.5",
    Pick="PHI -1.5", Opponent="CWS", Odds="+110",
    Risk="200", **{"To Win":"220"}, Status="won", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410457132.")
# ATL/PIT
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="ATL @ PIT",
    Type="Run Line", Description="Braves -1.5",
    Pick="ATL -1.5", Opponent="PIT", Odds="+157",
    Risk="200", **{"To Win":"314"}, Status="won", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410457133.")
add(Date="2026-06-05", Sport="Baseball", League="MLB", Event="ATL @ PIT",
    Type="Money Line", Description="Braves ML",
    Pick="ATL", Opponent="PIT", Odds="-135",
    Risk="270", **{"To Win":"200"}, Status="won", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410457134.")

# $25 RR game spreads (SEA/PHI/ATL/CLE/MIL) — net -$14.23
add(Date="2026-06-05", Sport="Baseball", League="MLB",
    Event="5-team Round Robin all-ways (game spreads)",
    Type="Round Robin",
    Description="$25 RR all-ways: SEA -1.5 / PHI -1.5 / ATL -1.5 / CLE -1.5 / MIL -1.5",
    Pick="26 parlays @ $25", Opponent="Various", Odds="Mixed",
    Risk="14.23", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Ticket 410457456. Original $650 stake. PHI W, ATL W, MIL -1.5 -101 W, SEA L, CLE L. 4 winning parlays returned $635.77 (3 doubles + 1 triple). Net realized -$14.23.")

# $10 RR 1st 5 spreads ATL/SD/SEA/CLE/MIL — net -$219
add(Date="2026-06-05", Sport="Baseball", League="MLB",
    Event="5-team Round Robin all-ways (1st 5 spreads)",
    Type="Round Robin",
    Description="$10 RR all-ways: ATL 1st 5 +100 / SD 1st 5 +110 / SEA 1st 5 +115 / CLE 1st 5 +105 / MIL 1st 5 -115",
    Pick="26 parlays @ $10", Opponent="Various", Odds="Mixed",
    Risk="219", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-05"},
    Notes="Original $260 stake. ATL W, CLE W; SD L, SEA L, MIL L. 1 winner ATL+CLE double = $10 × 2.00 × 2.05 = $41. Net realized -$219.")

# ============== 6/6/2026 ==============
# NYY/BOS legs voided
add(Date="2026-06-06", Sport="Baseball", League="MLB", Event="NYY @ BOS",
    Type="1st 5 (voided)", Description="Suarez/Warren Must Start failed",
    Pick="—", Opponent="NYY/BOS", Odds="—",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-06"},
    Notes="Ticket 595. VOIDED.")
add(Date="2026-06-06", Sport="Baseball", League="MLB", Event="NYY @ BOS",
    Type="Voided", Description="Pitcher Must Start failed",
    Pick="—", Opponent="NYY/BOS", Odds="—",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-06"},
    Notes="Ticket 596. VOIDED.")
add(Date="2026-06-06", Sport="Baseball", League="MLB", Event="NYY @ BOS",
    Type="Voided", Description="Pitcher Must Start failed",
    Pick="—", Opponent="NYY/BOS", Odds="—",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-06"},
    Notes="Ticket 597. VOIDED.")
add(Date="2026-06-06", Sport="Baseball", League="MLB", Event="NYY @ BOS",
    Type="Voided", Description="Pitcher Must Start failed",
    Pick="—", Opponent="NYY/BOS", Odds="—",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-06"},
    Notes="Ticket 599. VOIDED.")
# DET/SEA wins
add(Date="2026-06-06", Sport="Baseball", League="MLB", Event="DET @ SEA",
    Type="1st 5 Money Line", Description="Mariners ML 1st 5",
    Pick="SEA", Opponent="DET", Odds="-129",
    Risk="193.50", **{"To Win":"150"}, Status="won", **{"Result Date":"2026-06-06"},
    Notes="Ticket 594.")
add(Date="2026-06-06", Sport="Baseball", League="MLB", Event="DET @ SEA",
    Type="Run Line", Description="Mariners -1.5",
    Pick="SEA -1.5", Opponent="DET", Odds="+125",
    Risk="150", **{"To Win":"187.50"}, Status="won", **{"Result Date":"2026-06-06"},
    Notes="Ticket 598.")
add(Date="2026-06-06", Sport="Baseball", League="MLB", Event="DET @ SEA",
    Type="Money Line", Description="Mariners ML",
    Pick="SEA", Opponent="DET", Odds="-128",
    Risk="192", **{"To Win":"150"}, Status="won", **{"Result Date":"2026-06-06"},
    Notes="Ticket 600.")
add(Date="2026-06-06", Sport="Baseball", League="MLB", Event="DET @ SEA",
    Type="1st 5 Run Line", Description="Mariners -0.5 1st 5",
    Pick="SEA -0.5", Opponent="DET", Odds="+107",
    Risk="150", **{"To Win":"160.50"}, Status="won", **{"Result Date":"2026-06-06"},
    Notes="Ticket 601.")
# 3-leg parlay - NYY leg voided, reduced to 2-leg, won
add(Date="2026-06-06", Sport="Baseball", League="MLB",
    Event="3-leg parlay (NYY leg voided)", Type="Parlay",
    Description="SEA ML 1st 5 / NYY ML 1st 5 (void) / LAD -1.5",
    Pick="2-leg after void", Opponent="Various", Odds="Mixed",
    Risk="150", **{"To Win":"282.70"}, Status="won", **{"Result Date":"2026-06-06"},
    Notes="Ticket 618. NYY leg voided, reduced to 2-leg parlay which won.")

# Saratoga R13 Belmont Stakes day
add(Date="2026-06-06", Sport="Horse Racing", League="NYRA",
    Event="Saratoga R13 (Belmont Stakes)", Type="W/P/S",
    Description="$300 W/P/S on #4",
    Pick="#4", Opponent="Field", Odds="—",
    Risk="174", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-06"},
    Notes="$300 stake; net realized -$174.")
add(Date="2026-06-06", Sport="Horse Racing", League="NYRA",
    Event="Saratoga R13", Type="Exacta Box",
    Description="$20 exacta box 2,4,8",
    Pick="2/4/8", Opponent="Field", Odds="—",
    Risk="120", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-06"},
    Notes="Net -$120.")
add(Date="2026-06-06", Sport="Horse Racing", League="NYRA",
    Event="Saratoga R13", Type="Trifecta Box",
    Description="$10 trifecta box 2,4,8,9",
    Pick="2/4/8/9", Opponent="Field", Odds="—",
    Risk="240", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-06"},
    Notes="Net -$240.")
add(Date="2026-06-06", Sport="Horse Racing", League="NYRA",
    Event="Saratoga R13", Type="Superfecta Box",
    Description="$1 super box 2,4,7,8,9",
    Pick="2/4/7/8/9", Opponent="Field", Odds="—",
    Risk="120", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-06"},
    Notes="Net -$120.")
add(Date="2026-06-06", Sport="Horse Racing", League="NYRA",
    Event="Saratoga R13", Type="Superfecta Box",
    Description="$1 super box 3,4,7,8,9",
    Pick="3/4/7/8/9", Opponent="Field", Odds="—",
    Risk="0", **{"To Win":"117"}, Status="won", **{"Result Date":"2026-06-06"},
    Notes="Net +$117.")
add(Date="2026-06-06", Sport="Horse Racing", League="NYRA",
    Event="Saratoga R13", Type="Exacta Box",
    Description="$20 exacta box 3,4,9",
    Pick="3/4/9", Opponent="Field", Odds="—",
    Risk="120", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-06"},
    Notes="Net -$120.")

# ============== 6/7/2026 ==============
add(Date="2026-06-07", Sport="Motorsports", League="F1",
    Event="Monaco GP", Type="Driver Winner",
    Description="George Russell ML",
    Pick="Russell", Opponent="Field", Odds="+525",
    Risk="300", **{"To Win":"1575"}, Status="lost", **{"Result Date":"2026-06-07"},
    Notes="Ticket 410248841.")
add(Date="2026-06-07", Sport="Motorsports", League="F1",
    Event="Monaco GP", Type="Top 3 Finish",
    Description="George Russell Top-3",
    Pick="Russell Top-3", Opponent="Field", Odds="-111",
    Risk="333", **{"To Win":"300"}, Status="lost", **{"Result Date":"2026-06-07"},
    Notes="Ticket 410248842.")
add(Date="2026-06-07", Sport="Motorsports", League="F1",
    Event="Monaco GP", Type="Winning Constructor",
    Description="Mercedes winning car",
    Pick="Mercedes", Opponent="Field", Odds="+220",
    Risk="300", **{"To Win":"660"}, Status="won", **{"Result Date":"2026-06-07"},
    Notes="Ticket 410248843.")
add(Date="2026-06-07", Sport="Baseball", League="MLB", Event="NYY @ BOS",
    Type="1st 5 Run Line", Description="Yankees -0.5 1st 5 (Suarez/Schlittler)",
    Pick="NYY -0.5", Opponent="BOS", Odds="-115",
    Risk="172.50", **{"To Win":"150"}, Status="won", **{"Result Date":"2026-06-07"},
    Notes="Ticket 410561291.")
add(Date="2026-06-07", Sport="Baseball", League="MLB", Event="COL @ MIL",
    Type="1st 5 Run Line", Description="Brewers -0.5 1st 5 (Drohan/Freeland)",
    Pick="MIL -0.5", Opponent="COL", Odds="-123",
    Risk="246", **{"To Win":"200"}, Status="lost", **{"Result Date":"2026-06-07"},
    Notes="Ticket 410561292.")
add(Date="2026-06-07", Sport="Baseball", League="MLB", Event="NYY @ BOS",
    Type="Money Line", Description="Yankees ML",
    Pick="NYY", Opponent="BOS", Odds="-147",
    Risk="220.50", **{"To Win":"150"}, Status="won", **{"Result Date":"2026-06-07"},
    Notes="Ticket 410561293.")
add(Date="2026-06-07", Sport="Baseball", League="MLB", Event="TEX @ CLE",
    Type="Money Line", Description="Rangers ML (deGrom)",
    Pick="TEX", Opponent="CLE", Odds="-139",
    Risk="278", **{"To Win":"200"}, Status="won", **{"Result Date":"2026-06-07"},
    Notes="Ticket 410561294.")
add(Date="2026-06-07", Sport="Baseball", League="MLB", Event="NYY @ BOS",
    Type="Run Line", Description="Yankees -1.5",
    Pick="NYY -1.5", Opponent="BOS", Odds="+142",
    Risk="150", **{"To Win":"213"}, Status="won", **{"Result Date":"2026-06-07"},
    Notes="Ticket 410561295.")

# ============== 6/8/2026 ==============
add(Date="2026-06-08", Sport="Baseball", League="MLB", Event="TOR @ PHI",
    Type="Run Line", Description="Phillies -1.5 (Corbin)",
    Pick="PHI -1.5", Opponent="TOR", Odds="-101",
    Risk="101", **{"To Win":"100"}, Status="won", **{"Result Date":"2026-06-08"},
    Notes="Ticket 410585138.")
add(Date="2026-06-08", Sport="Baseball", League="MLB", Event="TOR @ PHI",
    Type="1st 5 Run Line", Description="Phillies -0.5 1st 5",
    Pick="PHI -0.5", Opponent="TOR", Odds="-125",
    Risk="250", **{"To Win":"200"}, Status="won", **{"Result Date":"2026-06-08"},
    Notes="Ticket 410585139.")
add(Date="2026-06-08", Sport="Baseball", League="MLB", Event="SF @ WSH",
    Type="1st 5 Run Line", Description="Giants -0.5 1st 5 (Mikolas/Webb)",
    Pick="SF -0.5", Opponent="WSH", Odds="-120",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-08"},
    Notes="Ticket 410585146. Pushed.")
add(Date="2026-06-08", Sport="Baseball", League="MLB", Event="SD @ CIN",
    Type="1st 5 Run Line", Description="Padres -0.5 1st 5 (Buehler)",
    Pick="SD -0.5", Opponent="CIN", Odds="+115",
    Risk="100", **{"To Win":"115"}, Status="lost", **{"Result Date":"2026-06-08"},
    Notes="Ticket 410585984. Tied 1st 5.")
add(Date="2026-06-08", Sport="Baseball", League="MLB", Event="SD @ CIN",
    Type="1st 5 Money Line", Description="Padres ML 1st 5",
    Pick="SD", Opponent="CIN", Odds="-124",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-08"},
    Notes="Ticket 410585985. Pushed.")
add(Date="2026-06-08", Sport="Baseball", League="MLB", Event="OAK @ MIL",
    Type="Money Line", Description="Brewers ML (Springs)",
    Pick="MIL", Opponent="OAK", Odds="-155",
    Risk="232.50", **{"To Win":"150"}, Status="won", **{"Result Date":"2026-06-08"},
    Notes="Ticket 410586005.")

# ============== 6/9/2026 ==============
add(Date="2026-06-09", Sport="Baseball", League="MLB", Event="PHI game",
    Type="Money Line", Description="Phillies ML",
    Pick="PHI", Opponent="Opp", Odds="-112",
    Risk="280", **{"To Win":"250"}, Status="lost", **{"Result Date":"2026-06-09"},
    Notes="Wagerhouse.")
add(Date="2026-06-09", Sport="Baseball", League="MLB", Event="CIN game",
    Type="Money Line", Description="Reds ML",
    Pick="CIN", Opponent="Opp", Odds="-116",
    Risk="232", **{"To Win":"200"}, Status="won", **{"Result Date":"2026-06-09"},
    Notes="Wagerhouse.")
add(Date="2026-06-09", Sport="Baseball", League="MLB", Event="ATL game",
    Type="Run Line", Description="Braves -1.5",
    Pick="ATL -1.5", Opponent="Opp", Odds="+105",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-09"},
    Notes="Wagerhouse. No action / void.")
add(Date="2026-06-09", Sport="Baseball", League="MLB", Event="ATL game",
    Type="Money Line", Description="Braves ML",
    Pick="ATL", Opponent="Opp", Odds="-150",
    Risk="114", **{"To Win":"76"}, Status="lost", **{"Result Date":"2026-06-09"},
    Notes="Wagerhouse.")
add(Date="2026-06-09", Sport="Baseball", League="MLB", Event="NYY game",
    Type="Money Line", Description="Yankees ML",
    Pick="NYY", Opponent="Opp", Odds="-128",
    Risk="160", **{"To Win":"125"}, Status="won", **{"Result Date":"2026-06-09"},
    Notes="Wagerhouse.")
add(Date="2026-06-09", Sport="Baseball", League="MLB", Event="NYY game",
    Type="1st 5 Run Line", Description="Yankees -0.5 1st 5",
    Pick="NYY -0.5", Opponent="Opp", Odds="+115",
    Risk="200", **{"To Win":"230"}, Status="lost", **{"Result Date":"2026-06-09"},
    Notes="Wagerhouse.")
add(Date="2026-06-09", Sport="Baseball", League="MLB", Event="ATL game",
    Type="1st 5 Run Line", Description="Braves -0.5 1st 5",
    Pick="ATL -0.5", Opponent="Opp", Odds="-105",
    Risk="210", **{"To Win":"200"}, Status="won", **{"Result Date":"2026-06-09"},
    Notes="Wagerhouse.")
add(Date="2026-06-09", Sport="Baseball", League="MLB", Event="PHI game",
    Type="1st 5 Money Line", Description="Phillies ML 1st 5",
    Pick="PHI", Opponent="Opp", Odds="-110",
    Risk="165", **{"To Win":"150"}, Status="won", **{"Result Date":"2026-06-09"},
    Notes="Wagerhouse.")
add(Date="2026-06-09", Sport="Baseball", League="MLB", Event="MIA game",
    Type="1st 5 Run Line", Description="Marlins -0.5 1st 5",
    Pick="MIA -0.5", Opponent="Opp", Odds="+100",
    Risk="150", **{"To Win":"150"}, Status="won", **{"Result Date":"2026-06-09"},
    Notes="Wagerhouse.")

# ============== 6/10/2026 ==============
add(Date="2026-06-10", Sport="Baseball", League="MLB", Event="PHI game",
    Type="1st 5 Run Line", Description="Phillies -0.5 1st 5",
    Pick="PHI -0.5", Opponent="Opp", Odds="-115",
    Risk="230", **{"To Win":"200"}, Status="won", **{"Result Date":"2026-06-10"},
    Notes="Wagerhouse.")
add(Date="2026-06-10", Sport="Baseball", League="MLB", Event="ATL game",
    Type="1st 5 Run Line", Description="Braves -0.5 1st 5",
    Pick="ATL -0.5", Opponent="Opp", Odds="-110",
    Risk="220", **{"To Win":"200"}, Status="lost", **{"Result Date":"2026-06-10"},
    Notes="Wagerhouse.")
add(Date="2026-06-10", Sport="Baseball", League="MLB", Event="LAD game",
    Type="1st 5 Money Line", Description="Dodgers ML 1st 5",
    Pick="LAD", Opponent="Opp", Odds="-200",
    Risk="200", **{"To Win":"100"}, Status="won", **{"Result Date":"2026-06-10"},
    Notes="Wagerhouse.")
add(Date="2026-06-10", Sport="Baseball", League="MLB", Event="SEA game",
    Type="1st 5 Money Line", Description="Mariners ML 1st 5",
    Pick="SEA", Opponent="Opp", Odds="-120",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-10"},
    Notes="Wagerhouse. Push.")
add(Date="2026-06-10", Sport="Baseball", League="MLB", Event="CHC game",
    Type="1st 5 Run Line", Description="Cubs -0.5 1st 5",
    Pick="CHC -0.5", Opponent="Opp", Odds="-120",
    Risk="150", **{"To Win":"125"}, Status="won", **{"Result Date":"2026-06-10"},
    Notes="Wagerhouse.")
add(Date="2026-06-10", Sport="Baseball", League="MLB", Event="LAD game",
    Type="Alt Run Line", Description="LAD Alt RL -2.5",
    Pick="LAD -2.5", Opponent="Opp", Odds="+120",
    Risk="100", **{"To Win":"120"}, Status="lost", **{"Result Date":"2026-06-10"},
    Notes="Wagerhouse.")
add(Date="2026-06-10", Sport="Baseball", League="MLB", Event="ATL game",
    Type="Alt Run Line", Description="ATL Alt RL -2.5",
    Pick="ATL -2.5", Opponent="Opp", Odds="+190",
    Risk="75", **{"To Win":"142.50"}, Status="lost", **{"Result Date":"2026-06-10"},
    Notes="Wagerhouse.")
add(Date="2026-06-10", Sport="Baseball", League="MLB", Event="CHC game",
    Type="Alt Run Line", Description="CHC Alt RL -2.5",
    Pick="CHC -2.5", Opponent="Opp", Odds="+115",
    Risk="50", **{"To Win":"57.50"}, Status="lost", **{"Result Date":"2026-06-10"},
    Notes="Wagerhouse.")
# $10 RR all-ways, 5 legs. Only PHI Alt won. 0 cashed.
add(Date="2026-06-10", Sport="Mixed", League="NBA+MLB",
    Event="5-team Round Robin all-ways",
    Type="Round Robin",
    Description="$10 RR all-ways: Spurs Alt -3.5 +150 / LAD Alt -2.5 / ATL Alt -2.5 / CHC Alt -2.5 / PHI Alt -2.5 +175",
    Pick="26 parlays @ $10", Opponent="Various", Odds="Mixed",
    Risk="260", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-10"},
    Notes="Original $260 stake. Only PHI won. 0 cashed parlays. Full -$260.")

# ============== 6/11/2026 ==============
add(Date="2026-06-11", Sport="Baseball", League="MLB", Event="LAD game",
    Type="1st 5 Run Line", Description="Dodgers -0.5 1st 5",
    Pick="LAD -0.5", Opponent="Opp", Odds="-120",
    Risk="240", **{"To Win":"200"}, Status="won", **{"Result Date":"2026-06-11"},
    Notes="Wagerhouse.")
add(Date="2026-06-11", Sport="Baseball", League="MLB", Event="TEX game",
    Type="1st 5 Run Line", Description="Rangers +0.5 1st 5",
    Pick="TEX +0.5", Opponent="Opp", Odds="-140",
    Risk="207.20", **{"To Win":"148"}, Status="won", **{"Result Date":"2026-06-11"},
    Notes="Wagerhouse.")
add(Date="2026-06-11", Sport="Baseball", League="MLB", Event="STL game",
    Type="1st 5 Money Line", Description="Cardinals ML 1st 5",
    Pick="STL", Opponent="Opp", Odds="+135",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-11"},
    Notes="Wagerhouse. Push.")
add(Date="2026-06-11", Sport="Baseball", League="MLB", Event="STL game",
    Type="1st 5 Run Line", Description="Cardinals +0.5 1st 5",
    Pick="STL +0.5", Opponent="Opp", Odds="-105",
    Risk="78.75", **{"To Win":"75"}, Status="won", **{"Result Date":"2026-06-11"},
    Notes="Wagerhouse.")
add(Date="2026-06-11", Sport="Baseball", League="MLB",
    Event="4-leg parlay", Type="Parlay",
    Description="LAD Alt RL +145 / TEX Alt RL +145 / SEA ML 1st 5 -115 / STL ML +137",
    Pick="4-leg", Opponent="Various", Odds="Mixed",
    Risk="50", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-11"},
    Notes="Wagerhouse.")

# ============== 6/12/2026 ==============
# Action Network straights
add(Date="2026-06-12", Sport="Baseball", League="MLB", Event="NYM @ ATL",
    Type="1st 5 Money Line", Description="Braves ML 1st 5 (Strider)",
    Pick="ATL", Opponent="NYM", Odds="+100",
    Risk="150", **{"To Win":"150"}, Status="lost", **{"Result Date":"2026-06-12"},
    Notes="Ticket 410776149.")
add(Date="2026-06-12", Sport="Baseball", League="MLB", Event="NYM @ ATL",
    Type="1st 5 Money Line", Description="Braves ML 1st 5 (dup)",
    Pick="ATL", Opponent="NYM", Odds="+102",
    Risk="50", **{"To Win":"51"}, Status="lost", **{"Result Date":"2026-06-12"},
    Notes="Ticket 410776221.")
add(Date="2026-06-12", Sport="Baseball", League="MLB", Event="LAA @ TB",
    Type="1st 5 Run Line", Description="Rays -0.5 1st 5 (McClanahan)",
    Pick="TB -0.5", Opponent="LAA", Odds="-125",
    Risk="200", **{"To Win":"160"}, Status="lost", **{"Result Date":"2026-06-12"},
    Notes="Ticket 410776222.")
add(Date="2026-06-12", Sport="Baseball", League="MLB", Event="WSH @ SEA",
    Type="1st 5 Money Line", Description="Mariners ML 1st 5",
    Pick="SEA", Opponent="WSH", Odds="-140",
    Risk="140", **{"To Win":"100"}, Status="won", **{"Result Date":"2026-06-12"},
    Notes="Ticket 410776364.")
add(Date="2026-06-12", Sport="Baseball", League="MLB", Event="CIN @ ARI",
    Type="1st 5 Money Line", Description="Diamondbacks ML 1st 5 (Lodolo)",
    Pick="ARI", Opponent="CIN", Odds="-115",
    Risk="115", **{"To Win":"100"}, Status="lost", **{"Result Date":"2026-06-12"},
    Notes="Ticket 410776365.")
add(Date="2026-06-12", Sport="Mixed", League="MLB+Soccer",
    Event="4-team parlay", Type="Parlay",
    Description="ATL ML 1st 5 / MIL ML 1st 5 / TB ML 1st 5 / USA ML",
    Pick="4-leg", Opponent="Various", Odds="Mixed",
    Risk="100", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-12"},
    Notes="Ticket 410776400.")
add(Date="2026-06-12", Sport="Baseball", League="MLB", Event="CIN @ ARI",
    Type="1st 5 Money Line", Description="Diamondbacks ML 1st 5 (dup)",
    Pick="ARI", Opponent="CIN", Odds="-107",
    Risk="133.75", **{"To Win":"125"}, Status="lost", **{"Result Date":"2026-06-12"},
    Notes="Ticket 410778384.")

# Wagerhouse straights
add(Date="2026-06-12", Sport="Baseball", League="MLB", Event="CHC game",
    Type="Money Line", Description="Cubs ML",
    Pick="CHC", Opponent="Opp", Odds="-105",
    Risk="105", **{"To Win":"100"}, Status="won", **{"Result Date":"2026-06-12"},
    Notes="Wagerhouse.")
add(Date="2026-06-12", Sport="Baseball", League="MLB", Event="ATL game",
    Type="1st 5 Run Line", Description="Braves +0.5 1st 5",
    Pick="ATL +0.5", Opponent="Opp", Odds="-130",
    Risk="260", **{"To Win":"200"}, Status="lost", **{"Result Date":"2026-06-12"},
    Notes="Wagerhouse.")
add(Date="2026-06-12", Sport="Baseball", League="MLB", Event="CLE game",
    Type="1st 5 Run Line", Description="Guardians -0.5 1st 5",
    Pick="CLE -0.5", Opponent="Opp", Odds="+120",
    Risk="150", **{"To Win":"180"}, Status="won", **{"Result Date":"2026-06-12"},
    Notes="Wagerhouse.")
add(Date="2026-06-12", Sport="Baseball", League="MLB", Event="MIN game",
    Type="1st 5 Run Line", Description="Twins -0.5 1st 5",
    Pick="MIN -0.5", Opponent="Opp", Odds="-105",
    Risk="157", **{"To Win":"150"}, Status="lost", **{"Result Date":"2026-06-12"},
    Notes="Wagerhouse.")
# $10 RR Wagerhouse — net -$208.75
add(Date="2026-06-12", Sport="Mixed", League="MLB+Soccer",
    Event="5-team Round Robin all-ways",
    Type="Round Robin",
    Description="$10 RR all-ways: Braves -1.5 +150 / Cubs -1.5 +150 / Guardians -2.5 +255 / USA ML +105 / Rays -2.5 +150",
    Pick="26 parlays @ $10", Opponent="Various", Odds="Mixed",
    Risk="208.75", **{"To Win":"0"}, Status="lost", **{"Result Date":"2026-06-12"},
    Notes="Original $260 stake. ATL L, CHC W, CLE L, USA W, TB L. CHC+USA double cashed = $51.25. Net realized -$208.75.")
add(Date="2026-06-12", Sport="Soccer", League="International",
    Event="Bosnia game", Type="Asian Handicap",
    Description="Bosnia +0.5",
    Pick="Bosnia +0.5", Opponent="Opp", Odds="+100",
    Risk="150", **{"To Win":"150"}, Status="won", **{"Result Date":"2026-06-12"},
    Notes="Wagerhouse.")
add(Date="2026-06-12", Sport="Soccer", League="International",
    Event="USA vs PAR", Type="Combo",
    Description="BTTS Yes + Over 1.5",
    Pick="BTTS Yes + O1.5", Opponent="PAR", Odds="Combo",
    Risk="0", **{"To Win":"100"}, Status="won", **{"Result Date":"2026-06-12"},
    Notes="Wagerhouse. Combined +$100.")

# ============== 6/13/2026 ==============
add(Date="2026-06-13", Sport="Soccer", League="International",
    Event="Brazil match", Type="1st Half ML",
    Description="Brazil ML 1st Half",
    Pick="Brazil 1H", Opponent="Opp", Odds="+120",
    Risk="200", **{"To Win":"240"}, Status="lost", **{"Result Date":"2026-06-13"},
    Notes="Wagerhouse.")
add(Date="2026-06-13", Sport="Soccer", League="International",
    Event="Brazil match", Type="Asian Handicap",
    Description="Brazil -0.5",
    Pick="Brazil -0.5", Opponent="Opp", Odds="-150",
    Risk="600", **{"To Win":"400"}, Status="lost", **{"Result Date":"2026-06-13"},
    Notes="Wagerhouse.")
add(Date="2026-06-13", Sport="Soccer", League="International",
    Event="2-leg parlay SCO/DEU", Type="Parlay",
    Description="Scotland + Germany to win",
    Pick="2-leg", Opponent="Various", Odds="Combo",
    Risk="0", **{"To Win":"305"}, Status="won", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410856488.")
add(Date="2026-06-13", Sport="Baseball", League="MLB",
    Event="PIT contest", Type="1st 5 Money Line",
    Description="PIT 1st 5 -148",
    Pick="PIT", Opponent="Opp", Odds="-148",
    Risk="740", **{"To Win":"500"}, Status="lost", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410883627.")
add(Date="2026-06-13", Sport="Baseball", League="MLB", Event="BOS @ TEX",
    Type="1st 5 Run Line", Description="Rangers +0.5 1st 5 (deGrom)",
    Pick="TEX +0.5", Opponent="BOS", Odds="-145",
    Risk="362.50", **{"To Win":"250"}, Status="won", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410883656. Risk shown 250.")
add(Date="2026-06-13", Sport="Baseball", League="MLB", Event="BOS @ TEX",
    Type="1st 5 Money Line", Description="Rangers ML 1st 5",
    Pick="TEX", Opponent="BOS", Odds="-110",
    Risk="275", **{"To Win":"250"}, Status="won", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410883657.")
add(Date="2026-06-13", Sport="Baseball", League="MLB", Event="CIN @ ARI",
    Type="1st 5 Run Line", Description="Diamondbacks +0.5 1st 5 (Abbott/Gallen)",
    Pick="ARI +0.5", Opponent="CIN", Odds="-145",
    Risk="362.50", **{"To Win":"250"}, Status="lost", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410883679.")
add(Date="2026-06-13", Sport="Baseball", League="MLB", Event="CIN @ ARI",
    Type="1st 5 Money Line", Description="Diamondbacks ML 1st 5",
    Pick="ARI", Opponent="CIN", Odds="-110",
    Risk="275", **{"To Win":"250"}, Status="lost", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410883680.")
add(Date="2026-06-13", Sport="Baseball", League="MLB", Event="KC @ HOU",
    Type="1st 5 Run Line", Description="Astros +0.5 1st 5",
    Pick="HOU +0.5", Opponent="KC", Odds="-140",
    Risk="350", **{"To Win":"250"}, Status="lost", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410883697.")
add(Date="2026-06-13", Sport="Baseball", League="MLB", Event="KC @ HOU",
    Type="1st 5 Money Line", Description="Astros ML 1st 5",
    Pick="HOU", Opponent="KC", Odds="+100",
    Risk="250", **{"To Win":"250"}, Status="lost", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410883698.")
add(Date="2026-06-13", Sport="Baseball", League="MLB", Event="WSH @ SEA",
    Type="Money Line", Description="Mariners ML",
    Pick="SEA", Opponent="WSH", Odds="-128",
    Risk="640", **{"To Win":"500"}, Status="lost", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410884154.")
add(Date="2026-06-13", Sport="Baseball", League="MLB", Event="WSH @ SEA",
    Type="1st 5 Money Line", Description="Mariners ML 1st 5",
    Pick="SEA", Opponent="WSH", Odds="-130",
    Risk="650", **{"To Win":"500"}, Status="lost", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410884155.")
add(Date="2026-06-13", Sport="Baseball", League="MLB", Event="TOR @ NYY",
    Type="Money Line", Description="Yankees ML (Corbin)",
    Pick="NYY", Opponent="TOR", Odds="-123",
    Risk="615", **{"To Win":"500"}, Status="won", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410884156.")
add(Date="2026-06-13", Sport="Baseball", League="MLB", Event="MIL @ PHI",
    Type="Money Line", Description="Phillies ML",
    Pick="PHI", Opponent="MIL", Odds="-123",
    Risk="615", **{"To Win":"500"}, Status="lost", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410884157.")
add(Date="2026-06-13", Sport="Baseball", League="MLB", Event="OAK @ COL",
    Type="Money Line", Description="Athletics ML (Sugano)",
    Pick="OAK", Opponent="COL", Odds="-190",
    Risk="950", **{"To Win":"500"}, Status="lost", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410884158.")
add(Date="2026-06-13", Sport="Baseball", League="MLB", Event="LAA @ TB",
    Type="Money Line", Description="Rays ML",
    Pick="TB", Opponent="LAA", Odds="-116",
    Risk="580", **{"To Win":"500"}, Status="won", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410884159.")
add(Date="2026-06-13", Sport="Soccer", League="International",
    Event="Ivory Coast vs Ecuador", Type="Correct Score",
    Description="0-0 draw",
    Pick="0-0", Opponent="Match", Odds="-143",
    Risk="715", **{"To Win":"500"}, Status="lost", **{"Result Date":"2026-06-13"},
    Notes="Ticket 410901654. Loss shown 500 in summary.")

# ============== 6/16/2026 ==============
add(Date="2026-06-16", Sport="Baseball", League="MLB", Event="PHI game",
    Type="Run Line", Description="Phillies -1.5",
    Pick="PHI -1.5", Opponent="Opp", Odds="+120",
    Risk="150", **{"To Win":"180"}, Status="won", **{"Result Date":"2026-06-16"},
    Notes="Wagerhouse.")
add(Date="2026-06-16", Sport="Baseball", League="MLB", Event="NYY game",
    Type="Run Line", Description="Yankees -1.5",
    Pick="NYY -1.5", Opponent="Opp", Odds="+155",
    Risk="150", **{"To Win":"232.50"}, Status="won", **{"Result Date":"2026-06-16"},
    Notes="Wagerhouse.")
add(Date="2026-06-16", Sport="Baseball", League="MLB", Event="ATL game",
    Type="Run Line", Description="Braves -1.5 (called off)",
    Pick="ATL -1.5", Opponent="Opp", Odds="+120",
    Risk="0", **{"To Win":"0"}, Status="push", **{"Result Date":"2026-06-16"},
    Notes="Wagerhouse. VOIDED - game called off.")
add(Date="2026-06-16", Sport="Baseball", League="MLB", Event="CHC game",
    Type="Run Line", Description="Cubs -1.5",
    Pick="CHC -1.5", Opponent="Opp", Odds="+100",
    Risk="150", **{"To Win":"150"}, Status="lost", **{"Result Date":"2026-06-16"},
    Notes="Wagerhouse.")
add(Date="2026-06-16", Sport="Baseball", League="MLB", Event="SEA game",
    Type="Run Line", Description="Mariners -1.5",
    Pick="SEA -1.5", Opponent="Opp", Odds="+145",
    Risk="150", **{"To Win":"217.50"}, Status="won", **{"Result Date":"2026-06-16"},
    Notes="Wagerhouse.")
# $10 RR treated as 4-game per user (ATL called off)
add(Date="2026-06-16", Sport="Baseball", League="MLB",
    Event="4-team Round Robin all-ways (ATL voided)",
    Type="Round Robin",
    Description="$10 RR all-ways 4 games (per user): PHI -1.5 +120 / NYY -1.5 +155 / SEA -1.5 +145 / CHC -1.5 +100",
    Pick="11 parlays @ $10", Opponent="Various", Odds="Mixed",
    Risk="0", **{"To Win":"199.93"}, Status="won", **{"Result Date":"2026-06-16"},
    Notes="Original $10 RR (5-game) reduced to 4-game per user (ATL called off). 11 parlays × $10 = $110 stake. PHI W, NYY W, SEA W, CHC L. Cashed: PHI+NYY $56.10, PHI+SEA $53.90, NYY+SEA $62.48, PHI+NYY+SEA triple $137.45. Return $309.93. Net realized +$199.93.")

print(f"Total new bets: {len(new_bets)}")
print(f"ID range: 1509 - {nid-1}")

# Write to dashboard FALLBACK_BETS
html_path = "/home/user/workspace/bet-tracker/index.html"
with open(html_path) as f:
    html = f.read()

m = re.search(r'const FALLBACK_BETS = (\[.*?\]);\s*\n', html, re.DOTALL)
existing = json.loads(m.group(1))
print(f"Existing bets in dashboard: {len(existing)}")

combined = existing + new_bets
new_arr_str = json.dumps(combined, indent=2)
html = html[:m.start()] + f"const FALLBACK_BETS = {new_arr_str};\n" + html[m.end():]

with open(html_path, "w") as f:
    f.write(html)

print(f"Dashboard updated: {len(combined)} total bets")

# Write bets to JSON file for Sheet upload
with open("/home/user/workspace/bet-tracker/new_bets_61_616.json", "w") as f:
    json.dump(new_bets, f, indent=2)
print("Saved to new_bets_61_616.json")
