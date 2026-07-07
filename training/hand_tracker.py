import time

import cv2
import mediapipe as mp

_MODEL_PATH = 'training/hand_landmarker.task'

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


class HandTracker:

    def __init__(self):
        self._closed = False
        self._latest_result = None
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=_MODEL_PATH),
            running_mode=VisionRunningMode.LIVE_STREAM,
            num_hands=2,
            result_callback=self._on_result)
        self._landmarker = HandLandmarker.create_from_options(options)
        self._start_time = time.time()

    def _on_result(self, result: HandLandmarkerResult, output_image: mp.Image,
                   timestamp_ms: int):
        self._latest_result = result
        # print(f'hand landmarker result: {result}')

    def _get_timestamp(self) -> float:
        return (time.time() - self._start_time) * 1000

    def process_frame(self, frame: np.ndarray) -> HandLandmarkerResult | None:
        if self._closed:
            raise RuntimeError("ERROR: process_frame called after close()")
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(mp.ImageFormat.SRGB, rgb_frame)
        self._landmarker.detect_async(mp_image, int(self._get_timestamp()))
        return self._latest_result

    def close(self) -> None:
        self._closed = True
        self._landmarker.close()
