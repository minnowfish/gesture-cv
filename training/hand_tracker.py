import cv2
import mediapipe as mp
import time

_MODEL_PATH = 'training/hand_landmarker.task'

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


class HandTracker:

    def __init__(self):
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
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(mp.ImageFormat.SRGB, rgb_frame)
        self._landmarker.detect_async(mp_image, int(self._get_timestamp()))
        return self._latest_result

    def close(self) -> None:
        self._landmarker.close()

    # To be moved to main function
    # def run(self):
    #     options = HandLandmarkerOptions(
    #         base_options = BaseOptions(model_asset_path=_MODEL_PATH),
    #         running_mode = VisionRunningMode.LIVE_STREAM,
    #         num_hands = 2,
    #         result_callback=self.print_result)

    #     with HandLandmarker.create_from_options(options) as landmarker:
    #         cam = cv2.VideoCapture(1)

    #         frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    #         frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #         start = time.time()
    #         while True:
    #             ret, frame = cam.read()
    #             if not ret:
    #                 continue

    #             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #             mp_image = mp.Image(mp.ImageFormat.SRGB, rgb_frame)
    #             landmarker.detect_async(mp_image, int((time.time() - start) * 1000))
    #             result = self._latest_result
    #             if result is not None:
    #                 for hand in result.hand_landmarks:
    #                     for landmark in hand:
    #                         pixel_x = int(landmark.x * frame_width)
    #                         pixel_y = int(landmark.y * frame_height)
    #                         cv2.circle(frame, (pixel_x, pixel_y), _RADIUS, _COLOR, _THICKNESS)

    #             cv2.imshow('Camera', frame)

    #             if cv2.waitKey(1) == ord('q'):
    #                 break

    #         cam.release()
    #         cv2.destroyAllWindows()


# def main():
#     tracker = HandTracker()
#     tracker.run()

# if __name__ == "__main__":
#     main()
