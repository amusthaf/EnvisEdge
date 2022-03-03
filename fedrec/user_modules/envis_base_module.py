from typing import Dict
from fedrec.utilities.random_state import Reproducible
import torch
from fedrec.serialization.serializable_interface import is_primitives

class EnvisBase(Reproducible):
    """
    Base class for Envis.
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.update(**kwargs)
        self._storables = None 

    @property
    def state(self):
        # check if self._storables is None
        # if yes, then add all the attributes of the object
        # to the dict.
        if self._storables is None:
            for key, value in self.__dict__.items():
                if isinstance(value, torch.optim.optimizer):
                    self._storables[key] = value
                elif isinstance(value, torch.nn.Module):
                    self._storables[key] = value
                elif isinstance(value, torch.nn.ModuleDict):
                    self._storables[key] = value
                elif is_primitives(value):
                    self._storables[key] = value
                else:
                    print("not able to store the type"
                    + "Please store one of the following types:"
                    + "torch.optim.optimizer, torch.nn.Module, "
                    + "torch.nn.ModuleDict, primitives")
        return self._storables

    def store(self, state: Dict):
        # self._storables will maintain dict
        # all class objects that user wants to store
        # and resuse.
        self._storables = state

    def update(self, state : Dict):
        self._storables = state
        for k, v in state.items():
            v.load_state_dict(state[k])

    def _attach_envis_wrapper(self, obj):
        # TODO: implement wapper function
        pass
