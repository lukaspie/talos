from ..utils.validation_split import validation_split
from ..utils.detector import prediction_type
from ..parameters.ParamGrid import ParamGrid
from ..utils.pred_class import classify
from ..utils.last_neuron import last_neuron
from ..utils.logging import debug_logging


TRAIN_VAL_RUNTIME_ERROR_MSG = """
If x_val or y_val is inputted, then the other must be inputted as well.
"""


def scan_prepare(self):

    '''Includes all preparation procedures up until starting the first scan
    through scan_run()'''

    # based on the 'debug' Scan() paramater
    self = debug_logging(self)

    # create the name for the experiment
    self.experiment_name = self.dataset_name + '_' + self.experiment_no

    # for the case where x_val or y_val is missing when other is present
    self.custom_val_split = False
    if (self.x_val is not None and self.y_val is None) or \
       (self.x_val is None and self.y_val is not None):
        raise RuntimeError(TRAIN_VAL_RUNTIME_ERROR_MSG)

    elif (self.x_val is not None and self.y_val is not None):
        self.custom_val_split = True

    # create the paramater object and move to self
    self.paramgrid_object = ParamGrid(self)
    self.param_log = self.paramgrid_object.param_log
    self.param_grid = self.paramgrid_object.param_grid
    del self.paramgrid_object

    # creates a reference dictionary for column number to label
    self.param_reference = {}
    for i, col in enumerate(self.params.keys()):
        self.param_reference[col] = i

    self.round_counter = 0
    self.peak_epochs = []
    self.epoch_entropy = []
    self.round_models = []

    # create the data asset
    self.y_max = self.y.max()
    self = validation_split(self)
    self.shape = classify(self.y)
    self.last_neuron = last_neuron(self)

    self._data_len = len(self.x)
    self = prediction_type(self)
    self.result = []

    return self
