import os
import torch
from torch import nn
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from tqdm import tqdm
from pathlib import Path
from typing import List
import numpy as np


class CustomNNTrainer:
    def __init__(
        self,
        model: nn.Module,
        optimizer: torch.optim.Optimizer,
        criterion: nn.Module,
        train_dataloader: DataLoader,
        valid_dataloader: DataLoader,
        epochs: int,
        early_stopping_rounds: int,
        path_to_save: Path,
        same_exp: bool = False
    ):
        self.model = model
        self.train_dataloader = train_dataloader
        self.valid_dataloader = valid_dataloader
        self.epochs = epochs
        self.early_stopping_rounds = early_stopping_rounds
        self.criterion = criterion
        self.optimizer = optimizer
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        self.train_losses = []
        self.valid_losses = []

        if same_exp:
            self.path_to_save = Path(
                path_to_save, str(len(os.listdir(path_to_save))))
            os.makedirs(self.path_to_save, exist_ok=True)
        else:
            self.path_to_save = Path(
                path_to_save, str(len(os.listdir(path_to_save))-1))
            os.makedirs(self.path_to_save, exist_ok=True)

    def train_step(self, inputs: torch.Tensor, labels: torch.Tensor) -> float:
        inputs, labels = inputs.to(self.device), labels.to(self.device)
        self.optimizer.zero_grad()
        outputs = self.model(inputs)
        loss = self.criterion(outputs, labels)
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def trainer(self) -> None:
        early_stop_counter = 0
        best_loss = float('inf')

        for epoch in tqdm(range(self.epochs), desc=f'Epochs for: {self.model.model_name}'):
            total_loss = 0
            self.model.train()
            train_progress_bar = tqdm(
                self.train_dataloader, desc=f"Training", leave=False)
            for inputs, labels in train_progress_bar:
                loss = self.train_step(inputs, labels)
                total_loss += loss
                train_progress_bar.set_postfix({"Loss": f"{loss:.4f}"})

            avg_train_loss = total_loss / len(self.train_dataloader)

            self.train_losses.append(avg_train_loss)

            validation_loss = self._evaluate()
            self.valid_losses.append(validation_loss)

            if validation_loss < best_loss:
                best_loss = validation_loss
                early_stop_counter = 0
            else:
                early_stop_counter += 1
            if early_stop_counter >= self.early_stopping_rounds:
                print("Early stopping!")
                break
        self.plot_losses()
        self.model.save_model(
            Path(self.path_to_save, f"{self.model.model_name}.pth"))

    def _evaluate(self) -> float:
        self.model.eval()
        total_loss = 0
        valid_progress_bar = tqdm(
            self.valid_dataloader, desc=f"Validation", leave=False)
        with torch.no_grad():
            for inputs, labels in valid_progress_bar:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                total_loss += loss.item()
        return total_loss / len(self.valid_dataloader)

    def check_early_stop(self, early_stop_counter: int) -> bool:
        if early_stop_counter >= self.early_stopping_rounds:
            return True
        else:
            return False

    def evaluate(self, dataloader: DataLoader) -> List[List[float]]:
        self.model.eval()
        with torch.no_grad():
            y_true: List[float] = []
            y_score: List[float] = []
            for inputs, labels in dataloader:
                inputs = inputs.to(self.device)
                y_score.extend(self.model(inputs).cpu().numpy())
                y_true.extend(labels.cpu().numpy())

        return [np.array(y_true), np.array(y_score)]

    def plot_losses(self) -> None:
        plt.plot(self.train_losses, label='Training loss')
        plt.plot(self.valid_losses, label='Validation loss')
        plt.legend()
        plt.savefig(Path(self.path_to_save, "losses.png"))
        plt.close()
