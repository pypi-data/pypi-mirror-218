from enum import Enum
from typing import Union, List
import torch
import torchvision.models as models
from torchvision.models import vision_transformer
from dataclasses import dataclass
import torch.nn as nn

class DenseNet(Enum):
    densenet121 = "DenseNet121_Weights"
    densenet161 = "DenseNet161_Weights"
    densenet169 = "DenseNet169_Weights"
    densenet201 = "DenseNet201_Weights"

class ResNet(Enum):
    resnet18 = "ResNet18_Weights"
    resnet34 = "ResNet34_Weights"
    resnet50 = "ResNet50_Weights"
    resnet101 = "ResNet101_Weights"
    resnet152 = "ResNet152_Weights"
    resnext50_32x4d = "ResNeXt50_32X4D_Weights"
    resnext101_32x8d = "ResNeXt101_32X8D_Weights"
    resnext101_64x4d = "ResNeXt101_64X4D_Weights"
    wide_resnet50_2 = "Wide_ResNet50_2_Weights"
    wide_resnet101_2 = "Wide_ResNet101_2_Weights"
    
    
class ViT(Enum):
    
    vit_b_16 = "vit_b_16"
    vit_b_32 = "vit_b_32"
    vit_l_16 = "vit_l_16"
    vit_l_32 = "vit_l_32"
    vit_h_14 = "vit_h_14"
    
@dataclass 
class CNNBackBoneType:
    DenseNet = DenseNet
    ResNet = ResNet
    ViT = ViT

class BuildBackBone:
    
    layer_names: List[str] = ["fc", "classifier", "last_linear", "heads"]
    
    @staticmethod
    def get_model(
            architecture: Union[DenseNet, ResNet, ViT], 
            pretrained_weights: bool) -> torch.nn.Module:

        if architecture in ViT:
            if pretrained_weights:
                selected_model = vision_transformer.__dict__[architecture.value](weights=True)
            else:
                selected_model = vision_transformer.__dict__[architecture.value](weights=False)
            
        elif pretrained_weights:
            weights = models.__dict__[architecture.value].DEFAULT
            selected_model = models.__dict__[architecture.name](weights=weights)
        else:
            selected_model = models.__dict__[architecture.name]()
        
        return selected_model
    
    @staticmethod
    def get_last_layer_name(model: torch.nn.Module) -> str:
        for layer_name in BuildBackBone.layer_names:
            if model._modules.get(layer_name, None):
                return layer_name
    @staticmethod
    def get_last_layer(model: torch.nn.Module) -> torch.nn.Linear:
        for layer_name in BuildBackBone.layer_names:
                if model._modules.get(layer_name, None):
                    return model._modules.get(layer_name)
                
    @staticmethod
    def get_last_in_features(model: torch.nn.Module) -> int:
        if isinstance(BuildBackBone.get_last_layer(model), nn.Sequential):
            return BuildBackBone.get_last_layer(model).head.in_features
        return BuildBackBone.get_last_layer(model).in_features


if __name__ == "__main__":  
    
    architecture = CNNBackBoneType.ResNet.resnet18
    selected_model = BuildBackBone.get_model(architecture, pretrained_weights=True)
    
    last_layer = BuildBackBone.get_last_layer(model=selected_model)
    
    print(last_layer)