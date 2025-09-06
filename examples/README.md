Hockey Stats Tools

This repository contains two Python scripts for analyzing player statistics
and calculating salaries in e-sports hockey tournaments.

1. Stats Report (stats_report.py)

This script calculates monthly statistics for players, including:

Win rate (including technical wins/losses)

Shifts played

Game results (wins, draws, losses)

Technical results for players who dropped out

Run:

python stats_report.py

The script fetches data from the Esports Battle Hockey API and aggregates statistics for all configured players.

2. Salary Report (salary_report.py)

This script calculates the monthly salary for a specific player, including:

Base salary

Payment per game

Bonuses for wins/draws per period

Shift bonuses

Handling of cancelled matches (as wins or losses depending on configuration)

Run:

python salary_report.py

It also fetches data from the same API and produces detailed statistics for salary calculation.

Dependencies

Python 3.9+

aiohttp

Install dependencies with:

pip install -r requirements.txt

Examples

Example outputs are provided in the examples/ folder:

examples/example_stats.txt → sample output of stats_report.py

examples/example_salary.txt → sample output of salary_report.py

Project Structure

my_hockey_repo/
├─ stats_report.py # Player statistics script
├─ salary_report.py # Salary calculation script
├─ requirements.txt # Python dependencies
├─ README.md # Project documentation
└─ examples/ # Example outputs
├─ example_stats.txt
└─ example_salary.txt

Notes

The scripts are configured for your team by default (list of nicknames inside the scripts).

You can modify NICKS in stats_report.py or NICKNAME in salary_report.py to analyze other players.

Timezone is set to UTC+3 by default; adjust if needed.