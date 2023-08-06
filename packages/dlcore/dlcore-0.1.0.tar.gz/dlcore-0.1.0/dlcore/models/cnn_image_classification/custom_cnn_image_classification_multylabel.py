from ..neural_network.custom_nn import CustomNN
from .cnn_backbone import CNNBackBoneType
from .custom_cnn_image_classification import CNNImageClassification
from typing import Union, List, Dict
import torch
from torch.nn import ModuleList


class CNNImageClassificationMultyLabel(CNNImageClassification):

    def __init__(self,
                 backbone_type: Union[CNNBackBoneType.DenseNet,
                                      CNNBackBoneType.ResNet,
                                      CNNBackBoneType.ViT],
                 classes_names: List[str],
                 num_hidden_layers: int = 2,
                 backbone_out_size: int = 500,
                 pretrained_weights: bool = True,
                 in_channels: int=3):
        super().__init__(
            backbone_type=backbone_type,
            num_classes=backbone_out_size,
            pretrained_weights=pretrained_weights,
            in_channels=in_channels,
            num_hidden_layers=num_hidden_layers
        )
        
        self.classes_names = classes_names
        
        
        # TODO: add params for: out_size, num_hidden_layers
        self.classes_ff_models = ModuleList([
            CustomNN(input_size=backbone_out_size, output_size=1, num_hidden_layers=0) for _ in self.classes_names
        ])


    def forward(self, inputs: torch.Tensor) -> Dict[str, torch.TensorType]:
        
        
        inputs = super().forward(inputs)
        predictions: Dict[str, torch.TensorType] = {}

        for class_name, class_ff_model in zip(self.classes_names, self.classes_ff_models):
            predictions[class_name] = class_ff_model(inputs)

        return predictions
