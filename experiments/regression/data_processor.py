from fedrec.preprocessor import PreProcessor
from fedrec.utilities import registry
from fedrec.utilities.serialization_utils import serializer_of
from fedrec.serialization.abstract_serializer import AbstractSerializer


@registry.load('preproc', 'regression')
class RegressionPreprocessor(PreProcessor):
    REGISTERED_NAME = 'regression'

    def __init__(
            self,
            dataset_config,
            client_id=0):
        super().__init__(dataset_config, client_id)

@serializer_of(RegressionPreprocessor)
class PreprocSerializer(AbstractSerializer):
    """Serializer for preprocessed data.
    """

    def __init__(self, serialization_strategy):
        super().__init__(serialization_strategy)

    def serialize(self, obj: PreProcessor):
        return {
            "proc_config": {"name": obj.REGISTERED_NAME},
            "client_id": obj.client_id,
            "dataset_config": obj.dataset_config
        }

    def deserialize(self, obj):
        obj = self.serialization_strategy.parse(obj)

        self.model_preproc: PreProcessor = registry.construct(
            "preproc", obj["proc_config"],
            dataset_config=obj["dataset_config"],
            client_id=obj["client_id"])