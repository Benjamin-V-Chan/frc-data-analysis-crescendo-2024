from utility_functions.print_formats import seperation_bar
import os
import json
import traceback

print(seperation_bar)
print("Script 04: Team Based Data Restructuring\n")

# File paths
cleaned_data_path = "data/processed/cleaned_port_h_matchapps.json"
team_performance_path = "outputs/team_data/team_performance.json"

# Functions to restructure and calculate statistics


def restructure_to_team_based(cleaned_file_path, team_file_path):
    """
    Restructures cleaned match data into a team-based format with advanced statistics.

    :param cleaned_file_path: Path to the cleaned JSON file.
    :param team_file_path: Path to save the team-based JSON file.
    """
    try:
        # Load cleaned data
        print(f"[INFO] Loading cleaned data from: {cleaned_file_path}")
        with open(cleaned_file_path, 'r') as infile:
            cleaned_data = json.load(infile)

        if not isinstance(cleaned_data, list):
            raise ValueError("Cleaned data must be a list of matches.")

        # Group matches by team
        team_data = {}
        for match in cleaned_data:
            team = match["metadata"]["robotTeam"]
            if team not in team_data:
                team_data[team] = {"matches": []}
            team_data[team]["matches"].append(match)

        # Add advanced statistics
        for team, data in team_data.items():
            for match in data["matches"]:
                # Advanced statistics for each match
                auto_notes = match["autoNotes"]
                tele_notes = match["teleNotes"]

                match["autoNotesSum"] = sum(auto_notes.values())
                match["teleopNotesSum"] = sum(tele_notes.values())
                match["totalNotes"] = match["autoNotesSum"] + match["teleopNotesSum"]

                match["autoShootNotes"] = auto_notes["near"] + auto_notes["mid"] + auto_notes["far"]
                match["teleopShootNotes"] = tele_notes["near"] + tele_notes["mid"] + tele_notes["far"]

                match["autoMissedNotes"] = auto_notes["miss"]
                match["teleopMissedNotes"] = tele_notes["miss"]

                match["missedNotes"] = match["autoMissedNotes"] + match["teleopMissedNotes"]

                match["shootNotes"] = match["autoShootNotes"] + match["teleopShootNotes"]

        # Save team-based data
        print(f"[INFO] Saving team-based data to: {team_file_path}")
        with open(team_file_path, 'w') as outfile:
            json.dump(team_data, outfile, indent=4)

        print("[INFO] Team-based restructuring completed successfully.")

    except FileNotFoundError as e:
        print(f"[ERROR] Cleaned data file not found: {e}")
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to decode JSON: {e}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred during restructuring: {e}")
        print(traceback.format_exc())


# Main script execution
try:
    os.makedirs(os.path.dirname(team_performance_path), exist_ok=True)
    restructure_to_team_based(cleaned_data_path, team_performance_path)
    print("\nScript 04: Completed.")
except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
    print(traceback.format_exc())
    print("\nScript 04: Failed.")

print(seperation_bar)
