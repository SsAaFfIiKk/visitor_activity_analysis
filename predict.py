import torch
import numpy as np
from PIL import Image
import torch.nn as nn
from torchvision import transforms
import torchvision.models as models


class Classifier:

    def __init__(self, device=torch.device("cpu")):
        labels = {"laptop": 0, "nothing": 1, "talking": 2}
        model = models.resnet101(pretrained=True)
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, 3)
        weight_path = "./model_new.pth"
        model.load_state_dict(torch.load(weight_path, map_location=device))
        model.to(device).eval()

        self.labels = {v: k for k, v in labels.items()}
        self.model = model
        self.device = device
        self.tf = transforms.Compose([
            transforms.Resize((112, 112)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

    def res(self, bytes):
        nparr = np.fromstring(bytes, np.uint8)
        image = Image.fromarray(np.uint8(nparr)).convert('RGB')
        img = self.tf(image)
        img = torch.unsqueeze(img, 0)
        with torch.no_grad():
            result = self.model(img)
            label = result.argmax(dim=1)
            answer = self.labels[label.sum().item()]
            return answer
