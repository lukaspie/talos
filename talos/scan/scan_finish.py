def scan_finish(self):
    # add best_model
    from ..scan.scan_addon import func_best_model, func_evaluate

    self.best_model = func_best_model.__get__(self)
    self.evaluate_models = func_evaluate.__get__(self)

    # reset the index
    self.data.index = range(len(self.data))
    
    return self
