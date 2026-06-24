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
# stats25 = leaguedashplayerstats.LeagueDashPlayerStats(
#     season='2025-26',
#     season_type_all_star='Regular Season',
#     per_mode_detailed='Per100Possessions'
# )
# #1 would get playoffs
# df25 = stats25.get_data_frames()[0]

#store seasons and stat types
seasons = []
for year in range(2008, 2025):
    start_year = year
    end_year = str(year + 1)[2:]  # Gets the last two digits of the next year
    seasons.append(f"{start_year}-{end_year}")

#^(Base)|(Advanced)|(Misc)|(Four Factors)|(Scoring)|(Opponent)|(Usage)|(Defense)$
measures = ['Base', 'Advanced', 'Usage', 'Scoring', 'Misc', 'Defense']
per_modes = ['Totals','PerGame']

# 2. Master storage dictionary {measure_type: [list_of_dfs]}
master_data = {m: [] for m in measures}

# # Lists to store DataFrames for combining later
# regular_season_dfs = []
# advanced_season_dfs = []

# 2. Loop through each season and fetch the data
for season in seasons:
    print(f"--- Pulling Season: {season} ---")
    for measure in measures:
        for per_mode in per_modes:
            try:
                stats = leaguedashplayerstats.LeagueDashPlayerStats(
                    season=season,
                    season_type_all_star='Regular Season',
                    per_mode_detailed=per_mode, #total or perGame
                    measure_type_detailed_defense=measure
                )
                df = stats.get_data_frames()[0]
                df['SEASON'] = season
                master_data[measure].append(df)
                time.sleep(2.6)
                
            except Exception as e:
                print(f"Error [{season} - {measure}]: {e}")
                time.sleep(10)

# 4. Concatenate and flatten each category
flattened_dfs = {m: pd.concat(master_data[m], ignore_index=True) for m in measures}

# 5. Merge all categories sequentially on unique identifiers
final_df = flattened_dfs[measures[0]]

for measure in measures[1:]:
    final_df = pd.merge(
        final_df, 
        flattened_dfs[measure], 
        on=['PLAYER_ID', 'TEAM_ID', 'SEASON'], 
        suffixes=('', f'_{measure.lower()}')
    )

# 6. Drop duplicate columns generated across the datasets
duplicate_cols = [c for c in final_df.columns if any(c.endswith(f'_{m.lower()}') for m in measures)]
final_df.drop(columns=duplicate_cols, inplace=True)

final_df.to_csv("2 deliveries\\nba_comprehensive_stats_08_to_25.csv", index=False)
print(f"Successfully compiled all matrices! Matrix shape: {final_df.shape}")

# Optional: Save the final datasets directly to CSV files
# df_all_regular_season = pd.concat(regular_season_dfs, ignore_index=True)
# df_all_advanced = pd.concat(advanced_season_dfs, ignore_index=True)

# df_all_regular_season.to_csv("per_game_seasons_08_to_25.csv", index=False)
# df_all_advanced.to_csv("adv_seasons_08_to_25.csv", index=False)
# df_all_playoffs.to_csv("nba_all_playoffs_08_to_25.csv", index=False)


# ## get them all into 1 df
# df_combined = pd.merge(
#     df_all_regular_season,
#     df_all_advanced,
#     on=['PLAYER_ID', 'TEAM_ID', 'SEASON'],
#     suffixes=('', '_advanced')  # Handles columns that exist in both datasets
# )
# # Clean up duplicate columns (like overlapping PLAYER_NAME or TEAM_ID fields)
# duplicate_cols = [col for col in df_combined.columns if col.endswith('_advanced')]
# df_combined.drop(columns=duplicate_cols, inplace=True)

# # Save the unified dataset to a CSV file
# df_combined.to_csv("nba_combined_stats_08_to_25.csv", index=False)
# print(f"Merge complete! Final dataset contains {df_combined.shape[1]} columns.")


# # 1. Search for a player to get their unique ID
# nba_players = players.get_players()
# lebron = [p for p in nba_players if p['full_name'] == 'LeBron James'][0]
# lebron_id = lebron['id']
# # 2. Fetch game logs for a specific season
# bron_games = playergamelog.PlayerGameLog(player_id=lebron_id, season='2025-26')
# # 3. Convert the results directly into a Pandas DataFrame
# bron_games2 = bron_games.get_data_frames()[0]

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
