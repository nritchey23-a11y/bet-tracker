"""
Grade all 27 settled WC futures (24 knockout + 2 dead-heat).
Spain (1390) and Argentina (1698) remain pending pending July 19 final.
"""
import json, re

INDEX_FILE = "/home/user/workspace/bet-tracker/index.html"

# Grades: {ID: (status, result_date, notes_addl, risk_override, towin_override)}
GRADES = {
    # --- Reach R16 tier (R32 played June 28 - July 3) ---
    1724: ("lost", "2026-07-03", "Uruguay eliminated in group stage — did not reach R32.", None, None),
    1725: ("won",  "2026-07-07", "Colombia beat Ghana in R32 to reach R16 (0-0, lost R16 on pens to SUI).", None, None),
    1726: ("won",  "2026-06-30", "Norway beat Ivory Coast in R32 to reach R16.", None, None),
    1727: ("lost", "2026-06-30", "Netherlands lost 1-1 (2-3 pens) to Morocco in R32.", None, None),

    # --- Reach QF tier (R16 played July 4-7) ---
    1720: ("won",  "2026-07-05", "Norway 2-1 Brazil in R16 to reach QF.", None, None),
    1721: ("lost", "2026-06-30", "Netherlands out R32 to Morocco (never reached R16, forfeits QF ticket).", None, None),
    1722: ("lost", "2026-07-04", "Germany 1-1 (3-4 pens) Paraguay in R32 — eliminated before QF.", None, None),
    1723: ("lost", "2026-07-06", "Portugal 0-1 Spain in R16 — eliminated before QF.", None, None),

    # --- Reach SF tier (QF played July 9-11) ---
    1714: ("lost", "2026-07-11", "Norway 1-2 (aet) England in QF — did not reach SF.", None, None),
    1715: ("lost", "2026-06-30", "Netherlands out R32 to Morocco — did not reach SF.", None, None),
    1716: ("lost", "2026-07-04", "Germany out R32 to Paraguay — did not reach SF.", None, None),
    1717: ("lost", "2026-07-06", "Portugal out R16 to Spain — did not reach SF.", None, None),

    # --- Reach Final tier (SF played July 14-15) ---
    1718: ("lost", "2026-07-04", "Germany out R32 to Paraguay — did not reach Final.", None, None),
    1719: ("lost", "2026-07-06", "Portugal out R16 to Spain — did not reach Final.", None, None),

    # --- Tournament Winner tier (Final July 19) ---
    1713: ("lost", "2026-07-04", "Germany out R32 to Paraguay — cannot win tournament.", None, None),
    1745: ("lost", "2026-07-06", "Portugal out R16 to Spain — cannot win tournament.", None, None),

    # --- Stage-of-elimination bets (placed 6/29 as hedges) ---
    1699: ("lost", "2026-07-11", "Norway eliminated in QF, not L16 — hedge does not pay.", None, None),
    1700: ("lost", "2026-06-30", "Netherlands eliminated in R32, not QF — hedge does not pay.", None, None),
    1701: ("lost", "2026-07-04", "Germany eliminated in R32, not L16 — hedge does not pay.", None, None),
    1702: ("won",  "2026-07-06", "Portugal eliminated in L16 by Spain — hedge cashes.", None, None),
    1695: ("lost", "2026-07-07", "Colombia eliminated in R16 on pens by Switzerland, not QF.", None, None),
    1696: ("won",  "2026-06-30", "Ivory Coast eliminated in R32 by Norway.", None, None),
    1697: ("lost", "2026-07-06", "USA eliminated in R16 by Belgium 1-4, not QF.", None, None),

    # --- UEFA Top Finish (Germany R32 exit) ---
    1711: ("lost", "2026-07-04", "Germany out R32 — Spain/England/France all finished higher.", None, None),

    # --- Top African Team (Senegal) ---
    1749: ("lost", "2026-07-01", "Senegal out R32 to Belgium; Morocco reached QF as top African side.", None, None),

    # --- DEAD HEAT: USA Top North American Team ---
    # +140 odds. Original stake $725. All 3 NA teams (USA, MEX, CAN) went out R16 → 3-way dead heat.
    # 1/3 of $725 = $241.67 wins at +140 → +$338.33 profit
    # 2/3 of $725 = $483.33 loses
    # Net: -$145.00
    1748: ("lost", "2026-07-06",
           "DEAD HEAT: USA, Mexico, Canada all eliminated R16 (3-way tie). Original stake $725 at +140. "
           "1/3 wins at full odds ($241.67 → +$338.33 profit); 2/3 loses ($483.33). Net -$145.00. "
           "Risk field overridden to net loss amount per partial-win convention.",
           145.00, 0),

    # --- DEAD HEAT: Mexico CONCACAF Top Finish ---
    # +160 odds. Original stake $1,000. All 3 CONCACAF teams (USA, MEX, CAN) went out R16 → 3-way dead heat.
    # 1/3 of $1000 = $333.33 wins at +160 → +$533.33 profit
    # 2/3 of $1000 = $666.67 loses
    # Net: -$133.33
    1712: ("lost", "2026-07-06",
           "DEAD HEAT: USA, Mexico, Canada all eliminated R16 (3-way tie). Original stake $1,000 at +160. "
           "1/3 wins at full odds ($333.33 → +$533.33 profit); 2/3 loses ($666.67). Net -$133.33. "
           "Risk field overridden to net loss amount per partial-win convention.",
           133.33, 0),
}

# --- Update the FALLBACK_BETS in index.html ---
with open(INDEX_FILE) as f:
    html = f.read()

# Find FALLBACK_BETS block
m = re.search(r"const FALLBACK_BETS\s*=\s*(\[[\s\S]*?\]);", html)
if not m:
    raise SystemExit("Could not find FALLBACK_BETS")
bets = json.loads(m.group(1))
by_id = {str(b["ID"]): b for b in bets}

wins = losses = 0
win_profit = loss_amount = 0.0
for bid_int, (status, rdate, notes_add, risk_over, towin_over) in GRADES.items():
    bid = str(bid_int)
    if bid not in by_id:
        print(f"WARN: bet ID {bid} not found in FALLBACK_BETS")
        continue
    b = by_id[bid]
    b["Status"] = status
    b["Result Date"] = rdate
    existing_notes = (b.get("Notes") or "").strip()
    b["Notes"] = (existing_notes + " | " + notes_add) if existing_notes else notes_add
    if risk_over is not None:
        b["Risk"] = risk_over
    if towin_over is not None:
        b["To Win"] = towin_over
    if status == "won":
        wins += 1
        win_profit += float(b["To Win"])
    elif status == "lost":
        losses += 1
        loss_amount += float(b["Risk"])

new_json = json.dumps(bets, indent=2)
html2 = html[:m.start(1)] + new_json + html[m.end(1):]
with open(INDEX_FILE, "w") as f:
    f.write(html2)

# --- Save grades for sheet sync ---
grades_out = []
for bid_int, (status, rdate, notes_add, risk_over, towin_over) in GRADES.items():
    bid = str(bid_int)
    b = by_id[bid]
    grades_out.append({
        "ID": bid,
        "Status": status,
        "Result Date": rdate,
        "Notes": b["Notes"],
        "Risk": b["Risk"],
        "To Win": b["To Win"],
    })
with open("/home/user/workspace/bet-tracker/wc_grades.json","w") as f:
    json.dump(grades_out, f, indent=2)

print(f"Graded {len(GRADES)} bets: {wins}W {losses}L")
print(f"  Wins to-win banked: +${win_profit:,.2f}")
print(f"  Losses risk lost:   -${loss_amount:,.2f}")
print(f"  Net from this grading pass: ${win_profit-loss_amount:+,.2f}")
print(f"Still pending: Spain to Win (1390), Argentina Runner-up (1698) — settle after July 19 final")
