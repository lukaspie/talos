def initialize_log(self):
    import os

    # create the experiment folder (unless one is already there)
    path = os.path.join(os.getcwd(), 'param_tests')
    self.experiment_dir = os.path.join(path,
                                       self.experiment_name)
    try:
        os.mkdir(self.experiment_dir)
    except FileExistsError:
        pass
    
    _csv_filename  = 'test_log.csv'
    self._experiment_log_csv = os.path.join(self.experiment_dir,
                                            _csv_filename)
    _pkl_filename  = 'test_log.pkl'
    self._experiment_log_pkl = os.path.join(self.experiment_dir,
                                            _pkl_filename)
    
    with open(self._experiment_log_csv, 'w') as f:
        f.write('') 
    
    with open(self._experiment_log_pkl, 'w') as f:
        f.write('') 
        
    return self._experiment_log_csv, self._experiment_log_pkl