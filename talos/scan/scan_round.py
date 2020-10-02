def scan_round(self):

    '''The main operational function that manages the experiment
    on the level of execution of each round.'''

    import time
    import datetime
    import pytz
    import gc
    import numpy as np

    # print round params
    if self.print_params is True:
        print(self.round_params)

    # set start time
    round_start = datetime.datetime.now().astimezone(
        pytz.timezone('Europe/Berlin')).strftime("%Y-%m-%d %H:%Mm")

    start = time.time()

    # fit the model
    from ..model.ingest_model import ingest_model
    model_history, round_model = ingest_model(self)

    # handle logging of results
    from ..logging.logging_run import logging_run
    self = logging_run(self, round_start, start, model_history)

    # apply reductions
    from ..reducers.reduce_run import reduce_run
    self = reduce_run(self)

    try:
        # save model and weights
        self.saved_models.append(round_model.to_json())

        if self.save_weights:
            self.saved_weights_list.append(round_model.get_weights())
            self.saved_weights = np.array(self.saved_weights_list)
        else:
            self.saved_weights_list.append(None)
            self.saved_weights = np.array(self.saved_weights_list)

    except AttributeError as e:
        # make sure that the error message is from torch
        if str(e) == "'Model' object has no attribute 'to_json'":
            if self.save_weights:
                self.saved_models.append(self.round_model.state_dict())
            else:
                self.saved_weights.append(None)

    # clear tensorflow sessions
    if self.clear_session is True:

        del self.round_model
        gc.collect()

        # try TF specific and pass for everyone else
        try:
            from tensorflow.keras import backend as K
            K.clear_session()
        except ImportError:
            pass

    return self
