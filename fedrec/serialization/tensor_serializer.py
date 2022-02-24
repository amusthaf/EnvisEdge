import torch
from fedrec.utilities import registry
from fedrec.serialization.abstract_serializer import AbstractSerializer
from fedrec.utilities.io_uitls import load_tensor, save_tensor
from fedrec.utilities.serialization_utils import serializer_of


@serializer_of(torch.Tensor)
class TensorSerializer(AbstractSerializer):
    """
    TensorSerializer serializes and deserializes torch tensors.

    Attributes:
    ----------
    serializer: str
        The serializer to use.
    """

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
            save_tensor(tensor, path)
            return path
        else:
            # create a buffer Bytes object,
            # which can be used to write to the file.
            save_tensor(tensor)
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
  
        tensor = load_tensor(path)
        return tensor
