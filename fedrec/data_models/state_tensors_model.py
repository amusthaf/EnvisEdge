from fedrec.utilities.serialization_utils import Serializable

class StateTensors(Serializable):
    def __init__(
            self,
            storage,
            worker_id,
            round_idx,
            tensors,
            tensor_type):
        self.worker_id = worker_id
        self.round_idx = round_idx
        self.torch_obj = tensors
        self.storage = storage
        self.tensor_type = tensor_type

    def get_name(self) -> str:
        return "_".join(
            [str(self.worker_id),
             str(self.round_idx),
             self.tensor_type])

    def get_path(self) -> str:
        return str(self.storage)+"/"+str(self.get_name())+".pt"

    def get_torch_obj(self):
        return self.torch_obj


