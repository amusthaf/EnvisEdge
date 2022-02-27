from fedrec.serialization.abstract_serializer import Serializable
from fedrec.utilities.io_uitls import load_tensors, save_tensors


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

    @classmethod
    def serialize(cls, tensor, path=None):
        """
        Serializes a tensor object.

        Parameters:
        -----------
        obj: object
            The object to serialize.
        file: file
            The file to write to.

        Returns:
        --------
        pkl_str: io.BytesIO
            The serialized object.

        """
        if path:
            # if file is provided, save the tensor
            # to the file and return the file path.
            save_tensors(tensor, path)
            return path
        else:
            # create a buffer Bytes object,
            # which can be used to write to the file.
            save_tensors(tensor)
            return path

    @classmethod
    def deserialize(cls, path):
        """
        Deserializes a tensor object.

        Parameters:
        -----------
        obj: object
            The object to deserialize.

        Returns:
        --------
        deserialized_obj: object
            The deserialized object.
        """

        tensor = load_tensors(path)
        return tensor
