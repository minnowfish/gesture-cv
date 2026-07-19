import torch
from torch import nn

from data_types import NO_FRAMES, NO_LANDMARKS, FIRST_LAYER, SECOND_LAYER, NO_OUTPUT

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.network = nn.Sequential(
            nn.Linear(NO_LANDMARKS * NO_FRAMES, FIRST_LAYER),
            nn.ReLU(),
            nn.Linear(FIRST_LAYER, SECOND_LAYER),
            nn.ReLU(),
            nn.Linear(SECOND_LAYER, NO_OUTPUT)
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.network(x)