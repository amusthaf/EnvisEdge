from grpc import server
import torch
from fedrec.data_models.envis_module import EnvisModule
from fedrec.serialization.serializable_interface import Serializable

from typing import Any, Dict
from fedrec.data_models.tensors_model import EnvisTensors
from fedrec.serialization.serializable_interface import Serializable
from fedrec.utilities.registry import Registrable
from fedrec.serialization.serializer_registry import (deserialize_attribute,
                                                      serialize_attribute)


torch.optim.Optimizer
torch.nn.Module
torch.nn.ModuleDict


def create_serializer_hooks(class_ref):

    def serialize(self):
        # TODO decide how to fill storage from config
        response_dict = {}
        response_dict["class_ref_name"] = serialize_attribute(
            self.get_name(class_ref))
        response_dict["state"] = serialize_attribute(self._envis_state)
        return self.append_type(response_dict)

    def deserialize(cls, obj: Dict):
        state = deserialize_attribute(obj["state"])
        class_ref = obj["class_ref_name"]
        return cls(class_ref_name=class_ref, state=state)

    setattr(class_ref, name="serialize", attr=serialize)
    setattr(class_ref, name="deserialize", attr=deserialize)


def create_envis_state_hooks(class_ref):
    
    def envis_state(self: Any):
        if self._envis_state is None:
            self._envis_state = EnvisTensors(
                storage="storage",
                tensors=self.state_dict(),
                tensor_type="user_module"
            )
        return self._envis_state

    def load_envis_state(self, state: Dict):
        self.load_state_dict(state)

    setattr(class_ref, name="envis_state", attr=envis_state)
    setattr(class_ref, name="load_envis_state", attr=load_envis_state)


def add_envis_hooks(class_ref):
    setattr(class_ref, name="_envis_state", attr=None)
    Registrable.register_class_ref(
        class_ref, class_ref.get_name(class_ref))
