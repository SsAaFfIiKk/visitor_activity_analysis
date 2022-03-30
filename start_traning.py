import os
import torch
import random
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models
from Model import TrainModel, l1loss
from Dataloader import ActivityDataset
from torch.utils.data import DataLoader
import torchvision.transforms as transforms

if __name__ == "__main__":
    model_ft = models.resnet101(pretrained=True)
    num_ftrs = model_ft.fc.in_features
    device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    model_ft = model_ft.to(device)
    for name, param in model_ft.named_parameters():
        if name in ['layer4.1.conv2.weight','layer4.1.bn2.weight', 'layer4.1.bn2.bias']:
            param.requires_grad = True
        else:
            param.requires_grad = False

    model_ft.fc = nn.Linear(num_ftrs, 5)
    for name, param in model_ft.named_parameters():
        print(name, ':', param.requires_grad)


    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    sz = 112
    bs = 1
    nw = 4

    tf = {'train': transforms.Compose([
               transforms.RandomRotation(degrees=0.2),
               transforms.RandomHorizontalFlip(p=.5),
               transforms.RandomGrayscale(p=.2),
               transforms.Resize((sz, sz)),
               transforms.ToTensor(),
               transforms.Normalize(mean, std)]),

        'test': transforms.Compose([
               transforms.Resize((sz, sz)),
               transforms.ToTensor(),
               transforms.Normalize(mean, std)])}

    path_to_dataset = "F:/Python/Data/cv_itmo_classes"

    paths_to_images = []
    paths = os.walk(path_to_dataset)
    for address, dirs, files in paths:
        for file in files:
            if file.endswith(".jpg"):
                paths_to_images.append(address.replace("\\", "/") + '/' + file)

    random.seed(0)
    random.shuffle(paths_to_images)
    train_size = int(0.8 * len(paths_to_images))
    labels = {"laptop": 0, "nothing": 1, "talking": 2}

    train_dataset = ActivityDataset(paths_to_images[:train_size], tf["train"], labels)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=bs, shuffle=True, num_workers=nw)

    test_dataset = ActivityDataset(paths_to_images[train_size:], tf["test"], labels)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=bs, shuffle=True, num_workers=nw)

    optimizer = optim.Adam(params=model_ft.parameters(), lr=0.001, weight_decay=0.001)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.9)
    history = TrainModel(model_ft, train_loader, test_loader, optimizer, l1loss, scheduler, 10)

    PATH = "./model_new.pth"
    torch.save(model_ft.state_dict(), PATH)