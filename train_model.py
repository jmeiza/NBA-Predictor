import pandas as pd

df = pd.read_csv("games.csv")
df_team_stats = pd.read_csv("team_stats.csv")

df = df.dropna()


# Dropping columns from games.csv that we don't actually need to train the model and keeping only the ones that we need.
df = df[['GAME_ID', 'TEAM_ID_home', 'TEAM_ID_away', 'HOME_TEAM_WINS']]

# Merging in the average stats for the home team in each game
complete_stats = df.merge(df_team_stats, left_on='TEAM_ID_home', right_on='TEAM_ID',)


# # Merging in the average stats for the away team in each game. We add the suffixes to differentiate between the stats for the home team and the stats for the away team.
complete_stats = complete_stats.merge(df_team_stats,left_on='TEAM_ID_away', right_on='TEAM_ID', suffixes=('_home_team', '_away_team'))


# HT: Home Team, AT: Away Team
complete_stats = complete_stats.rename(columns={
    'HOME_TEAM_WINS_x': 'label',
    'HOME_TEAM_WINS_y': 'HT_home_win_rate',
    'PTS_home_home_team': 'HT_home_pts',
    'FG_PCT_home_home_team': 'HT_home_fg_pct',
    'AST_home_home_team': 'HT_home_ast',
    'REB_home_home_team': 'HT_home_reb',
    'PTS_away_away_team': 'AT_away_pts',
    'FG_PCT_away_away_team': 'AT_away_fg_pct',
    'AST_away_away_team': 'AT_away_ast',
    'REB_away_away_team': 'AT_away_reb',
    'AWAY_TEAM_WINS_away_team': 'AT_away_win_rate'
})

# We are only keeping the columns the model will need to use to predict the winner.
features = complete_stats[['label','HT_home_pts', 'HT_home_fg_pct', 'HT_home_ast', 'HT_home_reb', 'HT_home_win_rate', 'AT_away_pts', 'AT_away_fg_pct', 'AT_away_ast', 'AT_away_reb', 'AT_away_win_rate']]


# Split the features into X(inputs)and Y(output). The model predicts Y using X. 
X = features.drop(columns=['label'])
Y = features['label']