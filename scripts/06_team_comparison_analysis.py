from utility_functions.print_formats import seperation_bar
import pandas as pd
import os
import traceback
import matplotlib.pyplot as plt
from scipy.stats import zscore

print(seperation_bar)
print("Script 06: Team Comparison Analysis\n")

# File paths
team_statistics_path = "outputs/team_data/team_statistical_analysis.json"
output_analysis_path = "outputs/team_data/team_advanced_comparative_statistical_analysis.json"
output_statistics_path = "outputs/statistics/team_comparison_stats.txt"
visualizations_dir = "outputs/visualizations"

try:
    # Check if team statistics data file exists
    if not os.path.exists(team_statistics_path):
        raise FileNotFoundError(f"Team statistics data file not found: {team_statistics_path}")

    # Load the team statistics data
    print(f"[INFO] Loading team statistics from: {team_statistics_path}")
    with open(team_statistics_path, "r") as infile:
        team_statistics = pd.read_json(infile, orient="index")

    # Ensure the DataFrame is not empty
    if team_statistics.empty:
        raise ValueError(f"Team statistics data is empty. Check the file: {team_statistics_path}")

    # Add calculated metrics
    print("[INFO] Calculating additional metrics.")
    team_statistics["shooting_efficiency"] = (
        team_statistics["shootNotes_average"] / team_statistics["totalNotes_average"]
    )
    team_statistics["missed_notes_percent"] = (
        team_statistics["missedNotes_average"] / team_statistics["totalNotes_average"] * 100
    )
    team_statistics["consistency_metric"] = (
        team_statistics["totalNotes_std_dev"] / team_statistics["totalNotes_average"]
    ).fillna(0)  # Handle potential division by zero
    team_statistics["performance_score"] = (
        0.5 * team_statistics["totalNotes_average"] +
        0.3 * team_statistics["shootNotes_average"] -
        0.2 * team_statistics["missed_notes_percent"]
    )
    team_statistics["performance_zscore"] = zscore(team_statistics["performance_score"])

    # Save advanced analysis as JSON
    print(f"[INFO] Saving advanced analysis to: {output_analysis_path}")
    os.makedirs(os.path.dirname(output_analysis_path), exist_ok=True)
    team_statistics.to_json(output_analysis_path, orient="index", indent=4)

    # Rank teams for each metric
    print("[INFO] Ranking teams for metrics.")
    rankable_metrics = [
        "totalNotes_average", "shooting_efficiency", "missed_notes_percent",
        "performance_score", "consistency_metric", "performance_zscore"
    ]
    rankings = {}
    for metric in rankable_metrics:
        ascending = metric in ["missed_notes_percent", "consistency_metric"]
        team_statistics[f"{metric}_rank"] = team_statistics[metric].rank(ascending=ascending)
        rankings[metric] = team_statistics.sort_values(by=metric, ascending=ascending)

    # Save rankings to the text file
    print(f"[INFO] Saving rankings to: {output_statistics_path}")
    os.makedirs(os.path.dirname(output_statistics_path), exist_ok=True)
    with open(output_statistics_path, 'w') as stats_file:
        stats_file.write("Team Rankings by Various Metrics\n")
        stats_file.write("=" * 80 + "\n\n")

        for metric, ranked_df in rankings.items():
            stats_file.write(f"Rankings by {metric}:\n")
            stats_file.write(
                ranked_df[[metric, f"{metric}_rank"]].to_string(index=True) + "\n\n"
            )

    # Generate visualizations
    print(f"[INFO] Generating visualizations in: {visualizations_dir}")
    os.makedirs(visualizations_dir, exist_ok=True)
    for metric, ranked_df in rankings.items():
        top_n = 10  # Top 10 teams for visualization
        ranked_df.head(top_n).plot(
            y=metric, kind="bar", title=f"Top {top_n} Teams by {metric.replace('_', ' ').title()}", legend=False
        )
        plt.ylabel(metric.replace("_", " ").title())
        plt.xticks(ticks=range(top_n), labels=ranked_df.head(top_n).index, rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(visualizations_dir, f"top_{top_n}_{metric}.png"))
        plt.close()

    print("\nScript 06: Completed.")

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