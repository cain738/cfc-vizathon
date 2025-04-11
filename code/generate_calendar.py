import pandas as pd
import random
from datetime import datetime, timedelta
import tabulate
import sys

import os

# Ensure the output directory exists
save_csv_dir = "data/csv"
os.makedirs(save_csv_dir, exist_ok=True)



# Save the datasets to a CSV file
def save_to_csv(df, filename, pathname):
    df.to_csv(os.path.join(pathname, filename), index=False)
    print(f"Dataset saved to {filename} in {pathname}")

# ---------------------

# Reconfigure stdout to use UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

def display(df):
    """Display the DataFrame in a table format."""
    print(tabulate.tabulate(df, headers='keys', tablefmt='psql', showindex=False))

# Define the date range for the calendar dataset: 1st August to 31st August 2024.
start_date = datetime(2024, 8, 1)
end_date = datetime(2024, 8, 31)
dates = pd.date_range(start_date, end_date)

# List of Chelsea FC players (now including Hakim Ziyech).
players = [
    "Kepa Arrizabalaga", "Édouard Mendy", "Reece James", "Ben Chilwell", 
    "César Azpilicueta", "Andreas Christensen", "Marcos Alonso", "N'Golo Kanté",
    "Jorginho", "Mason Mount", "Kai Havertz", "Christian Pulisic", "Mateo Kovačić", 
    "Conor Gallagher", "Timo Werner", "Olivier Giroud", "Tammy Abraham", 
    "Armando Broja", "Ross Barkley", "Callum Hudson-Odoi", "Emerson Palmieri", 
    "Ricardo Pereira", "João Félix", "Hakim Ziyech"   # Added Hakim Ziyech as RW
]

# Assign a primary position to each player based on rough positional data.
player_positions = {
    "Kepa Arrizabalaga": "GK",
    "Édouard Mendy": "GK",
    "Reece James": "RB",
    "Ben Chilwell": "LB",
    "César Azpilicueta": "CB",
    "Andreas Christensen": "CB",
    "Marcos Alonso": "LB",
    "N'Golo Kanté": "DM",            # Defensive Midfielder
    "Jorginho": "CDM",              # Central Defensive Midfielder
    "Mason Mount": "CAM",           # Attacking Midfielder
    "Kai Havertz": "WM",            # Wide/Attacking Midfielder
    "Christian Pulisic": "LW",      # Left Wing
    "Mateo Kovačić": "CM",          # Central Midfielder
    "Conor Gallagher": "CM",        # Central Midfielder
    "Timo Werner": "CF",            # Centre Forward
    "Olivier Giroud": "ST",         # Striker
    "Tammy Abraham": "ST",          # Striker
    "Armando Broja": "CF",          # Centre Forward
    "Ross Barkley": "CM",           # Central Midfielder
    "Callum Hudson-Odoi": "LW",     # Left Wing
    "Emerson Palmieri": "LB",       # Left Back
    "Ricardo Pereira": "CB",        # Centre Back
    "João Félix": "CF",             # Centre Forward
    "Hakim Ziyech": "RW"            # Right Wing
}

# Define the two formations the team may use on matchdays.
formations = ["4-3-3", "4-2-3-1"]

# Function to simulate training load based on session type and playing status.
def simulate_training_load(session_type, playing_status=None):
    if session_type == "Match":
        if playing_status == "Starting":
            return random.randint(90, 110)
        elif playing_status == "Substitute":
            return random.randint(70, 90)
        elif playing_status == "Not Selected":
            return random.randint(40, 60)
        else:
            return random.randint(40, 60)
    elif session_type == "Training":
        return random.randint(50, 70)
    else:
        return 0

# Function to assign session type based on the day of the week.
def get_session_type(date):
    weekday = date.weekday()  # Monday = 0, Sunday = 6.
    if weekday >= 5:
        return "Match"         # Saturdays and Sundays.
    elif weekday in [0, 2, 4]:
        return "Training"      # Mondays, Wednesdays, and Fridays.
    else:
        return "Rest"          # Other days are rest days (not used here)

# Simulate the calendar dataset.
calendar_rows = []

for date in dates:
    session_type = get_session_type(date)
    # Only include matchdays and training days in our simulation.
    if session_type in ["Match", "Training"]:
        if session_type == "Match":
            # Randomly select a formation for the match.
            formation = random.choice(formations)
            # Randomly select 11 players for the starting XI.
            starting = random.sample(players, 11)
            # Randomly select substitutes from the remaining players (e.g., 4 players).
            remaining = [p for p in players if p not in starting]
            substitutes = random.sample(remaining, 4) if len(remaining) >= 4 else remaining
        else:
            formation = "TRAIN"  # Label training sessions.
            starting = []        # Not applicable.
            substitutes = []
        
        # Simulate training load for each player on the day.
        for player in players:
            if session_type == "Match":
                if player in starting:
                    playing_status = "Starting"
                elif player in substitutes:
                    playing_status = "Substitute"
                else:
                    playing_status = "Not Selected"
            else:
                playing_status = "Training"
            training_load = simulate_training_load(session_type, playing_status)
            calendar_rows.append({
                "date": date.strftime("%Y-%m-%d"),
                "session_type": session_type,
                "formation": formation,
                "player": player,
                "position": player_positions.get(player, ""),
                "playing_status": playing_status,
                "training_load": training_load
            })

# Create the calendar DataFrame.
calendar_df = pd.DataFrame(calendar_rows)

# Display a sample of the simulated calendar dataset.
display(calendar_df.sample(20).reset_index(drop=True))
save_to_csv(calendar_df, "chelsea_fc_calendar.csv", save_csv_dir)