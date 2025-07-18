import pandas as pd

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

# Quick check
print(big_df[["Season", "Date"]].head())
