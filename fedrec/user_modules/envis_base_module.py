from fedrec.serialization.serializable_interface import Serializable
from fedrec.serialization.serializer_registry import deserialize_attribute, serialize_attribute
from fedrec.utilities.registry import Registrable


@Registrable.register_class_ref
class EnvisBase(Serializable):
    """
    Base class for Envis.
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.update(**kwargs)

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def serialize(self):
        return self.append_type({
            k: serialize_attribute(v) for k, v in self.__dict__.items()
        })

    @classmethod
    def deserialize(cls, obj):
        deserialized_output = {
            k: deserialize_attribute(v) for k, v in obj.items()
        }
        return cls(**deserialized_output)
