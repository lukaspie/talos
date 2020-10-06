def run_round_results(self, out):

    '''Called from logging/logging_run.py

    THE MAIN FUNCTION FOR CREATING RESULTS FOR EACH ROUNDself.
    Takes in the history object from model.fit() and handles it.

    NOTE: The epoch level data will be dropped here each round.

    '''
    round_result_out = {}

    round_result_out['round_epochs'] = len(list(out.history.values())[0])

    # record the last epoch result
    for result_key in out.history.keys():
        round_result_out[result_key] = out.history[result_key][-1]

    # record the round hyper-parameters
    for param_key in self.round_params.keys():
        round_result_out[param_key] = self.round_params[param_key]
        
    return round_result_out


def save_result(self):
    
    '''SAVES THE RESULTS/PARAMETERS TO A CSV SPECIFIC TO THE EXPERIMENT'''
    
    self.data.to_csv(self._experiment_log_csv)
    self.data.to_pickle(self._experiment_log_pkl)
    
def result_todf(self):

    '''ADDS A DATAFRAME VERSION OF THE RESULTS TO THE CLASS OBJECT'''

    import pandas as pd

    # create dataframe for results
    cols = self.result[0]
    self.result = pd.DataFrame(self.result[1:])
    self.result.columns = cols

    return self


def peak_epochs_todf(self):

    import pandas as pd

    return pd.DataFrame(self.peak_epochs, columns=self.peak_epochs[0]).drop(0)
