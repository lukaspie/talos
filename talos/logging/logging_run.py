def logging_run(self, round_start, start, model_history):
    import time
    import datetime
    import pytz
    import pandas as pd

    # count the duration of the round
    round_duration = time.time() - start

    # set end time and log
    round_end = datetime.datetime.now().astimezone(
        pytz.timezone('Europe/Berlin')).strftime("%Y-%m-%d %H:%Mm")
    
    round_times = {'start' : round_start,
                  'end' : round_end,
                  'duration' : round_duration}
    round_times = pd.Series(round_times)
    
    # handle first round only things
    if self.first_round:

        # capture the history keys for later
        self._all_kys = list(model_history.history.keys())
        self._metric_keys = [k for k in self._all_keys if 'val_' not in k]
        self._val_keys = [k for k in self._all_keys if 'val_' in k]
        self._round_keys = ['round_epochs',
                            'start',
                            'end',
                            'duration',
                            'entropy']

        # create a header column for output
        _results_header = self._round_keys + self._all_keys + \
            self._param_dict_keys 
        self.data.columns = _results_header
        
        # save the results
        from .results import save_result
        save_result(self)

        # avoid doing this again
        self.first_round = False

    # create log and other stats
    from ..metrics.entropy import epoch_entropy
    
    epoch_entropy = {'epoch_entropy' : epoch_entropy(self,
                                                     model_history.history)}
    epoch_entropy = pd.Series(epoch_entropy)

    # get round results to the results table and save it
    from .results import run_round_results    
    round_results = pd.Series(run_round_results(self, model_history))

    round_results.append(epoch_entropy)
    round_results.append(round_times)
    
    self.data.append(round_results)
    
    from .results import save_result
    save_result(self)
    
    self.details['end_time'] = round_end

    # return the Scan() self
    return self
