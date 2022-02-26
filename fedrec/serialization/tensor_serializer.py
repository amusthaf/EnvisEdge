from fedrec.data_models.state_tensors_model import StateTensors
from fedrec.serialization.abstract_serializer import AbstractSerializer
from fedrec.utilities.io_uitls import load_tensors, save_tensors
from fedrec.utilities.serialization_utils import serializer_of


@serializer_of(StateTensors)
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
