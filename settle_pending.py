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
            stype = comp.get("status", {}).get("type", {})
            return {
                "event": ev,
                "completed": stype.get("completed", False),
                "state": stype.get("state", ""),
                "name": stype.get("name", ""),
                "competitors": competitors,
                "id": ev.get("id"),
            }
    return None

VOIDED_STATES = {"STATUS_POSTPONED", "STATUS_CANCELED", "STATUS_CANCELLED",
                 "STATUS_SUSPENDED", "STATUS_FORFEIT", "STATUS_ABANDONED"}

def game_is_voided(game: dict) -> bool:
    return game.get("name", "") in VOIDED_STATES

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

# ---- Multi-leg (parlay/RR) support ----

ALL_LEAGUES = ["MLB", "NBA", "NHL", "NFL", "WNBA", "NCAAB", "NCAAF"]

def find_game_any_league(day: date, team_text: str):
    """Search every league's scoreboard for a team match. Returns (league, game)."""
    for lg in ALL_LEAGUES:
        g = find_game(lg, day, team_text)
        if g:
            return lg, g
    return None, None

# Robust leg parser. Accepts forms like:
#   "Spurs -2.5 (-110)", "Avalanche ML (-185)",
#   "Astros/Cubs Total Over 7 (-115)", "TEX -1.5 +115",
#   "MIL/LAD U8.5 -115", "Cavaliers +7 (-110)"
ODDS_TAIL_RE = re.compile(r"\(?\s*([+-]\d{2,4})\s*\)?\s*$")
TOTAL_LEG_RE = re.compile(r"(over|under|(?:^|[\s/])([OU])(?=\d))\s*(\d+(?:\.\d+)?)", re.I)
SPREAD_LEG_RE = re.compile(r"([+-]\d+(?:\.\d+)?)")

def parse_leg(text: str) -> dict:
    raw = text.strip().rstrip(";.")
    odds = None
    body = raw
    m = ODDS_TAIL_RE.search(raw)
    if m:
        odds = float(m.group(1))
        body = raw[:m.start()].strip().rstrip("(").strip()
    bl = body.lower()
    # Total?
    if "total" in bl or TOTAL_LEG_RE.search(body):
        sm = TOTAL_LEG_RE.search(body)
        if sm:
            side_token = (sm.group(2) or sm.group(1) or "").strip().lower()
            side = "Over" if side_token.startswith("o") else "Under"
            line = float(sm.group(3))
            # Extract team(s) before total
            team_text = re.sub(r"(?i)total|over|under|\b[ou]\b|\d+(?:\.\d+)?", "", body[:sm.start()]).strip()
            return {"type": "total", "side": side, "line": line, "odds": odds,
                    "teams_hint": team_text, "raw": raw}
    # ML?
    if re.search(r"\bml\b|moneyline", bl):
        team = re.sub(r"(?i)\bml\b|moneyline", "", body).strip()
        return {"type": "moneyline", "team": team, "odds": odds, "raw": raw}
    # Spread
    sm = SPREAD_LEG_RE.search(body)
    if sm:
        line = float(sm.group(1))
        team = body[:sm.start()].strip()
        return {"type": "spread", "team": team, "line": line, "odds": odds, "raw": raw}
    return {"type": "unknown", "raw": raw, "odds": odds}

def evaluate_leg(leg: dict, game_date: date) -> tuple:
    """Return (status, decimal_odds_multiplier, detail_str).
       Status: 'Won' | 'Lost' | 'Push' | 'Void' | 'Unknown'
       decimal_odds_multiplier = 1 + profit_per_$1 (e.g. -110 -> 1.909)."""
    odds_dec = None
    if leg.get("odds") is not None:
        po = parse_american_odds(str(int(leg["odds"])) if leg["odds"] == int(leg["odds"]) else str(leg["odds"]))
        odds_dec = (po + 1.0) if po else None

    if leg["type"] == "moneyline":
        league, game = find_game_any_league(game_date, leg["team"])
        if not game: return ("Unknown", odds_dec, f"Could not locate {leg['team']} game")
        if game_is_voided(game): return ("Void", odds_dec, f"Game voided ({game.get('name','')})")
        if not game["completed"]: return ("Unknown", odds_dec, "Game not completed")
        st, _, reason = eval_moneyline(game, leg["team"])
        return (st, odds_dec, reason)

    if leg["type"] == "spread":
        league, game = find_game_any_league(game_date, leg["team"])
        if not game: return ("Unknown", odds_dec, f"Could not locate {leg['team']} game")
        if game_is_voided(game): return ("Void", odds_dec, f"Game voided ({game.get('name','')})")
        if not game["completed"]: return ("Unknown", odds_dec, "Game not completed")
        st, _, reason = eval_spread(game, leg["team"], leg["line"])
        return (st, odds_dec, reason)

    if leg["type"] == "total":
        # Try each token in teams_hint
        teams = leg.get("teams_hint", "")
        candidates = re.split(r"[/&,]| and ", teams)
        game = None
        for c in candidates:
            c = c.strip()
            if len(c) < 2: continue
            _, g = find_game_any_league(game_date, c)
            if g:
                game = g
                break
        if not game: return ("Unknown", odds_dec, f"Could not locate total game ({teams})")
        if game_is_voided(game): return ("Void", odds_dec, f"Game voided ({game.get('name','')})")
        if not game["completed"]: return ("Unknown", odds_dec, "Game not completed")
        st, _, reason = eval_total(game, leg["side"], leg["line"])
        return (st, odds_dec, reason)

    return ("Unknown", odds_dec, f"Unrecognized leg: {leg.get('raw','')}")

def settle_parlay_legs(leg_results: list) -> tuple:
    """Action Network rules: any Lost → parlay lost. Push/Void legs drop out
    and the parlay recalculates with remaining Won legs at their original odds.
    All pushed → Push (refund). Returns (status, payout_multiplier).
    payout_multiplier is the gross return per $1 stake (1.0 = refund)."""
    if any(r[0] == "Lost" for r in leg_results):
        return ("Lost", 0.0, "At least one leg lost")
    if any(r[0] == "Unknown" for r in leg_results):
        return ("Unknown", None, "At least one leg unresolved")
    won = [r for r in leg_results if r[0] == "Won"]
    pushed = [r for r in leg_results if r[0] in ("Push", "Void")]
    if not won and pushed:
        return ("Push", 1.0, "All legs pushed/voided — refund")
    # Recompute multiplier from won legs only
    mult = 1.0
    for st, od, _ in won:
        if od is None:
            return ("Unknown", None, "Missing odds on a winning leg")
        mult *= od
    if pushed:
        return ("Won", mult, f"{len(pushed)} leg(s) pushed; settled on remaining {len(won)} won legs")
    return ("Won", mult, f"All {len(won)} legs won")

from itertools import combinations
def settle_round_robin(leg_results: list, combo_sizes: list, stake_per_combo: float) -> dict:
    """Settle an N-team RR "all ways" given leg_results in order.
    combo_sizes: e.g. [2,3,4,5] for an all-ways 5-team RR.
    Returns dict with net P&L, # winning combos, breakdown.
    Push legs drop out of combos (each combo recalculates with remaining Won legs)."""
    n = len(leg_results)
    statuses = [r[0] for r in leg_results]
    odds = [r[1] for r in leg_results]
    breakdown = {"combos": [], "by_size": {}, "net": 0.0, "winning_combos": 0, "total_combos": 0}
    for size in combo_sizes:
        size_net = 0.0
        size_wins = 0
        for combo in combinations(range(n), size):
            breakdown["total_combos"] += 1
            statuses_in = [statuses[i] for i in combo]
            odds_in = [odds[i] for i in combo]
            if "Lost" in statuses_in:
                size_net -= stake_per_combo
                continue
            if "Unknown" in statuses_in:
                # Treat as undetermined — skip this combo (no settlement)
                breakdown["total_combos"] -= 1
                continue
            won_idx = [i for i, s in enumerate(statuses_in) if s == "Won"]
            if not won_idx:
                # All pushed — refund
                continue
            mult = 1.0
            for i in won_idx:
                if odds_in[i] is None:
                    mult = None; break
                mult *= odds_in[i]
            if mult is None:
                breakdown["total_combos"] -= 1
                continue
            profit = stake_per_combo * (mult - 1.0)
            size_net += profit
            size_wins += 1
        breakdown["by_size"][size] = {"net": round(size_net, 2), "wins": size_wins}
        breakdown["net"] += size_net
        breakdown["winning_combos"] += size_wins
    breakdown["net"] = round(breakdown["net"], 2)
    return breakdown

def _extract_legs_from_description(desc: str) -> list:
    """Split the Description field into individual leg strings.
    Handles formats like:
      '2-leg parlay: Spurs -2.5 (-110); Avalanche ML (-185)'
      '5-team RR All Ways (26 combos x $25): TEX -1.5 +115; TB ML +123; ...'
    """
    # Drop everything up to and including the first ':' or ')' if it precedes legs
    body = desc
    if ":" in body:
        body = body.split(":", 1)[1]
    return [seg.strip() for seg in re.split(r";|\u2022", body) if seg.strip()]

def evaluate_parlay(bet: dict, game_date: date) -> Proposal:
    bid = str(bet.get("ID", ""))
    row = bet.get("_row", -1)
    desc = bet.get("Description", "")
    risk = float(str(bet.get("Risk", "0")).replace(",", "") or 0)
    legs = [parse_leg(s) for s in _extract_legs_from_description(desc)]
    if not legs:
        return Proposal(bid, row, bet.get("Date",""), bet.get("League",""),
                        bet.get("Pick",""), "parlay", "Pending", "low",
                        "Could not parse parlay legs from Description")
    leg_results = [evaluate_leg(l, game_date) for l in legs]
    detail = "; ".join(f"{l['raw']} → {r[0]} ({r[2]})" for l, r in zip(legs, leg_results))
    status, mult, reason = settle_parlay_legs(leg_results)
    if status == "Unknown":
        return Proposal(bid, row, bet.get("Date",""), bet.get("League",""),
                        bet.get("Pick",""), "parlay", "Pending", "low",
                        f"{reason}. Legs: {detail}")
    if status == "Lost":
        return Proposal(bid, row, bet.get("Date",""), bet.get("League",""),
                        bet.get("Pick",""), "parlay", "Lost", "high",
                        f"Parlay lost — {reason}. Legs: {detail}")
    if status == "Push":
        return Proposal(bid, row, bet.get("Date",""), bet.get("League",""),
                        bet.get("Pick",""), "parlay", "Push", "high",
                        f"Parlay refunded — {reason}. Legs: {detail}")
    # Won
    profit = risk * (mult - 1.0)
    note = (f"Parlay won — {reason}. Realized profit ${profit:.2f} "
            f"(mult={mult:.3f} on ${risk}). Legs: {detail}")
    p = Proposal(bid, row, bet.get("Date",""), bet.get("League",""),
                 bet.get("Pick",""), "parlay", "Won", "high", note)
    p.notes = f"realized_profit={profit:.2f}"
    return p

def evaluate_round_robin(bet: dict, game_date: date) -> Proposal:
    bid = str(bet.get("ID", ""))
    row = bet.get("_row", -1)
    desc = bet.get("Description", "")
    notes = bet.get("Notes", "") or ""
    risk = float(str(bet.get("Risk", "0")).replace(",", "") or 0)
    legs = [parse_leg(s) for s in _extract_legs_from_description(desc)]
    if len(legs) < 2:
        return Proposal(bid, row, bet.get("Date",""), bet.get("League",""),
                        bet.get("Pick",""), "round robin", "Pending", "low",
                        "Could not parse RR legs")
    # Extract combo sizes — default to all-ways (2..N)
    n = len(legs)
    combo_sizes = list(range(2, n+1))
    # Try to find stake per combo — 'x $25' or '$25/combo' or 'all ways $25/game'
    m = re.search(r"\$\s*(\d+(?:\.\d+)?)\s*(?:/combo|/game|per combo|per game)?", desc + " " + notes)
    stake_per_combo = float(m.group(1)) if m else None
    if stake_per_combo is None:
        # Try total_combos = sum(C(n,k)) and divide risk by that
        from math import comb
        total_combos = sum(comb(n, k) for k in combo_sizes)
        stake_per_combo = risk / total_combos if total_combos else 0
    leg_results = [evaluate_leg(l, game_date) for l in legs]
    detail = "; ".join(f"L{i+1} {l['raw']} → {r[0]}" for i, (l, r) in enumerate(zip(legs, leg_results)))
    if any(r[0] == "Unknown" for r in leg_results):
        return Proposal(bid, row, bet.get("Date",""), bet.get("League",""),
                        bet.get("Pick",""), "round robin", "Pending", "low",
                        f"Some legs unresolved. {detail}")
    bd = settle_round_robin(leg_results, combo_sizes, stake_per_combo)
    net = bd["net"]
    # Determine status from net
    if abs(net) < 0.01:
        status = "Push"; conf = "high"
    elif net > 0:
        status = "Won"; conf = "high"
    else:
        status = "Lost"; conf = "high"
    breakdown_str = ", ".join(f"{k}-leg: {v['wins']} win/${v['net']:.2f}" for k, v in bd["by_size"].items())
    reason = (f"RR realized P&L = ${net:+.2f}. "
              f"{bd['winning_combos']}/{bd['total_combos']} combos won "
              f"({breakdown_str}). Legs: {detail}")
    p = Proposal(bid, row, bet.get("Date",""), bet.get("League",""),
                 bet.get("Pick",""), "round robin", status, conf, reason)
    p.notes = f"realized_pnl={net:.2f}"
    return p

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
    if btype in ("round robin", "rr"):
        return evaluate_round_robin(bet, game_date)
    if btype == "parlay":
        return evaluate_parlay(bet, game_date)
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

    if game_is_voided(game):
        return Proposal(bid, row, bet_date_str, league, pick, btype, "Push", "high",
                        f"Game voided ({game.get('name','postponed')}); refund", score_str)

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
