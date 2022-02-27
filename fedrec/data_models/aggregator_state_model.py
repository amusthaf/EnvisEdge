from typing import Dict, List
import attr
from fedrec.data_models.base_actor_state_model import ActorState
from fedrec.serialization.serializer_registry import deserialize_attribute


@attr.s
class Neighbour:
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
    id = attr.ib()
    model = attr.ib(None)
    sample_num = attr.ib(None)
    last_sync = attr.ib(-1)

    def update(self, kwargs):
        for k, v in kwargs:
            if k == 'id' and v != self.id:
                return
            if hasattr(self, k):
                setattr(self, k, v)


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
        id: int,
        round_idx: int,
        state_dict: Dict,
        storage: str,
        in_neighbours: List[Neighbour],
        out_neighbours: List[Neighbour]
    ) -> None:
        super().__init__(id, round_idx, state_dict, storage)
        self.in_neighbours = in_neighbours
        self.out_neighbours = out_neighbours

    def serialize(self):
        response_dict = {}
        response_dict["id"] = self.id
        response_dict["round_idx"] = self.round_idx
        response_dict["state_dict"] = self.serialize_attribute(
            self.state_dict)
        response_dict["storage"] = self.storage
        response_dict["in_neighbours"] = self.serialize_attribute(
            self.in_neighbours)
        response_dict["out_neighbours"] = self.serialize_attribute(
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
