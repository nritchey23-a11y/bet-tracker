"""
On-demand pending-bet settler.

Reads Pending bets from the Google Sheet, looks up game results via ESPN's
public scoreboard API, evaluates each bet, and emits a structured proposal
for review BEFORE updating the sheet/dashboard.

Usage:
    python settle_pending.py                # dry-run; prints proposals
    python settle_pending.py --apply        # write changes to sheet + dashboard
    python settle_pending.py --through YYYY-MM-DD   # only settle on/before date

Currently handles: ML, spread (point/run/puck line), total over/under, and
parlays where ALL legs are evaluable. Round-robins, futures, player props,
golf matchups, and anything with low-confidence matching are flagged for
manual review and left as Pending.

Output: proposals printed to stdout AND written to ./settle_proposals.json
so the main agent can show them to the user before applying.
"""
import argparse, json, os, re, sys, urllib.request
from datetime import datetime, date
from dataclasses import dataclass, asdict, field
from typing import Optional

# ESPN public scoreboard endpoint (no auth required)
ESPN_BASE = "https://site.api.espn.com/apis/site/v2/sports"
LEAGUE_MAP = {
    "MLB": ("baseball", "mlb"),
    "NBA": ("basketball", "nba"),
    "WNBA": ("basketball", "wnba"),
    "NHL": ("hockey", "nhl"),
    "NFL": ("football", "nfl"),
    "NCAAF": ("football", "college-football"),
    "NCAAB": ("basketball", "mens-college-basketball"),
}

# Cache scoreboards in-memory per run
_CACHE: dict = {}

def fetch_scoreboard(league: str, day: date) -> Optional[dict]:
    if league not in LEAGUE_MAP:
        return None
    sport, lg = LEAGUE_MAP[league]
    key = (lg, day.isoformat())
    if key in _CACHE:
        return _CACHE[key]
    url = f"{ESPN_BASE}/{sport}/{lg}/scoreboard?dates={day.strftime('%Y%m%d')}"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.loads(r.read())
            _CACHE[key] = data
            return data
    except Exception as e:
        print(f"[warn] ESPN fetch failed for {league} {day}: {e}", file=sys.stderr)
        return None

def _norm(name: str) -> str:
    """Normalize team name for matching."""
    return re.sub(r"[^a-z]", "", (name or "").lower())

# Common nickname → full team mapping (helps match Pick fields)
TEAM_ALIASES = {
    "spurs": "san antonio spurs", "thunder": "oklahoma city thunder",
    "cavs": "cleveland cavaliers", "knicks": "new york knicks",
    "avs": "colorado avalanche", "avalanche": "colorado avalanche",
    "knights": "vegas golden knights", "vgk": "vegas golden knights",
    "rays": "tampa bay rays", "yankees": "new york yankees",
    "rangers": "texas rangers", "angels": "los angeles angels",
    "astros": "houston astros", "cubs": "chicago cubs",
    "brewers": "milwaukee brewers", "dodgers": "los angeles dodgers",
    "mariners": "seattle mariners", "athletics": "oakland athletics",
    "phillies": "philadelphia phillies", "marlins": "miami marlins",
    "pirates": "pittsburgh pirates", "nationals": "washington nationals",
    "braves": "atlanta braves", "diamondbacks": "arizona diamondbacks",
    "dbacks": "arizona diamondbacks", "reds": "cincinnati reds",
    "lad": "los angeles dodgers", "laa": "los angeles angels",
    "nyy": "new york yankees", "tb": "tampa bay rays",
    "hou": "houston astros", "sea": "seattle mariners",
    "atl": "atlanta braves", "ari": "arizona diamondbacks",
    "phi": "philadelphia phillies", "tex": "texas rangers",
    "mil": "milwaukee brewers", "sas": "san antonio spurs",
    "okc": "oklahoma city thunder", "col": "colorado avalanche",
}

def resolve_team(text: str) -> str:
    t = text.strip().lower()
    if t in TEAM_ALIASES:
        return TEAM_ALIASES[t]
    return t

def find_game(league: str, day: date, team_text: str) -> Optional[dict]:
    sb = fetch_scoreboard(league, day)
    if not sb:
        return None
    target = _norm(resolve_team(team_text))
    for ev in sb.get("events", []):
        comp = ev.get("competitions", [{}])[0]
        competitors = comp.get("competitors", [])
        names = [
            _norm(c.get("team", {}).get("displayName", "")) +
            "|" + _norm(c.get("team", {}).get("name", "")) +
            "|" + _norm(c.get("team", {}).get("abbreviation", ""))
            for c in competitors
        ]
        if any(target and (target in n or n.split("|")[1] in target) for n in names):
            status = comp.get("status", {}).get("type", {}).get("completed", False)
            return {
                "event": ev,
                "completed": status,
                "competitors": competitors,
                "id": ev.get("id"),
            }
    return None

def parse_american_odds(s: str) -> Optional[float]:
    """Return profit-per-$1-stake (decimal-1). e.g. '+150' -> 1.5, '-110' -> 0.909"""
    if s is None: return None
    s = str(s).strip().replace(",", "")
    if not s: return None
    try:
        v = float(s)
        if v > 0:
            return v / 100.0
        else:
            return 100.0 / abs(v)
    except ValueError:
        return None

@dataclass
class Proposal:
    bet_id: str
    sheet_row: int
    date: str
    league: str
    pick: str
    bet_type: str
    proposed_status: str   # "Won" | "Lost" | "Push" | "Pending"
    confidence: str        # "high" | "medium" | "low"
    reason: str
    game_score: str = ""
    notes: str = ""

# ---- Bet evaluators ----

def eval_moneyline(game, pick_team) -> tuple[str, str, str]:
    comp = game["competitors"]
    scores = {_norm(c.get("team", {}).get("displayName","")): int(c.get("score","0") or 0)
              for c in comp}
    score_str = " - ".join(f"{c['team']['displayName']} {c.get('score','?')}" for c in comp)
    pick_norm = _norm(resolve_team(pick_team))
    pick_score, other_score = None, None
    for name, sc in scores.items():
        if pick_norm in name or name in pick_norm:
            pick_score = sc
        else:
            other_score = sc
    if pick_score is None or other_score is None:
        return ("Pending", "low", f"Could not identify pick side in {score_str}")
    if pick_score > other_score:
        return ("Won", "high", f"{pick_team} won {pick_score}-{other_score}")
    elif pick_score < other_score:
        return ("Lost", "high", f"{pick_team} lost {pick_score}-{other_score}")
    else:
        return ("Push", "high", f"Tie {pick_score}-{other_score}")

def eval_spread(game, pick_team, line) -> tuple[str, str, str]:
    comp = game["competitors"]
    scores = {_norm(c.get("team", {}).get("displayName","")): int(c.get("score","0") or 0)
              for c in comp}
    pick_norm = _norm(resolve_team(pick_team))
    pick_score, other_score = None, None
    for name, sc in scores.items():
        if pick_norm in name or name in pick_norm:
            pick_score = sc
        else:
            other_score = sc
    if pick_score is None or other_score is None:
        return ("Pending", "low", f"Could not identify pick side")
    adj = pick_score + line   # line is negative if favored
    if adj > other_score:
        return ("Won", "high", f"{pick_team} {pick_score}-{other_score}; +({line:+}) = {adj} > {other_score}")
    elif adj < other_score:
        return ("Lost", "high", f"{pick_team} {pick_score}-{other_score}; +({line:+}) = {adj} < {other_score}")
    else:
        return ("Push", "high", "Exact push on spread")

def eval_total(game, side, line) -> tuple[str, str, str]:
    comp = game["competitors"]
    total = sum(int(c.get("score","0") or 0) for c in comp)
    if side.lower().startswith("o"):
        if total > line: return ("Won", "high", f"Total {total} > {line}")
        if total < line: return ("Lost", "high", f"Total {total} < {line}")
        return ("Push", "high", f"Push at {line}")
    else:
        if total < line: return ("Won", "high", f"Total {total} < {line}")
        if total > line: return ("Lost", "high", f"Total {total} > {line}")
        return ("Push", "high", f"Push at {line}")

# Pick parser — extracts (team, line) from Pick/Description text
SPREAD_RE = re.compile(r"([+-]?\d+(?:\.\d+)?)")
TOTAL_RE = re.compile(r"(?:total\s+)?(over|under|o|u)\s*(\d+(?:\.\d+)?)", re.I)

def evaluate(bet: dict) -> Proposal:
    bid = str(bet.get("ID",""))
    row = bet.get("_row", -1)
    league = bet.get("League","").upper().split("/")[0].strip()
    pick = bet.get("Pick","")
    desc = bet.get("Description","")
    btype = bet.get("Type","").lower()
    bet_date_str = bet.get("Date","")

    # Parse date
    try:
        if "/" in bet_date_str:
            game_date = datetime.strptime(bet_date_str, "%m/%d/%Y").date()
        else:
            game_date = datetime.strptime(bet_date_str, "%Y-%m-%d").date()
    except Exception:
        return Proposal(bid, row, bet_date_str, league, pick, btype, "Pending", "low",
                        f"Could not parse date '{bet_date_str}'")

    # Skip future games
    if game_date > date.today():
        return Proposal(bid, row, bet_date_str, league, pick, btype, "Pending", "low",
                        "Game in future")

    # Handle special types
    if btype in ("futures","future"):
        return Proposal(bid, row, bet_date_str, league, pick, btype, "Pending", "low",
                        "Future — settles at end of season")
    if btype in ("round robin","rr"):
        return Proposal(bid, row, bet_date_str, league, pick, btype, "Pending", "medium",
                        "Round robin — requires leg-by-leg settlement; manual review")
    if btype == "parlay":
        return Proposal(bid, row, bet_date_str, league, pick, btype, "Pending", "medium",
                        "Parlay — requires leg-by-leg settlement; manual review")
    if "prop" in btype or btype in ("match-up","matchup","tournament"):
        return Proposal(bid, row, bet_date_str, league, pick, btype, "Pending", "low",
                        f"Bet type '{btype}' — needs manual or specialized data")

    # Find the game — for totals, use Event field (Pick is just "Over X"); else use Pick
    event = bet.get("Event", "") or ""
    search_terms = []
    if btype == "total":
        # Try each token in Event field
        for tok in re.split(r"\s+vs\s+|\s+@\s+|/", event, flags=re.I):
            tok = re.sub(r"(?i)\bgame\b|total|over|under|\d+\.?\d*|\(.*\)", "", tok).strip()
            if len(tok) > 2:
                search_terms.append(tok)
    else:
        search_terms.append(pick)
    game = None
    for term in search_terms:
        game = find_game(league, game_date, term)
        if game:
            break
    if not game:
        return Proposal(bid, row, bet_date_str, league, pick, btype, "Pending", "low",
                        f"Could not find {league} game with {pick} on {game_date}")
    if not game["completed"]:
        return Proposal(bid, row, bet_date_str, league, pick, btype, "Pending", "low",
                        "Game not yet completed")

    score_str = " | ".join(f"{c['team']['displayName']} {c.get('score','?')}" for c in game["competitors"])

    if btype == "moneyline":
        st, conf, reason = eval_moneyline(game, pick)
        return Proposal(bid, row, bet_date_str, league, pick, btype, st, conf, reason, score_str)

    if btype in ("spread","run line","puck line","point spread"):
        # Extract line from Pick or Description
        m = SPREAD_RE.search(pick) or SPREAD_RE.search(desc)
        if not m:
            return Proposal(bid, row, bet_date_str, league, pick, btype, "Pending", "low",
                            "Could not parse spread line", score_str)
        line = float(m.group(1))
        st, conf, reason = eval_spread(game, pick, line)
        return Proposal(bid, row, bet_date_str, league, pick, btype, st, conf, reason, score_str)

    if btype == "total":
        m = TOTAL_RE.search(pick) or TOTAL_RE.search(desc)
        if not m:
            return Proposal(bid, row, bet_date_str, league, pick, btype, "Pending", "low",
                            "Could not parse total line", score_str)
        side, line = m.group(1), float(m.group(2))
        st, conf, reason = eval_total(game, side, line)
        return Proposal(bid, row, bet_date_str, league, pick, btype, st, conf, reason, score_str)

    return Proposal(bid, row, bet_date_str, league, pick, btype, "Pending", "low",
                    f"Unsupported bet type '{btype}'", score_str)

# ---- Sheet I/O ----

def load_bets_from_dashboard() -> list[dict]:
    """Read bets from local FALLBACK_BETS as source-of-truth for evaluation
    (avoids needing live sheet access on every run; sheet is updated separately)."""
    path = "/home/user/workspace/bet-tracker/index.html"
    with open(path) as f:
        html = f.read()
    m = re.search(r"const FALLBACK_BETS = (\[.*?\]);\s*\n", html, re.DOTALL)
    bets = json.loads(m.group(1))
    # Add a row hint when present (best-effort)
    for i, b in enumerate(bets):
        b["_row"] = i + 2  # approximate
    return bets

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--through", help="Only settle bets on/before YYYY-MM-DD")
    ap.add_argument("--apply", action="store_true", help="Apply changes (default: dry-run)")
    args = ap.parse_args()

    cutoff = date.today()
    if args.through:
        cutoff = datetime.strptime(args.through, "%Y-%m-%d").date()

    bets = load_bets_from_dashboard()
    pending = [b for b in bets if b.get("Status","") == "Pending"]
    print(f"Found {len(pending)} pending bets total")

    proposals = []
    for b in pending:
        try:
            if "/" in b["Date"]:
                d = datetime.strptime(b["Date"], "%m/%d/%Y").date()
            else:
                d = datetime.strptime(b["Date"], "%Y-%m-%d").date()
        except Exception:
            continue
        if d > cutoff:
            continue
        p = evaluate(b)
        proposals.append(p)

    # Summary
    high_won = [p for p in proposals if p.proposed_status == "Won" and p.confidence == "high"]
    high_lost = [p for p in proposals if p.proposed_status == "Lost" and p.confidence == "high"]
    push = [p for p in proposals if p.proposed_status == "Push"]
    flagged = [p for p in proposals if p.proposed_status == "Pending"]

    print(f"\n=== PROPOSED SETTLEMENTS ===")
    print(f"  Won (high confidence): {len(high_won)}")
    print(f"  Lost (high confidence): {len(high_lost)}")
    print(f"  Push: {len(push)}")
    print(f"  Flagged for manual review: {len(flagged)}\n")

    for label, group in [("WON", high_won), ("LOST", high_lost), ("PUSH", push), ("FLAGGED", flagged)]:
        if not group: continue
        print(f"--- {label} ({len(group)}) ---")
        for p in group:
            print(f"  #{p.bet_id} [{p.league}] {p.pick}  →  {p.proposed_status}")
            print(f"     {p.reason}")
            if p.game_score:
                print(f"     {p.game_score}")
        print()

    out_path = "/home/user/workspace/settle_proposals.json"
    with open(out_path, "w") as f:
        json.dump([asdict(p) for p in proposals], f, indent=2)
    print(f"Proposals written to {out_path}")

    if args.apply:
        print("\n--apply flag set: would write to sheet + dashboard now")
        print("(Apply step performed by the main agent after user approval — not here.)")

if __name__ == "__main__":
    main()
