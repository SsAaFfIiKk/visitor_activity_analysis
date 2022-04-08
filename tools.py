import torch
import numpy as np
from PIL import Image
from invoke import Config
from torchvision import transforms


labels = {0: "laptop", 1: "nothing", 2: "talking"}


net = torch.jit.load("torchscript.pt")


class Img:
    def __init__(self):
        self.img_bytes = None
        self.predict = None
        self.img_size = ()
        self.std = []
        self.mean = []
        self.transforms =None

    def read_config(self, config: Config):
        self.img_size = config.size_image
        self.std = config.std
        self.mean = config.mean
        self.transforms = transforms.Compose([
            transforms.Resize(self.img_size),
            transforms.ToTensor(),
            transforms.Normalize(self.std, self.mean)
        ])

    def set_img_bytes(self, bytes):
        self.img_bytes = bytes

    def generate_predict(self):
        nparr = np.fromstring(self.img_bytes, np.uint8)
        image = Image.fromarray(np.uint8(nparr)).convert('RGB')
        image = self.transforms(image)
        image = torch.unsqueeze(image, 0)

        with torch.no_grad():
            result = net(image)
            label = result.argmax(dim=1)
            res = labels[label.sum().item()]
            self.predict = res

    def get_predict(self):
        return self.predict