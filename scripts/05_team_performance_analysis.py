from utility_functions.print_formats import seperation_bar
import os
import json
import traceback
import pandas as pd
from collections import defaultdict

print(seperation_bar)
print("Script 05: Team Performance Statistics Aggregation\n")

# File paths
team_performance_path = "data/processed/team_performance.json"
team_statistics_path = "data/processed/team_statistics.json"

# Helper Functions


def calculate_team_statistics(team_data):
    """
    Calculates advanced statistics for each team.

    :param team_data: Dictionary containing match data for each team.
    :return: A dictionary with aggregated team statistics.
    """
    team_statistics = {}

    for team, data in team_data.items():
        matches = data["matches"]
        df = pd.DataFrame(matches)

        # Initialize statistics dictionary for this team
        stats = {
            "quantitative": {},
            "categorical": {},
            "binary": {}
        }

        # Process quantitative statistics
        quantitative_metrics = ["totalNotes", "missedNotes", "shootNotes", "autoNotesSum", "teleopNotesSum"]
        for metric in quantitative_metrics:
            if metric in df:
                stats["quantitative"][metric] = {
                    "average": df[metric].mean(),
                    "min": df[metric].min(),
                    "max": df[metric].max(),
                    "std_dev": df[metric].std()
                }

        # Process categorical statistics
        categorical_metrics = ["climb"]
        for metric in categorical_metrics:
            if metric in df:
                stats["categorical"][metric] = df[metric].value_counts().to_dict()

        # Process binary statistics
        binary_metrics = ["leftStartingZone"]
        for metric in binary_metrics:
            if metric in df:
                stats["binary"][metric] = {
                    "percent_true": df[metric].mean() * 100
                }

        # Add processed statistics for the team
        team_statistics[team] = stats

    return team_statistics


# Main Script Execution
try:
    print(f"[INFO] Loading team performance data from: {team_performance_path}")
    with open(team_performance_path, 'r') as infile:
        team_data = json.load(infile)

    if not isinstance(team_data, dict):
        raise ValueError("Team performance data must be a dictionary.")

    print("[INFO] Calculating team statistics.")
    team_statistics = calculate_team_statistics(team_data)

    print(f"[INFO] Saving team statistics to: {team_statistics_path}")
    os.makedirs(os.path.dirname(team_statistics_path), exist_ok=True)
    with open(team_statistics_path, 'w') as outfile:
        json.dump(team_statistics, outfile, indent=4)

    print("[INFO] Team performance statistics aggregation completed successfully.")

except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
    print(traceback.format_exc())

print(seperation_bar)
