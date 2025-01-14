from utility_functions.print_formats import seperation_bar
import os
import json
import traceback
from collections import defaultdict

# File paths
raw_data_path = "data/raw/raw_port_h_matchapps.json"
cleaned_data_path = "data/processed/cleaned_port_h_matchapps.json"
scouter_leaderboard_path = "outputs/statistics/scouter_error_leaderboard.txt"

# Correct structure
EXPECTED_STRUCTURE = {
    "_id": {"$oid": str},
    "metadata": {
        "scouterName": str,
        "matchNumber": int,
        "robotTeam": int,
        "robotPosition": str,
    },
    "leftStartingZone": bool,
    "autoNotes": {
        "near": int,
        "mid": int,
        "far": int,
        "amp": int,
        "miss": int,
    },
    "teleNotes": {
        "near": int,
        "mid": int,
        "far": int,
        "amp": int,
        "miss": int,
    },
    "trapNotes": int,
    "climb": str,
}

# Constants
VALID_CLIMB_VALUES = {"park", "center", "none", "amp", "source", "failed"}
VALID_ROBOT_POSITIONS = {"red_1", "red_2", "red_3", "blue_1", "blue_2", "blue_3"}
MAX_TRAP_NOTES = 3

print(seperation_bar)
print("Script 03: Robust Data Cleaning\n")

# Initialize tracking variables
warnings = []
scouter_warnings = defaultdict(int)
scouter_participation = defaultdict(int)
team_match_counts = defaultdict(int)
match_robot_positions = defaultdict(set)


def log_warning(message, scouter=None):
    """
    Logs a warning and associates it with the scouter.

    :param message: The warning message to log.
    :param scouter: The scouter responsible for the data.
    """
    global warnings, scouter_warnings
    warnings.append(message)
    if scouter:
        scouter_warnings[scouter] += 1

def validate_and_clean_entry(entry):
    """
    Validates and cleans a single entry, ensuring it adheres to the correct structure and rules.

    :param entry: The raw data entry.
    :return: A cleaned entry.
    """
    scouter = entry.get("metadata", {}).get("scouterName", "Unknown")
    scouter_participation[scouter] += 1

    def validate_structure(data, expected_structure, path=""):
        """
        Validates and fixes a nested structure.

        :param data: The input data to validate.
        :param expected_structure: The expected structure.
        :param path: The path to the current key for logging purposes.
        :return: A validated and cleaned version of the data.
        """
        validated = {}
        for key, expected_type in expected_structure.items():
            full_key_path = f"{path}.{key}" if path else key

            if key not in data:
                log_warning(f"[WARNING] Missing key '{full_key_path}'.", scouter)
                continue

            if isinstance(expected_type, dict):
                validated[key] = validate_structure(data[key], expected_type, full_key_path)
            else:
                value = data[key]
                if not isinstance(value, expected_type):
                    log_warning(
                        f"[WARNING] Incorrect type for '{full_key_path}'. Expected {expected_type}, got {type(value)}.",
                        scouter,
                    )
                else:
                    if key == "climb" and value not in VALID_CLIMB_VALUES:
                        log_warning(
                            f"[WARNING] Invalid climb value '{value}' at '{full_key_path}'. Defaulting to 'none'.",
                            scouter,
                        )
                        value = "none"

                    if key == "robotPosition" and value not in VALID_ROBOT_POSITIONS:
                        log_warning(
                            f"[WARNING] Invalid robot position '{value}' at '{full_key_path}'. Defaulting to 'unknown'.",
                            scouter,
                        )
                        value = "unknown"

                    if key == "trapNotes" and value > MAX_TRAP_NOTES:
                        log_warning(
                            f"[WARNING] Trap notes '{value}' exceeded max limit at '{full_key_path}'. Defaulting to {MAX_TRAP_NOTES}.",
                            scouter,
                        )
                        value = MAX_TRAP_NOTES

                    if isinstance(value, int) and value < 0:
                        log_warning(
                            f"[WARNING] Negative value '{value}' at '{full_key_path}'. Defaulting to 0.",
                            scouter,
                        )
                        value = 0

                    validated[key] = value

        # Remove extra keys
        extra_keys = set(data.keys()) - set(expected_structure.keys())
        for extra_key in extra_keys:
            if extra_key != "__v":  # Log removal of all keys except `__v`
                log_warning(f"[WARNING] Extra key '{path}.{extra_key}' found and removed.", scouter)

        return validated

    cleaned_entry = validate_structure(entry, EXPECTED_STRUCTURE)

    # Record team and match consistency
    match_number = cleaned_entry["metadata"]["matchNumber"]
    robot_team = cleaned_entry["metadata"]["robotTeam"]
    robot_position = cleaned_entry["metadata"]["robotPosition"]
    team_match_counts[robot_team] += 1
    match_robot_positions[match_number].add(robot_position)

    return cleaned_entry


def analyze_data_consistency():
    """
    Analyzes data consistency for matches and robot teams.
    """
    global warnings

    # Check team match counts
    match_count_groups = defaultdict(list)
    for team, count in team_match_counts.items():
        match_count_groups[count].append(team)

    if len(match_count_groups) > 1:
        log_warning(
            "[WARNING] Inconsistent match counts detected:\n"
            + "\n".join(
                f"  Teams with {count} matches: {teams}"
                for count, teams in match_count_groups.items()
            )
        )

    # Check match completeness
    for match, positions in match_robot_positions.items():
        if len(positions) != 6:
            missing_positions = VALID_ROBOT_POSITIONS - positions
            log_warning(
                f"[WARNING] Match {match} is missing positions: {missing_positions}."
            )


# Main Script Execution
try:
    print(f"[INFO] Loading raw data from: {raw_data_path}")
    with open(raw_data_path, "r") as infile:
        raw_data = json.load(infile)

    if not isinstance(raw_data, list):
        raise ValueError("Raw data must be a list of matches.")

    cleaned_data = []
    for entry in raw_data:
        cleaned_entry = validate_and_clean_entry(entry)
        cleaned_data.append(cleaned_entry)

    analyze_data_consistency()

    print(f"[INFO] Saving cleaned data to: {cleaned_data_path}")
    os.makedirs(os.path.dirname(cleaned_data_path), exist_ok=True)
    with open(cleaned_data_path, "w") as outfile:
        json.dump(cleaned_data, outfile, indent=4)

    # Save scouter leaderboard
    os.makedirs(os.path.dirname(scouter_leaderboard_path), exist_ok=True)
    with open(scouter_leaderboard_path, "w") as leaderboard_file:
        leaderboard_file.write("Scouter Error Leaderboard:\n")
        for scouter, count in sorted(scouter_warnings.items(), key=lambda x: -x[1]):
            leaderboard_file.write(f"{scouter}: {count} errors/warnings\n")
        leaderboard_file.write("\nScouter Participation:\n")
        for scouter, count in sorted(scouter_participation.items(), key=lambda x: -x[1]):
            leaderboard_file.write(f"{scouter}: {count} matches\n")

    print("\n".join(warnings))
    print(f"[INFO] Total warnings/errors: {len(warnings)}")
    print("[INFO] Data cleaning completed successfully.")

except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
    print(traceback.format_exc())

print(seperation_bar)