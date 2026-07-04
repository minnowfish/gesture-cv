from typing import List, Optional
from os import listdir
import data_types
import csv


class DataRecorder:

    def __init__(self, output_dir="training/data", clip_length=60):
        self.output_dir: str = output_dir
        self.clip_length: int = clip_length
        self.is_recording: bool = False
        self.current_label: Optional[Gesture] = None
        self.current_clip: List[List[float]] = [
        ]  # 60 x 63 array. store list of frames collected so far this clip
        self.clip_counters: dict[Gesture, int] = {
        }  # tracks how many samples created of the following gesture

    def start_recording(self, label: Gesture) -> None:
        self.is_recording = True
        self.current_label = label

        # reset current clip to account for case where user start new recording before last clip finishes
        self.current_clip = []

    def add_frame(self, landmarks_flat: List[float]) -> None:
        if (self.is_recording):
            self.current_clip.append(landmarks_flat)
            if (len(self.current_clip) >= self.clip_length):
                self._save_clip()

    def _get_next_count(self, label: Gesture) -> int:
        if label not in self.clip_counters:
            label_dir = f"{self.output_dir}/{label.value}"
            self.clip_counters[label] = len(listdir(label_dir))
        self.clip_counters[label] += 1
        return self.clip_counters[label]

    def _save_clip(self) -> None:
        count = self._get_next_count(self.current_label)
        filename = f"{self.output_dir}/{self.current_label.value}/{count:03d}.csv"

        try:
            with open(filename, "x", newline="") as f:
                csv.writer(f).writerows(self.current_clip)
        except FileExistsError:
            print(f"Error: File {filename} already exists")
        finally:
            self.is_recording = False
            self.current_clip = []
            self.current_label = None


# def main():
#     # TODO()
