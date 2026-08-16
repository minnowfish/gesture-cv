import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from pathlib import Path

DATA_DIR = "training/data"

class SubfolderDataset(Dataset):
    def __init__(self, root_dir = DATA_DIR):
        self.root_dir = Path(root_dir)

        self.classes = sorted([f.name for f in self.root_dir.iterdir() if f.is_dir()])
        self.class_to_idx = {cls_name: i for i, cls_name in enumerate(self.classes)}

        self.samples = []
        for cls_name in self.classes:
            cls_dir = self.root_dir / cls_name
            for file_path in cls_dir.glob('*.csv'):
                if file_path.is_file():
                    self.samples.append((file_path, self.class_to_idx[cls_name]))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        file_path, label = self.samples[idx]
        sample = pd.read_csv(file_path).to_numpy()
        tensor = torch.from_numpy(sample).float()
        return (tensor, label)
