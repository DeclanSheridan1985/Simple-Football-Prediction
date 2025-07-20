import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


import os
os.makedirs('visuals', exist_ok=True)


# Seasons to load (folder names in the URLs)
seasons = [
    "2425", "2324", "2223", "2122", "2021", "1920",
    "1819", "1718", "1617", "1516", "1415", "1314",
    "1213", "1112", "1011", "0910", "0809", "0708",
    "0607", "0506"
]

base_url = "https://www.football-data.co.uk/mmz4281/"
all_dfs = []

for season in seasons:
    url = f"{base_url}{season}/E0.csv"
    print(f"Loading {url}...")
    
    # Read CSV
    df = pd.read_csv(url)
    
    # Create Season label like "2005/2006"
    start_year = int("20" + season[:2])
    end_year = int("20" + season[2:])
    season_label = f"{start_year}/{end_year}"
    
    # Add Season column
    df["Season"] = season_label
    
    # Append to list
    all_dfs.append(df)

# Concatenate all DataFrames
big_df = pd.concat(all_dfs, ignore_index=True)


import matplotlib.pyplot as plt
import seaborn as sns

# 📊 Goals Scored per Team per Season (Top 6 Teams)
top_teams = ['Man City', 'Man United', 'Liverpool', 'Chelsea', 'Arsenal', 'Tottenham']

# Aggregate home and away goals
home_goals = big_df.groupby(['Season', 'HomeTeam'])['FTHG'].sum().reset_index()
away_goals = big_df.groupby(['Season', 'AwayTeam'])['FTAG'].sum().reset_index()

# Rename columns
home_goals.rename(columns={'HomeTeam': 'Team', 'FTHG': 'Goals'}, inplace=True)
away_goals.rename(columns={'AwayTeam': 'Team', 'FTAG': 'Goals'}, inplace=True)

# Combine and group
total_goals = pd.concat([home_goals, away_goals])
total_goals = total_goals.groupby(['Season', 'Team'])['Goals'].sum().reset_index()

# Filter for top teams
top_goals = total_goals[total_goals['Team'].isin(top_teams)]

# Plot
plt.figure(figsize=(14, 8))
sns.lineplot(data=top_goals, x='Season', y='Goals', hue='Team', marker='o')
plt.title('Goals Scored per Season (Top 6 Teams)', fontsize=16)
plt.xticks(rotation=45)
plt.ylabel('Goals Scored')
plt.xlabel('Season')
plt.tight_layout()
plt.savefig('visuals/goals_scored_top6_per_season.png')
plt.close()


# 📊 Goals Conceded per Team per Season (Top 6 Teams)
home_conceded = big_df.groupby(['Season', 'AwayTeam'])['FTHG'].sum().reset_index()
away_conceded = big_df.groupby(['Season', 'HomeTeam'])['FTAG'].sum().reset_index()

home_conceded.rename(columns={'AwayTeam': 'Team', 'FTHG': 'GoalsConceded'}, inplace=True)
away_conceded.rename(columns={'HomeTeam': 'Team', 'FTAG': 'GoalsConceded'}, inplace=True)

total_conceded = pd.concat([home_conceded, away_conceded])
total_conceded = total_conceded.groupby(['Season', 'Team'])['GoalsConceded'].sum().reset_index()

# Filter for top teams
top_conceded = total_conceded[total_conceded['Team'].isin(top_teams)]

# Plot
plt.figure(figsize=(14, 8))
sns.lineplot(data=top_conceded, x='Season', y='GoalsConceded', hue='Team', marker='o')
plt.title('Goals Conceded per Season (Top 6 Teams)', fontsize=16)
plt.xticks(rotation=45)
plt.ylabel('Goals Conceded')
plt.xlabel('Season')
plt.tight_layout()
plt.savefig('visuals/goals_conceded_top6_per_season.png')
plt.close()


