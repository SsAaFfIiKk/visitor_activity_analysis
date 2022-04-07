from typing import Any
import torch
from invoke import Config
from torch import nn
import os
from skorch import NeuralNetClassifier
from torchvision import datasets, transforms
from skorch import NeuralNetClassifier
from skorch.helper import predefined_split
from skorch.callbacks import LRScheduler
from skorch.callbacks import Checkpoint
from skorch.callbacks import Freezer
import wandb
from skorch.callbacks import WandbLogger

class Train:

    def __init__(self, config: Config, model: Any):
        super().__init__()
        self.config = config
        self.criterion = nn.CrossEntropyLoss
        self.optim = torch.optim.Adam
        self.device = torch.device(self.config.device if torch.cuda.is_available() else "cpu")        
        self.model = model.to(self.device)
        self.lrscheduler = LRScheduler(policy='StepLR', step_size=10, gamma=0.1)
        self.checkpoint = Checkpoint(f_params='model.pt', monitor='valid_acc_best')
        self.freezer = Freezer(lambda x: not x.startswith('model.fc'))
        self.train_transforms = transforms.Compose([
                        transforms.RandomRotation(degrees=0.2),
                        transforms.RandomHorizontalFlip(p=.5),
                        transforms.RandomGrayscale(p=.2),
                        transforms.Resize(config.size_image),
                        transforms.ToTensor(),
                        transforms.Normalize(config.std, config.mean)])
        self.val_transforms = transforms.Compose([
                        transforms.Resize(config.size_image ),
                        transforms.ToTensor(),
                        transforms.Normalize(config.std, config.mean)])
        self.train_ds = datasets.ImageFolder(os.path.join(config.data_dir, 'train'), self.train_transforms)
        self.val_ds = datasets.ImageFolder(os.path.join(config.data_dir, 'val'), self.val_transforms)


    def sckorh_train(self):
        wandb_run = wandb.init(name = self.config.name_wndb)
        wandb_run.config.update({"learning rate": self.config.lr, 
                                "batch size": self.config.batch_size, 
                                "epochs": self.config.max_epochs})

        net = NeuralNetClassifier(
                    self.model,  
                    criterion= self.criterion,
                    lr=self.config.lr,
                    batch_size=self.config.batch_size,
                    max_epochs=self.config.max_epochs,
                    module__output_features=self.config.output_features,
                    optimizer=self.optim,
                    iterator_train__shuffle=self.config.iterator_train__shuffle,
                    iterator_train__num_workers = self.config.iterator_train__num_workers,
                    iterator_valid__shuffle = self.config.iterator_valid__shuffle,
                    iterator_valid__num_workers=self.config.iterator_valid__num_workers,
                    train_split=predefined_split(self.val_ds),
                    callbacks=[self.lrscheduler, self.checkpoint, self.freezer, WandbLogger(wandb_run)],
                    device = self.device,) 
        
        net.fit(self.train_ds, y=None)
        net.initialize()
        net.load_params(f_params="model.pt")
        traced_model = torch.jit.script(net.module_, torch.zeros((1, 3, 224, 224)))
        torch.jit.save(traced_model, "torchscript.pt")  
        wandb.finish()  

