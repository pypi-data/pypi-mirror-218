from pathlib import Path
from dataclasses import dataclass


@dataclass
class Paths:
    log: Path
    data: Path
    parquet: Path
    images: Path
    h5: Path
    
    def __init__(self, log: str, data: str, parquet: str, images: str, h5: str):
        self.log: Path = Path(log)
        self.data: Path = Path(data)    
        self.parquet: Path = Path(parquet)
        self.images: Path = Path(images)
        self.h5: Path = Path(h5)
        self.log.mkdir(parents=True, exist_ok=True)
        self.data.mkdir(parents=True, exist_ok=True)
        self.parquet.mkdir(parents=True, exist_ok=True)
        self.images.mkdir(parents=True, exist_ok=True)
        self.h5.mkdir(parents=True, exist_ok=True)

@dataclass
class Files:
    train_data: str
    train_labels: str
    test_data: str
    test_labels: str
    valid_data: str
    valid_labels: str
    data: str
    labels: str


@dataclass
class ModelParams:
    epoch_count: int
    lr: float

@dataclass
class DatasetParams:
    image_size: tuple[int, int]
    batch_size: int
    shuffle: bool
    

@dataclass
class AppConfig:
    paths: Paths
    files: Files
    params: ModelParams
    dataset: DatasetParams