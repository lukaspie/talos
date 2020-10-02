def scan_finish(self):

    attrs_final = ['data', 'details', 'x', 'y', 'learning_entropy',
                   'round_times', 'params', 'saved_models', 'saved_weights',
                   'round_history', 'number', 'experiment_dir']

    # final cleanup
    keys = list(self.__dict__.keys())
    for key in keys:
        if key not in attrs_final:
            delattr(self, key)

    # add best_model

    from ..scan.scan_addon import func_best_model, func_evaluate

    self.best_model = func_best_model.__get__(self)
    self.evaluate_models = func_evaluate.__get__(self)

    # reset the index
    self.data.index = range(len(self.data))

    return self
