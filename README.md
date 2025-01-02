# frc-data-analysis-crescendo-2024

## Overview
This project is a data analysis pipeline designed to process and analyze scouting data from FRC matches for the 2024 game, *Crescendo*. The goal is to provide insightful statistics, advanced analytics, and visualizations to evaluate team performances effectively. The pipeline uses Python for data processing, aggregation, and visualization.

The datasets used to test and refine this pipeline were collected from my FRC team, Team 4201: *The Vitruvian Bots*.

---

## Features

1. **Robust Data Cleaning**:
   - Validates and corrects raw JSON data, removing inconsistencies and ensuring structure.
   - Logs warnings and errors, including scouter-specific issues, to identify data collection errors.

2. **Team-Based Metrics**:
   - Summarizes match-level data into team-level statistics.
   - Metrics include averages, min, max, standard deviation, frequencies, and percentages.

3. **Comprehensive Team Analysis**:
   - Aggregates team-level data across matches.
   - Provides insights into team performance, consistency, and efficiency.

4. **Rankings and Advanced Comparisons**:
   - Ranks teams using z-scores, weighted scoring, and consistency metrics.
   - Offers detailed comparisons of performance and shooting efficiency.

5. **Detailed Visualizations**:
   - Generates bar charts, scatter plots, and rankings to highlight top-performing teams.

---

## Directory Structure

```
.
├── data/
│   ├── raw/                     # Raw scouting data
│   ├── processed/               # Cleaned and structured data
│   │   ├── cleaned_port_h_matchapps.json
├── outputs/
│   ├── statistics/              # Statistical results and logs
│   │   ├── scouter_error_leaderboard.txt
│   │   ├── team_comparison_stats.txt
│   ├── team_data/               # Team-based data
│   │   ├── team_analysis.json
│   │   ├── team_statistics.json
│   ├── visualizations/          # Generated visualizations
│   │   ├── top_10_totalNotes_avg.png
│   │   ├── top_10_shooting_efficiency.png
│   │   ├── ...
├── scripts/                     # All scripts
│   ├── 01_json_structure_fixes.py                             # Fixes malformed JSON files
│   ├── 02_clear_outputs.py                                    # Clears outputs folder
│   ├── 03_data_cleaning_and_preprocessing.py                  # Cleans and preprocesses raw data
│   ├── 04_team_statistics_and_data_restructuring.py           # Structures team-level data
│   ├── 05_data_analysis_and_statistics_aggregation.py         # Data Analysis and Statistical Aggregation of team-level metrics
│   ├── 06_team_analysis_and_comparison.py                     # Full advanced comparative statistical-based analysis of different teams
```

---

## Scripts

### 1. `01_json_structure_fixes.py`
- **Purpose**: Fixes malformed JSON files which are results of the way our data was initially structured, by reformatting lines into valid JSON objects.
- **Output**: Reformatted JSON files in `data/raw`.

### 2. `02_clear_outputs.py`
- **Purpose**: Clears and recreates the `outputs` and `data` folders while preserving specific subdirectories (creset configuration can be customized).
- **Output**: Resets the outputs directory for fresh analyses.

### 3. `03_data_cleaning_and_preprocessing.py`
- **Purpose**: Validates, cleans, and preprocesses raw scouting data.
- **Features**:
  - Removes duplicate match entries and incorrect fields.
  - Tracks scouter-specific errors and generates a leaderboard.
  - Ensures consistent match counts and positions.
- **Output**: `cleaned_port_h_matchapps.json`.

### 4. `04_team_statistics_and_data_restructuring.py`
- **Purpose**: Restructures match-level data into team-based summaries.
- **Key Metrics**:
  - Total notes, shooting efficiency, missed notes, and amp notes.
  - Derived metrics like `autoShootNotes`, `teleopShootNotes`, and `missedNotes`.
- **Output**: `cleaned_port_h_team_matches.json`.

### 5. `05_data_analysis_and_statistics_aggregation.py`
- **Purpose**: Aggregates and analyzes team-level metrics across matches.
- **Key Metrics**:
  - Averages, min, max, standard deviations, and frequencies for all data types.
- **Output**: `team_statistical_analysis.json`.

### 6. `06_team_comparison_analysis.py`
- **Purpose**: Combines advanced analysis, rankings, and visualizations.
- **Features**:
  - Calculates z-scores, performance scores, and consistency metrics.
  - Ranks teams for each metric and saves textual summaries.
  - Generates visualizations for top-performing teams.
- **Outputs**:
  - Advanced team-level statistical analysis in `team_advanced_comparative_statistical_analysis.json`
  - Rankings in `team_comparison_stats.txt`.
  - Visualizations in `outputs/visualizations`.

---

## How to Use

### Prerequisites
- Python 3.9 or higher
- Required libraries (install using `pip install -r requirements.txt`):
  - `pandas`
  - `matplotlib`
  - `scipy`

### Steps
1. **Prepare Raw Data**:
   - Place raw JSON files in `data/raw`.

2. **Run Scripts in Order**:
   - `python scripts/01_json_structure_fixes.py`
   - `python scripts/02_clear_outputs.py`
   - `python scripts/03_data_cleaning_and_preprocessing.py`
   - `python scripts/04_team_statistics_and_data_restructuring.py`
   - `python scripts/05_data_analysis_and_statistics_aggregation.py`
   - `python scripts/06_team_comparison_analysis.py`

3. **View Results**:
   - Cleaned data in `data/processed`.
   - Team-based data in `outputs/team_data`.
   - Statistical results in `outputs/statistics`.
   - Visualizations in `outputs/visualizations`.

---

## Future Enhancements
- **Real-Time Integration**:
  - Scouting app integration for live data ingestion.
- **Predictive Analytics**:
  - Machine learning models to forecast match outcomes.
- **Interactive Dashboards**:
  - Web-based tools for interactive exploration of insights.