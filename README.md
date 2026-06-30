# NBA Game Winner Predictor
 
A machine learning pipeline that predicts NBA game winners using historical team performance data, with a live prediction mode powered by real-time NBA stats.
 
## How it works
 
The project is split into two phases:
 
**Phase 1 — Local ML pipeline**
Trains a logistic regression model on historical NBA game data to predict the winner of a matchup based on team performance metrics.
 
**Phase 2 — Live predictor**
Pulls current-season team standings from the NBA API and feeds them into the trained model to predict outcomes for real, current matchups.
 
## Pipeline
 
```
games.csv + ranking.csv
        │
        ▼
feature_engineering.py   → builds team_stats.csv
        │
        ▼
train_model.py            → trains model, saves model.pkl
        │
        ▼
predict.py                 → loads model.pkl + live NBA API data → prediction
```
 
## Features used
 
- **Season win percentage** (`W_PCT`) for both teams
- **Rolling win rate** — each team's win rate over their last 10 games, capturing current form/streaks
- **Win rate differential** — the gap between the two teams' win percentages and rolling win rates
## Model performance
 
| Model | Accuracy |
|---|---|
| Baseline (always predict home team wins) | 58.9% |
| Logistic Regression (season + rolling win rates) | 74.1% |
| Random Forest (same features) | 71.1% |
 
Logistic Regression was selected as the final model.
 
## Setup
 
### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/NBA-Predictor.git
cd NBA-Predictor
```
 
### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```
 
### 3. Install dependencies
```bash
pip install pandas scikit-learn nba_api kaggle
```
 
### 4. Download the dataset
This project uses the [NBA Games dataset](https://www.kaggle.com/datasets/nathanlauga/nba-games) by Nathan Lauga, downloaded via the Kaggle API.
 
Set up your Kaggle API token at `~/.kaggle/access_token`, then run:
```bash
kaggle datasets download -d nathanlauga/nba-games --unzip
```
 
This downloads `games.csv`, `teams.csv`, `ranking.csv`, `games_details.csv`, and `players.csv` into the project folder.
 
## Usage
 
### Run the full pipeline
```bash
python explore_data1.py        # explore the raw data
python feature_engineering.py  # builds team_stats.csv
python train_model.py          # trains and saves model.pkl
```
 
### Predict a live matchup
```bash
python predict.py
```
You'll be prompted to enter a home team and an away team. The script pulls current-season stats from the NBA API and returns a prediction with a confidence percentage.
 
Example:
```
Enter home team: Spurs
Enter away team: Thunder
Spurs wins (65.1% confidence)
```
 
## Project structure
 
```
NBA-Predictor/
├── explore_data1.py        # data exploration, establishes baseline
├── feature_engineering.py  # builds rolling win rates + season stats
├── train_model.py          # trains and saves the model
├── predict.py               # live prediction using NBA API
├── .gitignore                # excludes CSVs, model.pkl
└── README.md
```
 
## Key concepts applied
 
- Feature engineering (rolling averages, win rate differentials)
- Data leakage avoidance (only using pre-game data, never in-game stats)
- Train/test split and accuracy evaluation
- Model comparison (Logistic Regression vs Random Forest)
- Live API integration to apply a trained model to real-world data
## Future improvements
 
- Player-level stats (injuries, recent individual performance)
- Home-specific win rate as an explicit feature
- Automated retraining each season
- Web interface instead of CLI