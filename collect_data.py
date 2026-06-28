import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import time
from typing import TypeAlias

_RADIUS = 5
_COLOR = (0, 255, 0)
_THICKNESS = 2
_MODEL_PATH = 'hand_landmarker.task'

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    latest_result["data"] = result
    print(f'hand landmarker result: {result}')
    

def main():
    options = HandLandmarkerOptions(
        base_options = BaseOptions(model_asset_path=_MODEL_PATH),
        running_mode = VisionRunningMode.LIVE_STREAM,
        num_hands = 2,
        result_callback=print_result)

    latest_result = {"data": None}

    with HandLandmarker.create_from_options(options) as landmarker:
        cam = cv2.VideoCapture(1)

        frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        start = time.time()
        while True:
            ret, frame = cam.read()

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(mp.ImageFormat.SRGB, rgb_frame)
            landmarker.detect_async(mp_image, int((time.time() - start) * 1000))
            result = latest_result["data"]
            if result is not None:
                for hand in result.hand_landmarks:
                    for landmark in hand:
                        pixel_x = int(landmark.x * frame_width)
                        pixel_y = int(landmark.y * frame_height)
                        cv2.circle(frame, (pixel_x, pixel_y), _RADIUS, _COLOR, _THICKNESS)

            cv2.imshow('Camera', frame)

            if cv2.waitKey(1) == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()