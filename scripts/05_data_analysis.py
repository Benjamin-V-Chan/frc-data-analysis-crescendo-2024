from utility_functions.print_formats import seperation_bar
import pandas as pd
import os
import traceback

print(seperation_bar)
print("Script 05: Data Analysis\n")

# File paths
advanced_team_data_path = "data/processed/team_advanced_performance.json"
output_analysis_path = "outputs/team_data/team_analysis.json"

try:
    # Check if advanced team data file exists
    if not os.path.exists(advanced_team_data_path):
        raise FileNotFoundError(f"Advanced team data file not found: {advanced_team_data_path}")

    # Load the advanced team performance data
    print(f"[INFO] Loading advanced team data from: {advanced_team_data_path}")
    advanced_team_df = pd.read_json(advanced_team_data_path, orient="index")

    # Ensure the DataFrame is not empty
    if advanced_team_df.empty:
        raise ValueError(f"Advanced team data is empty. Check the file: {advanced_team_data_path}")

    # Prepare a new DataFrame for team-level analysis
    team_analysis = []

    for team, data in advanced_team_df.iterrows():
        matches = data["matches"]

        # Separate quantitative, categorical, and binary statistics
        quantitative_columns = [
            "autoNotesSum", "teleopNotesSum", "autoShootNotes", "teleopShootNotes",
            "totalShootNotes", "totalNotes", "totalAmpNotes", "totalMissedNotes"
        ]
        categorical_columns = ["climb"]
        binary_columns = ["leftStartingZone"]

        # Initialize aggregated statistics
        team_stats = {"team": team}

        # Process quantitative columns
        for col in quantitative_columns:
            if col in matches[0]:
                col_data = pd.Series([match[col] for match in matches])
                team_stats[f"{col}_avg"] = col_data.mean()
                team_stats[f"{col}_min"] = col_data.min()
                team_stats[f"{col}_max"] = col_data.max()
                team_stats[f"{col}_std"] = col_data.std()

        # Process categorical columns
        for col in categorical_columns:
            if col in matches[0]:
                col_data = pd.Series([match[col] for match in matches])
                col_freq = col_data.value_counts()
                for category, count in col_freq.items():
                    team_stats[f"{col}_{category}_freq"] = count

        # Process binary columns
        for col in binary_columns:
            if col in matches[0]:
                col_data = pd.Series([match[col] for match in matches])
                team_stats[f"{col}_percent_true"] = col_data.mean() * 100

        # Calculate missed notes percentage
        if "totalMissedNotes_avg" in team_stats and "totalNotes_avg" in team_stats:
            team_stats["missed_notes_percent"] = (
                team_stats["totalMissedNotes_avg"] / team_stats["totalNotes_avg"] * 100
            )

        # Append team stats
        team_analysis.append(team_stats)

    # Convert the aggregated statistics into a DataFrame
    team_analysis_df = pd.DataFrame(team_analysis)

    # Ensure output directories exist
    processed_data_dir = os.path.dirname(output_analysis_path)
    os.makedirs(processed_data_dir, exist_ok=True)

    # Save team analysis as JSON
    print(f"[INFO] Saving team analysis to: {output_analysis_path}")
    team_analysis_df.to_json(output_analysis_path, orient="records", indent=4)

    print("\nScript 05: Completed.")

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
