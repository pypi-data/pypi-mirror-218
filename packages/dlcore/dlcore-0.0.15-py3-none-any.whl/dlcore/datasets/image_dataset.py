import torch
from dataclasses import dataclass
from typing import Tuple, Optional
from .image_data_wrapper import ILabeledImageData, TransformFn


@dataclass
class ImageDataset(torch.utils.data.Dataset):
    """
    A pytorch Dataset that wraps a labeled image data instance and optionally applies a transform function.
    """
    image_data: ILabeledImageData
    transform: Optional[TransformFn] = None

    def __len__(self) -> int:
        """Returns the total number of samples."""
        return len(self.image_data)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Fetches an image-label pair from the dataset.

        Args:
            idx: The index of the item to fetch.

        Returns:
            A tuple where the first element is the image, and the second element is the label.
        """
        image, label = self.image_data.get_by_id(idx)

        if self.transform:
            image = self.transform(image)

        return image, torch.tensor(label)