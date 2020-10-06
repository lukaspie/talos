def scan_restore(self):
    import os
    import pandas as pd
    import numpy as np

    '''Includes all preparation procedures up until starting the first scan
    through scan_run()'''

         
    data_file = os.path.join(self.experiment_dir, 'test_log.pkl') 
        
    detail_file = os.path.join(self.experiment_dir, 'details.txt') 
    weights_file = os.path.join(self.experiment_dir, 'saved_weights.npy')
    model_file = os.path.join(self.experiment_dir, 'saved_models.txt') 

    self.data = pd.read_pickle(data_file)
    
    self.details = pd.read_csv(detail_file,
                               header = None,
                               squeeze = True,
                               index_col = 0)
        
    self.saved_weights = np.load(weights_file,
                                 allow_pickle = True)
                                     
    self.saved_weights_list = [self.saved_weights[i,:] for i in range(self.saved_weights.shape[0])]
        
    self.saved_models = []
    with open(model_file, 'r') as modelfile:
        for line in modelfile.readlines():
            self.saved_models.append(line[:-1])