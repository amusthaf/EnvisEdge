import os
import random
from typing import Dict
from fedrec.data_models.tensors_model import EnvisTensors
from fedrec.serialization.serializable_interface import Serializable
from fedrec.utilities.registry import Registrable
from fedrec.serialization.serializer_registry import (deserialize_attribute,
                                                      serialize_attribute)

@Registrable.register_class_ref
class EnvisModule(Serializable):
    def __init__(
        self,
        state: Dict = None,
        class_ref_name: str=None, 
        input_obj=None) -> None:
        super().__init__()

        if (class_ref_name is None) and (input_obj is None):
            raise ValueError("Either class_ref_name or input_obj must be provided")

        if "state_dict" in dir(input_obj):
            raise NotImplementedError(
                "EnvisModule needs \"state_dict\" method to be implemented")

        if "load_state_dict" in dir(input_obj):
            raise NotImplementedError(
                "EnvisModule needs \"load_state_dict\" method to be implemented")
        self.original_reference = input_obj
        self.class_ref_name = class_ref_name
        self._state = state
        if class_ref_name is not None:
            self.class_ref_name = class_ref_name
        elif input_obj is not None:
            self.class_ref_name = input_obj.__class__.__name__

    @property
    def state(self):
        if self._state is None:
            self._state = EnvisTensors(
            storage="storage",
            tensors=self.original_reference.state_dict(),
            tensor_type="user_module"
        )
        return self._state

    def serialize(self):
        #TODO decide how to fill storage from config 
        response_dict = {}
        response_dict["class_ref"] = serialize_attribute(self.class_ref_name)
        response_dict["state"] = serialize_attribute(self.state)
        return self.append_type(response_dict)

    @classmethod
    def deserialize(cls, obj: Dict):
        state = deserialize_attribute(obj["state"])
        class_ref = obj["class_ref"]
        return cls(class_ref_name=class_ref, state=state)