import torchmetrics
import torch.nn as nn
import pytorch_lightning as pl

from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts

class BinarySegmenter(pl.LightningModule):
    def __init__(self, model, train_loader=None, val_loader=None, test_loader=None):
        super().__init__()

        # Assign attributes
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader

        # Create loss function and account for imbalance of classes
        self.criterion = nn.BCEWithLogitsLoss(pos_weight=self.pos_weight)

        # Initialize some metrics to monitor the performance
        self.metrics = torchmetrics.MetricCollection([
            torchmetrics.F1Score(task="binary"),
            torchmetrics.Dice()
        ])

    @property
    def pos_weight(self):
        if self.train_loader is None:
            # Not known
            return None
        
        # Init counts
        pos, neg = 0, 0

        for _, mask in self.train_loader:
            # Update pos and neg sums
            pos += mask.sum()
            neg += (1 - mask).sum()

        return neg / pos

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        # Forward propagate and compute loss
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        self.log("train_loss", loss, prog_bar=True)
        return loss

    def eval_step(self, batch, prefix=''):
        # Forward pass
        x, y = batch
        y_hat = self(x)

        # Compute the loss and the metrics
        loss = self.criterion(y_hat, y)
        metrics = self.metrics(y_hat, y.long())

        # Log the loss and the metrics
        self.log(f"{prefix}_loss", loss, prog_bar=True)
        self.log(f"{prefix}_f1", metrics["BinaryF1Score"], prog_bar=True)
        self.log(f"{prefix}_dice", metrics["Dice"], prog_bar=True)
    
    def validation_step(self, batch, batch_idx):
        self.eval_step(batch, prefix="val")

    def test_step(self, batch, batch_idx):
        self.eval_step(batch, prefix="test")
    
    def train_dataloader(self):
        return self.train_loader

    def val_dataloader(self):
        return self.val_loader

    def test_dataloader(self):
        return self.test_loader

    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(), lr=1e-3, weight_decay=1e-4)
        scheduler = CosineAnnealingWarmRestarts(optimizer, 10, 2, 1e-6)

        return [optimizer], [scheduler]
