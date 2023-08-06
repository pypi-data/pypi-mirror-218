"""This module provides uncertainty structure classes for numerical
representation and hierarchical ordering of uncertain quantities.
"""
import imp
import random
import math

import arrow
import numpy as np
import statsmodels.api as sm
from scipy.interpolate import interp1d

# used with data files:
DATE_FORMAT = 'YYYY-MM-DD HH:mm:ss'

class UncertaintyStructure(object):
    """Base class of all uncertainty structures."""
    def __init__(self, minimum, maximum, num):
        """Any u-structure possesses a value range 'samp_space' that may be
        explored via sampling.
        Structures representing output uncertainty of models also possess a
        specification dict 'spec' and may model dynamic uncertainty via a
        function or a file.

        Arguments:
        minimum -- (float) minimum value of underlying interval
        maximum -- (float) maximum value of underlying interval
        num -- (int) number of strata dividing the interval
        """
        self.samp_space = np.linspace(minimum, maximum, num)

    def get_stratnum(self):
        """This function is used by the propagator in order to identify if
        the u-structure is compatible with a given sampling design.

        Return:
        (int) representing number of strata dividing the interval
        """
        return len(self.samp_space)

    def restratify(self, num):
        """This function is used by the propagator if the u-structure would not
        be compatible with a given sampling design.

        Arguments:
        num -- (int) new number of strata to divide the interval
        """
        minimum = self.samp_space[0]
        maximum = self.samp_space[-1]
        self.samp_space = np.linspace(minimum, maximum, num)

    def resize_space(self, minimum, maximum):
        """Helper function used when the dynamic uncertainty data has to be
        updated via an uncertainty function or file.

        Arguments:
        minimum -- (float) new minimum value for the interval
        maximum -- (float) new maximum value for the interval
        """
        num = len(self.samp_space)
        self.samp_space = np.linspace(minimum, maximum, num)

    def draw_sample(self, idx):
        """Draw a sample with a given index 'idx' from the interval's sampling
        space. This is only used for structures that represent parameter or
        input attr uncertainty.

        Arguments:
        idx -- (int) index of inquired interval stratum

        Retrun:
        (float) value at given stratum
        """
        if idx >= len(self.samp_space):
            raise IndexError('Sampling space too small for idx "%i"' % idx)

        return self.samp_space[idx]

    def _set_samp_func(self, samp_func):
        """This function should enable users to define a non-equally spaced
        samp_space for the given structure.
        """
        pass    # TODO: implement


class Interval(UncertaintyStructure):
    """Uncertainty structure that is defined only by a minimum and
    a maximum.
    """

    def __init__(self, minimum, maximum, num):
        super().__init__(minimum, maximum, num)


class Distribution(UncertaintyStructure):
    """Uncertainty structure that represents a probability distribution.
    """

    def __init__(self, values, weights=None, num=None, adjust=0.1):
        """Constructor function.

        Arguments:
        values -- (list) interval with possible values of underlying quantity
        weights -- (list) probability weights for given possible values
        num -- (int) number of strata dividing the interval
        adjust -- (float) scaling parameter for KDE creation
        """

        if num is None:
            num = len(values)
        super().__init__(min(values), max(values), num)

        if weights is not None:
            weights = np.array(weights) # weights has to be numpy array

        # Create and train KDE:
        self.kde = sm.nonparametric.KDEUnivariate(values)
        self.kde.fit(fft=False, weights=weights, cut=10, adjust=adjust)

        # Create CDF function from KDE's CDF information:
        self.base_cdf = interp1d(self.kde.support, self.kde.cdf,
                                 bounds_error=False)
        # Create inverse CDF function:
        pval_vec = np.linspace(0, 1, len(self.kde.support))
        self.icdf = interp1d(pval_vec, self.kde.icdf)

    def evaluate_vals(self, vals):
        """PDF function of the u-structure.

        Arguments:
        vals -- (list) possible values of the underlying quantity

        Return:
        (numpy array) associated probability densities for inquired vals
        """
        prob_vec = []
        for point in vals:
            prob_vec.extend(self.kde.evaluate(point))
        return np.array(prob_vec)

    def get_mean(self):
        """Function for obtaining the expected value of the probability
        distribution.
        """
        if self.samp_space[0] == self.samp_space[-1]:
            return self.samp_space[0]   # distribution is currently a single val
        else:
            # Estimation of expected value:
            density = []
            for point in self.samp_space:
                density.extend(self.kde.evaluate(point))
            density = np.array(density)
            return sum(self.samp_space*density)/sum(density)

    # TODO: Rework function for obtaining standard deviation
    """
    def get_std(self):
        if self.samp_space[0] == self.samp_space[-1]:
            return self.samp_space[0]

        mean = self.get_mean()
        density = []
        deviations = []
        nonzero_weights = 0
        for point in self.samp_space:
            density.extend(self.kde.evaluate(point))
            deviations.append((point - mean) ** 2)
            if density[-1] != 0.0:
                nonzero_weights += 1
        density = np.array(density)
        deviations = np.array(deviations)
        var = sum(density * deviations)/(nonzero_weights * sum(density))
        return math.sqrt(var)
    """

    def get_quantile(self, p_value):
        """Function for obtaining quantiles of the probability distribution.

        Arguments:
        p_value -- (float) probability values (from 0 to 1) of inquired quantile

        Return:
        (float) value of the underlying quantity at given p-value
        """
        # Start checking from smallest value if p-value < 0.5:
        if p_value > 0.5:
            for val in reversed(self.samp_space):
                if self.cdf(val) <= p_value:
                    return val
            return self.samp_space[-1]
        # Start checking from largest value if p-value >= 0.5:
        else:
            for val in self.samp_space:
                if self.cdf(val) >= p_value:
                    return val
            return self.samp_space[0]

    def draw_samples(self, samp_num):
        """Function for drawing random samples from probability distribution.
        So far, this function is UNUSED.

        Arguments:
        samp_num -- (int) number of desired samples

        Return:
        (numpy array) randomly sampled values
        """
        p_vals = [random.random() for i in range(samp_num)]
        return self.icdf(p_vals)

    def cdf(self, val):
        """Function for obtaining the probability of a given value.

        Arguments:
        val -- (float or list) possible value(s) of the underlying quantity

        Return:
        (float or list) associated probability(ies) of the given value(s)
        """

        cdf_out = self.base_cdf(val)
        # Filtering of values:
        val = np.array(val)
        lo_bound =  self.base_cdf.x[0]
        hi_bound = self.base_cdf.x[-1]
        nan_idcs = np.isnan(cdf_out)    # indices of NaN values (beyond bounds)
        lo_correct = (val < lo_bound) & nan_idcs
        hi_correct = (val > hi_bound) & nan_idcs
        # Adjusting NaN values:
        cdf_out[lo_correct] = 0.0 # values below the defined bounds
        cdf_out[hi_correct] = 1.0 # values above the defined bounds

        return cdf_out

    def prune_interval(self, prune_to=1e-5):
        """Procedure for decreasing the range of the underlying interval based
        on probabilities of the extreme values.
        So far, this procedure is UNUSED.

        Arguments:
        prune_to -- (float) probability of the new minimum values
        """

        lower_bound = self.get_quantile(prune_to)
        upper_bound = self.get_quantile(1 - prune_to)
        strat_num = len(self.samp_space)
        # Create new underlying interval:
        self.samp_space = np.linspace(lower_bound, upper_bound, strat_num)


class PBox(UncertaintyStructure):
    """Uncertainty structure that represents a probability box.
    """

    def __init__(self, values1, weights1, values2, weights2, num, adjust=0.1):
        """Constructor function.

        Arguments:
        values1 -- (list) possible lower bound values of underlying quantity
        weights1 -- (list) probability weights of lower bound values
        values2 -- (list) possible upper bound values of underlying quantity
        weights2 -- (list) probability weights of upper bound values
        num -- (int) number of strata dividing the underlying interval
        adjust -- (float) scaling parameter for KDE creation
        """

        super().__init__(min(min(values1), min(values2)),
                         max(max(values1), max(values2)), num)

        # Create and train two KDEs (for lower and upper bound distribution):
        self.kde1 = sm.nonparametric.KDEUnivariate(values1)
        self.kde1.fit(fft=False, weights=np.array(weights1), cut=10,
                      adjust=adjust)
        self.base_cdf1 = interp1d(self.kde1.support, self.kde1.cdf,
                                  bounds_error=False) # first CDF
        self.kde2 = sm.nonparametric.KDEUnivariate(values2)
        self.kde2.fit(fft=False, weights=np.array(weights2), cut=10,
                      adjust=adjust)
        self.base_cdf2 = interp1d(self.kde2.support, self.kde2.cdf,
                                  bounds_error=False) # second CDF

    def evaluate_vals(self, vals):
        """PDF function of the u-structure.

        Arguments:
        vals -- (list) possible values of the underlying quantity

        Return:
        (list) associated probability densities for the given vals
        """
        densi1 = []
        densi2 = []
        for val in vals:
            # Evaluate both boundary PDFs:
            densi1.extend(self.kde1.evaluate(val))
            densi2.extend(self.kde2.evaluate(val))
        return [np.array(densi1), np.array(densi2)]

    def get_mean(self):
        """Function for obtaining the expected values of the probability box
        """
        if self.samp_space[0] == self.samp_space[-1]:
            return self.samp_space[0]   # p-box is currently a single value
        else:
            # Estimation of the expected values for both boundary distributions
            density1 = []
            density2 = []
            for point in self.samp_space:
                density1.extend(self.kde1.evaluate(point))
                density2.extend(self.kde2.evaluate(point))
            density1 = np.array(density1)
            density2 = np.array(density2)
            mean1 = sum(self.samp_space*density1)/sum(density1)
            mean2 = sum(self.samp_space*density2)/sum(density2)
            # The lower bound has the higher expected value (has to come first):
            return [max(mean1, mean2), min(mean1, mean2)]

    def get_quantile(self, p_value):
        """Function for obtaining quantiles of the probability-box.

        Arguments:
        p_value -- (float) probability values (from 0 to 1) of inquired quantile

        Return:
        out_vec -- (list) values of the underlying quantity at given p-value
                    for both boundary distributions
        """

        out_vec = [None, None]
        # Start checking from smallest value if p-value < 0.5:
        if p_value > 0.5:
            for val in reversed(self.samp_space):
                # Searching until the quantiles for both boundary distributions
                # have been found:
                if self.cdf(val)[0] <= p_value and out_vec[0] == None:
                    out_vec[0] = val
                if self.cdf(val)[1] <= p_value and out_vec[1] == None:
                    out_vec[1] = val
                if out_vec[0] != None and out_vec[1] != None:
                    break
            # Pick largest possible value if quantile not found:
            if out_vec[0] == None: out_vec[0] = self.samp_space[-1]
            if out_vec[1] == None: out_vec[1] = self.samp_space[-1]
        # Start checking from largest value if p-value >= 0.5:
        else:
            for val in self.samp_space:
                # Searching until the quantiles for both boundary distributions
                # have been found:
                if self.cdf(val)[0] >= p_value and out_vec[0] == None:
                    out_vec[0] = val
                if self.cdf(val)[1] >= p_value and out_vec[1] == None:
                    out_vec[1] = val
                if out_vec[0] != None and out_vec[1] != None:
                    break
            # Pick smallest possible value if quantile not found:
            if out_vec[0] == None: out_vec[0] = self.samp_space[0]
            if out_vec[1] == None: out_vec[1] = self.samp_space[0]
        return out_vec

    def cdf(self, val):
        """Function for obtaining the probabilities of a given value.

        Arguments:
        val -- (float or list) possible value(s) of the underlying quantity

        Return:
        (float or list) associated probabilities of the given value(s) for both
            boundary distributions
        """

        cdf1_out = self.base_cdf1(val)
        cdf2_out = self.base_cdf2(val)
        # Filtering values that are beyond the underlying interval:
        val = np.array(val)
        lo_bound1 = self.base_cdf1.x[0]
        hi_bound1 = self.base_cdf1.x[-1]
        lo_bound2 = self.base_cdf2.x[0]
        hi_bound2 = self.base_cdf2.x[-1]
        nan_idcs1 = np.isnan(cdf1_out)
        nan_idcs2 = np.isnan(cdf2_out)
        lo_correct1 = (val < lo_bound1) & nan_idcs1
        hi_correct1 = (val > hi_bound1) & nan_idcs1
        lo_correct2 = (val < lo_bound2) & nan_idcs2
        hi_correct2 = (val > hi_bound2) & nan_idcs2
        # Replace NaN values with maximal or minimal probability:
        cdf1_out[lo_correct1] = 0.0
        cdf1_out[hi_correct1] = 1.0
        cdf2_out[lo_correct2] = 0.0
        cdf2_out[hi_correct2] = 1.0
        # Sort output according to lower and upper boundary distributions:
        return [np.minimum(cdf1_out, cdf2_out), np.maximum(cdf1_out, cdf2_out)]

    # TODO: Rework function for obtaining standard deviation
    """
    def get_std(self):
        if self.samp_space[0] == self.samp_space[-1]:
            return self.samp_space[0]

        means = self.get_mean()
        mean1 = means[0]
        mean2 = means[1]
        density1 = []
        density2 = []
        deviations1 = []
        deviations2 = []
        nonzero_weights1 = 0
        nonzero_weights2 = 0
        for point in self.samp_space:
            density1.extend(self.kde1.evaluate(point))
            density2.extend(self.kde2.evaluate(point))
            deviations1.append((point - mean1) ** 2)
            deviations2.append((point - mean2) ** 2)
            if density1[-1] != 0.0:
                nonzero_weights1 += 1
            if density2[-1] != 0.0:
                nonzero_weights2 += 1
        density1 = np.array(density1)
        density2 = np.array(density2)
        deviations1 = np.array(deviations1)
        deviations2 = np.array(deviations2)
        var1 = sum(density1 * deviations1)/(nonzero_weights1 * sum(density1))
        var2 = sum(density2 * deviations2)/(nonzero_weights2 * sum(density2))
        return [math.sqrt(var1), math.sqrt(var2)]
     """




class DSS(UncertaintyStructure):
    """CURRENTLY UNUSED -- this class may be fully implemented if Dempster-
    Shafer structures are to be supported explicitly. Currently they are
    covered implicitly by p-boxes.
    """
    def __init__(self, intervals, masses, num):
        min_vec = [min(i) for i in intervals]
        max_vec = [max(i) for i in intervals]
        super().__init__(min(min_vec), max(max_vec), num)

        self.intervals = intervals
        self.masses = masses

    def get_prob_at_vals(self, val):
        # This method has been replaced by 'cdf' in the other structures.
        min_prob = sum([self.masses[i] for i in range(len(self.intervals))
                        if self.intervals[i][-1] < val])
        max_prob = sum([self.masses[i] for i in range(len(self.intervals))
                        if self.intervals[0] <= val])
        return [min_prob, max_prob]

