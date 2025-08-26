# =========================
# Football Prediction – FULL SCRIPT (FutureWarnings fixed: observed=True)
# =========================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------------
# Setup
# -----------------------------------
os.makedirs('visuals', exist_ok=True)
sns.set_theme(context='talk')
plt.rcParams.update({'figure.dpi': 120})

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
    df = pd.read_csv(url)
    # Create Season label like "2005/2006"
    start_year = int("20" + season[:2])
    end_year = int("20" + season[2:])
    df["Season"] = f"{start_year}/{end_year}"
    all_dfs.append(df)

# Concatenate all DataFrames
big_df = pd.concat(all_dfs, ignore_index=True)

# Order seasons for nicer x-axes and to make Season categorical (used by groupby observed=True)
season_order = sorted(big_df['Season'].unique())
big_df['Season'] = pd.Categorical(big_df['Season'], categories=season_order, ordered=True)

# -----------------------------------
# Top-6 teams list
# -----------------------------------
top_teams = ['Man City', 'Man United', 'Liverpool', 'Chelsea', 'Arsenal', 'Tottenham']

# =============== Helpers to keep code DRY ===============
def sum_by(df, keys, value_col, out_name=None):
    """Groupby sum with observed=True to avoid FutureWarnings."""
    g = df.groupby(keys, observed=True)[value_col].sum().reset_index()
    if out_name and out_name != value_col:
        g = g.rename(columns={value_col: out_name})
    return g
# ========================================================

# ===================================
# Goals Scored (Top 6)
# ===================================
goals_home_scored = sum_by(big_df, ['Season', 'HomeTeam'], 'FTHG', 'Goals')
goals_away_scored = sum_by(big_df, ['Season', 'AwayTeam'], 'FTAG', 'Goals')
goals_home_scored = goals_home_scored.rename(columns={'HomeTeam': 'Team'})
goals_away_scored = goals_away_scored.rename(columns={'AwayTeam': 'Team'})
goals_total_scored = pd.concat([goals_home_scored, goals_away_scored], ignore_index=True)
goals_total_scored = sum_by(goals_total_scored, ['Season', 'Team'], 'Goals', 'Goals')
goals_total_scored_top6 = goals_total_scored[goals_total_scored['Team'].isin(top_teams)]

plt.figure(figsize=(14, 8))
sns.lineplot(data=goals_total_scored_top6, x='Season', y='Goals', hue='Team', marker='o')
plt.title('Goals Scored per Season (Top 6 Teams)', fontsize=16)
plt.xticks(rotation=45)
plt.ylabel('Goals Scored')
plt.xlabel('Season')
plt.tight_layout()
plt.savefig('visuals/goals_scored_top6_per_season.png')
plt.close()

# ===================================
# Goals Conceded (Top 6)
# ===================================
goals_home_conceded = sum_by(big_df, ['Season', 'HomeTeam'], 'FTAG', 'GoalsConceded')
goals_away_conceded = sum_by(big_df, ['Season', 'AwayTeam'], 'FTHG', 'GoalsConceded')
goals_home_conceded = goals_home_conceded.rename(columns={'HomeTeam': 'Team'})
goals_away_conceded = goals_away_conceded.rename(columns={'AwayTeam': 'Team'})
goals_total_conceded = pd.concat([goals_home_conceded, goals_away_conceded], ignore_index=True)
goals_total_conceded = sum_by(goals_total_conceded, ['Season', 'Team'], 'GoalsConceded', 'GoalsConceded')
goals_total_conceded_top6 = goals_total_conceded[goals_total_conceded['Team'].isin(top_teams)]

plt.figure(figsize=(14, 8))
sns.lineplot(data=goals_total_conceded_top6, x='Season', y='GoalsConceded', hue='Team', marker='o')
plt.title('Goals Conceded per Season (Top 6 Teams)', fontsize=16)
plt.xticks(rotation=45)
plt.ylabel('Goals Conceded')
plt.xlabel('Season')
plt.tight_layout()
plt.savefig('visuals/goals_conceded_top6_per_season.png')
plt.close()

# ===================================
# Net Goals (Top 6)
# ===================================
net_goals_df = pd.merge(
    goals_total_scored.rename(columns={'Goals': 'GoalsScored'}),
    goals_total_conceded,
    on=['Season', 'Team'],
    how='inner'
)
net_goals_df['NetGoals'] = net_goals_df['GoalsScored'] - net_goals_df['GoalsConceded']
net_goals_top6 = net_goals_df[net_goals_df['Team'].isin(top_teams)]

plt.figure(figsize=(14, 8))
sns.lineplot(data=net_goals_top6, x='Season', y='NetGoals', hue='Team', marker='o')
plt.title('Net Goals per Season (Top 6 Teams)', fontsize=16)
plt.xticks(rotation=45)
plt.ylabel('Net Goals (Scored - Conceded)')
plt.xlabel('Season')
plt.tight_layout()
plt.savefig('visuals/net_goals_top6_per_season.png')
plt.close()

# ===================================
# Average Goals per Match (Top 6)
# ===================================
home_matches = big_df.groupby(['Season', 'HomeTeam'], observed=True).size().reset_index(name='Matches')
away_matches = big_df.groupby(['Season', 'AwayTeam'], observed=True).size().reset_index(name='Matches')
home_matches = home_matches.rename(columns={'HomeTeam': 'Team'})
away_matches = away_matches.rename(columns={'AwayTeam': 'Team'})
total_matches = pd.concat([home_matches, away_matches], ignore_index=True)
total_matches = sum_by(total_matches, ['Season', 'Team'], 'Matches', 'Matches')

avg_goals = pd.merge(
    goals_total_scored.rename(columns={'Goals': 'GoalsScored'}),
    total_matches,
    on=['Season', 'Team'],
    how='inner'
)
avg_goals['AvgGoalsPerMatch'] = avg_goals['GoalsScored'] / avg_goals['Matches']
avg_goals_top6 = avg_goals[avg_goals['Team'].isin(top_teams)]

plt.figure(figsize=(14, 8))
sns.lineplot(data=avg_goals_top6, x='Season', y='AvgGoalsPerMatch', hue='Team', marker='o')
plt.title('Average Goals per Match per Season (Top 6 Teams)', fontsize=16)
plt.xticks(rotation=45)
plt.ylabel('Average Goals per Match')
plt.xlabel('Season')
plt.tight_layout()
plt.savefig('visuals/avg_goals_per_match_top6.png')
plt.close()

# ===================================
# NEW: Home vs Away Goals (Top 6) – side-by-side panels
# ===================================
home_goals_only = sum_by(big_df, ['Season', 'HomeTeam'], 'FTHG', 'HomeGoals').rename(columns={'HomeTeam': 'Team'})
away_goals_only = sum_by(big_df, ['Season', 'AwayTeam'], 'FTAG', 'AwayGoals').rename(columns={'AwayTeam': 'Team'})

home_goals_top6 = home_goals_only[home_goals_only['Team'].isin(top_teams)]
away_goals_top6 = away_goals_only[away_goals_only['Team'].isin(top_teams)]

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(22, 9), sharey=False)

# Panel A: Home Goals
sns.barplot(data=home_goals_top6, x='Season', y='HomeGoals', hue='Team', dodge=True, ax=axes[0])
axes[0].set_title('Home Goals per Season (Top 6 Teams)')
axes[0].set_xlabel('Season')
axes[0].set_ylabel('Home Goals')
for label in axes[0].get_xticklabels():
    label.set_rotation(45); label.set_ha('right')
axes[0].legend(title='Team', bbox_to_anchor=(1.02, 1), loc='upper left')

# Panel B: Away Goals
sns.barplot(data=away_goals_top6, x='Season', y='AwayGoals', hue='Team', dodge=True, ax=axes[1])
axes[1].set_title('Away Goals per Season (Top 6 Teams)')
axes[1].set_xlabel('Season')
axes[1].set_ylabel('Away Goals')
for label in axes[1].get_xticklabels():
    label.set_rotation(45); label.set_ha('right')
axes[1].legend(title='Team', bbox_to_anchor=(1.02, 1), loc='upper left')

plt.tight_layout()
plt.savefig('visuals/home_vs_away_goals_top6_per_season.png')
plt.close()

print(
    "Saved:",
    "visuals/goals_scored_top6_per_season.png,",
    "visuals/goals_conceded_top6_per_season.png,",
    "visuals/net_goals_top6_per_season.png,",
    "visuals/avg_goals_per_match_top6.png,",
    "visuals/home_vs_away_goals_top6_per_season.png"
)
