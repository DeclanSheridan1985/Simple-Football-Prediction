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


# Issue 3 Goals Scored per Team per Season (Top 6 Teams)
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


# Issue 3 Goals Conceded per Team per Season (Top 6 Teams)
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


# --- Issue 5 - Net Goals ---
# --- Goals Scored ---
home_goals = big_df.groupby(['Season', 'HomeTeam'])['FTHG'].sum().reset_index()
away_goals = big_df.groupby(['Season', 'AwayTeam'])['FTAG'].sum().reset_index()
home_goals.rename(columns={'HomeTeam': 'Team', 'FTHG': 'GoalsScored'}, inplace=True)
away_goals.rename(columns={'AwayTeam': 'Team', 'FTAG': 'GoalsScored'}, inplace=True)
total_goals = pd.concat([home_goals, away_goals])
total_goals = total_goals.groupby(['Season', 'Team'])['GoalsScored'].sum().reset_index()

# --- Goals Conceded ---
home_conceded = big_df.groupby(['Season', 'AwayTeam'])['FTHG'].sum().reset_index()
away_conceded = big_df.groupby(['Season', 'HomeTeam'])['FTAG'].sum().reset_index()
home_conceded.rename(columns={'AwayTeam': 'Team', 'FTHG': 'GoalsConceded'}, inplace=True)
away_conceded.rename(columns={'HomeTeam': 'Team', 'FTAG': 'GoalsConceded'}, inplace=True)
total_conceded = pd.concat([home_conceded, away_conceded])
total_conceded = total_conceded.groupby(['Season', 'Team'])['GoalsConceded'].sum().reset_index()

# --- Combine to calculate Net Goals ---
net_goals = pd.merge(total_goals, total_conceded, on=['Season', 'Team'])
net_goals['NetGoals'] = net_goals['GoalsScored'] - net_goals['GoalsConceded']

# Filter Top 6 Teams
net_goals_top6 = net_goals[net_goals['Team'].isin(top_teams)]

# Plot
plt.figure(figsize=(14, 8))
sns.lineplot(data=net_goals_top6, x='Season', y='NetGoals', hue='Team', marker='o')
plt.title('Net Goals per Season (Top 6 Teams)', fontsize=16)
plt.xticks(rotation=45)
plt.ylabel('Net Goals (Scored - Conceded)')
plt.xlabel('Season')
plt.tight_layout()
plt.savefig('visuals/net_goals_top6_per_season.png')
plt.close()



# 6 average goals per match
# --- Top teams filter ---
top_teams = ['Man City', 'Man United', 'Liverpool', 'Chelsea', 'Arsenal', 'Tottenham']

# --- Goals scored per team per season ---
home_goals = big_df.groupby(['Season', 'HomeTeam'])['FTHG'].sum().reset_index()
away_goals = big_df.groupby(['Season', 'AwayTeam'])['FTAG'].sum().reset_index()
home_goals.rename(columns={'HomeTeam': 'Team', 'FTHG': 'Goals'}, inplace=True)
away_goals.rename(columns={'AwayTeam': 'Team', 'FTAG': 'Goals'}, inplace=True)
total_goals = pd.concat([home_goals, away_goals])
total_goals = total_goals.groupby(['Season', 'Team'])['Goals'].sum().reset_index()

# --- Matches played per team per season ---
home_matches = big_df.groupby(['Season', 'HomeTeam']).size().reset_index(name='Matches')
away_matches = big_df.groupby(['Season', 'AwayTeam']).size().reset_index(name='Matches')
home_matches.rename(columns={'HomeTeam': 'Team'}, inplace=True)
away_matches.rename(columns={'AwayTeam': 'Team'}, inplace=True)
total_matches = pd.concat([home_matches, away_matches])
total_matches = total_matches.groupby(['Season', 'Team'])['Matches'].sum().reset_index()

# --- Merge and calculate average goals per match ---
avg_goals = pd.merge(total_goals, total_matches, on=['Season', 'Team'])
avg_goals['AvgGoalsPerMatch'] = avg_goals['Goals'] / avg_goals['Matches']

# --- Filter Top 6 teams ---
avg_goals_top6 = avg_goals[avg_goals['Team'].isin(top_teams)]

# --- Plot ---
plt.figure(figsize=(14, 8))
sns.lineplot(data=avg_goals_top6, x='Season', y='AvgGoalsPerMatch', hue='Team', marker='o')
plt.title('Average Goals per Match per Season (Top 6 Teams)', fontsize=16)
plt.xticks(rotation=45)
plt.ylabel('Average Goals per Match')
plt.xlabel('Season')
plt.tight_layout()
plt.savefig('visuals/avg_goals_per_match_top6.png')
plt.close()