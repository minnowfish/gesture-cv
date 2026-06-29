from typing import List, Optional

class DataRecorder:
    def __init__(self, output_dir, clip_length = 60):
        self.output_dir: str = output_dir
        self.clip_length: int = clip_length
        self.is_recording: bool = False
        self.current_label: Optional[str] = None
        self.current_clip: List[List[float]] = [] # 60 x 63 array. store list of frames collected so far this clip

    def start_recording(self, label: str):
        self.is_recording = True
        self.current_label = label

        # reset current clip to account for case where user start new recording before last clip finishes
        self.current_clip = [] 

    def add_frame(self, landmarks_flat: List[float]):
        if (self.is_recording):
            self.current_clip.append(landmarks_flat)
            if (len(self.current_clip) >= self.clip_length):
                self._save_clip()

    def _save_clip(self):
        # TODO(): FILE ERROR CHECKING + WRITE TO FILE
        f = open(f"{self.output_dir}/{self.current_label}/", "x")
        self.is_recording = False
        self.current_clip = []
        self.current_label = None




        

        
