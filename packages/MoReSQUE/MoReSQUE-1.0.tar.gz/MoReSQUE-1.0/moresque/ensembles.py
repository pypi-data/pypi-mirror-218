"""
Ensembles are employed by MoReSQUE users within a mosaik scenario. They capsule
an underlying simulator and provide it with means for uncertainty
quantification.

An instance of the :class:'EnsembleSet' is comprised of one or more ensembles
that each hold a number of model entities. Furthermore, it automatically
creates instances of the :class:'UQPropagator'. The required access is
established via mosaik.

"""
import json
import csv
import copy
import imp

import numpy as np
import moresque.ustructures as us
import moresque.assessment as af

class EnsembleSet():
    """An ensemble (set) takes in all data required to conduct uncertainty
    quantification for a given simulator. The actual UQ setup is established
    by the user via the :meth:'create_me'.

    Users have to provide a *config_dict* that provides necessary information
    about the underlying simulator and co-simulation scenario. The entries of
    this dict are given as follows:

        {
            'world': <mosaik world object>,
            'esim_name': <string>,
            'model_name': <string>,
            'sim_obj': <mosaik simulator object>,
            'ensemble_num': <int>,
            'u_config': <string>,
            'input_config': <dict>,
            'output_config': <dict>,
            'copula_config': <dict>,
            'strat_num': <int>,
            'step_size': <int>,
            'child_num': <int>,
            'cdm': <string>,
            'seed': <int>,
            'model_params': <dict>,
            'propagation_config': <dict>,
            'ep_flag': <bool>,
            'proptime_interval': <list>,
            'async_map': <dict>,
            'prune_flag': <bool>
        }

    Here *world* is the world object of the underlying mosaik simulation,
    *esim_name* gives the key of the UQ-propagator in the 'sim_config' dict of
    the mosaik simulation, *sim_obj' is the mosaik simulator object of the
    simulator in question, and *model_name* provides the name of the model that
    is to be instantiated from the simulator.
    The number of complete ensembles that should be instantiated is given by
    *ensemble_num*. The string *u_config* specifies the path to the JSON file
    describing the parameter and internal uncertainty of the simulator.
    The dicts *input_config*, *output_config* and *copula_config* allow
    specification of the number and types of uncertain inputs, outputs of
    interest, and copulas used to model correlation between uncertainty sources.
    The number of samples of the LHS sampling is given by *strat_num*. The time
    step size of the UQ propagator is defined by *step_size* and should be
    chosen according to the underlying simulator's step size.
    For composite simulators the number of input receiving and output providing
    children has to be specified via *child_num*. Similarly, these simulators
    require a child dependency map in the JSON format. The path to the according
    file is given as *cdm*.
    The seed of the employed random processes may theoretically be set via
    *seed*. However, this is currently not implemented.
    The dict *model_params* allows the specification of all certain parameters
    of the model in question, while *propagation_config* allows specification
    of control parameters for the propagation algorithms.
    The flag *ep_flag* defines whether extreme point sampling is part of the UQ
    process. If this is true, the number of samples and accordingly the number
    of ensemble members will increase.
    The entry *proptime_interval* interval consists of a start and an end time
    and specifies during which portion of the simulation process probabilistic
    propagation is conducted.
    The entries *async_map* and *prune_flag* are needed for scenarios with
    cyclic data dependencies. The former defines which output attributes of the
    underlying simulator are mapped to which input attributes of another one.
    The latter allows automatic truncation of calculated probabilistic
    u-structures.

    """
    def __init__(self, config_dict):
        # Default values:
        self.config = {'strat_num': 10,
                       'ep_flag': True,
                       'u_config': None,
                       'ensemble_num': 1,
                       'model_params': None,
                       'input_config': None,
                       'output_config': None,
                       'copula_config': None,
                       'proptime_interval': [0, np.inf],
                       'child_num': 0,
                       'propagation_config': None,
                       'cdm': None,
                       'async_map': None,
                       'prune_flag': False}
        self.config.update(config_dict)
        if self.config['copula_config'] == None:
            self.config['copula_config'] = {}

        if 'seed' in self.config.keys():
            np.random.seed(self.config['seed'])
        #TODO: This does not work in the current implementation.

        self.samp_dict = None
        """A dictionary to hold the sampled values and sampling points of
        uncertain parameters and input attributes."""

        self.ens_size = self.config['strat_num']
        """Number of expected ensemble members."""

        self.strat_num = self.config['strat_num']
        """Number of strata partitioning each sampling dimension."""

        self.prob_structs = None
        """A dictionary storing the u-structures of parameters with
        probabilistic uncertainty."""

        self.output_uncertainty = None
        """A dictionary storing the u-functions for outputs of interest."""

        self.members = None
        """A list of ensemble member entities."""

        self.param_map = None
        """A dictionary mapping between ensemble members and the parameter
        values."""

        self.input_child_num = 0
        """Number of child model entities that receive input."""

        self.output_child_num = 0
        """Number of child model entities that provide output."""

        self.input_sim = None
        """Instance of :class:'UQPropagator' for handling ensemble input."""

        self.input_modules = None
        """List of UQMI entities for handling ensemble input.'"""

        self.output_sim = None
        """Instance of :class:'UQPropagator' for handling ensemble output."""

        self.output_modules = None
        """List of UQMO entities for handling ensemble output.'"""

        self.cdm = None
        """A dictionary storing the child dependency information for composite
        simulators."""

        # Setting up everything:
        self.create_me()

    def create_me(self):
        """Create the UQ setup based on the problem description provided by the
        configuration input.

        """
        self.sampling()
        if self.config['u_config'] is None:
            self.output_uncertainty = {}
        else:
            self.def_output_uncertainty()
        self.create_members()

        # Necessary for composite simulators:
        self.calc_child_nums()
        self._read_child_dependecy_map()

        self.create_output_modules()
        self.connect_outputs()
        # Only simulators with input attributes need UQMIs:
        if self.config['input_config'] != None:
            self.create_input_modules()
            self.connect_inputs()
            self.connect_uq_ports()

    def sampling(self):
        """This function establishes a sampling design of uncertain parameters
        and input attribute data.

        """
        model_name = self.config['model_name']

        # Number of uncertain parameters:
        if self.config['u_config'] == None:
            u_dict = {model_name: {'params': {}}}
            param_num = 0
        else:
            u_dict = json.load(open(self.config['u_config']))
            param_num = len(list(u_dict[model_name]['params'].keys()))

        # Number of uncertain input data sources:
        input_num = 0
        if self.config['input_config'] != None:
            for attr_dict in self.config['input_config'].values():
                input_num += sum(list(attr_dict['attrs'].values()))
        # Ensure individual attr uncertainty sampling design for all child models:
        single_mod_input = input_num
        if self.config['child_num'] > 0:
            input_num *= self.config['child_num']

        input_sd = []
        # Get sampling design and update strata number and number of
        # ensemble members:
        samp_design, self.strat_num, self.ens_size = af.get_samp_design(
            param_num+input_num, self.strat_num, self.config['ep_flag'])

        samp_dim = 0
        param_dict = {}
        self.prob_structs = {}
        # Read parameter u-structs from JSON file:
        for param, pinfo in u_dict[model_name]['params'].items():
            ustruct = af.uinfo2struct(pinfo, self.strat_num)
            self.prob_structs[param] = ustruct
            samp_struct = copy.copy(ustruct) # original not restratified
            samp_struct.restratify(self.strat_num)
            param_vals = []
            # Draw parameter values from u-struct:
            for sp in samp_design:
                param_vals.append(samp_struct.draw_sample(int(sp[samp_dim])))
            samp_dim += 1
            param_dict[param] = param_vals

        # Cut off used sampling dimensions:
        if samp_design != None:
            for i in range(len(samp_design)):
                samp_design[i] = samp_design[i][samp_dim:]
            strt_idx = 0
            for c in range(max(1, self.config['child_num'])):
                single_design = copy.deepcopy(samp_design)
                for i in range(len(single_design)):
                    end_idx = (c+1) * single_mod_input
                    single_design[i] = single_design[i][strt_idx:end_idx]
                strt_idx += single_mod_input
                input_sd.append(single_design)
        else:
            input_sd = None

        # store parameter values and sampling points for attr uncertainty:
        self.samp_dict = {'params': param_dict, 'attrs': input_sd}

    def def_output_uncertainty(self):
        """Read and store u-functions that model internal uncertainty of a
        simulator.

        """
        u_dict = json.load(open(self.config['u_config']))
        self.output_uncertainty = {}
        # Check if models and attrs specified in JSON file match the underlying
        # uncertainty problem:
        for model, u_info in u_dict.items():
            if model in self.config['output_config'].keys():
                for attr, ainfo in u_info['attrs'].items():
                    if attr in self.config['output_config'][model]:
                        # If the output attr is not associated with internal
                        # uncertainty, no u-function is stored:
                        if ainfo.get('no_error', False):
                            self.output_uncertainty[attr] = None
                        else:
                            # ... otherwise read and store u-function:
                            self.output_uncertainty[
                                attr] = af.get_output_uncertainty(ainfo,
                                                                  self.config)

    def create_members(self):
        """Create model entities from the underlying simulator to function as
        ensemble members.

        """
        # Model create method as given by mosaik interface:
        mod_call = getattr(self.config['sim_obj'], self.config['model_name'])

        # Check and store certain parameter values:
        if self.config['model_params'] == None:
            cert_params = {}
        else:
            cert_params = self.config['model_params']
        # Previously drawn values for uncertain parameters:
        uncert_params = self.samp_dict['params']

        self.members = []
        self.param_map = {}
        # Create one set of members for each ensemble:
        for ens_idx in range(self.config['ensemble_num']):
            entities = []
            # Create members one by one with different values for uncertain
            # parameters:
            for mem_idx in range(self.ens_size):
                for param, param_vals in uncert_params.items():
                    cert_params[param] = param_vals[mem_idx]
                entities.append(mod_call(**cert_params))
                current_id = entities[-1].full_id
                # Store mapping between entity IDs and parameter values:
                for param, param_vals in uncert_params.items():
                    self.param_map.setdefault(current_id, {})
                    self.param_map[current_id][param] = param_vals[mem_idx]

            self.members.append(entities)

    def calc_child_nums(self):
        """Assess actual number of input receiving and output providing
        child entities of one ensemble member. This is needed for ensemble
        creation with composite simulators.

        """
        one_member = self.members[0][0] # select arbitrary ensemble member

        # Assess number of input receiving children by model type AND
        # common name in entity ID (Child entities of the same type that do
        # not receive inputs cause problems. They should get a different name):
        if self.config['input_config'] != None:
            for model, help_dict in self.config['input_config'].items():
                self.input_child_num += len([e for e in one_member.children
                                             if e.type == model and help_dict[
                                                 'name'] in e.eid])

        # Assess number of output providing children by model type alone
        # (Child entities of the same type that do not provide output cause no
        # problem in general):
        for model in self.config['output_config'].keys():
            self.output_child_num += len([e for e in one_member.children
                                          if e.type == model])

    def create_output_modules(self):
        """Create modules that gather and process the output of the ensemble
        members. They construct u-structs as the overall ensemble output.

        """
        # Initialize instances of :class:'UQPropagator':
        self.output_sim = self.config['world'].start(
            self.config['esim_name'], step_size=self.config['step_size'],
            simeta=self.config['sim_obj'].meta, async_map=self.config[
                'async_map'])

        # Create instances of :class:'UQMO' according to the number of ensembles
        # and output providing children in one member:
        self.output_modules = []
        for i in range(self.config['ensemble_num']):
            uqm = self.output_sim.UQMO.create(
                max(1, self.output_child_num), out_struct=self.output_uncertainty,
                parmap=self.param_map, copulas=self.config['copula_config'],
                proptime_interval=self.config['proptime_interval'],
                strat_num=self.strat_num, param_prob=self.prob_structs,
                propagation_config=self.config['propagation_config'],
                cdm=self.cdm, prune_flag=self.config['prune_flag'])
            self.output_modules.append(uqm)

    def connect_outputs(self):
        """Connect ensemble members to output modules.

        """
        world = self.config['world']
        con_lib = {}    # store the connections between members and modules for
                        # composite simulators

        # Select sets of members and UQMOs for every single ensemble:
        for ens_idx in range(len(self.members)):
            ens = self.members[ens_idx]
            out_mod = self.output_modules[ens_idx]
            # Composite simulators require several UQMOs in one ensemble:
            for hidx in range(len(out_mod)):
                con_lib[out_mod[hidx].eid] = {}
                mem_id = 0 # counter of ensemble members
                while mem_id < len(ens):
                    for model, attrs in self.config['output_config'].items():
                        # find and store related siblings and parents:
                        con_model, parent_id = self._get_con_model(ens, mem_id,
                                                                   model, hidx)
                        con_lib[out_mod[hidx].eid][con_model.full_id
                                                ] = parent_id
                        # establish actual mosaik connection:
                        for attr in attrs:
                            world.connect(con_model, out_mod[hidx], attr)
                        self.output_sim.update_eid_info(out_mod[hidx].eid,
                                                        con_model.eid)
                    mem_id += 1

        # input connection mapping into the :class:'UQPropagator' for output
        # handling:
        self.output_sim.set_connection_lib(con_lib)

    def create_input_modules(self):
        """Create modules that distribute ensemble input to the members. They
        receive u-structs from other ensembles and split them into realizations.

        """
        # Initialize instances of :class:'UQPropagator':
        self.input_sim = self.config['world'].start(
            self.config['esim_name'], step_size=self.config['step_size'],
            simeta=self.config['sim_obj'].meta)

        # Create instances of :class:'UQMI' according to the number of ensembles
        # and output providing children in one member:
        self.input_modules = []
        for i in range(self.config['ensemble_num']):
            uqm = []
            for j in range(max(1, self.input_child_num)):
                uqm.append(self.input_sim.UQMI(
                    samp_design=self.samp_dict['attrs'][j],
                    strat_num=self.strat_num))
            self.input_modules.append(uqm)

    def connect_inputs(self):
        """Connect input modules to ensemble members.

        """
        world = self.config['world']
        con_lib = {}    # Mapping between UQMI ports and model entities

        # Select member set and UQMIs for every single created ensemble:
        for ens_idx in range(len(self.members)):
            ens = self.members[ens_idx]                 # member set
            in_mod = self.input_modules[ens_idx]        # set of UQMIs
            # Composite simulators require several UQMIs:
            for hidx in range(len(in_mod)):
                con_lib[in_mod[hidx].eid] = {}
                uqchild_id = 0  # counter for children (output ports) of one UQMI
                mem_id = 0      # counter for ensemble members
                while uqchild_id < len(in_mod[hidx].children):
                    # Consult connection information given in problem description:
                    for model, con_dict in self.config['input_config'].items():
                        # Which entities actually receive inputs?
                        con_model, non = self._get_con_model(ens, mem_id,
                                                             model, hidx)
                        # How many input sources are expected for each attr?
                        for attr, con_num in con_dict['attrs'].items():
                            for i in range(con_num):
                                # Select output port (child) of UQMI:
                                current_child = in_mod[hidx].children[uqchild_id]
                                # Establish mosaik connection:
                                world.connect(current_child, con_model, attr)
                                # Document connection in mapping:
                                con_lib[in_mod[hidx].eid][current_child.eid
                                                        ] = con_model.full_id
                                uqchild_id += 1
                    mem_id += 1
        # Store connection mapping in :class:'UQPropagator' for input handling:
        self.input_sim.set_connection_lib(con_lib)

    def connect_uq_ports(self):
        """Connect UQMIs directly to UQMOs to enable exchange of necessary
        uncertainty information.

        """
        # Do this for each created ensemble:
        for ens_idx in range(len(self.input_modules)):
            for in_mod in self.input_modules[ens_idx]:
                for out_mod in self.output_modules[ens_idx]:
                    # mosaik connection:
                    self.config['world'].connect(in_mod, out_mod, 'uqi')

    def _get_con_model(self, ensemble, mem_id, modeltype, help_idx):
        """Identify model entities for connection with UQ modules.

        """
        # Case: underlying simulator is monolithic (not composite) so that the
        # primary instantiated model entities are to be connected:
        if ensemble[mem_id].type == modeltype:
            # Return member from ensemble based on counter:
            return ensemble[mem_id], ensemble[mem_id].full_id

        # Case: underlying simulator is composite and must be connected via
        # child entities:
        else:
            # Get set of children with required *modeltype* from ensemble member:
            modset = [e for e in ensemble[mem_id].children
                      if e.type == modeltype]
            # Return child entity via index and parent ID:
            return modset[help_idx], ensemble[mem_id].full_id

    def _read_child_dependecy_map(self):
        """Read dependencies between children of composite simulators from
        JSON file.

        """
        if self.config['cdm'] is not None:
            try:
                self.cdm = json.load(open(self.config['cdm']))
            except:
                raise RuntimeError('Cannot read file "%s" to access'
                    ' Children Dependency Map' % self.config['cdm'])
