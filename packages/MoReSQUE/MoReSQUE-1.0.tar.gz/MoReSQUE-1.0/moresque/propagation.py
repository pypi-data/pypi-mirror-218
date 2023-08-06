"""This module provides algorithms and helper functions for the processing of
different external and internal uncertainties. All functions are used by the
UQM objects of an ensemble.
"""
import itertools
import inspect
import copy

import pyDOE
import numpy as np
from scipy.interpolate import griddata

import moresque.ustructures as us

def update_dict(main_dict, add_dict):
    """Helper function that allows to sort the entries of a dict into another
    already existing one.

    Arguments:
    main_dict -- (dict) existing dictionary that is to be updated
    add_dict -- (dict) new dict that should provide information to *main_dict*

    Return:
    Updated version of *main_dict*
    """

    for key, entry in add_dict.items():
        if isinstance(entry, dict):
            main_dict.setdefault(key, {})
            # Recursive function call:
            main_dict[key].update(update_dict(main_dict[key], entry))
        else:
            main_dict[key] = entry

    return main_dict

def findiff_prepare(dim_num, findiff):
    """Helper function that sets up vectors needed for multidimensional
    derivation via finite differences method.

    Arguments:
    dim_num -- (int) number of all derivation dimensions
    findiff -- (float) width of the finite difference parameter

    Return:
    sign_vec -- (list) signes required for derivation in all dimensions
    findiff_vec -- (list) finite difference values required for derivation in
                all dimensions
    """

    d = 2**dim_num
    sign_vec = np.ones(d)
    findiff_vec = [[] for i in range(d)]
    mltpl = -1
    for i in range(dim_num):
        d /= 2
        for j in range(len(sign_vec)):
            if j % d == 0:
                mltpl *= -1
            sign_vec[j] *= mltpl
            findiff_vec[j].append(mltpl * findiff)

    return sign_vec, findiff_vec

def sort_surrogate_input(surrogate_input, grid_len, attr_prob, param_prob):
    """Helper functions that sorts all input needed for surrogate creation.

    Arguments:
    surrogate_input -- (dict) sampled parameter and input values that form the
                basis of the surrogate
    grid_len -- (int) number of evaluation points in each dimension
    attr_prob -- (dict) u-structures of ensemble input attributes
    param_prob -- (dict) u-structures of ensemble parameters

    Return:
    grid_data_in -- (list) points for surrogate creation
    mesh_vectors -- (list) points for surrogate evaluation
    distr_vec -- (list) u-structures sorted according to surrogate data
    """
    grid_data_in = []
    distr_vec = []
    mesh_vectors = []
    for factor, vec in surrogate_input.items():
        # Sorting foundation for surrogate creation:
        grid_data_in.append(np.array(vec))
        # Creating evaluation points:
        mesh_vectors.append(np.linspace(min(vec), max(vec), grid_len))
        # Sorting u-structures:
        if isinstance(factor, tuple):
            distr_vec.append(attr_prob[factor[0]][factor[1]])
        else:
            distr_vec.append(param_prob[factor])

    return grid_data_in, mesh_vectors, distr_vec

def format_surrogate_input(grid_data_in, surrogate_target, mesh_vectors,
                           grid_len, dim_num):
    """Helper function that provides final input formatting for the surrogate
    creation.

    Arguments:
    grid_data_in -- (list) input points for surrogate creation
    surrogate_target -- (list) input values for surrogate creation
    mesh_vectors -- (list) evaluation points for surrogate
    grid_len -- (int) number of evaluation points in one dimension
    dim_num -- (int) number of surrogate dimenions

    Return:
    grid_data_in -- (numpy array) transposed input points
    surrogate_target -- numpy array of input values
    target_grid -- (numpy array) evaluation points as grid
    input_grid -- (numpy array) transposed version of *target_grid*
    """
    grid_data_in = np.array(grid_data_in).transpose()

    surrogate_target = np.array(surrogate_target)

    target_grid = np.array(np.meshgrid(*mesh_vectors))
    target_grid = target_grid.reshape(dim_num, grid_len**dim_num)
    input_grid = target_grid.transpose()

    return grid_data_in, surrogate_target, target_grid, input_grid

def surrogate_filtering(surrogate, target_grid, dim_num):
    """Helper function that filter invalid values.

    Arguments:
    surrogate -- (numpy array) surrogate output
    target_grid -- (numpy array) evaluation grid associated to surrogate output
    dim_num -- (int) number of surrogate dimensions

    Return:
    surrogate -- (numpy array) surrogate output with invalid values filtered out
    target_grid -- (numpy array) evaluation grid with invalid values filtered out
    """
    filter_idcs = np.isfinite(surrogate)
    surrogate = surrogate[filter_idcs]

    if dim_num > 1:
        target_grid = target_grid[:, filter_idcs]
    # Filtering works differently if only one dimension exists:
    else:
        target_grid = target_grid[filter_idcs.transpose()]

    return surrogate, target_grid

def process_surrogate(surrogate_in, surrogate_target, param_prob, attr_prob,
                      dim_num, copula, prop_config):
    """Function that is used by objects of :class:"UQMO" to create u-structures
    based on external uncertainties.

    Arguments:
    surrogate_in -- (dict) input points for surrogate as provided by ensemble
                    members
    surrogate_target -- (list) input values for surrogate creation
    param_prob -- (dict) u-structures of ensemble member parameters
    attr_prob -- (dict) u-structures of ensemble member inputs
    dim_num -- (int) number of dimenions of the external uncertainty spaces
    copula -- (function) copula describing correlation of external uncertainties
    prop_config -- (dict) parameter values to control the propagation process

    Return
    ustruct -- (UncertaintyStructure) numerical representation of the ensemble
                output uncertainty based on the external uncertainties
    """

    # Unpack parameter structure for control of propagation process:
    findiff, grid_len, out_grid, kde_adjust = get_prop_config(prop_config,
                                                              dim_num)

    # Data formatting for surrogate creation (interpolation):
    grid_data_in, mesh_vectors, distr_vec = sort_surrogate_input(
        surrogate_in, grid_len, attr_prob, param_prob)
    format_data = format_surrogate_input(grid_data_in, surrogate_target,
                                         mesh_vectors, grid_len, dim_num)
    grid_data_in = format_data[0]
    surrogate_target = format_data[1]
    target_grid = format_data[2]
    input_grid = format_data[3]
    del format_data
    # Create surrogate via interpolation:
    surrogate = griddata(grid_data_in, surrogate_target, input_grid)
    surrogate, target_grid = surrogate_filtering(surrogate, target_grid, dim_num)
    # Vector of possible output values:
    output_vec = np.linspace(min(surrogate_target),
                             max(surrogate_target), out_grid)

    # Divide input dimensions based on u-structure types:
    distr_dims, intrv_dims, pbox_dims = divide_dimensiontypes(distr_vec)

    # Calculate output probabilities:
    pdf_eval = calculate_probabilities(output_vec, surrogate, dim_num,
                                        target_grid, distr_vec, findiff,
                                        copula, intrv_dims, distr_dims,
                                        pbox_dims)
    # Use probability values to train p-box or distribution structure:
    if len(pdf_eval) == 2:
        ustruct = us.PBox(values1=output_vec, weights1=pdf_eval[0],
                          values2=output_vec, weights2=pdf_eval[1],
                          num=len(output_vec))
    else:
        ustruct = us.Distribution(values=output_vec, weights=pdf_eval,
                                  num=len(output_vec), adjust=kde_adjust)
    return ustruct

def get_prop_config(prop_config, dim_num):
    """Helper function that organizes the parameter values provided for control
    of the propagation process.

    Arguments:
    prop_config -- (dict) configuration structure provided by the user
    dim_num -- (int) number of external uncertainty sources
    """

    # Scale surrogate evaluation grid based on number of uncertainty dimenions:
    dim2gridlen = {1: 200, 2: 100, 3: 100, 4: 50, 5: 30, 6: 10, 7: 10}

    # Default values for control parameters:
    out_dict = {'findiff': 0.001, 'grid_len': dim2gridlen[dim_num],
                'out_grid': 200, 'kde_adjust': 1}
    if prop_config is not None:
        out_dict.update(prop_config)

    return (out_dict['findiff'], out_dict['grid_len'], out_dict['out_grid'],
            out_dict['kde_adjust'])

def divide_dimensiontypes(distr_vec):
    """Helper functions that partitions the given u-structures based on their
    uncertainty model types:

    Arguments:
    distr_vec -- (list) u-structures of input attributes and ensemble parameters

    Return:
    distrs -- (list) indices of distribution structures
    intrvs -- (list) indices of interval structures
    pboxes -- (list) indices of p-box structures
    """
    distrs = []
    intrvs = []
    pboxes = []

    for i in range(len(distr_vec)):
        if isinstance(distr_vec[i], us.Interval):
            intrvs.append(i)
        elif isinstance(distr_vec[i], us.Distribution):
            distrs.append(i)
        elif isinstance(distr_vec[i], us.PBox):
            pboxes.append(i)

    return distrs, intrvs, pboxes

def calculate_probabilities(output_vec, surrogate, dim_num, target_grid,
                            distr_vec, findiff, copula, intrv_dims, distr_dims,
                            pbox_dims):
    """Functions that calculates probability values of the member output based
    on the given probabilities of the external uncertainty sources.

    Arguments:
    output_vec -- (list) possible member output values
    surrogate -- (numpy array) surrogate output values
    dim_num -- (int) number of external uncertainty dimenions
    target_grid -- (numpy array) evaluation grid of surrogate
    distr_vec -- (list) u-structures of external uncertainty sources
    findiff -- (float) parameter for derivation
    copula -- (function) copula describing correlation between external
            uncertainty sources
    intrv_dims -- (list) indices of interval structures in *distr_vec*
    distr_dims -- (list) indices of distribution structures in *distr_vec*
    pbox_dims -- (list) indices of p-box structures in *distr_vec*

    Return:
    probability weight values associated with *output_vec*
    """

    # Sort u-structures:
    distr_dims.extend(pbox_dims)
    distr_dims = sorted(distr_dims)
    prob_vec = [distr_vec[didx] for didx in distr_dims] # probabilistic u-structs
    pboxes = [distr_vec[didx] for didx in pbox_dims]    # p-box u-structs
    # Interval dimension check vector:
    idims = np.array([val in intrv_dims for val in range(dim_num)])

    # Get help vectors for derivation:
    sign_vec, findiff_vec = findiff_prepare(len(distr_dims), findiff)
    # Parameters value searhc:
    delta = abs(output_vec[1] - output_vec[0])  # distance parameter
    bin_size = 0.1  #TODO: change hard-coding

    min_pdf_eval = []
    max_pdf_eval = []
    pdf_eval = []

    # Check and partition target_grid based on interval dimenions:
    if len(idims) == 1:
        if idims[0] == False:
            intrvgrid = []
        else:
            raise RuntimeError('Only dimension should not be itvl at this point')
    else:
        intrvgrid = target_grid[idims]

    # Calculate probability weights for every possible output value:
    for out_val in output_vec:
        # Find all surrogate points near to the given output value:
        idcs = (surrogate > out_val - (bin_size * delta)) & (
            surrogate < out_val + (bin_size * delta))

        # Account for interval sources:
        if len(intrv_dims) > 0:
            subgrid = intrvgrid[:, idcs] # interval ensemble inputs
            intrv_points = []
            pdf_vals_min = []
            pdf_vals_max = []
            cdf_vals_min = []
            cdf_vals_max = []
            # Loop over interval ensemble input values:
            for ip in subgrid.T:
                # Check whether an equal input point occurred before:
                if ip.tolist() not in intrv_points:
                    intrv_points.append(ip.tolist())
                    adjust_idcs = idcs
                    # Adjusted found surrogate points based on equal interval
                    # points and find corresponding input points::
                    for didx in range(len(intrv_dims)):
                        intrv_adjust = target_grid[intrv_dims[didx]] == ip[didx]
                        adjust_idcs = np.logical_and(adjust_idcs, intrv_adjust)

                    # Calculate probability values and probability weights:
                    point_set = [target_grid[i][adjust_idcs] for i in distr_dims]
                    p_vals, cdfch = pdf_at_val(point_set, prob_vec, sign_vec,
                                         findiff_vec, findiff, copula,
                                         len(distr_dims), pboxes, check_cdf=True)
                    # Format calculated values:
                    p_vals = [max(0.0, p) for p in p_vals]
                    pdf_vals_min.append(p_vals[0])
                    pdf_vals_max.append(p_vals[1])
                    cdf_vals_min.append(cdfch[0].tolist())
                    cdf_vals_max.append(cdfch[1].tolist())
            # Choose correct values and account for missed points:
            if pdf_vals_min == []:
                min_pdf_eval.append(0.0)
            else:
                min_ind = cdf_vals_min.index(min(cdf_vals_min))
                min_pdf_eval.append(pdf_vals_min[min_ind])
            if pdf_vals_max == []:
                max_pdf_eval.append(0.0)
            else:
                max_ind = cdf_vals_max.index(max(cdf_vals_max))
                max_pdf_eval.append(pdf_vals_max[max_ind])

        # Only probabilistic uncertainty sources given:
        else:
            # Find input points corresponding to found surrogate values:
            if dim_num > 1:
                point_set = [target_grid[i][idcs] for i in distr_dims]
            else:
                point_set = [target_grid[idcs]]
            # Calculate probability weights:
            p_vals, temp = pdf_at_val(point_set, prob_vec, sign_vec,
                                      findiff_vec, findiff, copula,
                                      len(distr_dims), pboxes)
            p_vals = [max(0.0, p) for p in p_vals] # negative values cause problems
            min_pdf_eval.append(p_vals[0])
            max_pdf_eval.append(p_vals[1])
    # Differentiate between distribution and p-box output:
    if min_pdf_eval == max_pdf_eval:
        pdf_eval = min_pdf_eval
    else:
        pdf_eval = [min_pdf_eval, max_pdf_eval]

    return pdf_eval

def pdf_at_val(point_set, distr_vec, sign_vec, findiff_vec, findiff, copula,
               dim_num, pboxes, check_cdf=False):
    """Function that calculates the combined probability density of all points
    of the uncertainty space associated with a specific value of the output
    variable. It may be used with initial p-box uncertainties present (produces
    two different PDF values) or with distribution uncertainties only (produces
    two times the same value).

    Arguments:
    point_set -- list of lists representing points of the uncertainty space
    distr_vec -- (list) probabilistic uncertainty structures (distributions or
                p-boxes)
    sign_vec -- (list) help vector with signs needed for derivation
    findiff_vec -- (list) help vector with finite differences needed for derivation
    findiff -- (float) finite difference value
    copula -- (function) copula function describing the correlation between
                initial uncertainties
    dim_num -- (int) number of initial uncertainties (dimenions of the
                uncertainty space)
    pboxes -- (list) used uncertainty structures that are p-boxes
    check_cdf -- (bool) flag that indicates whether CDFs values of the points
                should be compared to find more or less probable points (needed
                if intervals are among initial uncertainties)

    Return:
    output_pdf -- (list) two PDF values of the inquired output variable value;
                in cases with purely distribution probability, both given
                values are the same; otherwise, the first value is associated
                with the lower p-box bound while the second belongs to the
                upper bound
    cdf_checker -- (list) the minimal and maximal CDF values associated to the
                processed points; needed for cases with interval uncertainties;
                is 'None' in other cases
    """

    prob_eval_min = 0
    prob_eval_max = 0
    # Loop over all elements of the finite differences derivation:
    for idx in range(2**dim_num):
        # Add/subtract small values two/from the initial values:
        element = np.array([p+h for p, h in zip(point_set, findiff_vec[idx])])
        prob_input_min = []
        prob_input_max = []
        # Obtain the probability values of all initial uncertainties:
        for i in range(dim_num):
            pav = distr_vec[i].cdf(element[i])
            # Two different probabilities are obtained for p-boxes:
            if distr_vec[i] in pboxes:
                prob_input_min.append(np.array(pav[0]))
                prob_input_max.append(np.array(pav[1]))
            # Use two times the same value for probabilities (for compatibility):
            else:
                prob_input_min.append(np.array(pav))
                prob_input_max.append(np.array(pav))
        # Calculate and add the joint probabilities for all elements of the
        # finite differences derivation process:
        prob_eval_min += (sign_vec[idx] * copula(*prob_input_min))
        prob_eval_max += (sign_vec[idx] * copula(*prob_input_max))
    # Divide by finite difference to complete derivation of CDF values to
    # PDF values:
    prob_eval_min /= (2**dim_num * findiff**dim_num)
    prob_eval_max /= (2**dim_num * findiff**dim_num)

    # Sum up PDF values to get the combined density of the output value:
    output_pdf = [sum(prob_eval_min), sum(prob_eval_max)]

    # In cases with interval uncertainties, CDF values have to be compared:
    if check_cdf:
        cdf_min = np.inf        # highest possible value to be corrected
        cdf_max = -1 * np.inf   # lowest possible value to be corrected
        # Loop over all given points:
        for i in range(len(point_set[0])):
            copula_input_min = []
            copula_input_max = []
            # Loop over all initial uncertainties:
            for j in range(dim_num):
                cdf_out = distr_vec[j].cdf(point_set[j][i])
                # P-boxes produces two values:
                if distr_vec[j] in pboxes:
                    copula_input_min.append(cdf_out[0])
                    copula_input_max.append(cdf_out[1])
                # Use two times the same value for distributions:
                else:
                    copula_input_min.append(cdf_out)
                    copula_input_max.append(cdf_out)
            # Calculate joint CDF values:
            copula_out_min = copula(*copula_input_min)
            copula_out_max = copula(*copula_input_max)
            # Update maximal and minimal detected probabilities:
            cdf_min = min(cdf_min, copula_out_min)
            cdf_max = max(cdf_max, copula_out_max)

        cdf_checker = [cdf_min, cdf_max]
    else:
        cdf_checker = None

    return output_pdf, cdf_checker

def merge_marginal_ustructs(ustruct1, ustruct2):
    """Function that merges u-structures representing internal uncertainty. It
    is used when the external uncertainty is entirely represented by an
    interval.

    Arguments:
    ustruct1 -- (uncertainty structure) associated with one boundary value of
                the external uncertainty interval
    ustruct2 -- (uncertainty structure) associated with the other boundary value

    Return:
    uncertainty structure of the combined internal and external uncertainties;
    since the external ones are intervals, the output will be an interval or a
    p-box
    """

    # Assure that both u-structures belong to the same type:
    assert type(ustruct1).__name__ == type(ustruct2).__name__

    # Merging of interval structures:
    if isinstance(ustruct1, us.Interval):
        new_min = min(ustruct1.samp_space[0], ustruct2.samp_space[0])
        new_max = max(ustruct1.samp_space[-1], ustruct2.samp_space[-1])

        return us.Interval(new_min, new_max, num=ustruct1.get_stratnum())

    # Merging of distribution structures:
    elif isinstance(ustruct1, us.Distribution):
        val_vec, p_vec1, p_vec2, cdf_vec1, cdf_vec2 = eval_prob_structs(
            ustruct1, ustruct2)
        # Sort out which probability densities belong to which boundary value:
        min_p, max_p = get_dstr_bounds(p_vec1, p_vec2, cdf_vec1,
                                              cdf_vec2)
        # Filtering for numerical stability:
        min_val, min_p = prune_input_vectors(val_vec, min_p)
        max_val, max_p = prune_input_vectors(val_vec, max_p)

        return us.PBox(values1=min_val, weights1=min_p, values2=max_val,
                       weights2=max_p, num=len(val_vec))

    # Merging of p-box structures:
    elif isinstance(ustruct1, us.PBox):
        val_vec, p_vecs1, p_vecs2, cdf_vecs1, cdf_vecs2 = eval_prob_structs(
            ustruct1, ustruct2)
        min_p, max_p = get_probability_bounds(p_vecs1, p_vecs2, cdf_vecs1,
                                              cdf_vecs2)

        return us.PBox(values1=val_vec, weights1=min_p, values2=val_vec,
                       weights2=max_p, num=len(val_vec))

    # Error handling:
    else:
        raise RuntimeError('Unknown ustructure type "%s"' % type(
            ustruct1).__name__)

def prune_input_vectors(val_vec, p_vec):
    """Helper function that filters out probability density values below zero
    (numerical artefacts that appear sometimes.

    Arguments:
    val_vec -- (list) possible output values
    p_vec -- (list) probability density values associated to *val_vec*

    Return:
    val_out -- (list) updated output values
    p_out -- (list) updated probability densities
    """

    new_vals = np.array(copy.copy(val_vec))
    p_vec = np.array(p_vec)
    idx_vec = p_vec > 0
    val_out = new_vals[idx_vec].tolist()
    p_out = p_vec[idx_vec].tolist()

    return val_out, p_out

def eval_prob_structs(ustruct1, ustruct2):
    """Helper function that extracts possible values, densities and
    probabilities from two uncertainty structures.

    Arguments:
    ustruct1 -- first uncertainty structure
    ustruct2 -- second uncertainty structure

    Return:
    val_vec -- (list) range of possible values represented by the two structures
    p_vecs1 -- (list) probability density values of first structure
    p_vecs2 -- (list) probability density values of second structure
    cdf_vecs1 -- (list) probability values of first structure
    cdf_vecs2 -- (list) probability values of second structure
    """

    val_vec = copy.copy(ustruct1.samp_space)
    val_vec = val_vec.tolist()
    val_vec.extend(ustruct2.samp_space)
    val_vec = sorted(set(val_vec))

    p_vecs1 = ustruct1.evaluate_vals(val_vec)
    p_vecs2 = ustruct2.evaluate_vals(val_vec)
    cdf_vecs1 = ustruct1.cdf(val_vec)
    cdf_vecs2 = ustruct2.cdf(val_vec)

    return val_vec, p_vecs1, p_vecs2, cdf_vecs1, cdf_vecs2

def get_probability_bounds(p_vecs1, p_vecs2, cdf_vecs1, cdf_vecs2):
    """Helper function that sorts probability density values for the merging of
    two p-box structures.

    Arguments:
    p_vecs1 -- (list) probability densities of first p-box
    p_vecs2 -- (list) probability densities of second p-box
    cdf_vec1 -- (list) probabilities of first p-box
    cdf_vecs2 -- (list) probabilities of second p-box

    Return:
    min_p -- (list) probability densities of the lower bound of the resulting
            p-box
    max_p -- (list) probability densities of the upper p-box bound
    """

    # Split input lists into vectors of lower and upper bounds:
    cdf1_min = cdf_vecs1[0]
    cdf1_max = cdf_vecs1[1]
    cdf2_min = cdf_vecs2[0]
    cdf2_max = cdf_vecs2[1]
    pdf1_min = p_vecs1[0]
    pdf1_max = p_vecs1[1]
    pdf2_min = p_vecs2[0]
    pdf2_max = p_vecs2[1]

    min_p = []
    max_p = []

    # Loop over all possible values and select density values based on the
    # associated probabilities:
    for i in range(len(cdf1_min)):
        if cdf1_min[i] < cdf2_min[i]:
            min_p.append(pdf1_min[i])
        else:
            min_p.append(pdf2_min[i])
        if cdf1_max[i] > cdf2_max[i]:
            max_p.append(pdf1_max[i])
        else:
            max_p.append(pdf2_max[i])

    return min_p, max_p

def get_dstr_bounds(p_vec1, p_vec2, cdf_vec1, cdf_vec2):
    """ Helper function that sorts probability density values for the merging
    of two distributions.

    Arguments:
    p_vec1 -- (list) probability densities of the first distribution
    p_vec2 -- (list) probability densities of the second distribution
    cdf_vec1 -- (list) probabilities of the first distribution
    cdf_vec2 -- (list) probabilities of the second distribution

    Return:
    min_p -- (list) probability densities of the lower bound of the resulting
            p-box
    max_p -- (list) probability densities of the upper bound
    """

    min_p = []
    max_p = []
    # Loop over all values and select densities according to highest or lowest
    # probability:
    for i in range(len(cdf_vec1)):
        if cdf_vec1[i] < cdf_vec2[i]:
            min_p.append(p_vec1[i])
            max_p.append(p_vec2[i])
        else:
            min_p.append(p_vec2[i])
            max_p.append(p_vec1[i])

    return min_p, max_p

def correct_uncertainty(ustruct, ufunc_struct, t, copula):
    """This function corrects the output uncertainty structure received from an
    ensemble calculation. The correction is performed via an uncertainty
    function that represents the 'internal' uncertainty of a simulation model.

    Arguments:
    ustruct -- UncertaintyStructure of subtype Distribution or PBox
    ufunc_struct -- (dict) contains function representing the model error, the
        associated uncertainty type, and additional arguments of the function
    t -- (int) current time stamp of the co-simulation
    copula -- object that defines the dependence between the model's input/
        parameter uncertainty and the internal uncertainty via a function

    Return:
    Adjusted UncertaintyStructure of type Distribution or PBox.
    """
    assert 'utype' in ufunc_struct.keys()
    assert ufunc_struct['utype'] in ['Interval', 'Distribution', 'PBox']

    ufunc = ufunc_struct['function']
    check_ufunc(ufunc)

    # Internal uncertainty is represented by intervals:
    if ufunc_struct['utype'] == 'Interval':
        return correct_itvlstructs(ustruct, ufunc_struct, ufunc, t)
    # Internal uncertainty is represented by p-boxes or distributions:
    else:
        h = 0.0001  #TODO: hardcoding not optimal
        ustruct.restratify(50)  #TODO: hardcoding not optimal
        return correct_probstructs(ustruct, ufunc_struct, ufunc, t, copula, h)

def correct_itvlstructs(ustruct, ufunc_struct, ufunc, t):
    """This function is called by 'correct_uncertainty' if the internal
    uncertainty of the simulation model is represented by an interval
    (i.e. ufunc's output is an Interval object).

    Arguments:
    ustruct -- (uncertainty structure) representation of influence of external
            uncertainties
    ufunc_struct -- (dict) additional information about the internal uncertainty
    ufunc -- Python object that contains a model of the internal uncertainty
    t -- (int) current simulation time

    Return:
    new_struct -- (uncertainty structure) combined representation of external
            and internal uncertainties
    """
    min_vals = []
    max_vals = []

    prob_vec = ustruct.evaluate_vals(ustruct.samp_space) # external density values
    if isinstance(ustruct, us.Distribution):
        prob_vec = [prob_vec, prob_vec] # for similar handling of Dstr and PBox

    # Evaluating internal u-function for each possible external value:
    for samp in ustruct.samp_space:
        updstruct = ufunc.main(samp, t, **ufunc_struct['kwargs'])
        min_vals.append(updstruct.samp_space[0])
        max_vals.append(updstruct.samp_space[-1])

    min_vals, prob_vec1 = filter_double_values(min_vals, [prob_vec[1]])
    max_vals, prob_vec2 = filter_double_values(max_vals, [prob_vec[0]])
    # (Indexing explanation: The maximal probability vector for the minimal
    # value vector poses as a boundary of the new p-box.)

    # Differentiating between distribution and p-box cases:
    if len(prob_vec1) == 1:
        weight_vec1 = prob_vec1[0]
    else:
        weight_vec1 = prob_vec1
    if len(prob_vec2) == 1:
        weight_vec2 = prob_vec2[0]
    else:
        weight_vec2 = prob_vec2

    new_struct = us.PBox(values1=min_vals, weights1=weight_vec1,
                             values2=max_vals, weights2=weight_vec2,
                             num=len(min_vals))
    return new_struct

def correct_probstructs(ustruct, ufunc_struct, ufunc, t, copula, h):
    """This function is called by 'correct_uncertainty' if the internal
    uncertainty of the simulation model is represented by a dstribution or pbox
    (i.e. ufunc's output is a Distribution or PBox object).

    Arguments:
    ustruct -- (uncertainty structure) representation of the influence of the
                external uncertainties
    ufunc_struct -- (dict) additional information about the internal uncertainty
    ufunc -- Python object that contains a model of the internal uncertainty
    t -- (int) current simulation time
    copula -- (function) model of the correlation between external and internal
                uncertainyt
    h -- (float) finite difference parameter for derivation

    Return:
    new_struct -- (uncertainty structure) combined representation of external
            and internal uncertainty
    """
    updvals = []
    updprobs1 = []
    updprobs2 = []

    if isinstance(ustruct, us.PBox) or ufunc_struct['utype'] == 'PBox':
        pbox_exists = True
    else:
        pbox_exists = False

    # Evaluate u-function of internal uncertainties for every possible value
    # of the external uncertainty:
    for samp in ustruct.samp_space:
        updstruct = ufunc.main(samp, t, **ufunc_struct['kwargs'])
        updstruct.restratify(30)
        updvals.extend(updstruct.samp_space)

        # Prepare external uncertainty values for derivation:
        elem1a, elem1b = get_findiff_elems(ustruct, samp, h)

        # Loop over possible values of internal uncertainties:
        for updval in updstruct.samp_space:
            # Prepare elements for derivation:
            elem2a, elem2b = get_findiff_elems(updstruct, updval, h)

            prob1 = derive_cdf(elem1a[0], elem1b[0], elem2a[0], elem2b[0],
                               copula, h)
            updprobs1.append(prob1)

            # Second derivation necessary if internal uncertainty is a p-box:
            if pbox_exists:
                prob2 = derive_cdf(elem1a[1], elem1b[1], elem2a[1], elem2b[1],
                                   copula, h)
                updprobs2.append(prob2)

    # Filtering and u-structure creation depending on the uncertainty types:
    if pbox_exists:
        new_vals, new_dstrs = filter_double_values(updvals, [updprobs1,
                                                             updprobs2])
        new_struct = us.PBox(values1=new_vals, weights1=new_dstrs[0],
                             values2=new_vals, weights2=new_dstrs[1],
                             num=len(new_vals))
    else:
        new_vals, new_dstrs = filter_double_values(updvals, [updprobs1])
        new_struct = us.Distribution(values=new_vals, weights=new_dstrs[0],
                                     num=len(new_vals))

    return new_struct

def get_findiff_elems(ustruct, val, h):
    """This function creates the finite difference values of a CDF function
    that are needed for local derivation around value 'val'.

    Arguments:
    ustruct -- uncertainty structure that provides the CDF
    val -- (float) value at which derivation is desired
    h -- (float) small increment for the derivation

    Return:
    elem1 -- (float) incremented element
    elem2 -- (float) decremented element
    """

    elem1 = ustruct.cdf(val + h)
    elem2 = ustruct.cdf(val - h)

    # Supporting equal handling of dstrs and pboxes:
    if isinstance(ustruct, us.Distribution):
        elem1 = [elem1, elem1]
        elem2 = [elem2, elem2]

    return elem1, elem2

def filter_double_values(value_vec, prob_vecs):
    """A weighted KDE expects the same input value only once. This functions
    searches for duplicated KDE input values and sums their weights (represented
    by probability density values).

    Arguments:
    value_vec -- (list) vector of possible output values, maybe with duplications
    prob_vecs -- (list) probability density values associated with *value_vec*

    Return:
    new_vals -- (list) vector of possible output values without duplications
    new_probs -- (list) probability density values associated with *new_vals*
    """

    new_vals = []
    new_probs = [[] for i in range(len(prob_vecs))]
    value_vec = np.array(value_vec)
    prob_vecs = [np.array(pv) for pv in prob_vecs] # two vecs in cases with pboxes

    # Loop over entries of possible values vector:
    for newval in value_vec:
        if newval not in new_vals:
            new_vals.append(newval)
            idx_vec = value_vec == newval
            # In case of pboxes, two probability vectors have to be handled:
            for i in range(len(new_probs)):
                new_probs[i].append(sum(prob_vecs[i][idx_vec]))

    return new_vals, new_probs

def derive_cdf(f1_elem1, f1_elem2, f2_elem1, f2_elem2, copula, h):
    """This function caclulates the probability density value at a point by
    locally deriving a cdf given by a copula-combination of two cdfs
    (one cdf obtained from ensemble calculation and one cdf associated with the
    model's internal uncertainty).

    Arguments:
    f1_elem1 -- (float) incremental element of external uncertainty
    f1_elem2 -- (float) decremental element of external uncertainty
    f2_elem1 -- (float) incremental element of internal uncertainty
    f2_elem2 -- (float) decremental element of internal uncertainty
    copula -- (function) correlation structure between external and internal
            uncertainty
    h -- (float) increment for finite difference derivation

    Return
    pdens -- (float) derived probability density value at the specific point
    """

    pdens = (copula(f1_elem1, f2_elem1) - copula(f1_elem2, f2_elem1)
             - copula(f1_elem1, f2_elem2) + copula(f1_elem2, f2_elem2))

    pdens = pdens / (4 * h * h)

    return pdens

def check_ufunc(ufunc):
    """Helper function that checks u-function object for the correct structure.
    """
    if 'main' not in dir(ufunc):
        raise RuntimeError("Module representing a model's internal uncertainty"
            " is expected to have a callable 'main' function!")
    if len(inspect.getargspec(ufunc.main).args) < 2:
        raise RuntimeError("Function 'main' describing a model's internal "
            "uncertainty is expected to have at least 2 arguments. The first "
            "being a model output, the second a mosaik time stamp (int).")
