class Restore:

    '''Restores the scan_object that had been stored locally as a result
    of talos.Deploy(scan_object, 'example')

    USE:

    diabetes = ta.Scan(x, y, p, input_model)
    ta.Deploy(diabetes.scan_dir)
    ta.Restore(diabetes.scan_dir)

    '''

    def __init__(self, scan_dir):
        import os
        import pandas as pd
        import numpy as np
        
        data_file = os.path.join(scan_dir, 'test_log.pkl') 
        
        detail_file = os.path.join(scan_dir, 'details.txt') 
        params_file = os.path.join(scan_dir, 'params.npy')
        weights_file = os.path.join(scan_dir, 'saved_weights.npy')
        model_file = os.path.join(scan_dir, 'saved_models.txt') 

        self.data = pd.read_pickle(data_file)
        
        self.details = pd.read_csv(detail_file, 
                                    header = None, 
                                    squeeze = True, 
                                    index_col = 0)
        
        # add params dictionary
        self.params = np.load(params_file,
                              allow_pickle = True).item()
        
        self.saved_weights = np.load(weights_file,
                                     allow_pickle = True)
        
        self.saved_models = []
        with open(model_file, 'r') as modelfile:
            for line in modelfile.readlines():
                self.saved_models.append(line[:-1])