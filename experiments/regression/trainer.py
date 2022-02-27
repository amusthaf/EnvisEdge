from typing import Dict

from fedrec.base_trainer import BaseTrainer, TrainConfig
from fedrec.utilities import registry
from fedrec.utilities.logger import BaseLogger


@registry.load('trainer', 'regression')
class RegressionTrainer(BaseTrainer):

    def __init__(
            self,
            config_dict: Dict,
            logger: BaseLogger,
            client_id=None) -> None:

        super().__init__(config_dict, logger, client_id)
        self.train_config = TrainConfig(
            **config_dict["trainer"]["config"]
        )
