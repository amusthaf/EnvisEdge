from collections import defaultdict
from typing import Dict

from defusedxml import NotSupportedError

from fedrec.serialization.serializable_interface import Serializable


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
