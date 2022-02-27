import torch
from fedrec.serialization.abstract_serializer import Serializable
from fedrec.utilities import registry


class PreProcessor(Serializable):
    def __init__(
            self,
            dataset_config,
            client_id=None) -> None:
        super().__init__()
        self.client_id = client_id
        self.dataset_config = dataset_config

        self.dataset_processor = registry.construct(
            'dataset', self.dataset_config,
            unused_keys=())

    def preprocess_data(self):
        self.dataset_processor.process_data()

    def load(self):
        self.dataset_processor.load(self.client_id)

    def load_data_description(self):
        pass

    def datasets(self, *splits):
        assert all([isinstance(split, str) for split in splits])
        return {
            split: self.dataset_processor.dataset(split)
            for split in splits
        }

    def dataset(self, split):
        assert isinstance(split, str)
        return self.dataset_processor.dataset(split)

    def data_loader(self, data, **kwargs):
        return torch.utils.data.DataLoader(
            data, **kwargs
        )

    def serialize(self):
        output = {
            "proc_config": {"name": self.REGISTERED_NAME},
            "client_id": self.client_id,
            "dataset_config": self.dataset_config
        }
        # return self.serialization_strategy.unparse(output)
        return output

    def deserialize(self, obj):
        obj = self.serialization_strategy.parse(obj)

        self.model_preproc: PreProcessor = registry.construct(
            "preproc", obj["proc_config"],
            dataset_config=obj["dataset_config"],
            client_id=obj["client_id"])
