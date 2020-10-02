class Deploy:

    '''Functionality for deploying a model to a filename'''

    def __init__(self, scan_object):

        '''Deploy a model to be used later or in a different system.

        NOTE: for a metric that is to be minimized, set asc=True or otherwise
        you will end up with the model that has the highest loss.

        Deploy() takes in the object from Scan() and creates a package locally
        that can be later activated with Restore().

        scan_object : object
            The object that is returned from Scan() upon completion.
        '''

        import os
        
        self.scan_object = scan_object
        scan_dir = self.scan_object.experiment_dir

        detail_file = os.path.join(scan_dir, 'details.txt') 
        params_file = os.path.join(scan_dir, 'params')
        weights_file = os.path.join(scan_dir, 'saved_weights')
        model_file = os.path.join(scan_dir, 'saved_models.txt') 

        # runtime
        self.save_details(detail_file)
        self.save_params(params_file)
        self.save_weights(weights_file)
        self.save_models(model_file)

    def save_details(self, detail_file):
        self.scan_object.details.to_csv(detail_file)
        
    def save_params(self, params_file):
        import numpy as np
        np.save(params_file, self.scan_object.params)
        
    def save_models(self, model_file):
        with open(model_file, 'w') as modelfile:
            for listitem in self.scan_object.saved_models:
                modelfile.write('%s\n' % listitem)
    
    def save_weights(self, weights_file):
        import numpy as np
        np.save(weights_file, self.scan_object.saved_weights)