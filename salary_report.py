# salary_report.py
import asyncio
import aiohttp
from datetime import datetime, timedelta, timezone
from collections import defaultdict

# CONFIG
NICKNAME = "Player1"
YEAR = 2025
MONTH = 9
GAMES_PER_SHIFT = 12
BASE_SALARY = 20000
PAY_PER_GAME = 20
PAY_WIN_GAME = 15
PAY_DRAW_GAME = 7.5
PAY_WIN_PERIOD = 10
PAY_DRAW_PERIOD = 5
PAY_SHIFT_BONUS = 400
CANCELLED_MODE = "as_win"  # or "as_loss"

UTC = timezone.utc
LOCAL_TZ = timezone(timedelta(hours=3))
CONCURRENCY = 10
REQUEST_TIMEOUT = 10
PLAY_STATUS_CODES = {"finished", "ready_to_finish"}


def safe_int(val):
    try:
        return int(val)
    except:
        return 0


async def fetch_json(session, url):
    """Fetch JSON from a placeholder API (mock example)."""
    try:
        async with session.get(url, timeout=REQUEST_TIMEOUT) as r:
            return await r.json()
    except:
        return None


async def fetch_tournaments_for_day(session, date):
    """Return placeholder tournaments for a day."""
    # Example: 3 tournaments per day
    return [{"id": str(i)} for i in range(1, 4)]


async def fetch_matches(session, tournament_id):
    """Return placeholder matches for a tournament."""
    matches = [
        {"participant1": {"nickname": "Player1", "score": 2, "prevPeriodsScores": [1, 0, 1]},
         "participant2": {"nickname": "Player2", "score": 1, "prevPeriodsScores": [0, 1, 0]},
         "status": "finished"},
        {"participant1": {"nickname": "Player3", "score": 0, "prevPeriodsScores": [0, 0, 0]},
         "participant2": {"nickname": "Player4", "score": 0, "prevPeriodsScores": [0, 0, 0]},
         "status": "finished"},
    ]
    return matches


def calculate_salary(matches, nickname):
    """Calculate salary and stats based on matches."""
    played_games = wins_game = draws_game = 0
    wins_period = draws_period = 0
    shifts_count = set()

    for m in matches:
        p1 = m["participant1"]
        p2 = m["participant2"]
        if nickname not in (p1["nickname"], p2["nickname"]):
            continue

        local_date = datetime.now(LOCAL_TZ).date()
        shifts_count.add(local_date)

        # Game result
        player = p1 if p1["nickname"] == nickname else p2
        opponent = p2 if player is p1 else p1
        ps = safe_int(player.get("score"))
        os = safe_int(opponent.get("score"))

        played_games += 1
        if ps > os:
            wins_game += 1
        elif ps == os:
            draws_game += 1

        # Period results
        for pp, op in zip(player.get("prevPeriodsScores", []), opponent.get("prevPeriodsScores", [])):
            if pp > op:
                wins_period += 1
            elif pp == op:
                draws_period += 1

    shifts = len(shifts_count) + played_games / GAMES_PER_SHIFT
    planned_games = shifts * GAMES_PER_SHIFT
    cancelled_games = max(0, planned_games - played_games)

    if CANCELLED_MODE == "as_win":
        wins_game += cancelled_games
        wins_period += cancelled_games * 3
        paid_games = played_games + cancelled_games
    else:
        paid_games = played_games + cancelled_games

    total_salary = (
        BASE_SALARY
        + paid_games * PAY_PER_GAME
        + wins_game * PAY_WIN_GAME
        + draws_game * PAY_DRAW_GAME
        + wins_period * PAY_WIN_PERIOD
        + draws_period * PAY_DRAW_PERIOD
        + shifts * PAY_SHIFT_BONUS
    )

    winrate = ((wins_game + draws_game * 0.5) /
               paid_games * 100) if paid_games else 0.0

    return {
        "played_games": played_games,
        "cancelled_games": cancelled_games,
        "shifts": round(shifts, 2),
        "wins": wins_game,
        "draws": draws_game,
        "winrate": round(winrate, 2),
        "total_salary": round(total_salary, 2)
    }


async def gather_monthly_report(year, month, nickname):
    """Gather matches and calculate salary for the month."""
    all_matches = []
    async with aiohttp.ClientSession() as session:
        days = 3  # placeholder for 3 days
        for day in range(1, days + 1):
            tournaments = await fetch_tournaments_for_day(session, datetime(year, month, day))
            for t in tournaments:
                matches = await fetch_matches(session, t["id"])
                all_matches.extend(matches)

    return calculate_salary(all_matches, nickname)


async def main():
    stats = await gather_monthly_report(YEAR, MONTH, NICKNAME)
    print(f"Player {NICKNAME} salary report for {YEAR}-{MONTH:02d}")
    print(f"Played games: {stats['played_games']}")
    print(f"Cancelled games: {stats['cancelled_games']}")
    print(f"Shifts: {stats['shifts']}")
    print(f"Wins: {stats['wins']}")
    print(f"Draws: {stats['draws']}")
    print(f"Winrate: {stats['winrate']} %")
    print(f"Total salary: ${stats['total_salary']}")


if __name__ == "__main__":
    asyncio.run(main())
