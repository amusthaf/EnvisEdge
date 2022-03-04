from typing import Dict
from fedrec.utilities.random_state import Reproducible
from fedrec.serialization.serializable_interface import is_primitives
from fedrec.utilities.registry import Registrable


class EnvisBase(Reproducible):
    """
    Base class for Envis.
    """

    def __init__(self, rand_config: Dict):
        super().__init__(rand_config)
        self._storables = None

    @property
    def state(self):
        # check if self._storables is None
        # if yes, then add all the attributes of the object
        # to the dict.
        if self._storables is None:
            self._storables = {}
            for k, v in self.__dict__.items():
                if Registrable.is_wrapped(v):
                    # TODO make it a recursive state search
                    self._storables[k] = Registrable.construct_wrapper(
                        v.__class__, input_obj=v
                    )
                elif is_primitives(v):
                    self._storables[k] = v
                else:
                    print("not able to store the type {}".format(type(v))
                          + "Please store one of the following types:"
                          + "torch.optim.optimizer, torch.nn.Module, "
                          + "torch.nn.ModuleDict, primitives")

        return self._storables

    def store(self, state: Dict):
        # self._storables will maintain dict
        # all class objects that user wants to store
        # and resuse.
        self._storables = state

    def update(self, state: Dict):
        self._storables = state
        for k, v in state.items():
            if Registrable.is_wrapped(v):
                self.__dict__[k].load_state_dict(v.state.get_torch_obj())
            elif is_primitives(v):
                self.__dict__[k] = v
            else:
                raise ValueError("Unable to update EnvisBase")
