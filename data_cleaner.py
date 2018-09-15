# %%

# Import modules

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os.path

# read files from csv

matches = pd.read_csv('./results.csv')

if os.path.isfile('world_ranking.csv'):
    world_ranking = pd.read_csv('world_ranking.csv')
else:
    world_ranking_list = pd.read_html(
        'https://us.soccerway.com/teams/rankings/fifa/?ICID=TN_03_05_01')
    world_ranking = world_ranking_list[0]
    world_ranking.to_csv('world_ranking.csv')

# World Cup teams

wc_teams = ['Australia', ' Iran', 'Japan', 'Korea Republic',
            'Saudi Arabia', 'Egypt', 'Morocco', 'Nigeria',
            'Senegal', 'Tunisia', 'Costa Rica', 'Mexico',
            'Panama', 'Argentina', 'Brazil', 'Colombia',
            'Peru', 'Uruguay', 'Belgium', 'Croatia',
            'Denmark', 'England', 'France', 'Germany',
            'Iceland', 'Poland', 'Portugal', 'Russia',
            'Serbia', 'Spain', 'Sweden', 'Switzerland']

# Check the matches data is properly imported

matches.head()
world_ranking.head()

# Drop unwanted column

matches.drop(columns='neutral', inplace=True)
matches.head()

world_ranking = world_ranking[['#', 'Team']]
world_ranking.rename({'#': 'Ranking'}, inplace=True)
world_ranking.to_csv('world_ranking.csv')
# Clean matches dataset

def clean_matches_dataframe(matches):
    # Check for null values in the matches data
    matches.apply(lambda x: sum(x.isnull()))    # zero null value

    type(matches)
    matches.shape

    # Adding winning_team column to the data
    winner = []
    for i in range(len(matches.home_team)):
        if matches['home_score'][i] > matches['away_score'][i]:
            winner.append(matches['home_team'][i])
        elif matches['home_score'][i] < matches['away_score'][i]:
            winner.append(matches['away_team'][i])
        else:
            winner.append('Draw')
    matches['winning_team'] = winner

    # Adding goal_difference column to the data
    matches['goal_difference'] = np.absolute(
        matches['home_score'] - matches['away_score'])

    # Remove unwanted columns
    matches = matches.drop(['date', 'home_score', 'away_score',
                            'goal_difference', 'tournament', 'city', 'country'], axis=1)

    return matches

matches = clean_matches_dataframe(matches)

#Remove teams that are not playing in World Cup 2018

df_teams_home = matches[matches['home_team'].isin(wc_teams)]
df_teams_away = matches[matches['away_team'].isin(wc_teams)]
df_teams = pd.concat((df_teams_home, df_teams_away))
df_teams.drop_duplicates()

# Adding team ranking to main dataframe

def attach_dataframes(team, df_teams):
    world_ranking = pd.read_csv('world_ranking.csv')
    df_teams.rename(columns={team: 'Team'}, inplace=True)
    df_teams = pd.merge(df_teams, world_ranking, on='Team', how='left')
    df_teams.rename(columns={'Team': team, '#': team[0:5]+'ranking'}, inplace=True)
    return df_teams

df_teams = attach_dataframes('home_team', df_teams)
df_teams = attach_dataframes('away_team', df_teams)

print(df_teams.apply(lambda x: sum(x.isnull())))        # find null values

df_teams.fillna(212, inplace=True)

print(df_teams.apply(lambda x: sum(x.isnull())))

# Export dataframe to csv file

df_teams.to_csv('train_wc.csv')

