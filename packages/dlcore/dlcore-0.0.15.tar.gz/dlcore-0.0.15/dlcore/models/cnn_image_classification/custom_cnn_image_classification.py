from torch.nn import Module, Sequential
from ..neural_network.custom_nn import CustomNN
from .cnn_backbone import BuildBackBone, CNNBackBoneType
from .cnn_backbone.cnn_layers import construct_composite_layer

from typing import Union
import torch
from pathlib import Path


class CNNImageClassification(Module):

    def __init__(self,
                 backbone_type: Union[CNNBackBoneType.DenseNet,
                                      CNNBackBoneType.ResNet,
                                      CNNBackBoneType.ViT],
                 num_classes: int,
                 num_hidden_layers: int = 2,
                 pretrained_weights: bool = True,
                 in_channels: int=3):
        super(CNNImageClassification, self).__init__()

        self.backbone_type = backbone_type
        self.num_hidden_layers = num_hidden_layers
        self.num_classes = num_classes
        self.in_channels = in_channels
        
        # Get Back Bone NN
        bb_model = BuildBackBone.get_model(backbone_type, pretrained_weights)
        bb_layer_name = BuildBackBone.get_last_layer_name(bb_model)
        bb_last_in_features = BuildBackBone.get_last_in_features(bb_model)
        
        if in_channels != 3:
            self.composite_layer = construct_composite_layer(in_channels=in_channels, out_channels=3)

        # Add Custion NN
        custom_nn = CustomNN(input_size=bb_last_in_features,
                             output_size=num_classes, num_hidden_layers=num_hidden_layers)

        setattr(bb_model, bb_layer_name, custom_nn)

        self.model = bb_model

    def forward(self, inputs: torch.Tensor):
        if self.in_channels != 3:
            inputs = self.composite_layer(inputs)
        return self.model(inputs)

    def save_model(self, path: Path) -> None:
        """
        Save the model to the specified path.
        """
        torch.save(self.model.state_dict(), path)
        print(f"Model saved at {path}")

    def load_model(self, path: Path) -> None:
        """
        Load a model from the specified path.
        """
        self.model.load_state_dict(torch.load(path))
        print(f"Model loaded from {path}")

    @property
    def model_name(self):

        return f'{self.backbone_type}_cnn_h_{self.num_hidden_layers}_num_classes_{self.num_classes}'
