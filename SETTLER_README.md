# On-Demand Bet Settler

## Usage

Just say "settle pending bets" (or "settle yesterday's bets") and the agent will:

1. Run `python settle_pending.py --through YYYY-MM-DD` (defaults to today)
2. Show you the proposed settlements grouped by:
   - **Won (high confidence)** — auto-settle approved
   - **Lost (high confidence)** — auto-settle approved
   - **Push** — auto-settle approved
   - **Flagged for manual review** — agent asks you about each
3. On your approval, apply changes to: Google Sheet → dashboard FALLBACK_BETS → git push → deploy

## What it handles automatically

| Bet type | Auto-settles? |
|---|---|
| Moneyline (ML) | Yes |
| Spread / Run line / Puck line | Yes |
| Total Over/Under | Yes |
| Parlay | No (flagged — each leg listed for review) |
| Round Robin | No (flagged — partial settlements need manual P&L) |
| Player props | No (flagged — needs box score data) |
| Futures (season-long) | No (correctly skipped — settles end of season) |
| Golf matchups / tournament | No (flagged — needs leaderboard lookup) |

## Data source

Public ESPN scoreboard API (`site.api.espn.com/.../scoreboard?dates=YYYYMMDD`). Free, no auth, supports MLB / NBA / WNBA / NHL / NFL / NCAAF / NCAAB.

## Promotion to daily cron

Once accuracy is verified across ~5 days of usage:

```
schedule_cron @ 09:00 PT → run settle_pending.py
  → if any high-confidence settlements:
      apply + deploy + send in-app notification with day's P&L
  → else: no notification
```

Estimated daily cost: low (1 ESPN fetch per league per day, all evaluation logic is local Python).
