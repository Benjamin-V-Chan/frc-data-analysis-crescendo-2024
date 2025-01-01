from utility_functions.print_formats import seperation_bar
import os
import shutil

# Function to clear and recreate each specific folder
def clear_and_recreate_folder(folder_path):

    # Clears all files in the specified folder and recreates the folder if it doesn't exist.

    # Delete files if the folder exists
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove file or symbolic link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove directory
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    
    # Recreate the folder
    os.makedirs(folder_path, exist_ok=True)
    print(f"Cleared and recreated folder: {folder_path}")



# MAIN SCRIPT

seperation_bar
print("Script 01: Clearing and Recreating Output Directories\n")

try:
    # Define the paths to the results and processed directories
    processed_data_dir = os.path.join("data", "processed")
    visualizations_outputs_dir = os.path.join("outputs", "visualizations")
    statistics_outputs_dir = os.path.join("outputs", "statistics")
    teams_outputs_dir = os.path.join("outputs", "teams")

    # Clear and recreate all directories
    clear_and_recreate_folder(processed_data_dir)
    clear_and_recreate_folder(visualizations_outputs_dir)
    clear_and_recreate_folder(statistics_outputs_dir)
    clear_and_recreate_folder(teams_outputs_dir)

    print("All output directories have been cleared and recreated.")
    print("\nScript 01: Completed.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("\nScript 01: Failed.")

seperation_bar