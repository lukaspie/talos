def scan_prepare(self):

    '''Includes all preparation procedures up until starting the first scan
    through scan_run()'''
    import pandas as pd
    import numpy as np

    from .scan_utils import initialize_log
    try:
        self._experiment_log_csv, self._experiment_log_pkl = \
            initialize_log(self, write = False)
        from .scan_restore import scan_restore
        scan_restore(self)
        self.first_round = False
        
        # Reload start and end times for the details file
        start_time = self.details['start_time']
        end_time = self.details['end_time']
        
        print('Previous scan data was loaded from scan folder!')
        
    except FileNotFoundError:
        self._experiment_log_csv, self._experiment_log_pkl = \
            initialize_log(self)
        self.data = pd.DataFrame()
        self.saved_models = []
        self.saved_weights_list = []
        self.saved_weights = np.array(self.saved_weights_list)
        # mark that it's a first round
        self.first_round = True
        
        # Store start time for the details file
        import datetime
        import pytz
    
        start_time = datetime.datetime.now().astimezone(
            pytz.timezone('Europe/Berlin')).strftime("%Y-%m-%d %H:%M")
        end_time = start_time

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
                                   
    # Remove parameter combinations that were already used.
    if self.data.shape != (0,0):
        data = self.data.copy()
        pop_list = ['round_epochs', 'start', 'end',
                    'duration', 'entropy', 
                    'loss', 'val_loss']
        for item in pop_list:
            _ = data.pop(item)

        del_list = []
        for i in range(data.shape[0]):
            values = data.iloc[i].values
            for j in range(self.param_object.param_space.shape[0]):
               if (values == self.param_object.param_space[j]).all():
                   if j not in del_list:
                       del_list.append(j)
        self.param_object.param_space = np.delete(
            self.param_object.param_space,
            del_list,
            axis = 0)
        
        if self.param_object.param_space.shape[0] == 0:
            self.param_object.param_index = []
            print('\n No scan performed because all ' +
                  'permutations were already scanned!')
    
    
    detail_attr = ['random_method', 'reduction_interval',
                   'experiment_name', 'reduction_method',
                   'reduction_metric', 'reduction_threshold',
                   'reduction_window']

    out = {}
    
    for key in detail_attr:
        out[key] = self.__dict__[key]

    try:
        out['x_shape'] = self.x.shape
    # for the case when x is list
    except AttributeError:
        out['x_shape'] = (len(self.x), self.x[0].shape)

    try:
        out['y_shape'] = self.y.shape
    except AttributeError:
        out['y_shape'] = (len(self.y), self.y[0].shape)
        
    out['start_time'] = start_time 
    out['end_time'] = end_time

    self.details = pd.Series(out) 
    
    from .scan_utils import save_details, save_models, save_weights
    save_details(self)
    save_models(self)
    save_weights(self)


    # handle validation split
    from ..utils.validation_split import validation_split
    self = validation_split(self)

    # set data and len
    self._data_len = len(self.x)

    return self
