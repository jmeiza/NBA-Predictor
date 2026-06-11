import pandas as pd

df = pd.read_csv("games.csv")
df_teams = pd.read_csv("teams.csv")

# Adding a column to record when the team that played away wins. Must come before dropna()
df['AWAY_TEAM_WINS'] = 1 - df['HOME_TEAM_WINS']

df = df.dropna() # dropping missing rows

# getting the average stats for each time when they were at home. We reset the index because after using groupby(), HOME_TEAM_ID becomes an index which can't be used in a merge.
home_stats=df.groupby('HOME_TEAM_ID')[['PTS_home','FG_PCT_home','AST_home','REB_home','HOME_TEAM_WINS']].mean().reset_index()


# getting the average stats for each time a team is playing away
away_stats = df.groupby('VISITOR_TEAM_ID')[['PTS_away','FG_PCT_away','AST_away','REB_away','AWAY_TEAM_WINS']].mean().reset_index()


# NOTE: "left_on" refers to the DataFrame you are merging from (home_stats) and "right_on" refers to the DataFrame you're merging in (df_teams). It merges whenever home_Team_id and team_id match.
home_stats = home_stats.merge(df_teams[['TEAM_ID','NICKNAME']], left_on='HOME_TEAM_ID', right_on='TEAM_ID')

complete_stats = home_stats.merge(away_stats, left_on='HOME_TEAM_ID', right_on='VISITOR_TEAM_ID')

print(complete_stats[['NICKNAME', 'PTS_home', 'FG_PCT_home', 'AST_home', 'REB_home', 'HOME_TEAM_WINS','PTS_away','FG_PCT_away','AST_away','REB_away','AWAY_TEAM_WINS']])