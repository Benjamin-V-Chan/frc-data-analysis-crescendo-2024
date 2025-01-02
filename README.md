Here’s the fully updated and refined README:

---

# frc-data-analysis-crescendo-2024

## Overview
This project is a data analysis pipeline designed to process and analyze scouting data from FRC matches for the 2024 game, *Crescendo*. The goal is to provide insightful statistics, advanced analytics, and visualizations to evaluate team performances effectively. The pipeline uses Python for data processing, aggregation, and visualization.

The datasets used to test and refine this pipeline were collected from my FRC team, Team 4201: *The Vitruvian Bots*.

---

## Features
1. **Robust Data Cleaning**:
   - Ensures raw JSON data is correctly formatted and removes inconsistencies.
   - Logs all warnings and errors for analysis.
   - Tracks scouter performance to identify data collection issues.

2. **Advanced Team Metrics**:
   - Calculates team-level statistics across all matches.
   - Key metrics include shooting efficiency, missed notes percentage, total notes, and amp notes.

3. **Comprehensive Analysis**:
   - Aggregates team-level data across matches.
   - Calculates averages, minimums, maximums, standard deviations, and rankings for all metrics.

4. **Detailed Visualizations**:
   - Generates bar charts, scatter plots, and other visuals to highlight team performance.
   - Visualizes rankings and top-performing teams across key metrics.

5. **Extensive Statistical Insights**:
   - Ranks teams using z-scores, weighted scoring, and advanced analytics.
   - Compares teams across performance metrics and consistency measures.

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
│   │   ├── team_performance.json
│   ├── visualizations/          # Generated visualizations
│   │   ├── top_10_totalNotes_avg.png
│   │   ├── top_10_shooting_efficiency.png
│   │   ├── ...
├── scripts/
│   ├── 01_fix_json.py                  # Fixes malformed JSON files
│   ├── 02_clear_outputs.py             # Clears outputs folder
│   ├── 03_data_cleaning_and_preprocessing.py   # Cleans and preprocesses raw data
│   ├── 04_team_statistics.py           # Structures team-level data
│   ├── 05_team_advanced_statistics.py  # Adds advanced statistics
│   ├── 06_data_analysis.py             # Aggregates and analyzes data
│   ├── 07_team_comparison_analysis.py  # Compares teams and generates visualizations
```

---

## Scripts

### 1. `01_fix_json.py`
- **Purpose**: Fixes malformed JSON files by reformatting lines into valid JSON objects.
- **Output**: Reformatted JSON files in `data/raw`.

### 2. `02_clear_outputs.py`
- **Purpose**: Clears and recreates the `outputs` folder while preserving specific subdirectories.
- **Output**: Resets the outputs directory for fresh analyses.

### 3. `03_data_cleaning_and_preprocessing.py`
- **Purpose**: Validates, cleans, and preprocesses raw scouting data.
- **Features**:
  - Removes duplicate match entries and incorrect fields.
  - Tracks scouter errors/warnings and generates a leaderboard.
  - Ensures consistent match counts and positions.
- **Output**: `cleaned_port_h_matchapps.json` in `data/processed`.

### 4. `04_team_statistics.py`
- **Purpose**: Restructures match-level data into team-based summaries.
- **Key Metrics**:
  - Total notes, shooting efficiency, missed notes, and amp notes.
  - Derived metrics like `autoShootNotes`, `teleopShootNotes`, and `missedNotes`.
- **Output**: `team_performance.json`.

### 5. `05_team_advanced_statistics.py`
- **Purpose**: Adds advanced metrics for team analysis.
- **Key Metrics**:
  - Aggregates like averages, min, max, and std deviation.
  - Percentages and frequencies for categorical data.
- **Output**: `team_advanced_performance.json`.

### 6. `06_data_analysis.py`
- **Purpose**: Aggregates and analyzes team-level data.
- **Key Metrics**:
  - Rankings based on performance, consistency, and efficiency.
  - Advanced scoring metrics using z-scores and weighted measures.
- **Output**: `team_analysis.json`.

### 7. `07_team_comparison_analysis.py`
- **Purpose**: Generates insights and visualizations.
- **Features**:
  - Visualizes top teams across metrics.
  - Generates rankings and comparisons.
- **Output**:
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
   - `python scripts/01_fix_json.py`
   - `python scripts/02_clear_outputs.py`
   - `python scripts/03_data_cleaning_and_preprocessing.py`
   - `python scripts/04_team_statistics.py`
   - `python scripts/05_team_advanced_statistics.py`
   - `python scripts/06_data_analysis.py`
   - `python scripts/07_team_comparison_analysis.py`

3. **View Results**:
   - Cleaned data in `data/processed`.
   - Team-based data in `outputs/team_data`.
   - Statistical results in `outputs/statistics`.
   - Visualizations in `outputs/visualizations`.

---

## Future Enhancements
- **Real-Time Integration**:
  - Scouting app integration for live data ingestion.
- **Machine Learning Models**:
  - Predictive analytics to forecast match outcomes.
- **Interactive Dashboards**:
  - Web-based tools for interactive exploration of insights.