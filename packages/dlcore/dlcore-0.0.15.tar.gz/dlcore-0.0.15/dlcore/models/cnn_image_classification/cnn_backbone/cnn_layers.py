from typing import List, Type
from torch.nn.modules.module import Module
from torch.nn.modules.conv import Conv2d
from torch.nn.modules.batchnorm import BatchNorm2d
from torch.nn.modules.dropout import Dropout
from torch.nn import ReLU, Sequential
import torch


class CompositeLayer(Module):
    def __init__(self, in_channels: int, out_channels: int, activation: Type[ReLU] = ReLU, 
                                dropout_rate: float = 0.0, apply_batch_norm: bool = True):
        super(CompositeLayer, self).__init__()
        
        layers: List[Module] = []
        layers.append(Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1))
        
        if apply_batch_norm:
            layers.append(BatchNorm2d(out_channels))
        
        layers.append(activation())
        
        if dropout_rate > 0.0:
            layers.append(Dropout(p=dropout_rate))
        
        self.composite_layer = Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.composite_layer(x)

def construct_composite_layer(in_channels: int, out_channels: int, activation: Type[ReLU] = ReLU, 
                                dropout_rate: float = 0.0, apply_batch_norm: bool = True):
    return CompositeLayer(in_channels, out_channels, activation, dropout_rate, apply_batch_norm)

