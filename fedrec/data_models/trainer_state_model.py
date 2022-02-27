import attr
from typing import Dict
from fedrec.data_models.base_actor_state_model import ActorState


@attr.s(kw_only=True)
class TrainerState(ActorState):
    """Construct a workerState object to reinstatiate a worker when needed.

    Attributes
    ----------
    id : int
        Unique worker identifier
    model_preproc : `Preprocessor`
        The local dataset of the worker
    round_idx : int
        The number of local training cycles finished
    state_dict : dict
        A dictionary of state dicts storing model weights and optimizer dicts
    storage : str
        The address for persistent storage
    """
    model_preproc = attr.ib()
    local_sample_number = attr.ib()
    local_training_steps = attr.ib()

    def serialize(self):
        response_dict = {}
        response_dict["id"] = self.id
        response_dict["round_idx"] = self.round_idx
        response_dict["state_dict"] = self.serialize_attribute(
            self.state_dict)
        response_dict["storage"] = self.storage
        response_dict["model_preproc"] = self.serialize_attribute(
            self.model_preproc)
        response_dict["local_sample_number"] = self.local_sample_number
        response_dict["local_training_steps"] = self.local_training_steps

        # return self.serialization_strategy.unparse(response_dict)
        return response_dict

    def deserialize(self, obj: Dict):
        obj = self.serialization_strategy.parse(obj)

        state_dict = self.deserialize_attribute(
            obj['state_dict'])
        model_preproc = self.deserialize_attribute(
            obj['model_preproc'])

        return TrainerState(id=obj["id"],
                            round_idx=obj["round_idx"],
                            state_dict=state_dict,
                            storage=obj["storage"],
                            model_preproc=model_preproc,
                            local_sample_number=obj["local_sample_number"],
                            local_training_steps=obj["local_training_steps"])
