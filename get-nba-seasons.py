# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 12:50:29 2026

@author: FFA2830
"""

#from youtube:
# import requests
# from bs4 import BeautifulSoup

# url = 'https://www.nba.com/players'

# content = requests.get(url)

import pandas as pd
import time
# for bron
from nba_api.stats.static import players
#for bron-log
from nba_api.stats.endpoints import playergamelog
#for seasons
#for ts% usg etc from https://www.nba.com/stats/players/advanced
from nba_api.stats.endpoints import leaguedashplayerstats

# 0 one example: get all players in season
stats25 = leaguedashplayerstats.LeagueDashPlayerStats(
    season='2025-26',
    season_type_all_star='Regular Season',
    per_mode_detailed='Per100Possessions'
)
#1 would get playoffs
df25 = stats25.get_data_frames()[0]

#store seasons and stat types
seasons = []
for year in range(2008, 2025):
    start_year = year
    end_year = str(year + 1)[2:]  # Gets the last two digits of the next year
    seasons.append(f"{start_year}-{end_year}")
measures = ['Defense', 'Scoring', 'Advanced', 'Misc', 'Usage']

# 2. Master storage dictionary {measure_type: [list_of_dfs]}
master_data = {m: [] for m in measures}

# # Lists to store DataFrames for combining later
# regular_season_dfs = []
# advanced_season_dfs = []

# 2. Loop through each season and fetch the data
for season_str in seasons:
    print(f"Fetching data for season: {season_str}...")

    try:
        # Fetch Regular Season stats (Per 100 Possessions)
        stats_reg = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season_str,
            season_type_all_star='Regular Season',
            per_mode_detailed='PerGame'
        )
        
        # Extract the DataFrame from the API wrapper
        df_reg = stats_reg.get_data_frames()[0]
        
        # Add a column to track the specific season
        df_reg['SEASON'] = season_str  
        regular_season_dfs.append(df_reg)

        # Pause to prevent the NBA API from blocking your IP
        time.sleep(3.0)

    except Exception as e:
        print(f"Error fetching season {season_str}: {e}")
        time.sleep(6)

    print(f"Fetching advanced data for season: {season_str}...")
    try:
        # Fetch Advanced Stats for the Regular Season
        stats_adv = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season_str,
            season_type_all_star='Regular Season',
            measure_type_detailed_defense='Advanced'  # <-- traditional,adv,scoring,usage,defense
        )
        
        # Extract the DataFrame from the API wrapper
        df_adv = stats_adv.get_data_frames()[0]
        
        # Add a column to track the specific season
        df_adv['SEASON'] = season_str  
        advanced_season_dfs.append(df_adv)

        # Pause to prevent the NBA API from blocking your IP
        time.sleep(2.5)

    except Exception as e:
        print(f"Error fetching advanced season {season_str}: {e}")
        time.sleep(6)

    print(f"Fetching scoring type data for season: {season_str}...")
    try:
        # Fetch Advanced Stats for the Regular Season
        stats_adv = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season_str,
            season_type_all_star='Regular Season',
            measure_type_detailed_defense='Advanced'  # <-- traditional,adv,scoring,usage,defense
        )
        
        # Extract the DataFrame from the API wrapper
        df_adv = stats_adv.get_data_frames()[0]
        
        # Add a column to track the specific season
        df_adv['SEASON'] = season_str  
        advanced_season_dfs.append(df_adv)

        # Pause to prevent the NBA API from blocking your IP
        time.sleep(2.5)

    except Exception as e:
        print(f"Error fetching advanced season {season_str}: {e}")
        time.sleep(6)

# 3. Combine all individual season data into master DataFrames
df_all_regular_season = pd.concat(regular_season_dfs, ignore_index=True)
df_all_advanced = pd.concat(advanced_season_dfs, ignore_index=True)
# df_all_playoffs = pd.concat(playoffs_dfs, ignore_index=True)

# Optional: Save the final datasets directly to CSV files
df_all_regular_season.to_csv("per_game_seasons_08_to_25.csv", index=False)
df_all_advanced.to_csv("adv_seasons_08_to_25.csv", index=False)
# df_all_playoffs.to_csv("nba_all_playoffs_08_to_25.csv", index=False)


## get them all into 1 df
df_combined = pd.merge(
    df_all_regular_season,
    df_all_advanced,
    on=['PLAYER_ID', 'TEAM_ID', 'SEASON'],
    suffixes=('', '_advanced')  # Handles columns that exist in both datasets
)
# Clean up duplicate columns (like overlapping PLAYER_NAME or TEAM_ID fields)
duplicate_cols = [col for col in df_combined.columns if col.endswith('_advanced')]
df_combined.drop(columns=duplicate_cols, inplace=True)

# Save the unified dataset to a CSV file
df_combined.to_csv("nba_combined_stats_08_to_25.csv", index=False)
print(f"Merge complete! Final dataset contains {df_combined.shape[1]} columns.")


# 1. Search for a player to get their unique ID
nba_players = players.get_players()
lebron = [p for p in nba_players if p['full_name'] == 'LeBron James'][0]
lebron_id = lebron['id']
# 2. Fetch game logs for a specific season
bron_games = playergamelog.PlayerGameLog(player_id=lebron_id, season='2025-26')
# 3. Convert the results directly into a Pandas DataFrame
bron_games2 = bron_games.get_data_frames()[0]

## failed below:
#make sure consoles > new console in env > conda:base
# from sportsipy.nba.roster import Player

# game_data = Boxscore('201806080CLE')
# print(game_data.away_points)  # Prints 108
# print(game_data.home_points)  # Prints 85
# df = game_data.dataframe  # Returns a Pandas DataFrame of game metrics

# bron = Player('jamesle01')
# bron.assists()


#player has no attribute data_tree
# for season in player.data_tree:
#     print(f'season: {season}')

# df_seasons = player.dataframe    
