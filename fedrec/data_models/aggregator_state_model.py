from typing import Dict, List

from fedrec.data_models.base_actor_state_model import ActorState
from fedrec.serialization.serializable_interface import Serializable
from fedrec.serialization.serializer_registry import (deserialize_attribute,
                                                      serialize_attribute)
from fedrec.utilities.logger import BaseLogger
from fedrec.utilities.registry import Registrable


class Neighbour(Serializable):
    """A class that represents a new Neighbour instance.

    Attributes
    ----------
    id : int
        Unique identifier for the worker
    model : Dict
        Model weights of the worker
    sample_num : int
        Number of datapoints in the neighbour's local dataset
    last_sync : int
        Last cycle when the models were synced
    """

    def __init__(
        self,
        id,
        model,
        sample_num,
        last_sync=0
    ) -> None:
        self.id = id
        self.model = model
        self.sample_num = sample_num
        self.last_sync = last_sync

    def update(self, kwargs):
        for k, v in kwargs:
            if k == 'id' and v != self.id:
                return
            if hasattr(self, k):
                setattr(self, k, v)

    def serialize(self):
        response_dict = {}
        response_dict["id"] = self.id
        response_dict["last_sync"] = self.last_sync
        response_dict["model"] = serialize_attribute(self.model)
        response_dict["sample_num"] = self.sample_num
        return self.append_type(response_dict)

    @classmethod
    def deserialize(cls, obj: Dict):
        id = obj["id"]
        last_sync = obj["last_sync"]
        model = deserialize_attribute(obj["model"])
        sample_num = obj["sample_num"]

        return cls(
            id=id,
            last_sync=last_sync,
            model=model,
            sample_num=sample_num,
        )


@ Registrable.register_class_ref
class AggregatorState(ActorState):
    """Construct a AggregatorState object to reinstatiate a worker when needed.

    Attributes
    ----------
    id : int
        Unique worker identifier
    round_idx : int
        The number of local training cycles finished
    state_dict : dict
        A dictionary of state dicts storing model weights and optimizer dicts
    storage : str
        The address for persistent storage
    neighbours :
        {"in_neigh" : List[`Neighbour`], "out_neigh" : List[`Neighbour`]]
        The states of in_neighbours and out_neighbours of the
        worker when last synced
    """

    def __init__(
        self,
        worker_index: int,
        config: Dict,
        logger: BaseLogger,
        state_dict: Dict,
        storage: str,
        in_neighbours: List[Neighbour],
        out_neighbours: List[Neighbour],
        round_idx: int = 0,
        is_mobile: bool = True,
    ) -> None:
        super().__init__(worker_index, config, logger,
                         is_mobile, round_idx, storage=storage)
        self.in_neighbours = in_neighbours
        self.out_neighbours = out_neighbours
        self.state_dict = state_dict

    def serialize(self):
        response_dict = {}
        response_dict["id"] = self.id
        response_dict["round_idx"] = self.round_idx
        response_dict["state_dict"] = serialize_attribute(
            self.state_dict)
        response_dict["storage"] = self.storage
        response_dict["in_neighbours"] = serialize_attribute(
            self.in_neighbours)
        response_dict["out_neighbours"] = serialize_attribute(
            self.out_neighbours)
        return self.append_type(response_dict)
        # return self.serialization_strategy.unparse(response_dict)

    @classmethod
    def deserialize(cls, obj: Dict):
        state_dict = deserialize_attribute(
            obj['state_dict'])
        in_neighbours = deserialize_attribute(
            obj['in_neighbours'])
        out_neighbours = deserialize_attribute(
            obj['out_neighbours'])

        return cls(
            id=obj['id'],
            round_idx=obj['round_idx'],
            state_dict=state_dict,
            storage=obj['storage'],
            in_neighbours=in_neighbours,
            out_neighbours=out_neighbours
        )
