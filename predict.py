import pickle
from nba_api.stats.endpoints import leaguestandings
import pandas as pd

# rb: read binary
model = pickle.load(open('model.pkl', 'rb'))

standings = leaguestandings.LeagueStandings()
df_standings = standings.get_data_frames()[0]

# L10 from the standings represents a team's record over the last 10 games. We need to parse it to turn it into a win rate.
def parse_l10(l10):
    wins, losses = l10.split('-')
    return int(wins)/(int(wins) + int(losses))

df_standings['rolling_win_rate'] = df_standings['L10'].apply(parse_l10)
print(df_standings[['TeamName', 'WinPCT', 'rolling_win_rate']].head())