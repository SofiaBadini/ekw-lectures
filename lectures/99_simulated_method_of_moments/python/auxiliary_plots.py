""" Auxiliary file containing functions for plots for the notebook on simulated method of moments estimation.
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import respy as rp
from python.auxiliary_core import *


def plot_criterion_params(params, criterion_args): 
    
    param_names = ['delta', 'wage_fishing', 'nonpec_fishing', 'nonpec_hammock', ('shocks_sdcorr, sd_fishing'), ('shocks_sdcorr, sd_hammock'), ('shocks_sdcorr, corr_hammock_fishing')]
    lbounds = [0.93, 0.069, -0.11, 1.02, 0.008, 0.008, -0.1] 
    ubounds = [0.97, 0.071, -0.09, 1.054, 0.012, 0.012, 0.1] 
    xticks_steps = [0.005 ,0.0005, 0.005, 0.005, 0.0005, 0.0005, 0.05] 
    detail = 20     
    
    for idx in range(len(param_names)):        
        parameters = params.copy()
        # Position of subplot
        plt.subplot(len(param_names), 1, idx+1)
        # Define grid of parameter values and calculate the criterion function value for this grid.
        x_grid = np.linspace(lbounds[idx], ubounds[idx], detail)
        fvals_grid = ([])
        for param in x_grid:
            parameters.loc[param_names[idx],'value'] = param
            fval = evaluate(parameters, *criterion_args)
            fvals_grid.append(fval)
       
        # Plot criterion function for the calculated values. 
        plt.xticks(np.arange(lbounds[idx], ubounds[idx], step=xticks_steps[idx]))
        plt.plot(x_grid, fvals_grid)
        plt.xlabel(param_names[idx])
        plt.ylabel('Criterion Function')    
        plt.show()
    

def plot_criterion_detail(params, criterion_args):
    """ Plots criterion function for one or multiple ranges of values for a single parameter in the model.
    Args:
    params(pd.DataFrame): Dataframe containing the parameters in the model.
    param_name(string): Name of the parameter that should be varied to plot the criterion function.
    lbounds(list): Lower bound of the range of parameter values that should be calculated. Multiple values can be 
                   specified to plot the criterion function at different ranges of the parameter values.
    ubounds(list): Upper bound of the range of parameter values that should be calculated. Must be the same length as
                    lbounds.
    xticks_steps(list): List that specifies the step size for the ticks of the xaxis.
    criterion_args(list): List of arguments that need to be specified for the criterion function which is called for 
                          plotting (Args: options, weighting_matrix, moments_obs, choice_options)
    detail(int): Number of parameter values that the criterion function should be calculated for. Determines
                 the accuracy of the plotted function. 
    Returns:
    plots 
    --------------------------------------------------------------------------------------------------------------------
    """
    params = params.copy()

    param_name = 'delta' 
    lbounds = [0.93, 0.9499]
    ubounds = [0.97, 0.9501]
    xticks_steps = [0.005, 0.00005]
    detail = 20

    
    for idx in range(len(lbounds)):
        # Position of subplot
        plt.subplot(len(lbounds), 1, idx+1)
        # Define grid of parameter values and calculate the criterion function value for this grid.
        x_grid = np.linspace(lbounds[idx], ubounds[idx], detail)
        fvals_grid = ([])
        for param in x_grid:
            params.loc[param_name,'value'] = param
            fval = evaluate(params, *criterion_args)
            fvals_grid.append(fval)
       
        # Plot criterion function for the calculated values. 
        plt.xticks(np.arange(lbounds[idx], ubounds[idx], step=xticks_steps[idx]))
        plt.plot(x_grid, fvals_grid)
        plt.xlabel(param_name)
        plt.ylabel('Criterion Function')
    plt.show()
            
    
    
def plot_moments_choices(moments_obs, moments_sim):
    
    moments = [moments_obs, moments_sim]
    titles = ["Data Moments", "Simulated Moments"]
    
    for idx in [0,1]:
        df = pd.DataFrame(moments[idx]['Choice Probabilities']).transpose()
        df = df.rename(columns={0: "fishing", 1: "hammock"})

        plt.subplot(1, 2, idx+1)
        plt.ylim((0,1))
        plt.title(titles[idx])
        plt.plot(pd.DataFrame(moments[idx]['Choice Probabilities']).transpose())
        plt.xlabel("Period")
        plt.ylabel("Choice Proportion")
        if idx == 1:
            plt.legend(df.columns, loc="best")
    
    plt.tight_layout()
    plt.show()
    
    
def plot_moments_wage(moments_obs, moments_sim):
    
    df_sim = pd.DataFrame(moments_sim['Wage Distribution']).transpose()    
    df_obs = pd.DataFrame(moments_obs['Wage Distribution']).transpose()    
    
    plt.subplot(1, 2, 1)
    plt.title('Mean')
    plt.plot(df_obs[0])
    plt.plot(df_sim[0])
    plt.xlabel('Period')
    
    plt.subplot(1, 2, 2)
    plt.title('Std')
    plt.plot(df_obs[1], label = "observed")
    plt.plot(df_sim[1], label = "simulated")
    plt.legend(loc="best")
    plt.xlabel('Period')
    
    plt.tight_layout()
    plt.show()