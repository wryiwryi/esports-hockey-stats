# esports-hockey-stats

Python scripts for analyzing e-sports hockey statistics and calculating player salaries.

## Overview

This repository contains two main Python scripts:

1. **stats_report.py** — calculates monthly statistics for players, including:
   - Win rate (including technical wins/losses)
   - Shifts played
   - Game results (wins, draws, losses)
   - Technical results for players who dropped out

2. **salary_report.py** — calculates monthly salary for a specific player, including:
   - Base salary
   - Payment per game
   - Bonuses for wins/draws per period
   - Shift bonuses
   - Handling of cancelled matches (as wins or losses depending on configuration)

Example outputs are provided in the `examples/` folder.

## Installation

Python 3.9+ is required. Install dependencies with:

pip install -r requirements.txt

## Usage

Run the scripts with:

python stats_report.py  
python salary_report.py

## Project Structure

esports-hockey-stats/  
├─ stats_report.py        # Player statistics script  
├─ salary_report.py       # Salary calculation script  
├─ requirements.txt       # Python dependencies  
├─ README.md              # Project documentation (this file)  
└─ examples/              # Example outputs  
   ├─ example_stats.txt  
   └─ example_salary.txt  

## Notes

- Scripts are configured for a default team; modify `NICKS` in `stats_report.py` or `NICKNAME` in `salary_report.py` to analyze other players.  
- Timezone is set to UTC+3 by default; adjust if needed.  
- Example outputs in `examples/` show expected script results.
