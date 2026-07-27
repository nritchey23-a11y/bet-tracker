"""
Settle bets with known outcomes as of July 27, 2026:
- WC Final (July 19): Spain 1-0 Argentina (ET) — Spain wins, Argentina Runner-up wins
- Two 5-leg parlays with DEU/NED legs — both dead once DEU lost R32 (7/4)
- 2026 Majors complete: Masters=McIlroy, PGA=Rai, US Open=Clark, Open=Fox — Aberg 0 wins
"""
import json, re

INDEX = "/home/user/workspace/bet-tracker/index.html"

GRADES = {
    1390: ("won",  "2026-07-19", "Spain 1-0 Argentina (ET) in WC Final; Ferran Torres 106' — Spain wins outright."),
    1698: ("won",  "2026-07-19", "Argentina reached Final but lost 0-1 to Spain (ET) — Runner-up prop cashes."),
    1693: ("lost", "2026-07-04", "Parlay dead: DEU-PAR leg lost when Germany fell to Paraguay on pens in R32."),
    1694: ("lost", "2026-07-04", "Parlay dead: DEU-PAR leg lost when Germany fell to Paraguay on pens in R32."),
    1:    ("lost", "2026-07-19", "2026 Majors complete: McIlroy (Masters), Rai (PGA), Clark (US Open), Fox (Open). Aberg finished T21 Masters, T4 PGA, no wins."),
    1409: ("lost", "2026-07-19", "2026 Majors complete: McIlroy (Masters), Rai (PGA), Clark (US Open), Fox (Open). Aberg no wins."),
}

with open(INDEX) as f:
    html = f.read()
m = re.search(r"const FALLBACK_BETS\s*=\s*(\[[\s\S]*?\]);", html)
bets = json.loads(m.group(1))
by_id = {str(b["ID"]): b for b in bets}

wins = losses = 0; win_p = 0.0; loss_a = 0.0
for bid, (status, rdate, notes_add) in GRADES.items():
    b = by_id[str(bid)]
    b["Status"] = status
    b["Result Date"] = rdate
    existing = (b.get("Notes") or "").strip()
    b["Notes"] = (existing + " | " + notes_add) if existing else notes_add
    if status=="won":
        wins += 1; win_p += float(b["To Win"])
    else:
        losses += 1; loss_a += float(b["Risk"])

new_json = json.dumps(bets, indent=2)
html2 = html[:m.start(1)] + new_json + html[m.end(1):]
with open(INDEX,"w") as f:
    f.write(html2)

print(f"Graded {len(GRADES)}: {wins}W {losses}L")
print(f"  Wins:   +${win_p:,.2f}")
print(f"  Losses: -${loss_a:,.2f}")
print(f"  Net:    ${win_p-loss_a:+,.2f}")
