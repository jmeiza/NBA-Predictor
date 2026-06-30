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

# Now we parse the data so we can extract what the model needs
def predict_winner(home_team, away_team):
    # HT: Home Team, AT: Away Team
    # iloc[] means select rows (or values) by their integer position. Like indexing into a list
    HT_row = df_standings[df_standings['TeamName'] == home_team].iloc[0]
    AT_row = df_standings[df_standings['TeamName'] == away_team].iloc[0]

    HT_WinPCT, HT_rolling_win_rate = HT_row['WinPCT'], HT_row['rolling_win_rate'] 

    AT_WinPCT, AT_rolling_win_rate = AT_row['WinPCT'], AT_row['rolling_win_rate']

    input_data = pd.DataFrame([{
        'W_PCT_home': HT_WinPCT,
        'W_PCT_away': AT_WinPCT,
        'home_rolling_win_rate': HT_rolling_win_rate,
        'away_rolling_win_rate': AT_rolling_win_rate,
        'W_PCT_diff': HT_WinPCT - AT_WinPCT,
        'ROLLING_WIN_RATE_diff': HT_rolling_win_rate - AT_rolling_win_rate
    }])
    
    # Passing the extracted data into the model
    probabilities= model.predict_proba(input_data)

    # probabilities[0][0]: probability the home team loses
    # probabilities[0][1]: probability the home team wins

    if probabilities[0][0] > 0.5:
        return f"{away_team} wins ({round(probabilities[0][0]*100, 1)}% confidence)"
    elif probabilities[0][1] > 0.5:
        return f"{home_team} wins ({round(probabilities[0][1]*100, 1)}% confidence)"
    else:
        return f"Too close to call - even odds"

home_team = input("Enter home team: ")
away_team = input("Enter away team: ")

print(predict_winner(home_team, away_team))



    