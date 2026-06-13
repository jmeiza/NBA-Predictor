import pandas as pd

df = pd.read_csv("games.csv")
df_team_stats = pd.read_csv("team_stats.csv")

df = df.dropna()

#Dropping columns from games.csv that we don't actually need to train the model and keeping only the ones that we need.
df = df[['GAME_ID', 'TEAM_ID_home', 'TEAM_ID_away', 'HOME_TEAM_WINS']]


# Merging in the average stats for the home team in each game
complete_stats = df.merge(df_team_stats, left_on='TEAM_ID_home', right_on='TEAM_ID',)

# Merging in the average stats for the away team in each game. We add the suffixes to differentiate between the stats for the home team and the stats for the away team.
complete_stats = complete_stats.merge(df_team_stats,left_on='TEAM_ID_away', right_on='TEAM_ID', suffixes=('_home_team', '_away_team'))

# We are only keeping the columns the model will need to use to predict the winner.

features = complete_stats[['PTS_home_home_team', 'FG_PCT_home_home_team', 'AST_home_home_team', 'REB_home_home_team', 'HOME_TEAM_WINS_y', 'PTS_away_away_team', 'FG_PCT_away_away_team', 'AST_away_away_team', 'REB_away_away_team', 'AWAY_TEAM_WINS_away_team', 'HOME_TEAM_WINS']]

# Split the features into X(inputs)and Y(output). The model predicts Y using X. 
X = features.drop(columns=['HOME_TEAM_WINS'])
Y = features['HOME_TEAM_WINS']