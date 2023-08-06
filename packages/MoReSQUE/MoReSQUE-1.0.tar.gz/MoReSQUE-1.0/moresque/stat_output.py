"""This module provides a utility component for co-simulation that may be
employed in mosaik scenarios to extract statistical measures from MoReSQUE
ensembles.
"""
import itertools

import mosaik_api

import moresque.ustructures as us

meta = {
    'type': 'time-based',
    'models': {
        # Module used for processing of interval structures:
        'ItvlOut': {
            'public': True,
            'params': [],
            'attrs': []
        },
        # Module used for processing of distribution structures:
        'DstrOut': {
            'public': True,
            'params': [],
            'attrs': []
        },
        # Module used for processing of p-box structures:
        'PboxOut': {
            'public': True,
            'params': [],
            'attrs': []
        },
    },
}

class StatOut(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(meta)
        self.sid = None
        self.step_size = None

        self.cache = {}
        self.eid_counters = {}

    def init(self, sid, time_resolution, step_size, attrs):
        """init function as required by the mosaik API.

        Arguments:
        sid -- (string) simulator ID
        time_resolution -- (float) time resolution
        step_size -- (int) number of time units for one simulation step
        attrs -- (list) name strings of attributes processed by the module

        Return:
        meta -- (dict) description of the component as required by mosaik
        """
        self.sid = sid
        self.step_size = step_size

        # Formulation of possible output attributes based on the processed
        # uncertainty type:
        for attr in attrs:
            # Minimum and maximum for intervals:
            itvl_list = [attr, attr+'_minA', attr+'_maxA']
            # Minimum, maximum, average, standard deviation, 5% quantile,
            # 95% quantile, 15.9% qunatile, 84.1% qunatile for distributions:
            dstr_list = [attr, attr+'_minA', attr+'_maxA', attr+'_aveA',
                         attr+'_stdA', attr+'_q05A', attr+'_q95A',
                         attr+'_q15A', attr+'_q84A']
            # All statistical measures for both boundary distributions of
            # p-boxes:
            pbox_list = [attr, attr+'_minA', attr+'_maxA',
                         attr+'_aveA', attr+'_aveB',
                         attr+'_stdA', attr+'_stdB',
                         attr+'_q05A', attr+'_q05B',
                         attr+'_q95A', attr+'_q95B',
                         attr+'_q15A', attr+'_q15B',
                         attr+'_q84A', attr+'_q84B']

            self.meta['models']['ItvlOut']['attrs'].extend(itvl_list)
            self.meta['models']['DstrOut']['attrs'].extend(dstr_list)
            self.meta['models']['PboxOut']['attrs'].extend(pbox_list)

        return self.meta

    def create(self, num, model, **model_params):
        """create function as required by the mosaik API.

        Arguments:
        num -- (int) number of instantiated modules
        model -- (string) name of the module type that is to be instantiated
        model_params -- (dict) module parameters (unused)

        Return:
        entities -- (dict) representation of instantiated module entities
                as required by mosaik
        """
        counter = self.eid_counters.setdefault(model, itertools.count())
        entities = []

        for idx in range(num):
            eid = '%s_%s' % (model, next(counter))
            entities.append({'eid': eid, 'type': model, 'rel': []})

        return entities

    def step(self, t, inputs, max_advance):
        """step function as required by the mosaik API.

        Arguments:
        t -- (int) current simulation time
        inputs -- (dict) input provided by other components (ensembles)
        max_advance -- (int)

        Return:
        simulation time stamp for the next step
        """
        for eid, attrs in inputs.items():
            self.cache[eid] = {}
            for attr, data in attrs.items():
                # Only one input source (ensemble) is expected, others are
                # ignored:
                self.cache[eid][attr] = list(data.values())[0]

        return t + self.step_size

    def get_data(self, outputs):
        """get_data function as required by the mosaik API.

        Arguments:
        outputs -- (dict) output data requested by other components

        Return:
        outdata -- (dict) structure with requested output data
        """
        outdata = {}
        for eid, attrs in outputs.items():
            outdata[eid] = {}
            for attr in attrs:
                attr_basic = attr[:-5]  # cut off statistical measure type
                stat_spec = attr[-5:]   # get statistical measure type

                ustrct = self.cache[eid][attr_basic]
                # Check if received input is really a u-structure:
                if isinstance(ustrct, us.UncertaintyStructure):
                    # Get appropriate function to extracted the inquired measure:
                    stat_fun = getattr(self, '_get'+stat_spec[:4])
                    outval = stat_fun(ustrct)
                    outdata[eid][attr] = self.organize_output(attr, eid, outval)
                else:
                    outdata[eid][attr] = ustrct # certain data needs no extraction

        return outdata

    def organize_output(self, attr, eid, outval):
        """Helper function that picks the appropriate output from data received
        from p-box structures.

        Arguments:
        attr -- (string) inquired module output attribute
        eid -- (string) entity ID of the module
        outval -- float or list received from u-structure

        Return:
        outval -- (float) statistical output measure
        """
        if isinstance(outval, list):
            assert 'Pbox' in eid
            if attr[-1] == 'A':
                return outval[0]
            elif attr[-1] == 'B':
                return outval[1]
        else:
            return outval

    def _get_min(self, ustrct):
        """Function that obtains the minimum of a u-structure *ustrct*.
        """
        return ustrct.samp_space[0]

    def _get_max(self, ustrct):
        """Function that obtains the maximum of a u-structure *ustrct*.
        """
        return ustrct.samp_space[-1]

    def _get_ave(self, ustrct):
        """Function that obtains the mean value of a u-structure *ustrct*.
        """
        if isinstance(ustrct, us.Interval):
            minimum = ustrct.samp_space[0]
            maximum = ustrct.samp_space[-1]
            return (maximum+minimum)/2.0
        else:
            return ustrct.get_mean()

    def _get_std(self, ustrct):
        """Function that obtains the standard deviation value of a u-structure
        *ustrct*.
        !!!This function is currently not fully functional!!!
        """
        if isinstance(ustrct, us.Interval):
            minimum = ustrct.samp_space[0]
            maximum = ustrct.samp_space[-1]
            return (maximum+minimum)/2.0
        else:
            return ustrct.get_std()

    def _get_q05(self, ustrct):
        """Function that obtains the 5% quantile of a u-structure *ustrct*.
        """
        if isinstance(ustrct, us.Interval):
            return ustrct.samp_space[0]
        else:
            return ustrct.get_quantile(0.05)

    def _get_q95(self, ustrct):
        """Function that obtains the 95% quantile of a u-structure *ustrct*.
        """
        if isinstance(ustrct, us.Interval):
            return ustrct.samp_space[-1]
        else:
            return ustrct.get_quantile(0.95)

    def _get_q15(self, ustrct):
        """Function that obtains the 15.9% quantile of a u-structure *ustrct*.
        May be used as a workaround to obtain information about the standard
        deviation.
        """
        if isinstance(ustrct, us.Interval):
            return ustrct.samp_space[0]
        else:
            return ustrct.get_quantile(0.159)

    def _get_q84(self, ustrct):
        """Function that obtains the 84.1% quantile of a u-structure *ustrct*.
        May be used as a workaround to obtain information about the standard
        deviation.
        """
        if isinstance(ustrct, us.Interval):
            return ustrct.samp_space[-1]
        else:
            return ustrct.get_quantile(0.841)


def main():
    mosaik_api.start_simulation(StatOut(), 'StatOut')
