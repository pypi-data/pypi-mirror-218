"""This module provides classes of Uncertainty Quantification Modules. They may
be instantiated by the :class:"UQPropagator" and handle the processing and
calculation of uncertainty structures.
"""
import copy
import time
import re

import numpy as np
from scipy.interpolate import griddata

import moresque.ustructures as us
import moresque.propagation as pf

class UQMI():
    """Uncertainty Quantification Module that provides input to an ensemble.
    """
    def __init__(self, eid, samp_design, strat_num):
        """Constructor function.

        Arguments:
        eid -- (string) entity ID of the UQM
        samp_design -- (list) sampling design represented by list of lists
        strat_num -- (int) number of strata dividing each input dimension
        """

        self.eid = eid
        self.strat_num = strat_num
        self.child_map = [] # mapping between children and sampling points
        self.children = []
        self.member_num = len(samp_design)
        self.con_dict = None

        # Instantiating objects of :class:"UQMc" as children based on the
        # sampling design:
        self._make_children_registers(samp_design)

    def step(self, in_dict, t):
        """Function that allows the UQM to split possibly uncertain input into
        single values for the ensemble members.

        Arguments:
        in_dict -- (dict) structured input preorganized by UQPropagator
        t -- (int) current simulation time

        Return:
        out_dict -- (dict) structured output to be sent of ensemble members and
        UQMO
        """

        out_dict = {}
        # Handling possibly uncertain input:
        if self.has_children():
            uq_prob_dict = {}
            uq_val_dict = {}
            # Looping over ensemble members:
            for bi in range(self.member_num):
                cind = 0        # child index
                for attr, vals in in_dict.items():
                    for src_id, val in vals.items():
                        # Selecting UQMchild corresponding to current member:
                        child = self.child_map[bi][cind]
                        if isinstance(val, us.UncertaintyStructure):
                            val, vd, pd = self.ustruct_handling(copy.copy(val),
                                                                child, attr,
                                                                src_id)
                            # Organizing uncertainty information required by
                            # the UQMO of the ensemble:
                            uq_val_dict = pf.update_dict(uq_val_dict, vd)
                            uq_prob_dict = pf.update_dict(uq_prob_dict, pd)
                        # Output for ensemble members:
                        out_dict[child.eid] = {attr: val}
                        cind += 1
            # Output for UQMO:
            out_dict[self.eid] = {'uqi': [uq_val_dict, uq_prob_dict]}
        # Handling definitly certain input (ensemble does not expect uncertain
        # input):
        else:
            out_dict[self.eid] = {}
            for attr, vals in in_dict.items():
                for src_id, val in vals.items():
                    if isinstance(val, us.UncertaintyStructure):
                        raise RuntimeError("UQM needs a sampling design to "
                            "handle input uncertainty.")
                    else:
                        if attr in out_dict[self.eid].keys():
                            raise RuntimeError("UQM needs children to handle "
                                "multiple input sources")
                        else:
                            out_dict[self.eid][attr] = val
        return out_dict

    def ustruct_handling(self, val, child, attr, src_id):
        """This function serves the actual value extraction from uncertainty
        structures.

        Arguments:
        val -- (UncertaintyStructure) input uncertainty structure
        child -- (UQMc) UQM child providing the needed sampling point
        attr -- (string) target input attribute of ensemble model
        src_id -- (string) entity ID of the sending ensemble

        Return:
        val -- (float) member input value extracted from u-structure
        vd -- (dict) structured information about input value (needed by UQMO)
        pd -- (dict) structured information about input u-structure (see above)
        """

        # Received uncertainty structure may not have proper spacing:
        if val.get_stratnum() != self.strat_num:
            val.restratify(self.strat_num)
        struct = val
        # Extract member input value from u-structure:
        val = struct.draw_sample(child.get_sp())
        # Organize value and u-structure information for UQMO:
        pd = {attr: {src_id: struct}}
        dest_id = self.con_dict[child.eid]
        vd = {dest_id: {attr: {src_id: val}}}

        return val, vd, pd

    def has_children(self):
        """Helper function that checks whether the UQM has children and thus
        expects uncertain input.
        """
        return self.children != []

    def _make_children_registers(self, samp_design):
        """This procedure creates the set of children of the UQMI based on the
        given sampling design.

        Arguments:
        samp_design -- (list) sampling points represented by list of lists
        """

        # Looping over child batches (each batch includes all children that are
        # responsible for one ensemble member - since it may receive input from
        # several different sources):
        for bi in range(len(samp_design)):
            self.child_map.append([])
            # Looping over all input sources in one batch:
            for pi in range(len(samp_design[bi])):
                # Create child and add to mapping:
                self.child_map[bi].append(UQMc(bi, pi, self.eid,
                                                  sampling_point=int(
                                                      samp_design[bi][pi])))
                # Add child to list of children (needed by UQPropagator):
                self.children.append(self.child_map[bi][pi])


class UQMc():
    """Submodule for UQMI. Each child provides one input value to one
    ensemble member.
    """
    def __init__(self, batch_ind, point_ind, parent_eid, sampling_point=None):
        """Constructor function.

        Arguments:
        batch_ind -- (int) index of the child batch (corresponding to ensemble
                    member
        point_ind -- (int) index of child within a batch (corresponding to
                    input source
        parent_eid -- (string) entity ID of the corresponding UQMI
        sampling_point -- (int) value from the sampling design
        """
        self.eid = parent_eid + '_child_%i_%i' % (batch_ind, point_ind)
        self.sampling_point = sampling_point

    def get_sp(self):
        """Function that returns the sampling information (stratum) provided
        by the UQM child.
        """
        return self.sampling_point


class UQMO():
    """Uncertainty Quantification Module that processes the output of ensembles.
    """
    def __init__(self, eid, out_struct, strat_num, copulas, parmap,
                 proptime_interval, param_prob, propagation_config, cdm,
                 prune_flag):
        """Constructor function.

        Arguments:
        eid -- (string) entity ID for the UQMO
        out_struct -- (dict) structure with information about the internal
                    uncertainty
        strat_num -- (int) number of strata dividing the input uncertainty space
        copulas -- (dict) structure providing copula function handles
        parmap -- (dict) structured information about the parameter vales of
                    the ensemble members
        proptime_interval -- (list) simulation time interval during which the
                    uncertainty propagation is to be conducted
        param_prob -- (dict) structured information about the uncertainty of the
                    ensemble parameters
        propagation_config -- (dict) structured information about the configuration
                    of the propagation algorithms
        cdm -- (dict) information about child entity interconnections (needed
                    for ensembles of composite simulators)
        prune_flag -- (bool) flag stating whether u-structure pruning should be
                    conducted (needed for cyclic dependencies)
        """
        self.eid = eid
        self.out_struct = out_struct
        self.strat_num = strat_num
        self.copulas = copulas
        self.uq_param_vals = parmap
        self.uq_param_probs = param_prob
        self.dim_num = 0 # might be increased later
        self.proptime_interval = proptime_interval
        self.con_dict = None
        self.cdm = cdm # Children Dependency Map
        self.prune_flag = prune_flag # Needed for cycles
        if propagation_config is None:
            self.prop_config = {}
        else:
            self.prop_config = propagation_config
        # Reformat *prop_config* to make it useable by the algorithms:
        for mode, attrs in self.copulas.items():
            self.prop_config.setdefault(mode, {})
            for attr in attrs.keys():
                self.prop_config[mode].setdefault(attr, None)

    def step(self, in_dict, t):
        """Function that allows the UQM to calculate u-structures based on the
        output values provided by the ensemble members.

        Arguments:
        in_dict -- (dict) structured member outputs preorganized by UQPropagator
        t -- (int) current simulation time

        Return:
        out_dict -- (dict) structured uncertainty output of the complete
            ensemble
        """
        out_dict = {self.eid: {}}

        # Information from UQMI needed for probabilistic propagation:
        if 'uqi' in in_dict.keys():
            uq_val_dict, uq_prob_dict = self.unpack_uqi(in_dict.pop('uqi'))
        else:
            uq_val_dict = {}
            uq_prob_dict = {}

        # Looping over the ensemble member output attribute:
        for attr, vals in in_dict.items():
            surrogate_target = []
            surrogate_in = {}
            dependency_check = True
            # Storage for the min and max of each output attribute:
            out_dict[self.eid][attr] = {'min': np.inf,
                                        'max': np.inf * -1}

            # Loop over ensemble members and the provided values:
            for src_id, val in vals.items():
                surrogate_target.append(val) # storing output attribute values
                # Perform probability propagation of external uncertainties
                # if copula is given:
                if 'input' in self.copulas.keys():
                    # Obtain interconnections of ensemble members:
                    parent_entity_id = self.con_dict[src_id]
                    input_entity_ids = [src_id]
                    if self.cdm is not None and dependency_check:
                        rough_id = self.get_rough_id(src_id)
                        input_entity_ids.extend(self.cdm[rough_id])
                    # Obtain and store parameter values of ensemble members:
                    if self.uq_param_vals != {}:
                        for in_par, in_val in self.uq_param_vals[
                            parent_entity_id].items():
                            surrogate_in.setdefault(in_par, [])
                            surrogate_in[in_par].append(in_val)
                    # Associate data providing members with the data:
                    for check_id in input_entity_ids:
                        spec_ids = self.get_spec_ids(check_id, uq_val_dict)
                        for spec_id in spec_ids:
                            for in_att, indict in uq_val_dict[spec_id].items():
                                for in_src, in_val in indict.items():
                                    surrogate_in.setdefault((in_att, in_src), [])
                                    surrogate_in[(in_att, in_src)].append(in_val)
                    dependency_check = False # go only once through member child
                                             # interdependencies
                # Store minimal and maximal possible member output:
                out_dict[self.eid][attr]['min'] = min(val, out_dict[self.eid][
                    attr]['min'])
                out_dict[self.eid][attr]['max'] = max(val,out_dict[self.eid][
                    attr]['max'])

            param_probs = copy.deepcopy(self.uq_param_probs)

            # Further preparations for surrogate creation:
            for factkey, surr_in in list(surrogate_in.items()):
                # Sensitivity analysis for numerical stability:
                if abs(max(surr_in) - min(surr_in)) < 1e-5:
                    del surrogate_in[factkey]
                    if isinstance(factkey, tuple):
                        del uq_prob_dict[factkey[0]][factkey[1]]
                    else:
                        del param_probs[factkey]
            distr_flag = self.check_for_dstrs(uq_prob_dict, param_probs)
            self.dim_num = len(surrogate_in)

            # Surrogate creation and u-structure calculation:
            if self.dim_num > 0 and len(set(surrogate_target)) > 1:
                if (t >= self.proptime_interval[0] and
                    t <= self.proptime_interval[-1] and distr_flag):
                    resultstr = pf.process_surrogate(surrogate_in,
                                                     surrogate_target,
                                                     param_probs,
                                                     uq_prob_dict,
                                                     self.dim_num,
                                                     self.copulas['input'][attr],
                                                     self.prop_config['input'][
                                                         attr])
                    if self.prune_flag:
                        resultstr.prune_interval()
                else:
                    resultstr = None
            else:
                resultstr = None
            attr_min = out_dict[self.eid][attr]['min']
            attr_max = out_dict[self.eid][attr]['max']

            # Output u-structure (or certain value) if no internal uncertainty
            # is given:
            if attr not in self.out_struct.keys() or self.out_struct[
                attr] == None:
                if resultstr == None:
                    if attr_min == attr_max:
                            out_dict[self.eid][attr] = val
                    else:
                        out_dict[self.eid][attr] = us.Interval(attr_min,
                                                               attr_max,
                                                               self.strat_num)
                else:
                    out_dict[self.eid][attr] = resultstr
            # Account for internal uncertainty:
            else:
                # Obtain u-function that models internal uncertainty:
                ufunc_struct = self.out_struct[attr]
                ufunc = ufunc_struct['function']
                # Case without external uncertainty:
                if attr_min == attr_max:
                    new_struct = ufunc.main(attr_max, t, **ufunc_struct[
                        'kwargs'])
                # Case with external uncertainty:
                else:
                    # Without probabilistic external uncertainty:
                    if resultstr == None:
                        new_struct1 = ufunc.main(attr_min, t, **ufunc_struct[
                            'kwargs'])
                        new_struct2 = ufunc.main(attr_max, t, **ufunc_struct[
                            'kwargs'])
                        new_struct = pf.merge_marginal_ustructs(new_struct1,
                                                                new_struct2)
                    # With probabilistic external uncertainty:
                    else:
                        new_struct = pf.correct_uncertainty(resultstr,
                                                            ufunc_struct, t,
                                                            self.copulas[
                                                                'output'][attr])
                out_dict[self.eid][attr] = new_struct

        return out_dict

    def unpack_uqi(self, info_pack):
        """Helper function that organizes the data directly provided from the
        UQMI to the UQMO.

        Arguments:
        info_pack -- (list) structure with input uncertainty information

        Return:
        uq_val_dict -- (dict) structure with input data the members received
        uq_prob_dict -- (dict) structure with input uncertainty structures
        """
        uq_val_dict = {}
        uq_prob_dict = {}

        for info_list in info_pack.values():
            if info_list is not None:   # None may appear in async context
                uq_val_dict.update(info_list[0])
                if info_list[1] != {}:
                    # Properly add entries of sent dict to local dict:
                    uq_prob_dict = pf.update_dict(uq_prob_dict, info_list[1])

        return uq_val_dict, uq_prob_dict

    def check_for_dstrs(self, attr_probs, param_probs):
        """Helper function that checks whether probabilistic uncertainty
        structures exist among the external uncertainties.

        Arguments:
        attr_probs -- (dict) structure with the u-structures for the ensemble
                    members' input attributes
        param_probs -- (dict) structure with the u-structures for the ensemble
                    members' parameters

        Return:
        flag -- (bool) True if probabilistic u-structures exist among
                *attr_probs* or *param_probs*
        """
        flag = False
        for subdict in attr_probs.values():
            for struct in subdict.values():
                if (isinstance(struct, us.Distribution)
                    or isinstance(struct, us.PBox)):
                    flag = True

        for struct in param_probs.values():
            if (isinstance(struct, us.Distribution)
                or isinstance(struct, us.PBox)):
                flag = True

        return flag

    def get_spec_ids(self, id_string, dictionary):
        """Helper function that obtains the entity IDs of all ensemble member
        children based on the IDs of children of a single member (necessary for
        the handling of composite simulators).

        Arguments:
        id_string -- (string) ID of one ensemble member child
        dictionary -- (dict) structure that associates entities with the input
                    they have received

        Return:
        spec_ids -- (list) all IDs of ensemble member children that correspond
                    to the one identified by *id_string*
        """
        spec_ids = []
        for k in dictionary.keys():
            if id_string in k:
                if id_string == k:
                    spec_ids.append(k)
                else:
                    # Sort out strings with longer numbers since they belong to
                    # other entities:
                    pattern = re.compile("^\S*" + id_string + "\D*$")
                    if pattern.match(k) != None:
                        spec_ids.append(k)

        return spec_ids

    def get_rough_id(self, id_string):
        """Helper function that obtains the entry ID in the Children Dependency
        Map associated with a specific entity ID.

        Arguments:
        id_string -- (string) specific entity ID of an ensemble member child

        Return:
        k -- (string) entitiy ID that is a key of the *cdm* and associated to
                *id_string*
        """
        for k in self.cdm.keys():
            if k in id_string:
                return k
        # Return None if no associated entry exists in *cdm*:
        return None
