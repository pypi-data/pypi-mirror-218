import torch
import torch.nn as nn
from typing import Optional, Any, List

class CustomNN(nn.Module):
    def __init__(self, 
                 input_size: int, 
                 output_size: int, 
                 num_hidden_layers: int=1, 
                 activation: Optional[Any]=nn.ReLU, 
                 dropout: Optional[float]=None, 
                 batch_norm: Optional[bool]=False):
        super(CustomNN, self).__init__()

        def _make_hidden_layer(in_features: int, out_features: int) -> List[Any]:
            layer: List[Any] = [nn.Linear(in_features, out_features)]
            if batch_norm:
                layer.append(nn.BatchNorm1d(num_features=out_features))
            if activation:
                layer.append(activation())
            if dropout:
                layer.append(nn.Dropout(p=dropout))
            return layer

        layers: List[Any] = []
        in_features = input_size
        for i in range(num_hidden_layers):
            in_features = input_size if i == 0 else int(in_features / 2) 
            layers.extend(_make_hidden_layer(in_features, int(in_features/2)))

        if num_hidden_layers > 0:
            in_features = int(in_features/2)
        layer: List[Any] = [nn.Linear(in_features, output_size)]
        
        if output_size > 1 and output_size < 100:
            layer.append(nn.Softmax(-1))
        elif output_size == 1:
            layer.append(nn.Sigmoid())
            
        layers.extend(layer)
        self.model = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)
