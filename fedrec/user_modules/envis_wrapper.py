import torch
from fedrec.data_models.torch_module import EnvisModule
from fedrec.utilities.registry import Registrable

Registrable.wrap_to_envis(EnvisModule)(torch.optim.Optimizer)

Registrable.wrap_to_envis(EnvisModule)(torch.nn.Module)

Registrable.wrap_to_envis(EnvisModule)(torch.nn.ModuleDict)
