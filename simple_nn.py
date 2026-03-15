# Acts as a tiny PyTorch scratchpad that seeds a generator and prints sample random values.

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

x = torch.Generator().manual_seed(786)
p = torch.rand(4, generator=x)
print(p)
