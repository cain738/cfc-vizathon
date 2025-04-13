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

# ---------------------
# 1. Simulation Setup & Helper Functions
# ---------------------

# Updated players list (24 players including Hakim Ziyech)
players = [
    "Kepa Arrizabalaga", "Édouard Mendy", "Reece James", "Ben Chilwell", 
    "César Azpilicueta", "Andreas Christensen", "Marcos Alonso", "N'Golo Kanté",
    "Jorginho", "Mason Mount", "Kai Havertz", "Christian Pulisic", "Mateo Kovačić", 
    "Conor Gallagher", "Timo Werner", "Olivier Giroud", "Tammy Abraham", 
    "Armando Broja", "Ross Barkley", "Callum Hudson-Odoi", "Emerson Palmieri", 
    "Ricardo Pereira", "João Félix", "Hakim Ziyech"
]

# Positional mapping – note Hakim Ziyech now mapped as RW.
player_positions = {
    "Kepa Arrizabalaga": "GK",
    "Édouard Mendy": "GK",
    "Reece James": "RB",
    "Ben Chilwell": "LB",
    "César Azpilicueta": "CB",
    "Andreas Christensen": "CB",
    "Marcos Alonso": "LB",
    "N'Golo Kanté": "DM",
    "Jorginho": "CDM",
    "Mason Mount": "CAM",
    "Kai Havertz": "WM",
    "Christian Pulisic": "LW",
    "Mateo Kovačić": "CM",
    "Conor Gallagher": "CM",
    "Timo Werner": "CF",
    "Olivier Giroud": "ST",
    "Tammy Abraham": "ST",
    "Armando Broja": "CF",
    "Ross Barkley": "CM",
    "Callum Hudson-Odoi": "LW",
    "Emerson Palmieri": "LB",
    "Ricardo Pereira": "CB",
    "João Félix": "CF",
    "Hakim Ziyech": "RW"
}

# Define formation choices for matchdays.
formations = ["4-3-3", "4-2-3-1"]

# Set the simulation period (1st August to 31st August 2024)
start_date = datetime(2024, 8, 1)
end_date = datetime(2024, 8, 31)
all_dates = pd.date_range(start_date, end_date)

# Function to get session type based on the day of the week.
def get_session_type(date):
    weekday = date.weekday()  # Monday = 0, Sunday = 6.
    if weekday >= 5:
        return "Match"         # Saturdays & Sundays assumed as match days.
    elif weekday in [0, 2, 4]:
        return "Training"      # Monday, Wednesday, Friday for training.
    else:
        return "Rest"          # The remaining days (e.g., Tuesday, Thursday) as rest days.

# GPS metrics simulation: intensity dependent on whether session is a match or training.
def simulate_gps_metrics(session_type):
    if session_type == 'Match':
        distance = random.randint(10000, 12000)
        day_duration = random.randint(90, 95)
        peak_speed = round(random.uniform(30, 35), 2)
    elif session_type == 'Training':
        distance = random.randint(4000, 8000)
        day_duration = random.randint(60, 85)
        peak_speed = round(random.uniform(25, 30), 2)
    else:
        return None
    # Simulate additional metrics as percentages of total distance
    distance_over_21 = int(distance * random.uniform(0.2, 0.4))
    distance_over_24 = int(distance * random.uniform(0.1, 0.3))
    distance_over_27 = int(distance * random.uniform(0.05, 0.15))
    # Simulate acceleration / deceleration events.
    accel_decel_over_2_5 = random.randint(20, 40)
    accel_decel_over_3_5 = random.randint(10, 25)
    accel_decel_over_4_5 = random.randint(5, 15)
    # Heart rate zones (minutes)
    hr_zone_1 = random.randint(5, 10)
    hr_zone_2 = random.randint(10, 20)
    hr_zone_3 = random.randint(15, 25)
    hr_zone_4 = random.randint(5, 15)
    hr_zone_5 = random.randint(2, 10)
    
    return {
        'distance': distance,
        'distance_over_21': distance_over_21,
        'distance_over_24': distance_over_24,
        'distance_over_27': distance_over_27,
        'accel_decel_over_2_5': accel_decel_over_2_5,
        'accel_decel_over_3_5': accel_decel_over_3_5,
        'accel_decel_over_4_5': accel_decel_over_4_5,
        'day_duration': day_duration,
        'peak_speed': peak_speed,
        'hr_zone_1_hms': hr_zone_1,
        'hr_zone_2_hms': hr_zone_2,
        'hr_zone_3_hms': hr_zone_3,
        'hr_zone_4_hms': hr_zone_4,
        'hr_zone_5_hms': hr_zone_5,
    }

# Physical Capability simulation: tests every Monday.
def simulate_physical_capability(session_date):
    movements = {
        'Agility': ['Acceleration'],
        'Sprint': ['Max velocity'],
        'Upper Body': ['Push', 'Pull'],
        'Jump': ['Take off', 'Land']
    }
    expressions = ['Isometric', 'Dynamic']
    rows = []
    for movement, qualities in movements.items():
        for quality in qualities:
            for expr in expressions:
                BenchmarkPct = round(random.uniform(90, 110), 2)
                rows.append({
                    'date': session_date,
                    'movement': movement,
                    'quality': quality,
                    'expression': expr,
                    'BenchmarkPct': BenchmarkPct
                })
    return rows

# Recovery Status simulation: daily collection for each player.
def simulate_recovery_status():
    categories = ['Bio', 'Msk_joint_range', 'Msk_load_tolerance', 'Subjective', 'Soreness', 'Sleep']
    data = {}
    for cat in categories:
        completeness = round(random.uniform(0.8, 1.0), 2) if random.random() > 0.1 else None
        composite = round(random.uniform(-10, 10), 2) if completeness is not None else None
        data[f'{cat}_completeness'] = completeness
        data[f'{cat}_composite'] = composite
    composites = [val for key, val in data.items() if 'composite' in key and val is not None]
    overall = round(sum(composites) / len(composites), 2) if composites else None
    data['emboss_baseline_score'] = overall
    return data

# Individual Priority Areas simulation: combining generic with role-specific priorities.
def simulate_priority_areas(player, role):
    generic_priorities = [
        {
            'priority_category': 'Recovery',
            'area': 'Sleep',
            'target_performance': 'Increase average sleep by 1hr per night',
            'type': 'Habit'
        },
        {
            'priority_category': 'Performance',
            'area': 'Sprint',
            'target_performance': 'Achieve >65% in max velocity score',
            'type': 'Outcome'
        },
        {
            'priority_category': 'Recovery',
            'area': 'Nutrition',
            'target_performance': 'Consume 45g carbohydrate at halftime',
            'type': 'Habit'
        }
    ]
    role_specific = {
        'Attacker': [
            {
                'priority_category': 'Performance',
                'area': 'Finishing',
                'target_performance': 'Improve goal conversion rate by 10%',
                'type': 'Outcome'
            },
            {
                'priority_category': 'Performance',
                'area': 'Dribbling',
                'target_performance': 'Enhance dribbling skills under pressure',
                'type': 'Habit'
            }
        ],
        'Midfielder': [
            {
                'priority_category': 'Performance',
                'area': 'Passing Accuracy',
                'target_performance': 'Achieve >85% pass accuracy',
                'type': 'Outcome'
            },
            {
                'priority_category': 'Performance',
                'area': 'Ball Control',
                'target_performance': 'Improve first touch and dribbling under pressure',
                'type': 'Habit'
            }
        ],
        'Defender': [
            {
                'priority_category': 'Performance',
                'area': 'Tackling',
                'target_performance': 'Achieve a 75% successful tackle rate',
                'type': 'Outcome'
            },
            {
                'priority_category': 'Performance',
                'area': 'Aerial Duels',
                'target_performance': 'Increase aerial challenge win percentage by 10%',
                'type': 'Outcome'
            }
        ]
    }
    # Define a simple role mapping for simulation purposes.
    # Here we assume attackers include players with positions CF, ST, LW, RW, WM.
    # Midfielders include CAM, CM, CDM.
    # Defenders include GK, LB, RB, CB.
    if role not in ['Attacker', 'Midfielder', 'Defender']:
        # Fallback: use generic if role unknown.
        assigned_role = None
    else:
        assigned_role = role

    # For the purposes of simulation, decide on the role group based on the primary position.
    # Here we have already assigned positions. For example, if a player's position is in:
    #  - {"CF", "ST", "LW", "RW", "WM"} we treat them as Attacker.
    #  - {"CAM", "CM", "CDM"} as Midfielder.
    #  - {"GK", "LB", "RB", "CB"} as Defender.
    attackers = {"CF", "ST", "LW", "RW", "WM"}
    midfielders = {"CAM", "CM", "CDM"}
    defenders = {"GK", "LB", "RB", "CB"}
    pos = player_positions.get(player, "")
    if pos in attackers:
        role_group = "Attacker"
    elif pos in midfielders:
        role_group = "Midfielder"
    elif pos in defenders:
        role_group = "Defender"
    else:
        role_group = "Attacker"  # Default
    selected_role = role_specific.get(role_group, [])
    # Randomly choose 2 generic and 2 role-specific priorities.
    selected_generic = random.sample(generic_priorities, 2)
    selected_role_spec = random.sample(selected_role, 2) if len(selected_role) >= 2 else selected_role
    final_priorities = selected_generic + selected_role_spec
    for priority in final_priorities:
        priority['player'] = player
        priority['target_set_date'] = '2024-08-07'
        priority['review_date'] = '2024-08-14'
        priority['tracking_status'] = random.choice(['On Track', 'Achieved', 'At Risk'])
    return final_priorities

# ---------------------
# 2. Generate the Datasets
# ---------------------

# A. GPS Dataset
gps_rows = []
# Generate records only for Match and Training days
for date in all_dates:
    session_type = get_session_type(date)
    if session_type in ["Match", "Training"]:
        # For matchdays, include opposition details.
        if session_type == "Match":
            # For demo purposes, use a simple static opposition
            opposition_full = random.choice(["Manchester United", "Arsenal", "Liverpool", 
                                              "Manchester City", "Tottenham", "Everton", 
                                              "Leicester City", "Southampton"])
            opposition_code = opposition_full[:3].upper()
        else:
            opposition_full = "TRAIN"
            opposition_code = "TRN"
        
        # For each player on that day
        for player in players:
            metrics = simulate_gps_metrics(session_type)
            if metrics:
                record = {
                    'date': date.strftime("%Y-%m-%d"),
                    'player': player,
                    'session_type': session_type,
                    'opposition_code': opposition_code,
                    'opposition_full': opposition_full,
                    'season': '2024-25'
                }
                record.update(metrics)
                gps_rows.append(record)
gps_df = pd.DataFrame(gps_rows)
print("GPS Data Sample:")
display(gps_df.head(10))
save_to_csv(gps_df, "gps_data.csv", save_csv_dir)

# B. Physical Capability Dataset (simulate on Mondays)
phys_rows = []
for date in all_dates:
    if date.weekday() == 0:  # Monday
        for player in players:
            tests = simulate_physical_capability(date.strftime("%Y-%m-%d"))
            for t in tests:
                t['player'] = player
                phys_rows.append(t)
phys_df = pd.DataFrame(phys_rows)
print("\nPhysical Capability Data Sample:")
display(phys_df.head(10))
save_to_csv(phys_df, "physical_capability.csv", save_csv_dir)

# C. Recovery Status Dataset (daily for every player)
recovery_rows = []
for date in all_dates:
    for player in players:
        recovery = simulate_recovery_status()
        rec_record = {
            'date': date.strftime("%Y-%m-%d"),
            'player': player
        }
        rec_record.update(recovery)
        recovery_rows.append(rec_record)
recovery_df = pd.DataFrame(recovery_rows)
print("\nRecovery Status Data Sample:")
display(recovery_df.head(10))
save_to_csv(recovery_df, "recovery_status.csv", save_csv_dir)

# D. Individual Priority Areas Dataset (using role-based logic)
priority_rows = []
for player in players:
    # Determine role group based on position using our simple grouping:
    pos = player_positions.get(player, "")
    if pos in {"CF", "ST", "LW", "RW", "WM"}:
        role_group = "Attacker"
    elif pos in {"CAM", "CM", "CDM"}:
        role_group = "Midfielder"
    else:
        role_group = "Defender"
    priorities = simulate_priority_areas(player, role_group)
    for pri in priorities:
        priority_rows.append(pri)
priority_df = pd.DataFrame(priority_rows)
print("\nIndividual Priority Areas Sample:")
display(priority_df.head(10))
save_to_csv(priority_df, "individual_priority_areas.csv", save_csv_dir)
