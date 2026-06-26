import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

df_team_stats = pd.read_csv("team_stats.csv")


# We are only keeping the columns the model will need to use to predict the winner.
features = df_team_stats[['W_PCT_home', 'W_PCT_away','HOME_TEAM_WINS']]

# Split the features into X(inputs)and Y(output). The model predicts Y using X. 
X = features.drop(columns=['HOME_TEAM_WINS'])
X['W_PCT_diff'] = X['W_PCT_home'] - X['W_PCT_away']
Y = features['HOME_TEAM_WINS']

# CODE FOR TRAINING THE MODEL

## Step 1: We split the data into training data and testing data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

## Step 2: Ceate and train (fit) the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

## Step 3: Evaluate the model
predictions = model.predict(X_test) # Runs the model on the test data
print(accuracy_score(y_test, predictions))  # Compares the preditions to the actua results

