from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from fedrec.utilities.serialization_utils import get_serializer

PRIMITIVES_TYPES = (str, int, float, bool)


def is_primitives(obj):
    if obj is None:
        return True
    else:
        return isinstance(obj, PRIMITIVES_TYPES)


class SerializationStrategy(ABC):

    @abstractmethod
    def parse(self, obj):
        raise NotImplementedError()

    @abstractmethod
    def unparse(self, obj):
        raise NotImplementedError()


class Serializable(ABC):
    """Abstract class for serializers and deserializers.

    Attributes:
    -----------
    serializer: str
        The serializer to use.

    Methods:
    --------
    serialize(obj):
        Serializes an object.
    deserialize(obj):
        Deserializes an object.
    """

    def __init__(self, serialization_strategy) -> None:
        super().__init__()
        self.serialization_strategy = serialization_strategy

    @abstractmethod
    def serialize(self):
        raise NotImplementedError()

    @abstractmethod
    def deserialize(self):
        raise NotImplementedError()

    @classmethod
    def type_name(cls):
        return cls.__name__

    def append_type(self, obj_dict):
        """Generates a dictionary from an object and
         appends type information for finding the appropriate serialiser.

        Parameters:
        -----------
        obj: object
            The object to serialize.

        Returns:
        --------
        dict:
            The dictionary representation of the object.
        """
        return {
            "__type__": self.type_name(),
            "__data__": obj_dict,
        }

    def get_class_serializer(self, obj):
        return get_serializer(obj, self.serialization_strategy)

    def serialize_attribute(self, obj):
        if isinstance(obj, Dict):
            return {k: self.serialize_attribute(v) for k, v in obj.items()}
        elif isinstance(obj, (List, Tuple)):
            return [self.serialise_attribute(v) for v in obj]
        elif is_primitives(obj):
            return obj
        else:
            assert isinstance(obj, Serializable), "Object must be serializable"
            return obj.serialize()

    def deserialize_atttribute(self, obj):
        if isinstance(obj, Dict):
            return {k: self.deserialize_attribute(v) for k, v in obj.items()}
        elif isinstance(obj, (List, Tuple)):
            return [self.deserialize_attribute(v) for v in obj]
        else:
            deserializer = self.get_class_serializer(obj)
            return deserializer.deserialize(obj)
