import csv
from os import listdir
from typing import List, Optional
from data_types import Gesture

import data_types
from data_types import Gesture


class DataRecorder:

    def __init__(self, output_dir="training/data", clip_length=60):
        self.output_dir: str = output_dir
        self._clip_length: int = clip_length
        self._is_recording: bool = False
        self._current_label: Optional[Gesture] = None
        self._current_clip: List[List[float]] = [
        ]  # 60 x 63 array. store list of frames collected so far this clip
        self._clip_counters: dict[Gesture, int] = {
        }  # tracks how many samples created of the following gesture

    @property
    def is_recording(self) -> bool:
        return self._is_recording

    def start_recording(self, label: Gesture) -> None:
        assert isinstance(label,
                          Gesture), "Error: invalid label to record: {label}"

        self._is_recording = True
        self._current_label = label

        # reset current clip to account for case where user start new recording before last clip finishes
        self._current_clip = []

    def add_frame(self, landmarks_flat: List[float]) -> None:
        if (self._is_recording):
            self._current_clip.append(landmarks_flat)
            if (len(self._current_clip) >= self._clip_length):
                self._save_clip()

    def _get_next_count(self, label: Gesture) -> int:
        assert isinstance(label,
                          Gesture), "Error: invalid label to record: {label}"
        if label not in self._clip_counters:
            label_dir = f"{self.output_dir}/{label.value}"
            self._clip_counters[label] = len(listdir(label_dir)) - 1 # -1 to account for .gitkeep file
        self._clip_counters[label] += 1
        return self._clip_counters[label]

    def _save_clip(self) -> None:
        assert self._current_label != None, "Error: current label not set"

        count = self._get_next_count(self._current_label)
        filename = f"{self.output_dir}/{self._current_label.value}/{count:03d}.csv"

        try:
            with open(filename, "x", newline="") as f:
                csv.writer(f).writerows(self._current_clip)
        except FileExistsError:
            print(f"Error: File {filename} already exists")
        finally:
            self._is_recording = False
            self._current_clip = []
            self._current_label = None
