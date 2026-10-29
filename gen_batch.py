#!/usr/bin/env python3
"""Generate parsed bets (IDs 2030+) for the 9/25-10/18 catch-up batches."""
import json, itertools

def dec(am):
    am = int(am)
    return 1 + (am/100 if am > 0 else 100/(-am))

def prod(legs):
    p = 1.0
    for l in legs: p *= dec(l)
    return p

def amer(p):
    if p >= 2:
        return f"+{round(100 * (p - 1))}"
    return str(round(-100 / (p - 1)))

B = []  # bets in schema form

def bet(date, sport, league, event, type_, desc, pick, opp, odds, risk, towin, status, rdate, notes, legs=None):
    if legs and towin is None:
        p = prod(legs)
        towin = round(float(risk) * (p - 1), 2)
        if not odds: odds = amer(p)
    B.append({"ID": "", "Date": date, "Sport": sport, "League": league, "Event": event,
              "Type": type_, "Description": desc, "Pick": pick, "Opponent": opp, "Odds": odds,
              "Risk": risk, "To Win": ("" if towin is None else towin), "Status": status,
              "Result Date": rdate, "Notes": notes})

WH = "Wagerhouse"

# ---------------- BATCH 1: 9/25-9/28 ----------------
bet("2026-09-25","Football","NCAAF","Indiana vs Northwestern (1st Half)","spread",
    "1st Half: Indiana -9.5 -119","Indiana","Northwestern","-119","2380","2000","won","2026-09-25",
    f"{WH} ticket #G313843932; 9/25 activity: 1 wager, +$2,000; risk derived from -119 odds and +$2,000 profit (2380 to win 2000)")

bet("2026-09-26","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Clemson -1 -110 + Louisville ML -575","Clemson -1, Louisville ML","","",  "300",None,"lost","2026-09-26",
    f"{WH}; 9/26 activity, net -$300; Clemson -1 leg won, Louisville ML leg lost; to-win computed from leg odds; no ticket number shown",["-110","-575"])

# RR 9/26: logged as 26 combo rows below (all lost) - no separate summary row

# RR combos 9/26 (all lost)
rr1_legs = [("Old Dominion ML +205","+205",False),("Iowa St ML +260","+260",False),
            ("West Virginia ML -130","-130",False),("Maryland ML +125","+125",False),
            ("Washington St ML +335","+335",False)]
for k in (2,3,4,5):
    for combo in itertools.combinations(rr1_legs, k):
        names = " + ".join(c[0] for c in combo)
        bet("2026-09-26","Football","NCAAF","CFB 5-team round robin","parlay",
            f"RR {k}-way: {names}", ", ".join(c[0].split(' ML')[0] for c in combo), "","",
            "10",None,"lost","2026-09-26",
            f"{WH}; combo of 9/26 5-team RR (all legs lost; $10/combo)",[c[1] for c in combo])

bet("2026-09-26","Football","NCAAF","CFB parlay","parlay",
    "3-team parlay: Oregon ML -175 + Alabama ML -525 + Washington ML -425","Oregon ML, Alabama ML, Washington ML","","",
    "500",None,"lost","2026-09-26",
    f"{WH}; 9/26 activity, net -$500; Oregon and Alabama legs won, Washington ML leg lost; to-win computed from leg odds; no ticket number shown",["-175","-525","-425"])

bet("2026-09-26","Football","NCAAF","Michigan vs Iowa / Florida vs Mississippi","parlay",
    "2-leg parlay: Michigan -378 (vs Iowa) + Mississippi +11.5 -135 (vs Florida)","Michigan ML, Mississippi +11.5","","",
    "500","600.63","lost","2026-09-26",
    f"{WH} ticket #G313982817; 9/26 activity, net -$500; to-win computed from leg odds; losing leg not identified on slip")

bet("2026-09-26","Football","NCAAF","USC vs Oregon","spread",
    "Oregon -3.5 -101","Oregon","USC","-101","1010","1000","won","2026-09-26",
    f"{WH} ticket #G314069977; 9/26 activity, net +$1,000; risk derived from -101 odds and +$1,000 profit")

bet("2026-09-26","Multi","NFL/NCAAF","CFB 2H + NFL parlay","parlay",
    "3-team parlay: USC +0.5 2H -110 + 49ers ML -375 + Chiefs ML -700","USC 2H +0.5, 49ers ML, Chiefs ML","","",
    "1000",None,"lost","2026-09-26",
    f"{WH}; 9/26 activity, net -$1,000; USC +0.5 2H leg lost, 49ers and Chiefs legs won; to-win computed from leg odds; no ticket number shown",["-110","-375","-700"])

bet("2026-09-26","Baseball","MLB","San Diego Padres vs Arizona Diamondbacks","run line",
    "Diamondbacks +2 -139 (run line)","Arizona Diamondbacks","San Diego Padres","-139","250","179.86","lost","2026-09-26",
    f"{WH} ticket #G314085961; 9/26 activity, net -$250; to-win computed from -139 odds")

bet("2026-09-26","Baseball","MLB","San Diego Padres vs Arizona Diamondbacks","moneyline",
    "Diamondbacks ML +300","Arizona Diamondbacks","San Diego Padres","+300","200","600","lost","2026-09-26",
    f"{WH} ticket #G314086136; 9/26 activity, net -$200")

# Huskies bets (game Sat 9/26, appeared in 9/27 activity view)
bet("2026-09-26","Football","NCAAF","Minnesota at Washington (Huskies)","moneyline",
    "Washington (Huskies) ML -110","Washington","Minnesota","-110","2200","2000","lost","2026-09-26",
    f"{WH} ticket #G314117725; net -$2,200; risk derived from -110 odds and $2,000 to-win; shown in 9/27 activity view but game was Sat 9/26 (Minnesota at Washington); placement date approx game day")

bet("2026-09-26","Football","NCAAF","Minnesota at Washington (Huskies)","spread",
    "Washington (Huskies) +1.5 -123","Washington","Minnesota","-123","2460","2000","lost","2026-09-26",
    f"{WH} ticket #G314117808; net -$2,460; risk derived from -123 odds and $2,000 to-win; shown in 9/27 activity view but game was Sat 9/26; placement date approx game day")

bet("2026-09-27","Football","NFL","NFL 4-team parlay","parlay",
    "4-team parlay: Seahawks ML -400 + Chiefs ML -700 + Bills ML -350 + 49ers ML -375",
    "Seahawks ML, Chiefs ML, Bills ML, 49ers ML","","",
    "1888",None,"lost","2026-09-27",
    f"{WH}; 9/27 activity, net -$1,888; Seahawks ML leg lost, other three legs won; to-win computed from leg odds; no ticket number shown",["-400","-700","-350","-375"])

bet("2026-09-27","Football","NFL","Chiefs vs Dolphins","moneyline",
    "Chiefs ML -700","Kansas City Chiefs","Miami Dolphins","-700","14672","2096","won","2026-09-27",
    f"{WH}; 9/27 activity, net +$2,096; risk derived from -700 odds and +$2,096 profit (14,672 to win 2,096) - verify stake; no ticket number shown")

bet("2026-09-27","Football","NFL","NFL 2-team teaser","parlay",
    "2-team 6-pt teaser: Buccaneers +7 + Broncos +7.5","Buccaneers +7, Broncos +7.5","","",
    "","","push","2026-09-27",
    f"{WH}; 9/27 activity, result $0 (push); Buccaneers line partially cropped on slip (read as +7); stake not shown on slip - left blank pending user confirmation; Broncos leg won")

bet("2026-09-27","Football","NFL","Saints vs Raiders","spread",
    "Saints -3.5 -110","New Orleans Saints","Las Vegas Raiders","-110","2200","2000","lost","2026-09-27",
    f"{WH}; 9/27 activity, net -$2,200; risk derived from -110 odds and $2,000 to-win; opponent inferred from same-day Raiders bet (NO vs LV); no ticket number shown")

bet("2026-09-27","Football","NFL","Saints vs Raiders","moneyline",
    "Raiders ML -625","Las Vegas Raiders","New Orleans Saints","-625","12500","2000","won","2026-09-27",
    f"{WH} ticket #G314302355; 9/27 activity, net +$2,000; risk derived from -625 odds and +$2,000 profit (12,500 to win 2,000) - verify stake")

bet("2026-09-27","Football","NFL","Titans vs Giants / Chiefs vs Dolphins","parlay",
    "2-leg parlay: Titans-Giants Under 40 -136 + Chiefs ML -649","Under 40, Chiefs ML","","",
    "300","300","won","2026-09-27",
    f"{WH} ticket #G12206939; 9/27 activity, net +$300; stake not printed - logged $300 risk / $300 win (combined odds +103, computed to-win 300.80 on $300)")

bet("2026-09-27","Multi","NFL/NCAAF","NFL player props + CFB parlay","parlay",
    "4-leg parlay: Quentin Johnston Over 0.5 TD +280 + AJ Barner Over 0.5 TD +300 + George Kittle Over 0.5 TD +164 + Clemson ML -117",
    "Johnston O0.5 TD, Barner O0.5 TD, Kittle O0.5 TD, Clemson ML","","",
    "65",None,"lost","2026-09-27",
    f"{WH} ticket #G12207231; 9/27 activity, net -$65; to-win computed from leg odds (large combined price); losing legs not identified on slip",["+280","+300","+164","-117"])

bet("2026-09-28","Football","NFL","Bears vs Eagles","spread",
    "Eagles +1.5 -126","Philadelphia Eagles","Chicago Bears","-126","2520","2000","lost","2026-09-28",
    f"{WH} ticket #G314430242; 9/28 activity, net -$2,520; risk derived from -126 odds and $2,000 to-win")

bet("2026-09-28","Football","NFL","Bears vs Eagles","team total",
    "Eagles team total Over 14.5 +139","Philadelphia Eagles Over 14.5","Chicago Bears","+139","2000","2780","lost","2026-09-28",
    f"{WH} ticket #G314445964; 9/28 activity, net -$2,000; to-win computed from +139 odds")

# ---------------- BATCH 2: 10/2-10/5 ----------------
bet("2026-10-02","Football","NCAAF","Liberty vs Delaware / Michigan vs Minnesota","parlay",
    "2-leg parlay: Liberty -20.5 +344 + Michigan -222 (ML)","Liberty -20.5, Michigan ML","","",
    "75",None,"lost","2026-10-03",
    f"{WH} ticket #G12630446; 10/2 activity (placed Fri 10/2), net -$75; legs were Sat 10/3 games; to-win computed from leg odds",["+344","-222"])

bet("2026-10-03","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Liberty -7 -110 + Ohio St ML -650","Liberty -7, Ohio St ML","","",
    "300",None,"won","2026-10-03",
    f"{WH}; 10/3 activity, net +$360; stake not printed - logged $300 risk (derived from combined odds +120); to-win computed from leg odds",["-110","-650"])

bet("2026-10-03","Football","NCAAF","Liberty vs Delaware / Michigan vs Minnesota","parlay",
    "2-leg parlay: Liberty -13.5 +170 + Michigan -222 (ML)","Liberty -13.5, Michigan ML","","",
    "150",None,"lost","2026-10-03",
    f"{WH} ticket #G12630397; 10/3 activity, net -$150; to-win computed from leg odds",["+170","-222"])

bet("2026-10-03","Football","NCAAF","CFB parlay","parlay",
    "3-team parlay: Ohio St -13.5 -130 (B+1) + Miami FL ML -750 + Wisconsin ML -350",
    "Ohio St -13.5, Miami FL ML, Wisconsin ML","","",
    "300",None,"won","2026-10-03",
    f"{WH}; 10/3 activity, net +$473; stake not printed - logged $300 risk (derived); to-win computed from leg odds; (B+1) = bought 1 point as printed",["-130","-750","-350"])

bet("2026-10-03","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: California PK -110 + Ohio St ML -700","California PK, Ohio St ML","","",
    "300",None,"lost","2026-10-03",
    f"{WH}; 10/3 activity, net -$300; California PK leg lost, Ohio St leg won; to-win computed from leg odds",["-110","-700"])

bet("2026-10-03","Football","NCAAF","CFB parlay","parlay",
    "3-team parlay: Texas A&M ML -650 + Missouri +7 -140 (B+1) + Texas Tech ML -650",
    "Texas A&M ML, Missouri +7, Texas Tech ML","","",
    "300",None,"won","2026-10-03",
    f"{WH}; 10/3 activity, net +$384; stake not printed - logged $300 risk (derived); to-win computed from leg odds",["-650","-140","-650"])

# RR 10/3 (winners: NC State, Georgia St)
rr2_legs = [("California PK -110","-110",False),("Washington St ML -125","-125",False),
            ("Washington ML +255","+255",False),("NC State ML +140","+140",True),
            ("Georgia St ML -135","-135",True)]
for k in (2,3,4,5):
    for combo in itertools.combinations(rr2_legs, k):
        names = " + ".join(c[0] for c in combo)
        won = all(c[2] for c in combo)
        bet("2026-10-03","Football","NCAAF","CFB 5-team round robin","parlay",
            f"RR {k}-way: {names}", ", ".join(c[0].split(' ML')[0].replace(' PK','') for c in combo), "","",
            "10",None,("won" if won else "lost"),"2026-10-03",
            f"{WH}; combo of 10/3 5-team RR ($10/combo); winners: NC State ML, Georgia St ML", [c[1] for c in combo])

bet("2026-10-03","Football","NCAAF","Colorado vs Texas Tech","moneyline",
    "Texas Tech ML -232","Texas Tech","Colorado","-232","4640","2000","won","2026-10-03",
    f"{WH} ticket #G315115915; 10/3 activity, net +$2,000; risk derived from -232 odds and +$2,000 profit (4,640 to win 2,000) - verify stake")

bet("2026-10-03","Multi","NFL/NCAAF","CFB + NFL parlay","parlay",
    "2-team parlay: BYU ML -225 + Buccaneers +3.5 -110","BYU ML, Buccaneers +3.5","","",
    "300",None,"won","2026-10-04",
    f"{WH}; shown in 10/4 activity (graded with Sunday Bucs leg); BYU leg was Sat 10/3 (at TCU); stake not printed - logged $300 risk (derived); to-win computed from leg odds",["-225","-110"])

bet("2026-10-04","Football","NFL","NFL parlay","parlay",
    "2-team parlay: Raiders +4.5 -110 + Vikings ML -650","Raiders +4.5, Vikings ML","","",
    "300",None,"won","2026-10-04",
    f"{WH}; 10/4 activity, net +$360; stake not printed - logged $300 risk (derived); to-win computed from leg odds",["-110","-650"])

bet("2026-10-04","Football","NFL","NFL parlay","parlay",
    "2-team parlay: 49ers -1.5 -105 (1H) + Ravens ML -700","49ers 1H -1.5, Ravens ML","","",
    "300",None,"lost","2026-10-04",
    f"{WH}; 10/4 activity, net -$300; 49ers 1H leg lost, Ravens leg won; to-win computed from leg odds",["-105","-700"])

bet("2026-10-04","Football","NFL","NFL 5-team free play parlay","parlay",
    "5-team parlay [FP]: Jaguars ML +125 + Seahawks ML -350 + Rams ML -190 + Raiders +4.5 -110 + Bears ML -190",
    "Jaguars ML, Seahawks ML, Rams ML, Raiders +4.5, Bears ML","","",
    "0","1886","won","2026-10-04",
    f"{WH} Free Play (FP) bonus wager - no cash stake; pays to-win only; all legs won; net +$1,886 as shown on slip",["+125","-350","-190","-110","-190"])

bet("2026-10-04","Football","NFL","NFL 5-team free play parlay","parlay",
    "5-team parlay [FP]: Jaguars ML +125 + Rams ML -190 + Seahawks ML -350 + Bears ML -190 + Chiefs ML -215",
    "Jaguars ML, Rams ML, Seahawks ML, Bears ML, Chiefs ML","","",
    "0","1410","won","2026-10-04",
    f"{WH} Free Play (FP) bonus wager - no cash stake; pays to-win only; all legs won; net +$1,410 as shown on slip",["+125","-190","-350","-190","-215"])

bet("2026-10-04","Football","NFL","NFL 2-team teaser","parlay",
    "2-team 6-pt teaser: Broncos +9 + Falcons +8","Broncos +9, Falcons +8","","",
    "330","300","lost","2026-10-04",
    f"{WH}; 10/4 activity, net -$330; Broncos +9 leg lost, Falcons +8 leg won; teaser price not shown - to-win assumes -110 (330 to win 300); verify")

bet("2026-10-04","Football","NFL","NFL 8-leg parlay","parlay",
    "8-leg parlay: Lions team total Over 27.5 -122 + Darnold Over 1.5 pass TD -140 + Hubbard Over 1.5 TD +450 + Barner Over 0.5 TD +264 + Gibbs Over 1.5 TD +140 + Seahawks ML -361 + Ravens ML -752 + Vikings ML -559",
    "Lions TT O27.5, Darnold O1.5 TD, Hubbard O1.5 TD, Barner O0.5 TD, Gibbs O1.5 TD, Seahawks ML, Ravens ML, Vikings ML","","",
    "50",None,"lost","2026-10-04",
    f"{WH} ticket #G12759691; 10/4 activity, net -$50; to-win computed from leg odds",["-122","-140","+450","+264","+140","-361","-752","-559"])

bet("2026-10-04","Football","NFL","NFL 6-leg props parlay","parlay",
    "6-leg parlay: Jaxon Smith-Njigba Over 1.5 TD +474 + AJ Barner Over 0.5 TD +264 + Sam Darnold Over 4.5 rush yds -111 + Darnold Over 249.5 pass yds +130 + Justin Herbert Over 14.5 rush yds -222 + Barner Over 2.5 receptions -182","JSN O1.5 TD, Barner O0.5 TD, Darnold rush O4.5, Darnold pass O249.5, Herbert rush O14.5, Barner rec O2.5","","",
    "50",None,"lost","2026-10-04",
    f"{WH} ticket #G12764884; 10/4 activity, net -$50; to-win computed from leg odds; legs: JSN O1.5 TD +474, Barner O0.5 TD +264, Darnold rush O4.5 -111, Darnold pass yds O249.5 +130, Herbert rush O14.5 -222, Barner receptions O2.5 -182",["+474","+264","-111","+130","-222","-182"])

bet("2026-10-04","Football","NFL","NFL 3-team parlay","parlay",
    "3-team parlay: Rams -6.5 -120 (2H) + Seahawks ML -360 + Vikings ML -600",
    "Rams 2H -6.5, Seahawks ML, Vikings ML","","",
    "300",None,"won","2026-10-04",
    f"{WH}; 10/4 activity, net +$519; stake not printed - logged $300 risk (derived); to-win computed from leg odds",["-120","-360","-600"])

bet("2026-10-04","Football","NFL","Vikings vs Dolphins / Chargers vs Seahawks","parlay",
    "2-leg parlay: Vikings ML -636 + Chargers +3.5 +216","Vikings ML, Chargers +3.5","","",
    "750",None,"lost","2026-10-04",
    f"{WH} ticket #G315293348; 10/4 activity, net -$750; to-win computed from leg odds",["-636","+216"])

# RR 10/4 (all underdog MLs; user confirmed 26-combo all-ways at $15/combo)
rr4_legs = [("Panthers ML +165","+165",True),("Raiders ML +180","+180",False),
            ("Eagles ML +150","+150",False),("Falcons ML +120","+120",True),
            ("Buccaneers ML +155","+155",False)]
for k in (2,3,4,5):
    for combo in itertools.combinations(rr4_legs, k):
        names = " + ".join(c[0] for c in combo)
        won = all(c[2] for c in combo)
        bet("2026-10-04","Football","NFL","NFL 5-team round robin","parlay",
            f"RR {k}-way: {names}", ", ".join(c[0].split(' ML')[0] for c in combo), "","",
            "15",None,("won" if won else "lost"),"2026-10-04",
            f"{WH}; combo of 10/4 5-team RR ($15/combo); winners: Panthers ML, Falcons ML; activity card showed the 5-leg combo (-$15) and the winning 2-team combo (+$72, shown in 10/5 activity)", [c[1] for c in combo])

bet("2026-10-04","Football","NFL","NFL 5-team free play parlay","parlay",
    "5-team parlay [FP]: Cowboys ML +140 + Jaguars ML +125 + 49ers ML -145 + Seahawks ML -350 + Saints ML -135",
    "Cowboys ML, Jaguars ML, 49ers ML, Seahawks ML, Saints ML","","",
    "0","","lost","2026-10-05",
    f"{WH} Free Play (FP) - no cash stake; Saints ML leg lost, others won; FP loss = $0 cash impact; FP stake not shown - potential to-win left blank; shown in 10/5 activity",["+140","+125","-145","-350","-135"])

bet("2026-10-04","Football","NFL","NFL 5-team free play parlay","parlay",
    "5-team parlay [FP]: Cowboys ML +140 + Jaguars ML +125 + 49ers ML -145 + Seahawks ML -350 + Falcons ML +115",
    "Cowboys ML, Jaguars ML, 49ers ML, Seahawks ML, Falcons ML","","",
    "0","3633","won","2026-10-05",
    f"{WH} Free Play (FP) - no cash stake; all legs won; net +$3,633 as shown on slip; shown in 10/5 activity",["+140","+125","-145","-350","+115"])

bet("2026-10-05","Football","NFL","Falcons vs Saints (MNF) props parlay","parlay",
    "2-leg parlay: Kyle Pitts 1st Touchdown +1710 + Michael Penix Jr Over 1.5 pass TD +117",
    "Pitts 1st TD, Penix O1.5 TD","","",
    "150",None,"lost","2026-10-05",
    f"{WH} ticket #G12875887; 10/5 activity, net -$150; to-win computed from leg odds",["+1710","+117"])

bet("2026-10-05","Football","NFL","Saints vs Falcons (MNF)","prop",
    "Kyle Pitts Over 1.5 receptions -110","Pitts Over 1.5 rec","","-110","550","500","won","2026-10-05",
    f"{WH} ticket #G315466407; 10/5 activity, net +$500; risk derived from -110 odds and +$500 profit")

bet("2026-10-05","Football","NFL","Saints vs Falcons (MNF)","prop",
    "Kyle Pitts Under 1.5 receptions +160","Pitts Under 1.5 rec","","+160","343","548.80","lost","2026-10-05",
    f"{WH} ticket #G315475900; 10/5 activity, net -$343; to-win computed from +160 odds (548.80)")

bet("2026-10-05","Football","NFL","Saints vs Falcons (MNF)","spread",
    "Saints +10.5 -113","New Orleans Saints","Atlanta Falcons","-113","500","442.48","lost","2026-10-05",
    f"{WH} ticket #G315480858; 10/5 activity, net -$500; to-win computed from -113 odds (442.48)")

# ---------------- BATCH 3: 10/8-10/11 ----------------
bet("2026-10-08","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Troy -10 +100 + Liberty ML -575","Troy -10, Liberty ML","","",
    "106.83","144","won","2026-10-08",
    f"{WH}; 10/8 activity, net +$144; stake not printed - risk derived from combined odds (+135) and +$144 net (106.83); Liberty hosted Sam Houston Thu 10/8; Troy opponent not shown on slip",["+100","-575"])

bet("2026-10-08","Multi","NFL/NCAAF","CFB + NFL 11-leg parlay","parlay",
    "11-leg parlay: Cowboys -470 + Bengals -332 + Texans -386 + Lions -245 + McBride O0.5 TD +124 + Ollie Gordon II O0.5 TD +150 + Gibbs O1.5 TD +120 + Boise State -247 + Oregon State -708 + Oregon -448 + BYU -420",
    "Cowboys, Bengals, Texans, Lions, McBride, Gordon, Gibbs, Boise State, Oregon State, Oregon, BYU","","",
    "50",None,"lost","2026-10-11",
    f"{WH} ticket #G12977443; 10/8 activity (placed Thu 10/8), net -$50; legs span Sat/Sun games, graded Sun 10/11; to-win computed from leg odds",["-470","-332","-386","-245","+124","+150","+120","-247","-708","-448","-420"])

bet("2026-10-08","Multi","NFL/NCAAF","CFB + NFL parlay","parlay",
    "3-team parlay: Liberty ML -575 + Cowboys ML -525 + UNLV +3.5 -135 (B+1/2)",
    "Liberty ML, Cowboys ML, UNLV +3.5","","",
    "300",None,"lost","2026-10-11",
    f"{WH}; 10/8 activity (placed Thu 10/8), net -$300; Liberty and UNLV legs won, Cowboys ML leg lost; graded Sun 10/11; to-win computed from leg odds",["-575","-525","-135"])

# 10/10 Saturday (16 wagers, day reconciles to -$1,387.65)
bet("2026-10-10","Football","NCAAF","Iowa State vs BYU / Arizona vs West Virginia","parlay",
    "2-leg parlay: BYU -447 + West Virginia +4.5 -134","BYU ML, WVU +4.5","","",
    "300",None,"lost","2026-10-10",
    f"{WH} ticket #G12862692; 10/10 activity, net -$300; to-win computed from leg odds",["-447","-134"])

bet("2026-10-10","Football","NCAAF","Texas vs Oklahoma / Iowa State vs BYU","parlay",
    "2-leg parlay: Oklahoma +9.5 -122 + BYU -447","Oklahoma +9.5, BYU ML","","",
    "300",None,"won","2026-10-10",
    f"{WH} ticket #G12862765; 10/10 activity, net +$368; stake not printed - logged $300 risk (derived); to-win computed from leg odds",["-122","-447"])

bet("2026-10-10","Multi","NCAAF/NFL","Duke vs Georgia Tech / Falcons vs Saints","parlay",
    "2-leg parlay: Georgia Tech +7 -110 + Michael Penix Jr Over 199.5 pass yds -221",
    "Georgia Tech +7, Penix O199.5","","",
    "300",None,"won","2026-10-10",
    f"{WH} ticket #G12863108; 10/10 activity, net +$531; stake not printed - logged $300 risk (derived); to-win computed from leg odds; placement date unknown - logged as settlement date 10/10 (approx)",["-110","-221"])

bet("2026-10-10","Multi","NCAAF/NFL","Nevada vs UTEP / Texans vs Titans","parlay",
    "2-leg parlay: UTEP +10 -118 + Texans ML -325","UTEP +10, Texans ML","","",
    "300",None,"lost","2026-10-10",
    f"{WH} ticket #G12863370; 10/10 activity, net -$300; to-win computed from leg odds; Texans leg from Sun 10/11 game",["-118","-325"])

bet("2026-10-10","Football","NCAAF","UCLA vs Oregon / Air Force vs Northern Illinois","parlay",
    "2-leg parlay: Oregon -471 + Northern Illinois +11.5 -136","Oregon ML, NIU +11.5","","",
    "300",None,"lost","2026-10-10",
    f"{WH} ticket #G12863499; 10/10 activity, net -$300; to-win computed from leg odds",["-471","-136"])

bet("2026-10-10","Football","NCAAF","James Madison vs Georgia Southern / Iowa State vs BYU","parlay",
    "2-leg parlay: Georgia Southern +9 -122 + BYU -428","Georgia Southern +9, BYU ML","","",
    "300",None,"won","2026-10-10",
    f"{WH} ticket #G12863582; 10/10 activity, net +$373; stake not printed - logged $300 risk (derived); to-win computed from leg odds",["-122","-428"])

bet("2026-10-10","Football","NCAAF","Minnesota vs Purdue / UCLA vs Oregon","parlay",
    "2-leg parlay: Purdue +3.5 -146 + Oregon -471","Purdue +3.5, Oregon ML","","",
    "300",None,"lost","2026-10-10",
    f"{WH} ticket #G12863820; 10/10 activity, net -$300; to-win computed from leg odds",["-146","-471"])

bet("2026-10-10","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: BYU ML -425 + Penn St ML -125","BYU ML, Penn St ML","","",
    "300",None,"lost","2026-10-10",
    f"{WH}; 10/10 activity, net -$300; BYU leg won, Penn St leg lost; to-win computed from leg odds",["-425","-125"])

bet("2026-10-10","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Indiana -6.5 -130 (B+1/2) + Iowa +3.5 -110","Indiana -6.5, Iowa +3.5","","",
    "300",None,"lost","2026-10-10",
    f"{WH}; 10/10 activity, net -$300; Indiana leg lost, Iowa leg won; to-win computed from leg odds",["-130","-110"])

bet("2026-10-10","Football","NCAAF","CFB 5-leg totals parlay","parlay",
    "5-leg totals parlay: Ole Miss-Vandy U56 -114 + Duke-GT U44.5 -120 + Indiana-Nebraska U48.5 -111 + UAB-Memphis U52.5 -110 + LSU-Kentucky U54.5 -144",
    "U56, U44.5, U48.5, U52.5, U54.5","","",
    "427",None,"lost","2026-10-10",
    f"{WH} ticket #G12995050; 10/10 activity, net -$427; to-win computed from leg odds",["-114","-120","-111","-110","-144"])

bet("2026-10-10","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Ball St +35 -110 + Liberty ML -575","Ball St +35, Liberty ML","","",
    "300",None,"won","2026-10-10",
    f"{WH}; 10/10 activity, net +$372; stake not printed - logged $300 risk (derived); to-win computed from leg odds",["-110","-575"])

bet("2026-10-10","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: North Carolina +4.5 -130 (B+1) + Indiana ML -325","UNC +4.5, Indiana ML","","",
    "300",None,"won","2026-10-10",
    f"{WH}; 10/10 activity, net +$394; stake not printed - logged $300 risk (derived); to-win computed from leg odds",["-130","-325"])

bet("2026-10-10","Multi","NCAAF/NFL","UCLA vs Oregon / Texas A&M vs Missouri / Texans vs Titans","parlay",
    "3-leg parlay: Oregon -419 + Texas A&M +5 -134 + Texans -370","Oregon ML, A&M +5, Texans ML","","",
    "300",None,"lost","2026-10-10",
    f"{WH} ticket #G13087779; 10/10 activity, net -$300; to-win computed from leg odds; Texans leg from Sun 10/11 game",["-419","-134","-370"])

bet("2026-10-10","Football","NCAAF","San Diego State vs Oregon State / UL Lafayette vs Louisiana Tech","parlay",
    "2-leg parlay: Oregon State -776 + Louisiana Tech -3 -111","Oregon State ML, La Tech -3","","",
    "300",None,"lost","2026-10-10",
    f"{WH} ticket #G13087805; 10/10 activity, net -$300; to-win computed from leg odds",["-776","-111"])

bet("2026-10-10","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Oregon -10 -110 + Oregon St ML -850","Oregon -10, Oregon St ML","","",
    "300",None,"lost","2026-10-10",
    f"{WH}; 10/10 activity, net -$300; Oregon -10 leg lost, Oregon St leg won; to-win computed from leg odds",["-110","-850"])

bet("2026-10-10","Football","NCAAF","Air Force vs Northern Illinois / Boise State vs Fresno State","parlay",
    "2-leg parlay: Northern Illinois +11.5 -192 + Boise State -313","NIU +11.5, Boise State ML","","",
    "300",None,"lost","2026-10-10",
    f"{WH} ticket #G13134957; 10/10 activity, net -$300; to-win computed from leg odds",["-192","-313"])

# RR 10/11 (all underdog MLs; user confirmed 26-combo all-ways at $15/combo)
rr6_legs = [("Eagles ML +305","+305",False),("Colts ML +125","+125",False),
            ("Packers ML +130","+130",True),("Chargers ML +160","+160",False),
            ("Ravens ML +155","+155",True)]
for k in (2,3,4,5):
    for combo in itertools.combinations(rr6_legs, k):
        names = " + ".join(c[0] for c in combo)
        won = all(c[2] for c in combo)
        bet("2026-10-11","Football","NFL","NFL 5-team round robin","parlay",
            f"RR {k}-way: {names}", ", ".join(c[0].split(' ML')[0] for c in combo), "","",
            "15",None,("won" if won else "lost"),"2026-10-11",
            f"{WH}; combo of 10/11 5-team RR ($15/combo); winners: Packers ML, Ravens ML; activity card showed the 5-leg combo (-$15)", [c[1] for c in combo])

bet("2026-10-11","Football","NFL","NFL parlay","parlay",
    "2-team parlay: Eagles +7.5 -110 + Texans ML -400","Eagles +7.5, Texans ML","","",
    "300",None,"won","2026-10-11",
    f"{WH}; 10/11 activity, net +$415; stake not printed - logged $300 risk (derived); to-win computed from leg odds",["-110","-400"])

bet("2026-10-10","Multi","NCAAF/NFL","North Dakota State vs UNLV / Texans vs Titans","parlay",
    "2-leg parlay: UNLV +3.5 -122 + Texans -400","UNLV +3.5, Texans ML","","",
    "300",None,"won","2026-10-11",
    f"{WH} ticket #G13064031; shown in 10/11 activity (graded with Sun Texans leg); UNLV leg was Sat 10/10; stake not printed - logged $300 risk (derived); to-win computed from leg odds",["-122","-400"])

bet("2026-10-10","Football","NCAAF","Georgia vs Alabama / Boise State vs Fresno State","parlay",
    "2-leg parlay: Georgia-Alabama Under 55.5 -174 + Boise State -265","U55.5, Boise State ML","","",
    "300",None,"won","2026-10-11",
    f"{WH} ticket #G13087813; shown in 10/11 activity (settled Sun); both legs Sat 10/10 games; stake not printed - logged $300 risk (derived); to-win computed from leg odds",["-174","-265"])

bet("2026-10-10","Football","NCAAF","Minnesota vs Purdue / Boise State vs Fresno State","parlay",
    "2-leg parlay: Purdue +3.5 -136 + Boise State -313","Purdue +3.5, Boise State ML","","",
    "300",None,"won","2026-10-11",
    f"{WH} ticket #G13134868; shown in 10/11 activity (settled Sun); both legs Sat 10/10 games; stake not printed - logged $300 risk (derived); to-win computed from leg odds",["-136","-313"])

bet("2026-10-11","Football","NFL","Seahawks vs 49ers / Cardinals vs Lions","parlay",
    "2-leg parlay: Seahawks team total Under 26.5 -117 + Lions ML -200","Seahawks TT U26.5, Lions ML","","",
    "50",None,"lost","2026-10-11",
    f"{WH} ticket #G316392237; 10/11 activity, net -$50; to-win computed from leg odds",["-117","-200"])

# ---------------- BATCH 4: 10/17-10/18 ----------------
bet("2026-10-17","Multi","NCAAF/NFL","CFB + NFL parlay","parlay",
    "3-team parlay: VA Tech ML -350 + Oklahoma ML -250 + 49ers ML -400",
    "VA Tech ML, Oklahoma ML, 49ers ML","","",
    "300",None,"lost","2026-10-18",
    f"{WH}; 10/17 activity, net -$300; VA Tech and 49ers legs won, Oklahoma ML leg lost; 49ers leg was Sun 10/18 game; to-win computed from leg odds",["-350","-250","-400"])

bet("2026-10-17","Football","NCAAF","Tennessee vs Alabama","moneyline",
    "Alabama ML -113","Alabama","Tennessee","-113","300","265.49","lost","2026-10-17",
    f"{WH} ticket #G317253542; 10/17 activity, net -$300; to-win computed from -113 odds (265.49)")

bet("2026-10-17","Football","NCAAF","Notre Dame vs BYU / Washington State vs Oregon State","parlay",
    "5-leg parlay: BYU +320 + Legend Glasker Over 49.5 rec yds +112 + Bear Bachmeier Over 0.5 TD +120 + Bear Bachmeier Over 49.5 rush yds +169 + Oregon State -16.5 -150",
    "BYU ML, Glasker O49.5, Bachmeier O0.5 TD, Bachmeier O49.5 rush, OSU -16.5","","",
    "58",None,"lost","2026-10-17",
    f"{WH} ticket #G13548726; 10/17 activity, net -$58; to-win computed from leg odds",["+320","+112","+120","+169","-150"])

bet("2026-10-17","Football","NCAAF","Nebraska vs Oregon","total",
    "Nebraska/Oregon Under 51 -110","Under 51","","-110","165","150","won","2026-10-17",
    f"{WH}; 10/17 activity, net +$150; risk derived from -110 odds and +$150 profit (165 to win 150)")

bet("2026-10-17","Football","NCAAF","Hawaii vs New Mexico (2H)","spread",
    "New Mexico -7 -120 (2nd Half)","New Mexico","Hawaii","-120","60","50","won","2026-10-17",
    f"{WH}; 10/17 activity, net +$50; risk derived from -120 odds and +$50 profit (60 to win 50); 2H bet")

bet("2026-10-17","Football","NCAAF","Washington vs Purdue / Nebraska vs Oregon","parlay",
    "2-leg parlay: Washington +3.5 -122 + Oregon -252","Washington +3.5, Oregon ML","","",
    "300",None,"won","2026-10-18",
    f"{WH} ticket #G13498314; shown in 10/18 activity (settled Sun); both legs Sat 10/17 games; stake not printed - logged $300 risk (derived); to-win computed from leg odds",["-122","-252"])

# RR 10/18 (winners: Texans, Titans, Washington)
rr4_legs = [("Texans ML +125","+125",True),("Eagles ML +160","+160",False),
            ("Titans ML +255","+255",True),("Raiders ML +195","+195",False),
            ("Washington ML +135","+135",True)]
for k in (2,3,4,5):
    for combo in itertools.combinations(rr4_legs, k):
        names = " + ".join(c[0] for c in combo)
        won = all(c[2] for c in combo)
        bet("2026-10-18","Football","NFL","NFL 5-team round robin","parlay",
            f"RR {k}-way: {names}", ", ".join(c[0].split(' ML')[0] for c in combo), "","",
            "10",None,("won" if won else "lost"),"2026-10-18",
            f"{WH}; combo of 10/18 5-team RR ($10/combo); winners: Texans ML, Titans ML, Washington ML", [c[1] for c in combo])

bet("2026-10-17","Football","NCAAF","Nebraska vs Oregon / Utah vs Colorado","parlay",
    "2-leg parlay: Nebraska-Oregon Under 51.5 -110 + Utah -775","U51.5, Utah ML","","",
    "449.01","519","won","2026-10-18",
    f"{WH} ticket #G13564346; shown in 10/18 activity (settled Sun); both legs Sat 10/17 games; stake not printed - risk derived from combined odds (+116) and +$519 net (449.01) - verify stake; to-win computed from leg odds",["-110","-775"])

bet("2026-10-17","Football","NCAAF","Hawaii vs New Mexico / California vs Wake Forest","parlay",
    "2-leg parlay: New Mexico -658 + Wake Forest -9.5 -127","New Mexico ML, Wake Forest -9.5","","",
    "1000",None,"won","2026-10-18",
    f"{WH} ticket #G317379373; shown in 10/18 activity (settled Sun); both legs Sat 10/17 games; stake not printed - logged $1,000 risk (derived from +$1,059 net and combined odds +106); to-win computed from leg odds",["-658","-127"])

bet("2026-10-17","Multi","NCAAF/NFL","Hawaii vs New Mexico (2H) + NFL parlay","parlay",
    "2-team parlay: New Mexico -7 -120 (2H) + Rams ML -850","New Mexico 2H -7, Rams ML","","",
    "1000",None,"lost","2026-10-18",
    f"{WH}; shown in 10/18 activity, net -$1,000; NM 2H leg won, Rams ML leg lost (Sun 10/18 game); to-win computed from leg odds",["-120","-850"])

# ---------------- BATCH 5: 10/24-10/26 ----------------
bet("2026-10-24","Football","NCAAF","Army vs Tulsa / Houston vs Utah / Pittsburgh vs Miami FL / California vs SMU / Boise State vs Washington State","parlay",
    "5-leg parlay: Tulsa PK -110 + Utah -248 + Miami FL -2.5 -216 (1Q) + SMU -1150 + Boise State -641",
    "Tulsa PK, Utah ML, Miami FL 1Q -2.5, SMU ML, Boise State ML","","",
    "300",None,"lost","2026-10-24",
    f"{WH} ticket #G13959136; 10/24 activity, net -$300; to-win computed from leg odds",["-110","-248","-216","-1150","-641"])

bet("2026-10-24","Football","NCAAF","Army vs Tulsa","moneyline",
    "Tulsa ML -207","Tulsa","Army","-207","2070","1000","lost","2026-10-24",
    f"{WH} ticket #G318270888; 10/24 activity, net -$2,070; risk derived from -207 odds and $1,000 to-win")

bet("2026-10-24","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: S Carolina ML -135 + Alabama ML -600","S Carolina ML, Alabama ML","","",
    "1500",None,"won","2026-10-24",
    f"{WH}; 10/24 activity, net +$1,546; stake not printed - logged $1,500 risk (derived); to-win computed from leg odds",["-135","-600"])

bet("2026-10-24","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Bowling Green +3.5 -135 (B+1/2) + Alabama ML -600","Bowling Green +3.5, Alabama ML","","",
    "1500",None,"lost","2026-10-24",
    f"{WH}; 10/24 activity, net -$1,500; Bowling Green leg lost, Alabama leg won; to-win computed from leg odds",["-135","-600"])

bet("2026-10-24","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: North Texas ML -145 + Alabama ML -600","North Texas ML, Alabama ML","","",
    "1500",None,"won","2026-10-24",
    f"{WH}; 10/24 activity, net +$1,456; stake not printed - logged $1,500 risk (derived); to-win computed from leg odds",["-145","-600"])

bet("2026-10-24","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: UCF +7.5 -110 + Alabama ML -600","UCF +7.5, Alabama ML","","",
    "1500",None,"won","2026-10-24",
    f"{WH}; 10/24 activity, net +$1,840; stake not printed - logged $1,500 risk (derived); to-win computed from leg odds",["-110","-600"])

bet("2026-10-24","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Minnesota +7.5 -110 + Alabama ML -600","Minnesota +7.5, Alabama ML","","",
    "1500",None,"won","2026-10-24",
    f"{WH}; 10/24 activity, net +$1,840; stake not printed - logged $1,500 risk (derived); to-win computed from leg odds",["-110","-600"])

bet("2026-10-24","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Northern Illinois +3.5 -135 (B+1/2) + Alabama ML -600","NIU +3.5, Alabama ML","","",
    "1500",None,"lost","2026-10-24",
    f"{WH}; 10/24 activity, net -$1,500; NIU leg lost, Alabama leg won; to-win computed from leg odds",["-135","-600"])

bet("2026-10-24","Football","NCAAF","CFB parlay","parlay",
    "3-team parlay: Alabama ML -600 + Arizona St +1 -110 + Boise St ML -700",
    "Alabama ML, Arizona St +1, Boise St ML","","",
    "1500",None,"won","2026-10-24",
    f"{WH}; 10/24 activity, net +$2,318; stake not printed - logged $1,500 risk (derived); to-win computed from leg odds (2,313.73; displayed +2,318)",["-600","-110","-700"])

bet("2026-10-24","Football","NCAAF","CFB parlay","parlay",
    "3-team parlay: Alabama ML -600 + Boise St ML -700 + Vanderbilt +11 -120 (B+1/2)",
    "Alabama ML, Boise St ML, Vanderbilt +11","","",
    "1500",None,"lost","2026-10-24",
    f"{WH}; 10/24 activity, net -$1,500; Vanderbilt leg lost, others won; to-win computed from leg odds",["-600","-700","-120"])

bet("2026-10-24","Football","NCAAF","CFB parlay","parlay",
    "3-team parlay: Alabama ML -600 + Boise St ML -700 + Houston +7 -130 (B+1/2)",
    "Alabama ML, Boise St ML, Houston +7","","",
    "1500",None,"lost","2026-10-24",
    f"{WH}; 10/24 activity, net -$1,500; Houston leg lost, others won; to-win computed from leg odds",["-600","-700","-130"])

bet("2026-10-24","Football","NCAAF","CFB parlay","parlay",
    "3-team parlay: Houston Alt Line +14.5 -275 + North Dakota St/New Mexico Under 41.5 -150 (B+2) + Boise St ML -700",
    "Houston +14.5, U41.5, Boise St ML","","",
    "250",None,"won","2026-10-24",
    f"{WH}; 10/24 activity, net +$399; stake not printed - logged $250 risk (derived); to-win computed from leg odds",["-275","-150","-700"])

bet("2026-10-24","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Wisconsin ML +115 + Boise St ML -700","Wisconsin ML, Boise St ML","","",
    "1500",None,"won","2026-10-24",
    f"{WH}; 10/24 activity, net +$2,185; stake not printed - logged $1,500 risk (derived); to-win computed from leg odds",["+115","-700"])

bet("2026-10-24","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: VA Tech +3 -110 + Arizona ML -375","VA Tech +3, Arizona ML","","",
    "1500",None,"won","2026-10-24",
    f"{WH}; 10/24 activity, net +$2,127; stake not printed - logged $1,500 risk (derived); to-win computed from leg odds",["-110","-375"])

# RR 10/25 (winners: Falcons, Dolphins)
rr5_legs = [("Cardinals ML +180","+180",False),("Falcons ML +130","+130",True),
            ("Dolphins ML +180","+180",True),("Titans ML +110","+110",False),
            ("Colts ML +225","+225",False)]
for k in (2,3,4,5):
    for combo in itertools.combinations(rr5_legs, k):
        names = " + ".join(c[0] for c in combo)
        won = all(c[2] for c in combo)
        bet("2026-10-25","Football","NFL","NFL 5-team round robin","parlay",
            f"RR {k}-way: {names}", ", ".join(c[0].split(' ML')[0] for c in combo), "","",
            "15",None,("won" if won else "lost"),"2026-10-25",
            f"{WH}; combo of 10/25 5-team RR ($15/combo); winners: Falcons ML, Dolphins ML", [c[1] for c in combo])

bet("2026-10-25","Football","NFL","NFL 3-team teaser","parlay",
    "3-team 6-pt teaser: Titans +7.5 + Chiefs +9 + Cardinals +10.5","Titans +7.5, Chiefs +9, Cardinals +10.5","","",
    "300","","lost","2026-10-25",
    f"{WH}; 10/25 activity, net -$300; Titans leg won, Chiefs and Cardinals legs lost; teaser payout odds not shown on slip - to-win left blank pending user confirmation")

bet("2026-10-25","Football","NCAAF","NDSU vs New Mexico / Texas A&M vs Alabama / Boise State vs Washington State","parlay",
    "3-leg parlay: NDSU-New Mexico Under 41.5 -138 + Alabama -590 + Boise State -646",
    "U41.5, Alabama ML, Boise State ML","","",
    "500",None,"won","2026-10-25",
    f"{WH} ticket #G14005178; 10/25 activity, net +$664; stake not printed - logged $500 risk (derived); to-win computed from leg odds",["-138","-590","-646"])

bet("2026-10-25","Football","NFL","NFL 3-leg TD props parlay","parlay",
    "3-leg parlay: Jonathan Taylor Over 1.5 TD +500 + Kenneth Walker III Over 1.5 TD +500 + Jahmyr Gibbs Over 1.5 TD +144",
    "Taylor O1.5 TD, Walker O1.5 TD, Gibbs O1.5 TD","","",
    "120",None,"lost","2026-10-25",
    f"{WH} ticket #G14059765; 10/25 activity, net -$120; to-win computed from leg odds",["+500","+500","+144"])

bet("2026-10-25","Football","NFL","Falcons vs 49ers / Texans vs Giants","parlay",
    "2-leg parlay: Falcons +3.5 -120 + Texans -479","Falcons +3.5, Texans ML","","",
    "300",None,"lost","2026-10-25",
    f"{WH} ticket #G318575841; 10/25 activity, net -$300; to-win computed from leg odds",["-120","-479"])

bet("2026-10-25","Football","NFL","Titans vs Browns / Vikings vs Colts / Ravens vs Bengals","parlay",
    "3-leg parlay: Titans -399 + Colts +102 + Ravens -133","Titans ML, Colts ML, Ravens ML","","",
    "300",None,"lost","2026-10-25",
    f"{WH} ticket #G318576945; 10/25 activity, net -$300; to-win computed from leg odds",["-399","+102","-133"])

bet("2026-10-25","Football","NFL","Texans vs Giants / Panthers vs Buccaneers / Ravens vs Bengals","parlay",
    "3-leg parlay: Texans -2.5 -163 + Buccaneers -577 + Ravens -232","Texans -2.5, Buccaneers ML, Ravens ML","","",
    "300",None,"lost","2026-10-25",
    f"{WH} ticket #G318593460; 10/25 activity, net -$300; to-win computed from leg odds",["-163","-577","-232"])

bet("2026-10-25","Football","NFL","Seahawks vs Chiefs","spread",
    "Seahawks -3 -110","Seattle Seahawks","Kansas City Chiefs","-110","1650","1500","won","2026-10-25",
    f"{WH}; 10/25 activity, net +$1,500; risk derived from -110 odds and +$1,500 profit (1,650 to win 1,500); no ticket number shown")

# 10/26 Monday
bet("2026-10-26","Football","NFL","Chiefs vs Seahawks 3-leg parlay","parlay",
    "3-leg parlay: Seahawks -155 + George Holani Over 0.5 TD +450 + Kenneth Walker III Over 1.5 TD +450",
    "Seahawks ML, Holani O0.5 TD, Walker O1.5 TD","","",
    "50",None,"lost","2026-10-26",
    f"{WH} ticket #G14148961; 10/26 activity, net -$50; to-win computed from leg odds",["-155","+450","+450"])

bet("2026-10-26","Football","NFL","Chiefs vs Seahawks 4-leg parlay","parlay",
    "4-leg parlay: Seahawks -155 + AJ Barner Over 0.5 TD +240 + Travis Kelce Over 0.5 TD +220 + Kenneth Walker III Over 0.5 TD -136",
    "Seahawks ML, Barner O0.5 TD, Kelce O0.5 TD, Walker O0.5 TD","","",
    "50",None,"lost","2026-10-26",
    f"{WH} ticket #G14149044; 10/26 activity, net -$50; to-win computed from leg odds",["-155","+240","+220","-136"])

bet("2026-10-26","Football","NFL","Cowboys vs Eagles (MNF) prop","prop",
    "Tanner McKee Under 0.5 interceptions +109","McKee U0.5 INT","","+109","250","272.50","lost","2026-10-26",
    f"{WH} ticket #G14189826; 10/26 activity, net -$250; to-win computed from +109 odds")

bet("2026-10-26","Multi","Multi","4-leg cross-sport parlay (NFL/MLB/NBA/NHL)","parlay",
    "4-leg parlay: Cowboys-Eagles Under 44.5 -120 + Rays +0.5 -190 (1st 5) + Kyrie Irving Under 20.5 pts -109 + Kings ML +117",
    "U44.5, Rays F5 +0.5, Kyrie U20.5, Kings ML","","",
    "100",None,"lost","2026-10-26",
    f"{WH} ticket #G14205636; 10/26 activity, net -$100; to-win computed from leg odds",["-120","-190","-109","+117"])

bet("2026-10-26","Multi","Multi","4-leg cross-sport parlay (NFL/MLB/NHL/NBA)","parlay",
    "4-leg parlay: Dameon Pierce Over 17.5 rush yds -113 + Jake Bauers Over 0.5 hits -147 + Zayne Parekh Over 1.5 SOG -111 + Jalen Johnson Over 16.5 reb+ast -106",
    "Pierce O17.5, Bauers O0.5, Parekh O1.5, Johnson O16.5","","",
    "100",None,"lost","2026-10-26",
    f"{WH} ticket #G14206117; 10/26 activity, net -$100; to-win computed from leg odds",["-113","-147","-111","-106"])

bet("2026-10-26","Multi","Multi","4-leg cross-sport parlay (NFL/MLB/NHL/NBA)","parlay",
    "4-leg parlay: Tanner McKee Over 196.5 pass yds -112 + Brewers -103 + Connor McDavid Over 1.5 assists +145 + Cameron Boozer Over 9.5 rebounds +106",
    "McKee O196.5, Brewers ML, McDavid O1.5, Boozer O9.5","","",
    "200",None,"lost","2026-10-26",
    f"{WH} ticket #G14207386; 10/26 activity, net -$200; to-win computed from leg odds",["-112","-103","+145","+106"])

# ---------------- BATCH 6: open bets, week of 10/29 (pending) ----------------
bet("2026-10-29","Multi","NFL/NCAAF","NFL + CFB parlay","parlay",
    "3-team parlay: Lions ML -180 + Ohio St ML -245 + Miami FL ML -650","Lions ML, Ohio St ML, Miami FL ML","","",
    "500","763","pending","",
    f"{WH}; open bet on this week's games (NFL Sun + CFB Sat); stake and to-win as printed on slip; placement date approx (screenshots undated)")

bet("2026-10-29","Football","NCAAF","CFB parlay","parlay",
    "3-team parlay: Ohio St ML -245 + Boise St ML -425 + Oregon St ML -225","Ohio St ML, Boise St ML, Oregon St ML","","",
    "500","756","pending","",
    f"{WH}; open bet on this week's games; stake and to-win as printed on slip")

bet("2026-10-29","Multi","NFL/NCAAF","Seahawks + Washington schools parlay","parlay",
    "3-team parlay: Seahawks ML -170 + Washington St ML +115 + Washington +9 -130 (B+1/2)","Seahawks ML, WSU ML, Washington +9","","",
    "250","1260","pending","",
    f"{WH}; open bet on this week's games; stake and to-win as printed on slip")

bet("2026-10-29","Multi","NFL/NCAAF","Seahawks + Washington schools parlay","parlay",
    "3-team parlay: Seahawks ML -170 + Washington St ML +115 + Washington ML +255","Seahawks ML, WSU ML, Washington ML","","",
    "250","2780","pending","",
    f"{WH}; open bet on this week's games; stake and to-win as printed on slip")

bet("2026-10-29","Football","NFL","NFL 4-team parlay","parlay",
    "4-team parlay: Lions ML -180 + Chiefs ML -120 + Patriots ML -330 + Seahawks ML -170",
    "Lions ML, Chiefs ML, Patriots ML, Seahawks ML","","",
    "400","1960","pending","",
    f"{WH}; open bet on this week's games; stake and to-win as printed on slip")

bet("2026-10-29","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Illinois -2.5 -110 + Michigan ML -700","Illinois -2.5, Michigan ML","","",
    "500","590","pending","",
    f"{WH}; open bet on this week's games; stake and to-win as printed on slip")

bet("2026-10-29","Multi","NFL/NCAAF","NFL + CFB parlay","parlay",
    "2-team parlay: Chiefs ML -120 + Michigan ML -700","Chiefs ML, Michigan ML","","",
    "500","547","pending","",
    f"{WH}; open bet on this week's games; stake and to-win as printed on slip")

bet("2026-10-29","Football","NFL","Panthers vs Packers same-game props parlay","parlay",
    "4-leg same-game parlay: Josh Jacobs Over 0.5 TD -146 + Chuba Hubbard Over 0.5 TD -120 + Jalen Coker Over 59.5 rec yds -124 + Christian Watson Over 4.5 receptions -136",
    "Jacobs O0.5 TD, Hubbard O0.5 TD, Coker O59.5, Watson O4.5 rec","","",
    "143","848","pending","",
    f"{WH} ticket #G14328287; open bet on this week's CAR-GB game; stake and to-win as printed on slip")

bet("2026-10-29","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Colorado +1 -110 + Boise St ML -425","Colorado +1, Boise St ML","","",
    "500","679","pending","",
    f"{WH}; open bet on this week's games; stake and to-win as printed on slip")

bet("2026-10-29","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Maryland ML +115 + Boise St ML -425","Maryland ML, Boise St ML","","",
    "500","827","pending","",
    f"{WH}; open bet on this week's games; stake and to-win as printed on slip")

bet("2026-10-29","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Ohio St -6.5 -130 (B+1/2) + Boise St ML -450","Ohio St -6.5, Boise St ML","","",
    "500","581","pending","",
    f"{WH}; open bet on this week's games; stake and to-win as printed on slip")

bet("2026-10-29","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: North Carolina +15 -110 + Boise St ML -450","North Carolina +15, Boise St ML","","",
    "500","666","pending","",
    f"{WH}; open bet on this week's games; stake and to-win as printed on slip")

bet("2026-10-29","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Florida Intl +14 -110 + Boise St ML -450","FIU +14, Boise St ML","","",
    "500","666","pending","",
    f"{WH}; open bet on this week's games; stake and to-win as printed on slip")

bet("2026-10-29","Football","NCAAF","CFB parlay","parlay",
    "2-team parlay: Indiana -19.5 -110 + Boise St ML -450","Indiana -19.5, Boise St ML","","",
    "500","666","pending","",
    f"{WH}; open bet on this week's games; stake and to-win as printed on slip")

# ---- assign IDs, sanitize, write files ----
STR_FIELDS = ["ID","Date","Sport","League","Event","Type","Description","Pick","Opponent",
              "Odds","Risk","To Win","Status","Result Date","Notes"]
for b in B:
    for k in STR_FIELDS:
        v = b.get(k)
        if v is None: b[k] = ""
        elif not isinstance(v, str):  # floats from computed to-wins
            f = float(v)
            b[k] = str(int(f)) if abs(f - round(f)) < 1e-9 else f"{f:.2f}"

for i, b in enumerate(B):
    b["ID"] = str(2030 + i)

json.dump({"bets": B}, open("parsed_bets.json", "w"), indent=1)
print("total bets:", len(B), "IDs", B[0]["ID"], "-", B[-1]["ID"])

Bp = [dict(b) for b in B]
for b in Bp:
    b["Status"] = "pending"
    b["Result Date"] = ""
json.dump({"bets": Bp}, open("parsed_bets_pending.json", "w"), indent=1)

def fnum(v):
    try: return float(v)
    except (TypeError, ValueError): return None
tot_risk = sum(fnum(b["Risk"]) or 0 for b in B)
settled = [b for b in B if b["Status"] in ("won","lost","push")]
net = sum((fnum(b["To Win"]) or 0) if b["Status"]=="won" else (-(fnum(b["Risk"]) or 0) if b["Status"]=="lost" else 0) for b in settled)
open_risk = sum(fnum(b["Risk"]) or 0 for b in B if b["Status"]=="pending")
from collections import Counter
sc = Counter(b["Status"] for b in B)
print(f"total risk: {tot_risk:,.2f} | settled net: {net:,.2f} | open risk: {open_risk:,.2f}")
print("statuses:", dict(sc))

# ---- confirmation table ----
L = []
L.append(f"# Staged bet additions - IDs {B[0]['ID']}-{B[-1]['ID']} - DRAFT FOR CONFIRMATION (nothing written yet)")
L.append("")
L.append(f"**{len(B)} staged records** | Statuses: {sc.get('won',0)} won, {sc.get('lost',0)} lost, {sc.get('push',0)} push, {sc.get('pending',0)} pending (this week's open bets)")
L.append(f"**Provisional totals (include derived stakes pending your OK; exclude 3 held RR cards):** total risk ${tot_risk:,.2f} | settled net ${net:,.2f} | open risk ${open_risk:,.2f}")
L.append("")
L.append("3 round-robin cards (10/4, 10/5, 10/11) are UNRESOLVED and excluded from the append until you confirm their structure (see Unresolved items). Placement dates are approximations from Wagerhouse activity views (noted per bet). 'To Win' = profit.")
L.append("")
cur_day = None
day_risk = day_net = 0.0
HDR = ["ID","Date","Sport/League","Type","Description","Pick","Odds","Risk","To Win","Status","Result Date","Book/Ticket"]
def table_end():
    L.append(f"| | | | | **{cur_day} totals** | | | **${day_risk:,.2f}** | | **net ${day_net:+,.2f}** | | |")
    L.append("")
for b in B:
    if b["Date"] != cur_day:
        if cur_day: table_end()
        cur_day = b["Date"]; day_risk = day_net = 0.0
        L.append(f"## {cur_day}")
        L.append("")
        L.append("| " + " | ".join(HDR) + " |")
        L.append("|" + "---|" * len(HDR))
    r = fnum(b["Risk"]) or 0
    w = fnum(b["To Win"])
    day_risk += r
    if b["Status"] == "won": day_net += w or 0
    elif b["Status"] == "lost": day_net -= r
    book = "Wagerhouse"
    import re as _re
    m = _re.search(r"#(G?\d+)", b["Notes"])
    tk = (" #" + m.group(1)) if m else ""
    L.append(f"| {b['ID']} | {b['Date']} | {b['Sport']}/{b['League']} | {b['Type']} | {b['Description']} | {b['Pick']} | {b['Odds']} | {b['Risk']} | {b['To Win']} | {b['Status']} | {b['Result Date']} | {book}{tk} |")
table_end()

# ---- held items ----
L.append("## UNRESOLVED ITEMS - excluded from the append until you confirm")
L.append("")
L.append("| Item | What the slips show | Open question |")
L.append("|---|---|---|")
L.append("| 10/4 'Round Robin - 5 Teams' card | Panthers +165 W, Raiders +180 L, Eagles +150 L, Falcons +120 W, Buccaneers +155 L; card result -$15 | If this is a 26-combo all-ways RR at $15/combo (like your verified 9/26 and 10/25 RRs), the -$15 card is just the 5-leg parlay combo and the full RR nets about -$302.55. Confirm structure/stake. |")
L.append("| 10/5 'Round Robin - 2 Teams' card | Panthers +165 W, Falcons +120 W; card result +$72 | Possibly the winning 2-team combo of the 10/4 RR (at $15 it pays +$72.45), not a separately placed wager. Confirm identity and stake. |")
L.append("| 10/11 'Round Robin - 5 Teams' card | Eagles +305 L, Colts +125 L, Packers +130 W, Chargers +160 L, Ravens +155 W; card result -$15 | Same question: 26-combo all-ways at $15/combo would net about -$302.02. Confirm structure/stake. |")
L.append("| 9/27 2-team 6-pt teaser (push) | Bucs +7 / Broncos +7.5, result $0 | Stake not shown - risk left blank. OK? |")
L.append("| 10/25 3-team 6-pt teaser | Titans +7.5 / Chiefs +9 / Cardinals +10.5, risk $300, net -$300 | Payout odds not shown - to-win left blank. OK? |")
L.append("")

# ---- assumptions table ----
L.append("## DERIVED / ASSUMED VALUES - please review (each is also noted in that bet's Notes)")
L.append("")
L.append("All 14 open bets (10/29 group) carry the approximate placement date 10/29:")
L.append("")
L.append("| ID | Bet | Derived value | Basis |")
L.append("|---|---|---|---|")
import re as _re2
for b in B:
    n = b["Notes"]
    if b["Status"] == "pending":
        L.append(f"| {b['ID']} | {b['Description'][:70]} | date {b['Date']} | placement date approximated as 10/29 (games 10/31-11/1) - confirm |")
    elif any(k in n for k in ("derived", "assumes", "approx", "pending user", "not printed", "not shown", "logged $")):
        basis = _re2.split(r";", n)
        key = next((s for s in basis if any(k in s for k in ("derived","assumes","approx","pending user"))), "")
        L.append(f"| {b['ID']} | {b['Description'][:70]} | risk {b['Risk'] or 'blank'} / to-win {b['To Win'] or 'blank'} | {key.strip()[:120]} |")
L.append("")

# ---- settlement updates for existing bets ----
L.append("## SETTLEMENT UPDATES TO EXISTING BETS (no new rows)")
L.append("")
L.append("| ID | Bet | Current | Proposed |")
L.append("|---|---|---|---|")
L.append("| 1836 | Mariners World Series +3500, $250 | pending | lost, result 2026-09-26 (account activity shows -$250) |")
L.append("| 1837 | Mariners AL Pennant +1200, $250 | pending | lost, result 2026-09-26 (account activity shows -$250) |")
L.append("")
open("confirmation_table.md", "w").write("\n".join(L) + "\n")
print("wrote confirmation_table.md")
