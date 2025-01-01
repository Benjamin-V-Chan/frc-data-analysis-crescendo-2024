from utility_functions.print_formats import seperation_bar
import pandas as pd
import os
import traceback
import matplotlib.pyplot as plt
from scipy.stats import zscore

print(seperation_bar)
print("Script 06: Advanced Team Comparison Analysis\n")

# File paths
team_analysis_data_path = "outputs/team_data/team_analysis.json"
output_statistics_path = "outputs/statistics/team_comparison_stats.txt"
visualizations_dir = "outputs/visualizations"

try:
    # Check if team analysis data file exists
    if not os.path.exists(team_analysis_data_path):
        raise FileNotFoundError(f"Team analysis data file not found: {team_analysis_data_path}")

    # Load the team analysis data
    print(f"[INFO] Loading team analysis data from: {team_analysis_data_path}")
    team_analysis_df = pd.read_json(team_analysis_data_path)

    # Ensure the DataFrame is not empty
    if team_analysis_df.empty:
        raise ValueError(f"Team analysis data is empty. Check the file: {team_analysis_data_path}")

    # Ensure output directories exist
    os.makedirs(os.path.dirname(output_statistics_path), exist_ok=True)
    os.makedirs(visualizations_dir, exist_ok=True)

    # Calculate metrics for rankings
    team_analysis_df["shooting_efficiency"] = (
        team_analysis_df["totalShootNotes_avg"] / team_analysis_df["totalNotes_avg"]
    )
    team_analysis_df["missed_notes_percent"] = (
        team_analysis_df["totalMissedNotes_avg"] / team_analysis_df["totalNotes_avg"] * 100
    )
    team_analysis_df["performance_score"] = (
        0.5 * team_analysis_df["totalNotes_avg"] +
        0.3 * team_analysis_df["totalShootNotes_avg"] +
        -0.2 * team_analysis_df["missed_notes_percent"]
    )
    team_analysis_df["consistency_metric"] = (
        team_analysis_df["totalNotes_std"] / team_analysis_df["totalNotes_avg"]
    )
    team_analysis_df["performance_zscore"] = zscore(team_analysis_df["performance_score"])

    # Rank teams for each metric
    rankable_metrics = [
        "totalNotes_avg", "shooting_efficiency", "missed_notes_percent",
        "performance_score", "consistency_metric", "performance_zscore"
    ]
    rankings = {}
    for metric in rankable_metrics:
        ascending = metric in ["missed_notes_percent", "consistency_metric"]
        team_analysis_df[f"{metric}_rank"] = team_analysis_df[metric].rank(ascending=ascending)
        rankings[metric] = team_analysis_df.sort_values(by=metric, ascending=ascending)

    # Save statistics to the text file
    with open(output_statistics_path, 'w') as stats_file:
        stats_file.write("Team Rankings by Various Metrics\n")
        stats_file.write("=" * 80 + "\n\n")

        for metric, ranked_df in rankings.items():
            stats_file.write(f"Rankings by {metric}:\n")
            stats_file.write(ranked_df[["team", metric, f"{metric}_rank"]].to_string(index=False) + "\n\n")

    # Generate visualizations for each metric
    print(f"[INFO] Generating visualizations in: {visualizations_dir}")
    for metric, ranked_df in rankings.items():
        top_n = 10  # Top 10 teams for visualization
        ranked_df.head(top_n).plot(
            x="team", y=metric, kind="bar", title=f"Top {top_n} Teams by {metric}", legend=False
        )
        plt.ylabel(metric.replace("_", " ").title())
        plt.savefig(os.path.join(visualizations_dir, f"top_{top_n}_{metric}.png"))
        plt.close()

    print("\nScript 06: Successfully Completed.")

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
