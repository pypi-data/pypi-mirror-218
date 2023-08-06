"""
This module provides a set of help functions that are employed during the
creation of MoReSQUE ensembles. This can be considered the assessment phase of
the UQ process.

"""
import itertools
import csv
import imp

import pyDOE

import moresque.ustructures as us

def get_samp_design(dim_num, strat_num, ep_sampling=True):
    """Helper function that creates a (possibly combined) sampling design.

    Arguments:
    dim_num -- (int) number of dimensions of the sampling space
    strat_num -- (int) number of latin hypercube sampling points
    ep_sampling -- (bool) flag that indicates if extreme-point sampling is used

    Return:
    samp_design -- list of sampling points (that are again lists)
    strat_num -- (int) number of strata used to divide each sampling space
        dimension (internally set if only ep_sampling is applied)
    """
    # If no uncertainty dimensions are given, no sampling design is created:
    if dim_num <= 0:
        return None, strat_num, 1

    # Latin Hypercube Sampling (LHS):
    samp_design = []    # List for storage of sampling points
    ens_size = 0        # Number of members is given by number of sampling points
    # Condition for conducting LHS:
    if strat_num > 0:
        samp_design = latin_hypercube_sampling(dim_num, strat_num)
        ens_size += strat_num   # increase ensemble size by LHS sample number
    # If no LHS is conducted, two strata are still needed for functional purpose:
    else:
        strat_num = 2

    # Extreme point sampling (EPS):
    if ep_sampling:
        samp_design, point_num = extreme_point_sampling(
            dim_num, strat_num, samp_design)
        ens_size += point_num   # increase ensemble size by EPS sample number

    return samp_design, strat_num, ens_size

def latin_hypercube_sampling(dim_num, strat_num):
    """Function used by *get_samp_design* to create an LHS design.

    Arguments:
    dim_num -- (int) number of dimensions of the sampling space
    strat_num -- (int) number of LHS points

    Return:
    design -- list of lists representing sampling points
    """

    design = pyDOE.lhs(dim_num, samples=strat_num, criterion='center'
                       ) * strat_num
    design = design.tolist() # convert numpy array to list

    return design

def extreme_point_sampling(dim_num, strat_num, design):
    """Function used by *get_samp_design* to create an EPS design.

    Arguments:
    dim_num -- (int) number of dimensions of the sampling space
    strat_num -- (int) number of strata dividing the sampling space
    design -- (list) preliminary sampling design (LHS or empty)

    Return:
    design -- list of lists representing the extended design
    count -- (int) number of EPS points
    """
    # Creating the EPS design:
    eps = itertools.product([0, strat_num-1], repeat=dim_num)
    # Integration the EPS design into the preliminary one:
    count = 0
    for point in eps:
        design.append(list(point))
        count += 1      # counting the actually drawn new samples

    return design, count

def uinfo2struct(info_dict, strat_num):
    """Helper function that translates dict-type uncertainty information into
    an uncertainty structure.

    Arguments:
    info_dict -- (dict) information structure about uncertainty source
    strat_num -- (int) number of strata dividing the sampling space

    Return:
    uncertainty structure object
    """

    utype = info_dict['utype']
    # Get the appropriate uncertainty structure object according to the
    # uncertainty type:
    structcall = getattr(us, utype)

    # Obtain uncertainty data directly from dict (typical for intervals),
    # or from linked file (typical for distribution and p-box):
    argdict = {}
    for arg, data in info_dict['data'].items():
        if isinstance(data, str):
            argdict[arg] = file2list(data)
        else:
            argdict[arg] = data

    # Obtain stratification information based on the uncertainty type
    # (distributions/p-boxes are stratified based on the linked data;
    # intervals are stratified based on the sampling design):
    if utype == 'Distribution':
        argdict['num'] = max(2, len(argdict['values']))
    elif utype == 'PBox':
        argdict['num'] = max(2, len(argdict['values1']))
    else:
        argdict['num'] = strat_num

    return structcall(**argdict)

def file2list(filename):
    """Function used by *uinfo2struct* to read uncertainty assessment data
    from a CSV file.

    Arguments:
    filename -- (string) path to the target CSV file

    Return:
    datalist -- list with uncertainty data
    """
    f = open(filename, newline='')
    reader = csv.reader(f, delimiter=',')

    datalist = []
    for row in reader:
        datalist.append(float(row[0])) # data only expected in first column

    return datalist

def get_output_uncertainty(error_dict, config):
    """Helper function that prepares structure for the handling of internal
    uncertainty.

    Arguments:
    error_dict -- (dict) information structure about internal uncertainty
    config -- (dict) ensemble configuration structure

    Return:
    outstruct -- (dict) information structure for practical uncertainty
                handling
    """

    if not "function" in error_dict.keys():
        raise RuntimeError('expecting "function" entry for output attribute '
            'uncertainty specification')

    outstruct = {'utype': error_dict['utype'], 'kwargs': {}}
    # Load function that models internal uncertainty from provided python script:
    function = error_dict['function']
    f_obj = open(function, 'rb')
    outstruct['function'] = imp.load_source(function, function, f_obj)
    # Obtain additional provided keyword argument values for u-function:
    if 'kwargs' in error_dict.keys():
        for kwarg in error_dict['kwargs']:
            outstruct['kwargs'][kwarg] = config[kwarg]

    return outstruct
