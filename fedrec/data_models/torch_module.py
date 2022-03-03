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
        input_obj) -> None:
        super().__init__()
        if "state_dict" in dir(input_obj):
            raise NotImplementedError(
                "EnvisModule needs \"state_dict\" method to be implemented")

        if "load_state_dict" in dir(input_obj):
            raise NotImplementedError(
                "EnvisModule needs \"load_state_dict\" method to be implemented")
        self.original_reference = input_obj


    def serialize(self):
        #TODO decide how to fill storage from config 
        response_dict = {}
        state_dict = EnvisTensors(
            storage="storage",
            tensors=self.original_reference.state_dict(),
            tensor_type="user_module"
        )

        response_dict["input_ref"] = serialize_attribute(state_dict)
        return self.append_type(response_dict)

    @classmethod
    def deserialize(cls, obj: Dict):
        storage = # TODO: fill storage from config
        tensor = deserialize_attribute(obj["tensor"])
        tensor_type = obj["tensor_type"]
        return cls(storage, tensor, tensor_type)