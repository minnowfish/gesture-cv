from data_types import Gesture

# File Paths
MODE_WEIGHTS_PATH = "model/model.pth"
DATA_DIR = "training/data"

# OpenCV Constants
RADIUS = 5
COLOR = (0, 255, 0)
THICKNESS = 2

# Sample Constants
NO_FRAMES = 60
NO_LANDMARKS = 63

# Hidden Layer Constants
FIRST_LAYER = 128
SECOND_LAYER = 64
NO_OUTPUT = len(Gesture)
