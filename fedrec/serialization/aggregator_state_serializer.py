from typing import Dict

from fedrec.serialization.abstract_serializer import AbstractSerializer
from fedrec.data_models.aggregator_state_model import AggregatorState
from fedrec.utilities.serialization_utils import serializer_of

@serializer_of(AggregatorState)
class AggregatorStateSerializer(AbstractSerializer):

    def __init__(self, serialization_strategy):
        super().__init__(serialization_strategy)

 