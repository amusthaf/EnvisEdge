from fedrec.preprocessor import PreProcessor
from fedrec.utilities import registry


@registry.load('preproc', 'regression')
class RegressionPreprocessor(PreProcessor):
    REGISTERED_NAME = 'regression'

    def __init__(
            self,
            dataset_config,
            client_id=0):
        super().__init__(dataset_config, client_id)