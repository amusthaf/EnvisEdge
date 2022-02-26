from abc import ABC, abstractmethod


class PreProcessor(ABC):
    def __init__(self, client_id=None) -> None:
        super().__init__()
        self.client_id = client_id

    def preprocess_data(self):
        pass

    @abstractmethod
    def load(self):
        pass

    def load_data_description(self):
        pass

    @abstractmethod
    def datasets(self, *splits):
        pass

    @abstractmethod
    def dataset(self, split):
        pass
