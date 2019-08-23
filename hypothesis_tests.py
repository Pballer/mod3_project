"""
This module is for your final hypothesis tests.
Each hypothesis test should tie to a specific analysis question.

Each test should print out the results in a legible sentence
return either "Reject the null hypothesis" or "Fail to reject the null hypothesis" depending on the specified alpha
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower

import math

power_analysis = TTestIndPower()
BUCKS = 'Milwaukee Bucks'

def create_sample_dists(cleaned_data_a, cleaned_data_b, y_var=None, categories=[], size = 1000):
    """
    Each hypothesis test will require you to create a sample distribution from your data
    Best make a repeatable function

    :param cleaned_data:
    :param y_var: The numeric variable you are comparing
    :param categories: the categories whose means you are comparing
    :return: a list of sample distributions to be used in subsequent t-tests

    """
    htest_dfs = []
    
    means1 = []
    means2 = []
    for i in range(100):
        means1.append(np.random.choice(cleaned_data_a, size = size, replace=True).mean())
        means2.append(np.random.choice(cleaned_data_b, size = size, replace=True).mean())
    htest_dfs = [np.array(means1), np.array(means2)]

    # Main chunk of code using t-tests or z-tests
    return htest_dfs

def cohen_d(group1, group2):
    """Compute Cohen's d."""

    diff = abs(group1.mean() - group2.mean())

    n1 = len(group1)
    n2 = len(group2)
    var1 = group1.var()
    var2 = group2.var()

    # Calculate the pooled threshold as shown earlier
    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)

    # Calculate Cohen's d statistic
    d = diff / np.sqrt(pooled_var)

    return d


def compare_pval_alpha(p_val, alpha):
    status = ''
    if p_val > alpha:
        status = "Fail to reject"
    else:
        status = 'Reject'
    return status


def hypothesis_test_one(alpha, clean_data):
    """
    Describe the purpose of your hypothesis test in the docstring
    These functions should be able to test different levels of alpha for the hypothesis test.
    If a value of alpha is entered that is outside of the acceptable range, an error should be raised.

    :param alpha: the critical value of choice
    :param cleaned_data:
    :return:
    """
    
    team_wins = clean_data.loc[clean_data.game_season > 2008, ['game_date', 'team_full_name', 
                                                            'is_home', 'home_won', 'game_home_team_score', 
                                                            'game_visitor_team_score', 'home_spread', 'away_spread']]
    team_wins = team_wins.drop_duplicates()
    home_teams = team_wins.loc[(team_wins.is_home == 1)]
    away_teams = team_wins.loc[(team_wins.is_home == 0)]
    
    # Get data for tests
    comparison_groups = create_sample_dists(home_teams.game_home_team_score.copy(), 
                                            away_teams.game_visitor_team_score.copy())

    ttest_results = stats.ttest_ind(home_teams.game_home_team_score, away_teams.game_visitor_team_score, equal_var=False)
    print(ttest_results)
    p_val = ttest_results[1]

    # starter code for return statement and printed results
    status = compare_pval_alpha(ttest_results[1], alpha)
    
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = cohen_d(home_teams.game_home_team_score, away_teams.game_visitor_team_score)
        power = power_analysis.solve_power(effect_size=coh_d, nobs1=30, alpha=alpha)

    print(f'Based on the p value of {p_val} and our aplha of {alpha} we {status.lower()}  the null hypothesis.'
          f'\n Due to these results, we  {assertion} state that there is a difference between total points scored at home vs away.')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} and power of {power}.")
    else:
        print(".")

    return status

def hypothesis_test_two(alpha, clean_data):
    """
    Describe the purpose of your hypothesis test in the docstring
    These functions should be able to test different levels of alpha for the hypothesis test.
    If a value of alpha is entered that is outside of the acceptable range, an error should be raised.

    :param alpha: the critical value of choice
    :param cleaned_data:
    :return:
    """
    
    bucks = clean_data.loc[clean_data.team_full_name == BUCKS, 
                           ['game_date', 'team_full_name', 
                            'is_home', 'home_won', 'game_home_team_score', 
                            'game_visitor_team_score', 'home_spread', 
                            'away_spread', 'game_season']
                          ].drop_duplicates()
    
    bucks_home_spread = bucks.loc[bucks.is_home == 1, ['is_home', 'home_spread']]
    bucks_away_spread = bucks.loc[bucks.is_home == 0, ['is_home', 'away_spread']]
    
    # Get data for tests
    comparison_groups = create_sample_dists(bucks_home_spread.home_spread, 
                                            bucks_away_spread.away_spread,
                                            size=50)

    ttest_results = stats.ttest_ind(bucks_home_spread.home_spread, 
                                    bucks_away_spread.away_spread, 
                                    equal_var=False)
    p_val = ttest_results[1]

    # starter code for return statement and printed results
    status = compare_pval_alpha(ttest_results[1], alpha)
    
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = cohen_d(bucks_home_spread.home_spread, 
                        bucks_away_spread.away_spread)
        power = power_analysis.solve_power(effect_size=coh_d, nobs1=30, alpha=alpha)

    print(f'Based on the p value of {p_val} and our aplha of {alpha} we {status.lower()}  the null hypothesis.'
          f'\n Due to these results, we  {assertion} state that there is a difference '
          f'between the spread of the Bucks when they play at home vs away.')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} and power of {power}.")
    else:
        print(".")

    return status

def hypothesis_test_three(alpha, clean_data):
    """
    Describe the purpose of your hypothesis test in the docstring
    These functions should be able to test different levels of alpha for the hypothesis test.
    If a value of alpha is entered that is outside of the acceptable range, an error should be raised.

    :param alpha: the critical value of choice
    :param cleaned_data:
    :return:
    """
    
    bucks = clean_data.loc[
        clean_data.team_full_name == BUCKS, 
        ['game_date', 'team_full_name', 
         'is_home', 'home_won', 'game_home_team_score', 
         'game_visitor_team_score', 'home_spread', 
         'away_spread', 'game_season']
    ].drop_duplicates()
    
    bucks_2017 = bucks.loc[bucks.game_season == 2017]
    bucks_2018 = bucks.loc[bucks.game_season == 2018]
    
    bucks_2017_final = pd.concat(
        [bucks_2017.loc[(bucks_2017.is_home == 1), 'game_home_team_score'],
         bucks_2017.loc[(bucks_2017.is_home == 0), 'game_visitor_team_score']])
    
    bucks_2018_final = pd.concat(
        [bucks_2018.loc[(bucks_2018.is_home == 1), 'game_home_team_score'],
         bucks_2018.loc[(bucks_2018.is_home == 0), 'game_visitor_team_score']])
    
    # Get data for tests
    comparison_groups = create_sample_dists(bucks_2017_final, 
                                            bucks_2018_final)

    ttest_results = stats.ttest_ind(bucks_2017_final, 
                                    bucks_2018_final, 
                                    equal_var=False)
    p_val = ttest_results[1]

    # starter code for return statement and printed results
    status = compare_pval_alpha(ttest_results[1], alpha)
    
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = cohen_d(bucks_2017_final, 
                        bucks_2018_final)
        power = power_analysis.solve_power(effect_size=coh_d, nobs1=30, alpha=alpha)

    print(f'Based on the p value of {p_val} and our aplha of {alpha} we {status.lower()}  the null hypothesis.'
          f'\n Due to these results, we  {assertion} state that there is a difference '
          f'between Gianni\'s total points scored when he plays at home vs away.')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} and power of {power}.")
    else:
        print(".")

    return status


def hypothesis_test_four(alpha, clean_data):
    """
    Describe the purpose of your hypothesis test in the docstring
    These functions should be able to test different levels of alpha for the hypothesis test.
    If a value of alpha is entered that is outside of the acceptable range, an error should be raised.

    :param alpha: the critical value of choice
    :param cleaned_data:
    :return:
    """
    
    giannis = clean_data.loc[(clean_data.player_first_name == 'Giannis') & (clean_data.player_last_name == 'Antetokounmpo')
                            & clean_data.game_season.isin([2017, 2018])]
    giannis = giannis.reset_index()
    
    giannis_home = giannis.loc[giannis.is_home == 1, ['pts']]
    giannis_away = giannis.loc[giannis.is_home == 0, ['pts']]
    
    # Get data for tests
    comparison_groups = create_sample_dists(giannis_home.pts, 
                                            giannis_away.pts)

    ttest_results = stats.ttest_ind(giannis_home.pts, 
                                    giannis_away.pts, 
                                    equal_var=False)
    p_val = ttest_results[1]

    # starter code for return statement and printed results
    status = compare_pval_alpha(ttest_results[1], alpha)
    
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = cohen_d(giannis_home.pts, 
                        giannis_away.pts)
        power = power_analysis.solve_power(effect_size=coh_d, nobs1=30, alpha=alpha)

    print(f'Based on the p value of {p_val} and our aplha of {alpha} we {status.lower()}  the null hypothesis.'
          f'\n Due to these results, we  {assertion} state that there is a difference '
          f'between Gianni\'s total points scored when he plays at home vs away.')

    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {str(coh_d)} and power of {power}.")
    else:
        print(".")

    return status

