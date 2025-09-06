# stats_report.py
"""
Hockey Stats Tools — Player Monthly Statistics

This script calculates monthly statistics for a team of players,
including winrate, shifts played, wins, draws, losses, and technical results.

Example usage:
    python stats_report.py
"""

import asyncio
import aiohttp
from datetime import datetime, timedelta, timezone
import calendar
from collections import defaultdict

# Example player names, replace with real team nicknames if needed
PLAYER_NICKS = ["Player1", "Player2", "Player3", "Player4", "Player5"]
GAMES_PER_SHIFT = 12
UTC = timezone.utc
LOCAL_TZ = timezone(timedelta(hours=3))


async def fetch_json(session, url):
    """
    Fetch JSON data from a URL using aiohttp.
    Returns None on failure.
    """
    try:
        async with session.get(url, timeout=10) as resp:
            return await resp.json()
    except Exception:
        return None


def get_date_range(date):
    """
    Return the start and end datetime of a given day in UTC ISO format.
    """
    start = date.replace(hour=0, minute=0, second=0,
                         microsecond=0, tzinfo=LOCAL_TZ)
    end = date.replace(hour=23, minute=59, second=59,
                       microsecond=999999, tzinfo=LOCAL_TZ)
    return (
        start.astimezone(UTC).isoformat().replace('+00:00', 'Z'),
        end.astimezone(UTC).isoformat().replace('+00:00', 'Z')
    )


async def gather_tournament_data(session, tournament_id):
    """
    Gather tournament data and return matches and technical results.
    Example implementation uses placeholder data.
    """
    matches = [
        {"participant1": {"nickname": "Player1", "score": 2},
         "participant2": {"nickname": "Player2", "score": 1}},
        {"participant1": {"nickname": "Player3", "score": 0},
         "participant2": {"nickname": "Player4", "score": 0}},
    ]
    tech_wins, tech_losses = defaultdict(int), defaultdict(int)
    player_stats = {nick: {"gp": 1, "w": 1, "d": 0, "l": 0} for nick in PLAYER_NICKS}
    return matches, dict(tech_wins), dict(tech_losses), player_stats


async def calculate_player_stats(year, month, nickname):
    """
    Calculate monthly stats for a single player, including:
    - Total games
    - Wins, draws, losses
    - Shifts played
    - Winrate (including draws counted as 0.5)
    """
    async with aiohttp.ClientSession() as session:
        all_matches = []

        # Example: process first 3 days of the month
        for day in range(1, 4):
            # Example tournament IDs for the day
            tournament_ids = [str(i) for i in range(1, 4)]
            for tid in tournament_ids:
                matches, tech_w, tech_l, _ = await gather_tournament_data(session, tid)
                all_matches.extend(matches)

        # Count wins, draws, losses
        wins = draws = losses = 0
        for match in all_matches:
            if nickname in (match["participant1"]["nickname"], match["participant2"]["nickname"]):
                s1 = match["participant1"]["score"]
                s2 = match["participant2"]["score"]

                if (match["participant1"]["nickname"] == nickname and s1 > s2) or \
                   (match["participant2"]["nickname"] == nickname and s2 > s1):
                    wins += 1
                elif s1 == s2:
                    draws += 1
                else:
                    losses += 1

        total_games = wins + draws + losses
        winrate = round(((wins + draws * 0.5) / total_games) * 100, 1) if total_games else 0

        return {
            "total_games": total_games,
            "winrate": winrate,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "shifts": round(total_games / GAMES_PER_SHIFT, 2)
        }


async def main():
    """
    Main function to calculate and display monthly statistics for all players.
    """
    year, month = 2025, 9
    print(f"Calculating monthly stats for {year}-{month:02d}...\n")

    tasks = [calculate_player_stats(year, month, nick) for nick in PLAYER_NICKS]
    results = await asyncio.gather(*tasks)

    # Combine player names with stats and sort by winrate
    stats_list = list(zip(PLAYER_NICKS, results))
    stats_list.sort(key=lambda x: x[1]['winrate'], reverse=True)

    # Display results
    print(f"🏆 Top players for {year}-{month:02d}\n")
    for rank, (player, stats) in enumerate(stats_list, 1):
        print(
            f"{rank}. {player:<10} | {stats['winrate']:5.1f}% | "
            f"{stats['shifts']:.1f} Shifts | "
            f"{stats['wins']}-{stats['draws']}-{stats['losses']}"
        )


if __name__ == "__main__":
    asyncio.run(main())
