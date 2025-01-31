'''Data loader for UCI letter, spam and MNIST datasets.
'''

########################################################################################################################
# Note: This script is almost a verbatim copy of the counterpart one at https://github.com/jsyoon0823/GAIN,
#       the minimal changes were introduced due to the fact that in our study we used more data per each dataset
#       than what was used in
#       Jinsung Yoon, James Jordon, Mihaela van der Schaar,
#       "GAIN: Missing Data Imputation using Generative Adversarial Nets,"
#       International Conference on Machine Learning (ICML), 2018.
#       The rationale to keep the code, as much as possible, identical to that of (the original) GAIN is to allow
#       fair comparisons.
########################################################################################################################

# Necessary packages
import numpy as np

try:
    from DataLab.GAIN.utils import binary_sampler
except ModuleNotFoundError:
    from DataLab.GAIN.utils import binary_sampler

from typing import Dict, List

DATASETS: Dict[str, List[int]] = {

    # evalution datasets where random missingness has been introduced
    #'2018.ARM.urban' : [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    #'2018.ARM.rural' : [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    #'2011.IND.urban': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
    #'2011.IND.rural': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],

    # outlier-removed datasets ready for imputation
    '2002.BRA.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2004.IND.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2005.GHA.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2008.BRA.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2010.MNG.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2010.VNM.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2011.IND.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2014.GTM.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2014.KHM.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2014.ZAF.urban': [1,2,3,4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
    '2017.BRA.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2017.GHA.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2018.ARM.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2018.ETH.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2018.NGA.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2019.KHM.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2019.NPL.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2019.UGA.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2020.MEX.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2020.RUS.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2020.VNM.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2021.MNG.urban': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2002.BRA.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2004.IND.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2005.GHA.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2008.BRA.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2010.MNG.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2010.VNM.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2011.IND.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2014.GTM.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2014.KHM.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2014.ZAF.rural': [1,2,3,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2017.BRA.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2017.GHA.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2018.ARM.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2018.ETH.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2018.NGA.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2019.KHM.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2019.NPL.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2019.UGA.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2020.MEX.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2020.RUS.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2020.VNM.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],
    '2021.MNG.rural': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27],


    # subsets 1: ['year', 'country', 'hhid', 'hhweight','climatezone', 'urban',  'head_age',
    # 'nrooms', 'head_literate','hhsize', 'tv', 'music', 'fridge', 'exp', 'exp_cap_group']
    "ARM2018_subset1": [5, 6, 7, 8, 9, 10, 11, 12, 13],
    'BRA2008_subset1': [5, 6, 7, 8, 9, 10, 11, 12, 13],
    'BRA2017_subset1': [5, 6, 7, 8, 9, 10, 11, 12, 13],
    'ETH2018_subset1': [5, 6, 7, 8, 9, 10, 11, 12, 13],
    'GHA2005_subset1': [5, 6, 7, 8, 9, 10, 11, 12, 13],
    'GHA2017_subset1': [5, 6, 7, 8, 9, 10, 11, 12, 13],
    'GTM2014_subset1': [5, 6, 7, 8, 9, 10, 11, 12, 13],
    'IND2004_subset1': [5, 6, 7, 8, 9, 10, 11, 12, 13],

    # evaluation datasets
    'ARM2018_subset1_eval': [5, 6, 7, 8, 9, 10, 11, 12, 13],
    'GHA2017_subset1_eval': [5, 6, 7, 8, 9, 10, 11, 12, 13],
    'ARM2018_subset1_noNA': [5, 6, 7, 8, 9, 10, 11, 12, 13],
    'ARM2018_subset1_eval_log': [5, 6, 7, 8, 9, 10, 11, 12, 13],

    # subsets 4: ["year","country","hhid","hhweight", "climatezone", "urban", "head_age",
    # "nrooms", "head_literate", "hhsize", "tv", "music", "fridge", "exp", "exp_cap_group",
    # "head_male", "frwd_exp", "frwd_cons", "petrol_exp", "scooter", "car", "publictransport_exp",
    # "publictransport", "washmach", "elec_any", "totbiom_cons", "elec_cons", "gas_cons"]

    "ARM2018_subset4": [ 5, 6, 7, 8, 9, 10, 11, 12,13,15,16,17,18,19,21,22,23,24,25,26,27],
    'BRA2008_subset4': [ 5, 6, 7, 8, 9, 10, 11, 12,13,15,16,17,18,19,21,22,23,24,25,26,27],
    'BRA2017_subset4': [ 5, 6, 7, 8, 9, 10, 11, 12,13,15,16,17,18,19,21,22,23,24,25,26,27],
    'ETH2018_subset4': [ 5, 6, 7, 8, 9, 10, 11, 12,13,15,16,17,18,19,21,22,23,24,25,26,27],
    'GHA2005_subset4': [ 5, 6, 7, 8, 9, 10, 11, 12,13,15,16,17,18,19,21,22,23,24,25,26,27],
    'GHA2017_subset4': [ 5, 6, 7, 8, 9, 10, 11, 12,13,15,16,17,18,19,21,22,23,24,25,26,27],
    'GTM2014_subset4': [ 5, 6, 7, 8, 9, 10, 11, 12,13,15,16,17,18,19,21,22,23,24,25,26,27],
    'IND2004_subset4': [ 5, 6, 7, 8, 9, 10, 11, 12,13,15,16,17,18,19,21,22,23,24,25,26,27],

    # evaluation datasets:
    'ARM2018_subset4_eval': [ 5, 6, 7, 8, 9, 10, 11, 12,13,15,16,17,18,19,21,22,23,24,25,26,27],
    'GHA2017_subset4_eval': [ 5, 6, 7, 8, 9, 10, 11, 12,13,15,16,17,18,19,21,22,23,24,25,26,27],
    'ARM2018_subset4_noNA': [ 5, 6, 7, 8, 9, 10, 11, 12,13,15,16,17,18,19,21,22,23,24,25,26,27],
    'GHA2017_subset4_noNA': [ 5, 6, 7, 8, 9, 10, 11, 12,13,15,16,17,18,19,21,22,23,24,25,26,27],
    'ETH2018_subset4_eval': [ 5, 6, 7, 8, 9, 10, 11, 12,13,15,16,17,18,19,21,22,23,24,25,26,27],
    'BRA2002_subset4_eval': [5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27]

}


########################################################################################################################
# ORIGINAL IMPLEMENTATION
# def data_loader (data_name, miss_rate):
#     '''Loads datasets and introduce missingness.
#
#     Args:
#       - data_name: letter, spam, or mnist
#       - miss_rate: the probability of missing components
#
#     Returns:
#       data_x: original data
#       miss_data_x: data with missing values
#       data_m: indicator matrix for missing components
#     '''
#
#     # Load data
#     if data_name in ['letter', 'spam']:
#         file_name = 'data/'+data_name+'.csv'
#         data_x = np.loadtxt(file_name, delimiter=",", skiprows=1)
#     elif data_name == 'mnist':
#         (data_x, _), _ = mnist.load_data()
#         data_x = np.reshape(np.asarray(data_x), [60000, 28*28]).astype(float)
#
#     # Parameters
#     no, dim = data_x.shape
#
#     # Introduce missing data
#     data_m = binary_sampler(1-miss_rate, no, dim)
#     miss_data_x = data_x.copy()
#     miss_data_x[data_m == 0] = np.nan
#
#     return data_x, miss_data_x, data_m
########################################################################################################################


########################################################################################################################
# HACK TO ORIGINAL IMPLEMENTATION TO MAKE IT WORK WITH THE SELECTED DATASETS
def data_loader(data_name, miss_rate):
    '''Loads datasets and introduce missingness.

    Args:
      - data_name: letter, spam, or mnist
      - miss_rate: the probability of missing components

    Returns:
      data_x: original data
      miss_data_x: data with missing values
      data_m: indicator matrix for missing components
    '''

    # Load data
    if data_name in DATASETS.keys():
        file_name = f"cleaned_df/{data_name}.csv"
        try:
            data_x = np.genfromtxt(file_name,delimiter=",", filling_values=np.nan, skip_header=1,usecols=DATASETS[data_name])#data_x = np.loadtxt(file_name,delimiter=",", skiprows=1, usecols=DATASETS[data_name])
        except OSError:
            data_x = np.loadtxt(f"../{file_name}", delimiter=",", skiprows=1, usecols=DATASETS[data_name])
    else:
        raise ValueError(f"Unsupported dataset, got '{data_name}' and expected one of {list(DATASETS.keys())}.")


    # Parameters
    no, dim = data_x.shape

    # Introduce missing data
    data_m = binary_sampler(1 - miss_rate, no, dim)

    miss_data_x = data_x.copy()

    miss_data_x[data_m == 0] = np.nan
    miss_data_x[data_x == np.nan] = np.nan

    return data_x, miss_data_x, data_m
