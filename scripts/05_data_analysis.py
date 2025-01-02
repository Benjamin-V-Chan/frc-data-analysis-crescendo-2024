from utility_functions.print_formats import seperation_bar
import os
import json
import traceback
import pandas as pd

print(seperation_bar)
print("Script 05: Data Analysis & Team Statistics Aggregation\n")

# File paths
team_matches_path = "data/processed/cleaned_port_h_team_matches.json"
team_statistics_path = "outputs/team_data/team_statistics.json"

# Helper Functions


def convert_to_serializable(obj):
    """
    Converts all non-serializable types (like NumPy types) to Python native types.

    :param obj: Object to convert.
    :return: Serializable object.
    """
    if isinstance(obj, (pd.Series, pd.DataFrame)):
        return obj.to_dict()
    if isinstance(obj, (pd.Timestamp, pd.Timedelta)):
        return str(obj)
    if isinstance(obj, (pd.Int64Dtype, pd.Float64Dtype)):
        return float(obj)
    if isinstance(obj, (int, float, str, bool, list, dict)):
        return obj
    if hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes)):
        return [convert_to_serializable(item) for item in obj]
    return obj


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
        stats = {}

        # Number of matches played
        stats["number_of_matches"] = len(df)

        # Process quantitative statistics
        quantitative_metrics = ["totalNotes", "missedNotes", "shootNotes", "autoNotesSum", "teleopNotesSum"]
        for metric in quantitative_metrics:
            if metric in df:
                stats[f"{metric}_average"] = float(df[metric].mean())
                stats[f"{metric}_min"] = int(df[metric].min())
                stats[f"{metric}_max"] = int(df[metric].max())
                stats[f"{metric}_std_dev"] = float(df[metric].std())

        # Process categorical statistics
        categorical_metrics = ["climb"]
        for metric in categorical_metrics:
            if metric in df:
                stats[f"{metric}_value_counts"] = df[metric].value_counts().to_dict()

        # Process binary statistics
        binary_metrics = ["leftStartingZone"]
        for metric in binary_metrics:
            if metric in df:
                stats[f"{metric}_percent_true"] = float(df[metric].mean() * 100)

        # Add processed statistics for the team
        team_statistics[team] = stats

    return team_statistics


# Main Script Execution
try:
    print(f"[INFO] Loading team performance data from: {team_matches_path}")
    with open(team_matches_path, 'r') as infile:
        team_data = json.load(infile)

    if not isinstance(team_data, dict):
        raise ValueError("Team performance data must be a dictionary.")

    print("[INFO] Calculating team statistics.")
    team_statistics = calculate_team_statistics(team_data)

    # Convert data to serializable format
    team_statistics_serializable = convert_to_serializable(team_statistics)

    print(f"[INFO] Saving team statistics to: {team_statistics_path}")
    os.makedirs(os.path.dirname(team_statistics_path), exist_ok=True)
    with open(team_statistics_path, 'w') as outfile:
        json.dump(team_statistics_serializable, outfile, indent=4)

    print("[INFO] Team performance statistics aggregation completed successfully.")

except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
    print(traceback.format_exc())

print(seperation_bar)
