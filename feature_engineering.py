import pandas as pd

df = pd.read_csv("games.csv")
df_teams = pd.read_csv("teams.csv")
df_ranking = pd.read_csv("ranking.csv")


# Adding a column to record when the team that played away wins. Must come before dropna()
df['AWAY_TEAM_WINS'] = 1 - df['HOME_TEAM_WINS']

df = df.dropna() # dropping missing rows

# Dropping seasons that are before the 2020 season
df = df[df['SEASON'] >= 2020]

# NOTE: "left_on" refers to the DataFrame you are merging from (df) and "right_on" refers to the DataFrame you're merging in (df_ranking). It merges whenever the value of the columns in the lists match,

# Merging the stats for the home team in each game
home_stats = df.merge(df_ranking[['TEAM_ID', 'STANDINGSDATE', 'W_PCT']], left_on=['TEAM_ID_home', 'GAME_DATE_EST'], right_on=['TEAM_ID', 'STANDINGSDATE'])

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


# print(complete_stats.columns)

complete_stats.to_csv("team_stats.csv", index=False)