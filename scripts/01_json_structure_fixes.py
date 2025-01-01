from utility_functions.print_formats import seperation_bar
import os
import json
import traceback

def reformat_json(file_path):
    """
    Reformats a JSON file with improperly separated objects into valid JSON.

    :param file_path: Path to the JSON file to fix.
    """
    try:
        print(f"  [INFO] Reading file: {file_path}")

        # Read and parse each line as a separate JSON object
        with open(file_path, 'r') as infile:
            raw_lines = infile.readlines()

        if not raw_lines:
            print(f"  [WARNING] File is empty: {file_path}")
            return False

        json_objects = []
        for i, line in enumerate(raw_lines):
            try:
                json_obj = json.loads(line.strip())
                json_objects.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"    [WARNING] Skipping malformed line {i+1} in {file_path}: {line.strip()} - Error: {e}")

        if not json_objects:
            print(f"  [ERROR] No valid JSON objects found in file: {file_path}")
            return False

        # Write the corrected JSON objects into a valid JSON array
        with open(file_path, 'w') as outfile:
            json.dump(json_objects, outfile, indent=4)
            print(f"  [INFO] Successfully reformatted JSON saved to: {file_path}")
        return True

    except FileNotFoundError:
        print(f"  [ERROR] File not found: {file_path}")
    except PermissionError:
        print(f"  [ERROR] Permission denied for file: {file_path}")
    except Exception as e:
        print(f"  [ERROR] An unexpected error occurred while processing {file_path}: {e}")
        print(traceback.format_exc())
    return False


def process_json_directory(directory_path):
    """
    Processes all JSON files in a directory.

    :param directory_path: Path to the directory containing JSON files.
    """
    if not os.path.exists(directory_path):
        print(f"[ERROR] Directory does not exist: {directory_path}")
        return

    print(f"[INFO] Processing JSON files in directory: {directory_path}")

    json_files_processed = 0
    json_files_skipped = 0
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory_path, file_name)
            print(f"[INFO] Fixing JSON file: {file_name}")
            success = reformat_json(file_path)
            if success:
                json_files_processed += 1
            else:
                json_files_skipped += 1

    if json_files_processed == 0 and json_files_skipped == 0:
        print(f"[WARNING] No JSON files found in directory: {directory_path}")
    else:
        print(f"[INFO] Completed processing JSON files in: {directory_path}")
        print(f"[INFO] Successfully processed: {json_files_processed} files")
        print(f"[WARNING] Skipped: {json_files_skipped} files")


# MAIN SCRIPT

print(seperation_bar)
print("Script 01: JSON Reformatting Tool\n")

try:
    # Define the directory containing the JSON files
    json_directory = "data/raw"

    # Process all JSON files in the specified directory
    process_json_directory(json_directory)

    print("\nAll JSON files have been reformatted successfully.")
    print("Script 01: Successfully Completed.")

except Exception as e:
    print(f"[ERROR] An unexpected error occurred during execution: {e}")
    print(traceback.format_exc())
    print("\nScript 01: Failed.")

print(seperation_bar)
