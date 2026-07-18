from enum import Enum


class Gesture(Enum):
    GRAB = "grab"
    PINCH_OPEN = "pinch_open"
    PINCH_CLOSE = "pinch_close"


RADIUS = 5
COLOR = (0, 255, 0)
THICKNESS = 2

# Sample Constants
NO_FRAMES = 60
NO_LANDMARKS = 63

# Hidden Layer Constants
FIRST_LAYER = 128
SECOND_LAYER = 64
