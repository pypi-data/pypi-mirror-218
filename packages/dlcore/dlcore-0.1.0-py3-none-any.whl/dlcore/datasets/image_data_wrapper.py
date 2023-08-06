from typing import List, Tuple, Callable
from PIL import Image
from abc import ABC, abstractmethod
from pathlib import Path
import torch

TransformFn = Callable[[Image.Image], torch.Tensor]


class ILabeledImageData(ABC):
    """Abstract base class for labeled image data."""
    
    @abstractmethod
    def __len__(self) -> int:
        """Returns the number of items in the dataset."""
        pass

    @abstractmethod
    def get_by_id(self, idx: int) -> Tuple[Image.Image, int]:
        """Given an index, returns the corresponding image and label."""
        pass


class LabeledImagePathData(ILabeledImageData):
    """Implementation of ILabeledImageData, using file paths and integer labels."""

    def __init__(self, image_sources: List[Path], labels: List[int]):
        """
        Constructs a new LabeledImagePathData instance.

        Args:
            image_sources: A list of file paths to images.
            labels: A list of corresponding labels.
        """
        self.image_sources = image_sources
        self.labels = labels

    def __len__(self) -> int:
        """See ILabeledImageData.__len__"""
        return len(self.image_sources)

    def get_by_id(self, idx: int) -> Tuple[Image.Image, int]:
        """See ILabeledImageData.get_by_id"""
        image_source = Image.open(self.image_sources[idx])
        return image_source, self.labels[idx]