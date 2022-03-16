import torch
from fedrec.data_models.envis_module import EnvisModule

torch.optim.Optimizer = EnvisModule(torch.optim.Optimizer)
torch.nn.Module = EnvisModule(torch.nn.Module)
torch.nn.ModuleDict = EnvisModule(torch.nn.ModuleDict)
