"""This module provides a mosaik-compatible co-simulation component that is
used by MoReSQUE ensembles to organize their inputs and outputs.
"""
import itertools

import mosaik_api

from moresque import uqm

# Meta description for handling of the component in mosaik
meta = {
    'type': 'time-based',
    'models': {
        'UQMI': {
            'public': True,
            'params': ['samp_design',
                       'strat_num'],
            'attrs': ['uqi', 'async'],
        },
        'UQMc': {
            'public': False,
            'params': [],
            'attrs': [],
        },
        'UQMO': {
            'public': True,
            'params': ['out_struct',
                       'strat_num',
                       'copulas',
                       'parmap',
                       'proptime_interval',
                       'param_prob',
                       'propagation_config',
                       'cdm',
                       'prune_flag'],
            'attrs': ['uqi', 'async'],
        },
    },
    'extra_methods': [
        'set_connection_lib',
        'update_eid_info',
        'get_eid_info',
    ],
}

class UQPropagator(mosaik_api.Simulator):
    """Propagator class that provides input and output modules for ensembles.
    """
    def __init__(self):
        super().__init__(meta)
        self.sid = None
        self.step_size = None

        self.cache = {}
        self._entities = {}
        self.eid_counters = {}
        self.active_eids = None
        self.eid_info = {}

        # Attributes for support of cyclic data dependencies:
        self.has_inputs = True  # for interaction with simulators that vary
                                # in their input behavior (e.g. controllers)
        self.async_map = None

    def init(self, sid, time_resolution, step_size, simeta, async_map=None):
        """Mosaik function for initialization of the propagator.

        Arguments:
        sid -- (string) simulator ID for propagator, set by mosaik
        time_resolution -- (float) time resolution
        step_size -- (int) number of time units in one time step
        simeta -- (dict) meta description of the underlying simulator
        async_map -- (dict) description of cyclic data dependency if existing

        Return:
        meta description (dict) of propagator
        """

        self.sid = sid
        self.step_size = step_size
        self.async_map = async_map

        # Adding attributes of underlying simulation model:
        for mname, model in self.meta['models'].items():
            for ext_mod in simeta['models'].values():
                model['attrs'].extend(ext_mod['attrs'])

        return self.meta

    def create(self, num, model, **model_params):
        """Mosaik function for the creation of model entities (in this context
        uncertainty quantification modules (UQMs).

        Arguments:
        num -- (int) number of created UQMs
        model -- (string) type of UQM to be created
        model_params -- (dict) inputs for keyword arguments of UQMs

        Return:
        List of dicts describing the creating entities
        """

        # Check set model_params for correctness:
        self._check_modpars(model, model_params)

        counter = self.eid_counters.setdefault(model, itertools.count())
        entities = []
        mod_call = getattr(uqm, model)  # get access to creation of selected
                                        # UQM type

        for idx in range(num):
            eid = '%s_%s' % (model, next(counter))

            self._entities[eid] = mod_call(eid, **model_params)
            # UQMIs are created with child entities:
            if model == 'UQMI' and self._entities[eid].has_children():
                children = []
                for child in self._entities[eid].children:
                    children.append({
                        'eid': child.eid,
                        'type': 'UQMc',
                        'rel': []
                    })
                entities.append({'eid': eid, 'type': model, 'rel': [],
                                 'children': children})
            else:
                entities.append({'eid': eid, 'type': model, 'rel': []})

        return entities

    def step(self, t, inputs={}, max_advance=None):
        """Mosaik function for performing an uncertainty propagation step.

        Arguments:
        t -- (int) current point in simulation time
        inputs -- (dict) input structure for the current propagation step
        max_advance -- (int)

        Return:
        Next point in simulation time when the propagator is to be stepped
        """

        set_data = {} # data storage for cyclic dependency handling
        # Check whether inputs are provided (important for cyclic dependencies):
        if inputs == {}:
            self.has_inputs = False
        else:
            self.has_inputs = True

        self.active_eids = []
        for eid, attrs in inputs.items():
            # Check if input contain request for cyclic exchange:
            if 'async' in attrs.keys():
                async_src = attrs.pop('async')
            else:
                async_src = None
            # Stepping UQM and storing its outputs:
            self.cache.update(self._entities[eid].step(attrs, t))
            # Provide data for cyclic exchange if necessary:
            if async_src is not None:
                set_data = self.handle_async_requests(set_data, eid,
                                                      async_src)
            # Storing information of UQM children involved in stepping:
            self.active_eids.append(eid)
            if 'UQMI' in eid and self._entities[eid].has_children():
                for child in self._entities[eid].children:
                    self.active_eids.append(child.eid)

        # Set data for cyclic exchange if necessary:
        if set_data != {}:
            yield self.mosaik.set_data(set_data)

        return t + self.step_size

    def get_data(self, outputs):
        """Mosaik function that request the data produced in a calculation step.

        Arguments:
        outputs -- (dict) structure with data request information

        Return:
        data -- (dict) structure with output data
        """
        data = {}
        for eid, attrs in outputs.items():
            if eid in self.active_eids or not self.has_inputs:
                data[eid] = {}
                for attr in attrs:
                    if not self.has_inputs or attr == 'async':
                        data[eid][attr] = None
                        # Simulators that are able to work with no input
                        # must be able to accept 'None' to switch to default
                    else:
                        data[eid][attr] = self.cache[eid][attr]
        return data

    def handle_async_requests(self, set_data, eid, src_dict):
        """Helper function for organization associated with cyclic data
        dependencies.

        Arguments:
        set_data -- (dict) preliminary structure with data that is to be set
        eid -- (string) ID of the UQM that received data
        src_dict -- (dict) received structure with data request

        Return:
        Updated set_data structure
        """

        set_data.setdefault(eid, {})
        for dest_eid in src_dict.keys():
            set_data[eid].setdefault(dest_eid, {})
            for src_attr, dest_attr in self.async_map.items():
                set_data[eid][dest_eid][dest_attr] = self.cache[eid][src_attr]

        return set_data

    def set_connection_lib(self, con_lib):
        """Procedure that provides UQMs with information about the connection
        between UQM children and ensemble members.

        Arguments:
        con_lib -- (dict) structure with connection information, provided by
                    ensemble
        """
        for eid, con_dict in con_lib.items():
            self._entities[eid].con_dict = con_dict

    def update_eid_info(self, my_eid, connected_eid):
        """Procedure that stores info about UQM connections. May serve users
        in future software versions.

        Arguments:
        my_eid -- (string) ID of the target UQM
        connected_eid -- (string) ID of the connected model entity
        """
        self.eid_info[my_eid] = connected_eid

    def get_eid_info(self, my_eid):
        """Function that allows access to information about ensemble entities.
        So far, the function is UNUSED.
        """
        return self.eid_info[my_eid]

    def _check_modpars(self, model, model_params):
        """Procedure for checking whether the required UQM parameters have
        been set during creation.

        Arguments:
        model -- (string) name of the desired UQM type
        model_params -- (dict) structure with UQM parameter values
        """

        # TODO: Functionality so far incomplete
        if model == 'UQMI':
            if 'samp_design' not in model_params.keys():
                raise RuntimeError("Model '%s' is missing a parameter "
                    "'samp_design'" % model)
            if 'strat_num' not in model_params.keys():
                raise RuntimeError("Model '%s' is missing a parameter "
                    "'strat_num'" % model)

        if model == 'UQMO':
            if 'out_struct' not in model_params.keys():
                raise RuntimeError("Model '%s' is missing a parameter "
                "'out_struct'" % model)


def main():
    mosaik_api.start_simulation(UQPropagator(), 'UQPropagator')
