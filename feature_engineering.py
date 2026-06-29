import pandas as pd

df = pd.read_csv("games.csv")
df_teams = pd.read_csv("teams.csv")
df_ranking = pd.read_csv("ranking.csv")


# Adding a column to record when the team that played away wins. Must come before dropna()
df['AWAY_TEAM_WINS'] = 1 - df['HOME_TEAM_WINS']

df = df.dropna() # dropping missing rows

# Dropping seasons that are before the 2020 season
df = df[df['SEASON'] >= 2020]

## CREATING TWO DATAFRAMES OF GAMES.CSV SO THAT FOR EACH GAME WE HAVE A ROW FOR 
# THE HOME TEAM AND ONE FOR THE AWAY TEAM. NEEDED FOR THE ROLLING AVERAGES WE WANT 
# TO IMPLEMENT.

# A rolling average is used to calculate the win percent a team has based on its most recent games. 
# The more games a team has won within their last 10 games, the higher their winning percentage for 
# the game they about to play next. So this rolling avergae sort of like tracks winning and losing streaks.

home_team_games = df[['GAME_DATE_EST', 'HOME_TEAM_ID','HOME_TEAM_WINS']]
away_team_games = df[['GAME_DATE_EST', 'VISITOR_TEAM_ID', 'AWAY_TEAM_WINS']]

# RENAMING THE COLUMNS SO AS TO MAKE THE STACKING EASIER
home_team_games = home_team_games.rename(columns={
    'GAME_DATE_EST': 'DATE',
    'HOME_TEAM_ID': 'TEAM_ID',
    'HOME_TEAM_WINS': 'WON'
})

away_team_games = away_team_games.rename(columns={
    'GAME_DATE_EST': 'DATE',
    'VISITOR_TEAM_ID': 'TEAM_ID',
    'AWAY_TEAM_WINS': 'WON'
})

# STACKING BOTH DATAFRAMES ON TOP EACH OTHER
all_team_games = pd.concat([home_team_games, away_team_games])
all_team_games = all_team_games.sort_values(['TEAM_ID','DATE'])
all_team_games = all_team_games.drop_duplicates(['TEAM_ID', 'DATE']) 

# ROLLING AVERAGE CODE
# .transform() adds the rolling average for each game(row) into that row in the dataframe under the column "rolling_win_rate"

all_team_games['rolling_win_rate'] = all_team_games.groupby('TEAM_ID')['WON'].transform(lambda x: x.rolling(10, min_periods=1).mean())

df = df.merge(all_team_games[['DATE','TEAM_ID','rolling_win_rate']], left_on=['GAME_DATE_EST','HOME_TEAM_ID'], right_on=['DATE','TEAM_ID'])

df = df.merge(all_team_games[['DATE','TEAM_ID','rolling_win_rate']], left_on=['GAME_DATE_EST','VISITOR_TEAM_ID'], right_on=['DATE','TEAM_ID'])

df = df.drop(columns=['DATE_x','DATE_y','TEAM_ID_x','TEAM_ID_y'])

df = df.rename(columns={
    'rolling_win_rate_x':'home_rolling_win_rate',
    'rolling_win_rate_y': 'away_rolling_win_rate'
})



################################################
# NOTE: "left_on" refers to the DataFrame you are 
# merging from (df) and "right_on" refers to 
# the DataFrame you're merging in (df_ranking). 
# It merges whenever the value of the columns in the lists match,

# Merging the stats for the home team in each game
home_stats = df.merge(df_ranking[['TEAM_ID', 'STANDINGSDATE', 'W_PCT']], left_on=['HOME_TEAM_ID', 'GAME_DATE_EST'], right_on=['TEAM_ID', 'STANDINGSDATE'])

# Renaming columns to improve clarity
home_stats = home_stats.rename(columns={
    'W_PCT': 'W_PCT_home',
    'TEAM_ID': 'TEAM_ID_home_rank'})

# Merging the stats for the away team for each game
complete_stats = home_stats.merge(df_ranking[['TEAM_ID', 'STANDINGSDATE', 'W_PCT']], left_on=['VISITOR_TEAM_ID', 'GAME_DATE_EST'], right_on=['TEAM_ID', 'STANDINGSDATE'])

# Renaming columns to improve clarity
complete_stats = complete_stats.rename(columns={
    'W_PCT': 'W_PCT_away',
    'VISITOR_TEAM_ID': 'AWAY_TEAM_ID'
})

# Dropping redundant columns
complete_stats = complete_stats.drop(columns=['TEAM_ID_home_rank', 'STANDINGSDATE_x', 'STANDINGSDATE_y', 'TEAM_ID', 'TEAM_ID_home', 'TEAM_ID_away'])


print(complete_stats.columns)

complete_stats.to_csv("team_stats.csv", index=False)