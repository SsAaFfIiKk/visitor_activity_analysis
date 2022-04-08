import os
import wandb
import torch
from torch import nn
from typing import Any
from invoke import Config
from torchvision import datasets, transforms
from skorch import NeuralNetClassifier
from skorch.helper import predefined_split
from skorch.callbacks import LRScheduler
from skorch.callbacks import Checkpoint
from skorch.callbacks import Freezer
from skorch.callbacks import WandbLogger


class Train:

    def __init__(self, model_config: Config, dataset_config: Config,  model: Any):
        super().__init__()
        self.model_config = model_config
        self.dataset_config = dataset_config
        self.criterion = nn.CrossEntropyLoss
        self.optim = torch.optim.Adam
        self.device = torch.device(self.model_config.device if torch.cuda.is_available() else "cpu")
        self.model = model.to(self.device)
        self.lrscheduler = LRScheduler(policy='StepLR', step_size=10, gamma=0.1)
        self.checkpoint = Checkpoint(f_params='model.pt', monitor='valid_acc_best')
        self.freezer = Freezer(lambda x: not x.startswith('model.fc'))

        self.train_transforms = transforms.Compose([
                        transforms.RandomRotation(degrees=0.2),
                        transforms.RandomHorizontalFlip(p=.5),
                        transforms.RandomGrayscale(p=.2),
                        transforms.Resize(self.model_config.size_image),
                        transforms.ToTensor(),
                        transforms.Normalize(self.model_config.std, self.model_config.mean)])

        self.val_transforms = transforms.Compose([
                        transforms.Resize(self.model_config.size_image),
                        transforms.ToTensor(),
                        transforms.Normalize(self.model_config.std, self.model_config.mean)])

        self.train_ds = datasets.ImageFolder(os.path.join(self.dataset_config.path_to_dataset,
                                                          self.dataset_config.train_folder), self.train_transforms)

        self.val_ds = datasets.ImageFolder(os.path.join(self.dataset_config.path_to_dataset,
                                                        self.dataset_config.valid_folder), self.val_transforms)

    def sckorh_train(self):
        wandb_run = wandb.init(name=self.model_config.name_wndb)
        wandb_run.model_config.update({"learning rate": self.model_config.lr,
                                       "batch size": self.model_config.batch_size,
                                       "epochs": self.model_config.max_epochs})

        net = NeuralNetClassifier(
                    self.model,  
                    criterion=self.criterion,
                    lr=self.model_config.lr,
                    batch_size=self.model_config.batch_size,
                    max_epochs=self.model_config.max_epochs,
                    module__output_features=self.model_config.output_features,
                    optimizer=self.optim,
                    iterator_train__shuffle=self.model_config.iterator_train__shuffle,
                    iterator_train__num_workers=self.model_config.iterator_train__num_workers,
                    iterator_valid__shuffle=self.model_config.iterator_valid__shuffle,
                    iterator_valid__num_workers=self.model_config.iterator_valid__num_workers,
                    train_split=predefined_split(self.val_ds),
                    callbacks=[self.lrscheduler, self.checkpoint, self.freezer, WandbLogger(wandb_run)],
                    device=self.device,)
        
        net.fit(self.train_ds, y=None)
        net.initialize()
        net.load_params(f_params="model.pt")
        traced_model = torch.jit.script(net.module_, torch.zeros((1, 3, 224, 224)))
        torch.jit.save(traced_model, "torchscript.pt")  
        wandb.finish()
