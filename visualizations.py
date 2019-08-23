"""
This module is for your final visualization code.
One visualization per hypothesis question is required.
A framework for each type of visualization is provided.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Set specific parameters for the visualizations
large = 22; med = 16; small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")


def overlapping_density(package=None, input_vars=None, target_vars=None):
    """
    Set the characteristics of your overlapping density plot
    All arguments are set to None purely as a filler right now

    Function takes package name, input variables(categories), and target variable as input.
    Returns a figure

    Should be able to call this function in later visualization code.

    PARAMETERS

    :param package:        should only take sns or matplotlib as inputs, any other value should throw and error
    :param input_vars:     should take the x variables/categories you want to plot
    :param target_vars:    the y variable of your plot, what you are comparing
    :return:               fig to be enhanced in subsequent visualization functions
    """

    # Set size of figure
    fig = plt.figure(figsize=(16, 10), dpi=80)

    # Starter code for figuring out which package to use
    if package == "sns":
        for variable in input_vars:
            sns.kdeplot(...)
    elif package == 'matplotlib':
        for variable in input_vars:
            plt.plot(..., label=None, linewidth=None, color=None, figure = fig)

    return fig



def boxplot_plot(package=None, input_vars=None, target_vars=None):
    """
    Same specifications and requirements as overlapping density plot

    Function takes package name, input variables(categories), and target variable as input.
    Returns a figure

    PARAMETERS

    :param package:        should only take sns or matplotlib as inputs, any other value should throw and error
    :param input_vars:     should take the x variables/categories you want to plot
    :param target_vars:    the y variable of your plot, what you are comparing
    :return:               fig to be enhanced in subsequent visualization functions
    """
    plt.figure(figsize=(16, 10), dpi=80)

    pass


def visualization_one(htest_dfs, output_image_name=None):
    """
    The visualization functions are what is used to create each individual image.
    The function should be repeatable if not generalizable
    The function will call either the boxplot or density plot functions you wrote above

    :param target_var:
    :param input_vars:
    :param output_image_name: the desired name for the image saved
    :return: outputs a saved png file and returns a fig object for testing
    """
    
    fig = plt.figure(figsize=(15,9))
    sns.distplot(htest_dfs[0], label='Home Team')
    sns.distplot(htest_dfs[1], label='Away Team')
    plt.xlabel('Points Per Game', figure=fig)
    plt.title('Home Team vs Away Team', figure=fig)
    plt.ylabel('Frequency', figure=fig)
    plt.legend();

    # exporting the image to the img folder
    plt.savefig(f'img/{output_image_name}.png', transparent = True, figure = fig)
    return fig


# please fully flesh out this function to meet same specifications of visualization one

def visualization_two(comparison_groups, output_image_name):
    
    spreads = pd.DataFrame(comparison_groups).T
    spreads.columns = ['Home', 'Away']
    
    fig = plt.figure(figsize=(5,10))
    box_plot = sns.boxplot(x="Location", y="Points", data=pd.melt(spreads, value_name='Points', var_name='Location'), width=.5)
    box_plot.set_title('Home vs Away Point Spread');
    
    plt.savefig(f'img/{output_image_name}.png', transparent = True, figure = fig)

def visualization_three(comparison_groups, output_image_name):
    
    fig = plt.figure(figsize=(15,9))
    sns.distplot(comparison_groups[0], label='Bucks 2017')
    sns.distplot(comparison_groups[1], label='Bucks 2018')
    plt.title('Bucks Performance 2017 vs 2018 Season', figure=fig)
    plt.xlabel('Points Scored', figure=fig)
    plt.ylabel('Frequency', figure=fig)
    plt.legend();
    
    plt.savefig(f'img/{output_image_name}.png', transparent = True, figure = fig)

def visualization_four(htest_dfs, output_image_name):
    
    fig = plt.figure(figsize=(15,9))
    sns.distplot(htest_dfs[0], label='Home')
    sns.distplot(htest_dfs[1], label='Away')
    plt.legend()
    plt.ylabel('Frequency', figure=fig)
    plt.xlabel('Points Scored', figure=fig)
    plt.title('Giannis Antetokounmpo Home vs Away Performance', figure=fig)
    
    plt.savefig(f'img/{output_image_name}.png', transparent = True, figure = fig)
