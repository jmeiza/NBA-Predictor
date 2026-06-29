import pandas as pd

df = pd.read_csv("games.csv")
df_teams = pd.read_csv("teams.csv")
df_ranking = pd.read_csv("ranking.csv")

# Dropping rows where stats are missing
df = df.dropna()

# print(df.shape) # (row,columns)
# print(df.columns) # column names
# print(df[['HOME_TEAM_ID','TEAM_ID_home','TEAM_ID_away']])
# print(df.head()) # first 5 rows
# print(df.isnull().sum()) # missing values

# print(df['HOME_TEAM_WINS'].mean())

# print(df_teams.shape) # (row,columns)
# print(df_teams.columns) # column names
# print(df_teams.head()) # first 5 rows
# print(df_teams.isnull().sum()) # missing values

#print(df_teams[['TEAM_ID','NICKNAME', 'CITY']].head(10))

print(df_ranking[df_ranking['TEAM_ID'] == 1610612747].sort_values('STANDINGSDATE').head(20))
