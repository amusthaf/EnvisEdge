from collections import defaultdict
from typing import Dict, List, Tuple

from defusedxml import NotSupportedError
from fedrec.serialization.serializable_interface import (Serializable,
                                                         is_primitives)

SERIALIZER_MAP = defaultdict(dict)
ACTIVE_SERIALIZERS = defaultdict(dict)


def register_deserializer(class_ref):
    assert issubclass(class_ref, Serializable), (
        NotSupportedError(class_ref))

    cls_type_name = class_ref.type_name()
    if cls_type_name in SERIALIZER_MAP:
        raise LookupError('{} already present'.format(cls_type_name))
    SERIALIZER_MAP[cls_type_name] = class_ref
    return class_ref


def get_deserializer(serialized_obj: Dict):
    if "__type__" not in serialized_obj:
        raise NotSupportedError(serialized_obj)
    type_name = serialized_obj["__type__"]
    if type_name in SERIALIZER_MAP:
        if type_name not in ACTIVE_SERIALIZERS:
            ACTIVE_SERIALIZERS[type_name] = SERIALIZER_MAP[type_name]
    else:
        raise LookupError('{} class not present'.format(type_name))

    return ACTIVE_SERIALIZERS[type_name]


def serialize_attribute(obj):
    if isinstance(obj, Dict):
        return {k: serialize_attribute(v) for k, v in obj.items()}
    elif isinstance(obj, (List, Tuple)):
        return [serialize_attribute(v) for v in obj]
    elif is_primitives(obj):
        return obj
    else:
        assert isinstance(obj, Serializable), "Object must be serializable"
        return obj.serialize()


def deserialize_attribute(obj):
    if "__type__" in obj:
        type_name = obj["__type__"]
        data = obj["__data__"]
        return get_deserializer(type_name).deserialize(data)
    elif isinstance(obj, Dict):
        return {k: deserialize_attribute(v) for k, v in obj.items()}
    elif isinstance(obj, (List, Tuple)):
        return [deserialize_attribute(v) for v in obj]
    else:
        raise ValueError("Object is not serializable")
