import torch


class StateTensorDict():
    def __init__(
            self,
            storage,
            worker_id,
            round_idx,
            state_dict,
            state_type):
        self.worker_id = worker_id
        self.round_idx = round_idx
        self.state = state_dict
        self.storage = storage
        self.state_type = state_type

    def get_state_name(self) -> str:
        return "_".join(
            [str(self.worker_id),
             str(self.round_idx),
             self.state_type])

    def get_state_path(self) -> str:
        return self.storage+"/"+self.get_state_name()+".pt"


