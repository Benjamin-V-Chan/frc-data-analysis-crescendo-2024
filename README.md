# frc-data-analysis-crescendo-2024

## Overview
This project is a data analysis pipeline designed to process and analyze scouting data from FRC matches from the 2024 game, Crescendo. The goal is to provide insightful statistics, advanced analytics, and visualizations to evaluate team performances effectively. The pipeline uses Python for data processing, aggregation, and visualization.

The datasets used to test and refine this pipeline were collected from my FRC team, Team 4201: The Vitruvian Bots.

---

## Features
1. **Data Preprocessing**:
   - Cleans raw JSON data.
   - Aggregates match-level data into team-level summaries.

2. **Advanced Team Statistics**:
   - Calculates advanced match-level statistics for each team.
   - Includes metrics like total notes, shooting efficiency, and missed notes percentage.

3. **Comprehensive Analysis**:
   - Aggregates team-level data across matches.
   - Calculates averages, minimums, maximums, standard deviations, and rankings.

4. **Detailed Visualizations**:
   - Generates bar charts to visualize top-performing teams across various metrics.

5. **Extensive Statistical Analysis**:
   - Ranks teams across metrics like performance score, consistency, and efficiency.
   - Provides advanced insights using z-scores and weighted scoring.

---

## Directory Structure
```
.
├── data/
│   ├── raw/                     # Raw scouting data
│   ├── processed/               # Processed data files
│   │   ├── team_performance.json
│   │   ├── team_advanced_performance.json
├── outputs/
│   ├── statistics/              # Statistical results
│   │   ├── team_comparison_stats.txt
│   ├── team_data/               # Analyzed team data
│   │   ├── team_analysis.json
│   ├── visualizations/          # Generated visualizations
│   │   ├── top_10_totalNotes_avg.png
│   │   ├── top_10_shooting_efficiency.png
│   │   ├── ...
├── scripts/
│   ├── 01_fix_json.py           # Fixes malformed JSON files
│   ├── 02_data_preprocessing.py # Processes raw data
│   ├── 03_team_statistics.py    # Aggregates team-level data
│   ├── 04_team_advanced_statistics.py # Adds advanced statistics
│   ├── 05_data_analysis.py      # Aggregates and analyzes data
│   ├── 06_team_comparison_analysis.py # Generates insights and visualizations
```

---

## Scripts

### 1. `01_fix_json.py`
- **Purpose**: Fixes malformed JSON files by reformatting lines into valid JSON objects.
- **Output**: Reformatted JSON files.

### 2. `02_data_preprocessing.py`
- **Purpose**: Processes raw scouting data, removes duplicates, and fills missing values.
- **Output**: Preprocessed data in CSV and JSON formats.

### 3. `03_team_statistics.py`
- **Purpose**: Aggregates match-level data into team-level summaries.
- **Output**: `team_performance.json`.

### 4. `04_team_advanced_statistics.py`
- **Purpose**: Adds advanced statistics to each team's match performance.
- **Key Metrics**:
  - Total notes, shooting notes, missed notes, and amp notes.
  - Combined statistics like `totalShootNotes`, `totalNotes`, and percentages.
- **Output**: `team_advanced_performance.json`.

### 5. `05_data_analysis.py`
- **Purpose**: Aggregates team-level data and calculates advanced analytics.
- **Key Metrics**:
  - Average, min, max, std deviation for all numerical data.
  - Frequencies for categorical data.
  - Rankings and percentages for binary data.
- **Output**: `team_analysis.json`.

### 6. `06_team_comparison_analysis.py`
- **Purpose**: Generates statistical comparisons, rankings, and visualizations.
- **Key Insights**:
  - Rankings for shooting efficiency, missed notes, performance scores, and more.
  - Visualizations for top teams in key metrics.
- **Output**:
  - Textual rankings in `team_comparison_stats.txt`.
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
   - `python scripts/02_data_preprocessing.py`
   - `python scripts/03_team_statistics.py`
   - `python scripts/04_team_advanced_statistics.py`
   - `python scripts/05_data_analysis.py`
   - `python scripts/06_team_comparison_analysis.py`

3. **View Results**:
   - Processed data in `data/processed`.
   - Analyzed team data in `outputs/team_data`
   - Statistical results in `outputs/statistics`.
   - Visualizations in `outputs/visualizations`.

---

## Future Enhancements
   - Integration with scouting apps for real-time data ingestion.
   - Predictive analytics using machine learning models.
   - Web dashboard for interactive visualization and reporting.