#!/usr/bin/env python3
"""Settle-date + horizon derivation for the bet tracker.

WHY THIS EXISTS
---------------
The ledger only stores `Date` = when the bet was PLACED. That makes it
impossible to answer "what is riding today?", because a Week-1 moneyline
placed on 8/24 and a season win total placed on 8/24 look identical.

This module adds a derived `Event Date` (when the bet SETTLES) and a
`Horizon` bucket, so the digests can separate today's action from
season-long futures.

PRECEDENCE
----------
1. Explicit `Event Date` field on the bet row  (manual override, always wins)
2. Rule match on Sport / League / Type / Description  (the tables below)
3. Fall back to the placement `Date`             (right for same-day tickets)

MAINTENANCE
-----------
Season anchors move every year. Update SEASON_ANCHORS each August and the
whole tracker re-derives itself. Sources for the current values are cited
in the table.
"""
from datetime import date, datetime, timedelta
import re

# --------------------------------------------------------------- anchors
# Last verified 2026-08-31. Each value is the date the market GRADES,
# i.e. the last day the outcome can still change.
SEASON_ANCHORS = {
    # NFL regular season Sept 9 2026 - Jan 10 2027 (en.wikipedia.org/wiki/2026_NFL_season)
    "nfl_regular_season_end": "2027-01-10",
    # NCAAF regular season Aug 29 - Dec 12 2026
    # (en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_season)
    "ncaaf_regular_season_end": "2026-12-12",
    # NCAAF conference championship games Dec 4-5 2026
    "ncaaf_conf_champ": "2026-12-05",
    # MLB final day of regular season Sun Sept 27 2026 (mlb.com/news/mlb-announces-2026-game-times)
    "mlb_regular_season_end": "2026-09-27",
    # MLB postseason begins Sept 29; pennants decided before the World Series
    "mlb_pennant": "2026-10-21",
    # World Series Oct 23 - Oct 31 2026 (en.wikipedia.org/wiki/2026_Major_League_Baseball_season)
    "mlb_world_series": "2026-10-31",
    # F1 finale: Abu Dhabi GP race day Dec 6 2026 (formula1.com/en/racing/2026)
    "f1_season_end": "2026-12-06",
    # 2027 Masters final round Sun April 11 2027
    "masters_2027": "2027-04-11",
}

# Season openers, used to date game bets placed BEFORE the season starts.
# A Week-1 moneyline bought in August settles in September, not in August.
SEASON_OPENERS = {
    "nfl": ("2026-09-09", "2026-09-14"),     # opener .. end of Week 1
    "ncaaf": ("2026-08-29", "2026-09-06"),   # Week 0 .. end of Week 1
}

# Hand-set settle dates for rows the rules cannot infer. Keyed by bet ID.
# Prefer filling the sheet's "Event Date" column over growing this map.
OVERRIDES = {
    "1839": "2026-09-14",  # 4-leg NFL Week 1 ML parlay bought 8/24
}

# Horizon thresholds, in days between placement and settlement.
DAY_MAX = 1      # settles same day / next day  -> "day"
WEEK_MAX = 10    # settles inside ~a week       -> "week"
                 # anything longer              -> "season"

FUTURE_TYPES = ("future", "futures", "outright")
# Types that are inherently short-dated: they settle on the event they name.
GAME_TYPES = ("straight", "spread", "moneyline", "total", "prop",
              "parlay", "live", "teaser", "round robin", "rr")


def _s(b, k):
    return (b.get(k) or "").strip()


def _lower(b, k):
    return _s(b, k).lower()


def is_future(b):
    return _lower(b, "Type") in FUTURE_TYPES


def _sunday_of(d):
    """Golf/racing outrights settle on the final round -- the Sunday of that week."""
    try:
        dt = datetime.strptime(d, "%Y-%m-%d").date()
    except Exception:
        return d
    return (dt + timedelta(days=(6 - dt.weekday()) % 7)).isoformat()


def settle_date(b):
    """Return (event_date_str, source) where source is override|rule|placement."""
    explicit = _s(b, "Event Date")
    if explicit:
        return explicit, "override"
    hard = OVERRIDES.get(str(b.get("ID") or "").strip())
    if hard:
        return hard, "override"

    placed = _s(b, "Date")
    desc = (_s(b, "Description") + " " + _s(b, "Event")).lower()
    league = _lower(b, "League")
    sport = _lower(b, "Sport")
    A = SEASON_ANCHORS

    if is_future(b):
        # --- golf / motorsport single events -------------------------------
        if "masters" in desc:
            return A["masters_2027"], "rule"
        if sport == "golf":
            # "Tournament Outright Winner: X" -- settles the Sunday of the week placed
            return _sunday_of(placed), "rule"
        if "drivers championship" in desc or "constructors" in desc:
            return A["f1_season_end"], "rule"

        # --- baseball -------------------------------------------------------
        if league == "mlb" or sport == "baseball":
            if "world series" in desc:
                return A["mlb_world_series"], "rule"
            if "pennant" in desc:
                return A["mlb_pennant"], "rule"
            if "division" in desc or "regular season" in desc or "win total" in desc:
                return A["mlb_regular_season_end"], "rule"
            return A["mlb_world_series"], "rule"

        # --- college football ----------------------------------------------
        if league in ("ncaaf", "ncaa fb", "cfb"):
            if "conference champion" in desc or "championship game" in desc \
                    or "conference championship" in desc:
                return A["ncaaf_conf_champ"], "rule"
            if "national champion" in desc or "playoff" in desc:
                return "2027-01-25", "rule"
            return A["ncaaf_regular_season_end"], "rule"

        # --- NFL ------------------------------------------------------------
        if league == "nfl":
            if "super bowl" in desc and "division of" not in desc:
                return "2027-02-07", "rule"
            # win totals, division winners, "division of Super Bowl winner"
            return A["nfl_regular_season_end"], "rule"

        # unmatched future: assume season-long, park it a year out so it never
        # masquerades as today's action
        try:
            dt = datetime.strptime(placed, "%Y-%m-%d").date()
            return (dt + timedelta(days=180)).isoformat(), "rule"
        except Exception:
            return placed, "placement"

    # --- game bets ------------------------------------------------------
    # Normally the event is the day the ticket was written. The exception is a
    # game bet bought before its season even opens -- clamp it to Week 1.
    opener = SEASON_OPENERS.get(league)
    if opener and placed and placed < opener[0]:
        return opener[1], "rule"
    return placed, "placement"


def horizon(b):
    """day | week | season -- how the bet should be SURFACED, not how long it sat.

    A game bet is always near-term action even if it was bought weeks early
    (a Week-1 moneyline shopped in August is still a single-game ticket).
    Only futures get bucketed by how far out they settle.
    """
    if not is_future(b):
        return "day"

    ev, _ = settle_date(b)
    placed = _s(b, "Date")
    try:
        d0 = datetime.strptime(placed, "%Y-%m-%d").date()
        d1 = datetime.strptime(ev, "%Y-%m-%d").date()
    except Exception:
        return "season"
    span = (d1 - d0).days
    if span <= DAY_MAX:
        return "day"
    if span <= WEEK_MAX:
        return "week"
    return "season"


def enrich(bets):
    """Attach 'Event Date', '_evsrc' and 'Horizon' to every bet in place."""
    for b in bets:
        ev, src = settle_date(b)
        b["Event Date"] = ev
        b["_evsrc"] = src
        b["Horizon"] = horizon(b)
    return bets


def days_out(b, today=None):
    """Days until settlement. Negative = should already have graded."""
    today = today or date.today()
    try:
        return (datetime.strptime(b.get("Event Date") or "", "%Y-%m-%d").date() - today).days
    except Exception:
        return None


def is_stale(b, today=None, grace=0):
    """Pending bet whose event finished more than `grace` days ago."""
    d = days_out(b, today)
    return d is not None and d < -grace
