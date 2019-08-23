"""
This module is for your data cleaning.
It should be repeatable.

## PRECLEANING
There should be a separate script recording how you
transformed the json api calls into a dataframe and csv.

## SUPPORT FUNCTIONS
There can be an unlimited amount of support functions.
Each support function should have an informative name
and return the partially cleaned bit of the dataset.
"""
import ast
import pandas as pd



def convert_str_to_dict(nested_dict):
    """Convert json string representation of dictionary to a python dict."""
    return ast.literal_eval(nested_dict)


def expand_dict_to_columns(stats, col_name):
    """Expand nested dict into columns."""
    expanded = pd.DataFrame(stats[col_name]
                            .apply(convert_str_to_dict)
                            .tolist()).add_prefix('{}_'.format(col_name))
    return expanded


def drop_unused_cols(stats):
    """Drop unused cols."""
    cols = ['Unnamed: 0', 'Unnamed: 0.1', 'team', 'player',
            'game', 'ast', 'blk', 'dreb', 'fg3_pct', 'fg3a', 'fg3m', 'fg_pct',
            'fga', 'fgm', 'ft_pct', 'fta', 'ftm', 'id', 'min', 'oreb',
            'pf', 'reb', 'stl', 'turnover', 'team_abbreviation',
            'team_city', 'team_conference', 'team_division', 'team_name',
            'player_height_feet', 'player_height_inches', 'player_id',
            'player_position', 'player_team_id', 'player_weight_pounds',
            'game_period', 'game_status',
            'game_time', 'game_visitor_team_id', ]
    stats = stats.drop(columns=cols)
    return stats


def derived_cols(clean_data):
    """Add columns for home team and spread."""
    clean_data['is_home'] = \
        (clean_data.game_home_team_id == clean_data.team_id).astype(int)
    clean_data['home_won'] = \
        (clean_data.game_home_team_score >= clean_data.game_visitor_team_score).astype(int)
    clean_data['home_spread'] = \
        (clean_data.game_home_team_score - clean_data.game_visitor_team_score).astype(int)
    clean_data['away_spread'] = \
        (clean_data.game_visitor_team_score - clean_data.game_home_team_score).astype(int)
    return clean_data


def remove_postseason(clean_data):
    """Remove post season games."""
    clean_data = clean_data[clean_data['game_postseason'] == False]
    return clean_data


def full_clean():
    """
    This is the one function called that will run all the support functions.
    Assumption: Your data will be saved in a data folder and named "dirty_data.csv"

    :return: cleaned dataset to be passed to hypothesis testing and visualization modules.
    """
    dirty_data = pd.read_csv("./data/dirty_data.csv")
    dirty_data = dirty_data.dropna()

    # Expand nested dicts into columns.
    teams = expand_dict_to_columns(dirty_data, 'team')
    players = expand_dict_to_columns(dirty_data, 'player')
    games = expand_dict_to_columns(dirty_data, 'game')

    dirty_data = dirty_data.join([teams, players, games])
    dirty_data = drop_unused_cols(dirty_data)
    dirty_data = dirty_data.dropna()
    dirty_data = derived_cols(dirty_data)
    cleaned_data = remove_postseason(dirty_data)

    cleaned_data.to_csv('./data/cleaned_for_testing.csv')

    return cleaned_data
