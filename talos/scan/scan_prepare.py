def scan_prepare(self):

    '''Includes all preparation procedures up until starting the first scan
    through scan_run()'''

    from .scan_utils import initialize_log

    self._experiment_log_csv, self._experiment_log_pkl = initialize_log(self)

    # for the case where x_val or y_val is missing when other is present
    self.custom_val_split = False
    if (self.x_val is not None and self.y_val is None) or \
       (self.x_val is None and self.y_val is not None):
        raise RuntimeError("If x_val/y_val is inputted, other must as well.")

    elif self.x_val is not None and self.y_val is not None:
        self.custom_val_split = True

    # create reference for parameter keys
    self._param_dict_keys = sorted(list(self.params.keys()))

    # create the parameter object and move to self
    from ..parameters.ParamSpace import ParamSpace
    self.param_object = ParamSpace(params = self.params,
                                   param_keys = self._param_dict_keys,
                                   random_method = self.random_method,
                                   fraction_limit = self.fraction_limit,
                                   round_limit = self.round_limit,
                                   time_limit = self.time_limit,
                                   boolean_limit = self.boolean_limit)

    # mark that it's a first round
    self.first_round = True
    
    import pandas as pd
    self.data = pd.DataFrame()
    
    self.saved_models = []
    self.saved_weights_list = []
    
    detail_attr = ['random_method', 'grid_downsample',
                   'reduction_interval', 'reduce_loss',
                   'reduction_method', 'reduction_metric',
                   'reduction_threshold', 'reduction_window',
                   'experiment_name']

    out = {}
    
    for key in list(detail_attr.keys()):
        out[key] = self.__dict__[key]

    try:
        out['x_shape'] = self.x.shape
    # for the case when x is list
    except AttributeError:
        out['x_shape'] = 'list'

    try:
        out['y_shape'] = self.y.shape
    except AttributeError:
        out['y_shape'] = 'list'
        
    import datetime
    import pytz
    
    start_time = datetime.datetime.now().astimezone(
        pytz.timezone('Europe/Berlin')).strftime("%Y-%m-%d %H:%Mm")
    out['start_time'] = start_time 
    out['end_time'] = start_time

    self.details = pd.Series(out) 

    # handle validation split
    from ..utils.validation_split import validation_split
    self = validation_split(self)

    # set data and len
    self._data_len = len(self.x)

    return self
