from utility_functions.print_formats import seperation_bar
import pandas as pd
import os
import json
import traceback

print(seperation_bar)
print("Script 03: Team Performance Processing\n")

# File paths
raw_matchapps_data_path = "data/raw/raw_port_h_matchapps.json"
processed_team_data_path = "data/processed/team_performance.json"
output_statistics_path = "outputs/statistics/data_preprocessing_stats.txt"

try:
    # Check if raw data file exists
    if not os.path.exists(raw_matchapps_data_path):
        raise FileNotFoundError(f"Raw data file not found: {raw_matchapps_data_path}")

    # Load the raw JSON data
    print(f"[INFO] Loading raw match data from: {raw_matchapps_data_path}")
    matchapps_df = pd.read_json(raw_matchapps_data_path)

    # Display the shape of the raw data
    raw_data_shape = f"Raw Data Shape: {matchapps_df.shape}\n"
    print(raw_data_shape)

    # Preprocess the data: Reshape to group by teams
    print("[INFO] Reshaping data to group by teams.")
    team_performance = {}

    for _, match in matchapps_df.iterrows():
        team = match["metadata"]["robotTeam"]
        match_data = {
            "matchNumber": match["metadata"]["matchNumber"],
            "robotPosition": match["metadata"]["robotPosition"],
            "leftStartingZone": match["leftStartingZone"],
            "autoNotes": match["autoNotes"],
            "teleNotes": match["teleNotes"],
            "trapNotes": match["trapNotes"],
            "climb": match["climb"]
        }

        if team not in team_performance:
            team_performance[team] = {"matches": []}

        team_performance[team]["matches"].append(match_data)

    # Convert the dictionary to a DataFrame
    team_performance_df = pd.DataFrame.from_dict(team_performance, orient="index")

    # Ensure output directories exist
    processed_data_dir = os.path.dirname(processed_team_data_path)
    output_statistics_dir = os.path.dirname(output_statistics_path)

    os.makedirs(processed_data_dir, exist_ok=True)
    os.makedirs(output_statistics_dir, exist_ok=True)

    # Save team performance data as JSON
    print(f"[INFO] Saving processed team data to: {processed_team_data_path}")
    team_performance_df.to_json(processed_team_data_path, orient="index", indent=4)

    # Save some statistics about the processing
    processed_data_shape = f"Processed Data Shape: {team_performance_df.shape}\n"
    print(processed_data_shape)
    with open(output_statistics_path, 'w') as f:
        f.write(raw_data_shape)
        f.write(processed_data_shape)

    print("\nScript 03: Successfully Completed.")

except FileNotFoundError as fnf_error:
    print(f"[ERROR] File not found: {fnf_error}")
except pd.errors.EmptyDataError:
    print("[ERROR] The input JSON file is empty or improperly formatted.")
except PermissionError as perm_error:
    print(f"[ERROR] Permission denied while accessing a file: {perm_error}")
except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
    print(traceback.format_exc())

print(seperation_bar)