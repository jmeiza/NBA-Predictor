import pandas as pd

df = pd.read_csv("games.csv")
df_teams = pd.read_csv("teams.csv")

df.dropna() # dropping missing rows

# getting the average stats for each time when they were at home
home_stats=df.groupby('HOME_TEAM_ID')[['PTS_home','FG_PCT_home','AST_home','REB_home','HOME_TEAM_WINS']].mean()

# NOTE: "left_on" refers to the DataFrame you are merging from (home_stats) and "right_on" refers to the DataFrame you're merging in (df_teams). It merges whenever home_Team_id and team_id match.
home_stats = home_stats.merge(df_teams[['TEAM_ID','NICKNAME']], left_on='HOME_TEAM_ID', right_on='TEAM_ID')

print(home_stats[['NICKNAME', 'PTS_home', 'FG_PCT_home', 'AST_home', 'REB_home', 'HOME_TEAM_WINS']])