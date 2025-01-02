from utility_functions.print_formats import seperation_bar
import pandas as pd
import os
import traceback

print(seperation_bar)
print("Script 04: Advanced Team Statistics\n")

# File paths
processed_team_data_path = "data/processed/team_performance.json"
advanced_team_data_path = "data/processed/team_advanced_performance.json"

try:
    # Check if processed team data file exists
    if not os.path.exists(processed_team_data_path):
        raise FileNotFoundError(f"Processed team data file not found: {processed_team_data_path}")

    # Load the processed team performance data
    print(f"[INFO] Loading processed team data from: {processed_team_data_path}")
    team_performance_df = pd.read_json(processed_team_data_path, orient="index")

    # Ensure the DataFrame is not empty
    if team_performance_df.empty:
        raise ValueError(f"Processed team data is empty. Check the file: {processed_team_data_path}")

    # Add advanced statistics for each team's matches
    advanced_performance = {}

    for team, data in team_performance_df.iterrows():
        matches = data["matches"]
        advanced_matches = []

        for match in matches:
            # Initialize advanced statistics
            auto_notes_sum = sum(match["autoNotes"][k] for k in match["autoNotes"] if k != "miss")
            teleop_notes_sum = sum(match["teleNotes"][k] for k in match["teleNotes"] if k != "miss")

            auto_shoot_notes = match["autoNotes"]["near"] + match["autoNotes"]["mid"] + match["autoNotes"]["far"]
            teleop_shoot_notes = match["teleNotes"]["near"] + match["teleNotes"]["mid"] + match["teleNotes"]["far"]

            total_shoot_notes = auto_shoot_notes + teleop_shoot_notes
            total_notes = auto_notes_sum + teleop_notes_sum
            total_amp_notes = match["autoNotes"]["amp"] + match["teleNotes"]["amp"]
            total_missed_notes = match["autoNotes"]["miss"] + match["teleNotes"]["miss"]

            # Add advanced statistics to the match
            match["autoNotesSum"] = auto_notes_sum
            match["teleopNotesSum"] = teleop_notes_sum
            match["autoShootNotes"] = auto_shoot_notes
            match["teleopShootNotes"] = teleop_shoot_notes
            match["totalShootNotes"] = total_shoot_notes
            match["totalNotes"] = total_notes
            match["totalAmpNotes"] = total_amp_notes
            match["totalMissedNotes"] = total_missed_notes

            advanced_matches.append(match)

        advanced_performance[team] = {"matches": advanced_matches}

    # Convert the dictionary to a DataFrame
    advanced_performance_df = pd.DataFrame.from_dict(advanced_performance, orient="index")

    # Ensure output directories exist
    processed_data_dir = os.path.dirname(advanced_team_data_path)

    os.makedirs(processed_data_dir, exist_ok=True)

    # Save advanced team performance as JSON
    print(f"[INFO] Saving advanced team performance to: {advanced_team_data_path}")
    advanced_performance_df.to_json(advanced_team_data_path, orient="index", indent=4)

    print("\nScript 04: Completed.")

except FileNotFoundError as fnf_error:
    print(f"[ERROR] File not found: {fnf_error}")
except ValueError as value_error:
    print(f"[ERROR] Data validation error: {value_error}")
except PermissionError as perm_error:
    print(f"[ERROR] Permission denied while accessing a file: {perm_error}")
except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
    print(traceback.format_exc())

print(seperation_bar)