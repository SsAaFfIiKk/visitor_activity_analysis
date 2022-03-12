import torch
from PIL import Image
from torch.utils.data import Dataset


class ActivityDataset(torch.utils.data.Dataset):
    def __init__(self, paths_to_images, transforms, labels):
        self.paths_to_images = paths_to_images
        self.transforms = transforms
        self.get_label = labels

    def __len__(self):
        return len(self.paths_to_images)

    def __getitem__(self, idx):
        path_to_img = self.paths_to_images[idx]
        img = Image.open(path_to_img)
        img_tensor = self.transforms(img)

        label_name = path_to_img.split("/")[-2]
        label_idx = self.get_label[label_name]

        return img_tensor, torch.tensor(label_idx).int()