from sys import argv

import cv2
import mediapipe as mp
from data_recorder import DataRecorder
from data_types import COLOR, RADIUS, THICKNESS, Gesture
from hand_tracker import HandTracker
from utils import flatten_landmarks


def main():

    if len(argv) != 3:
        print("Usage: collect_video.py <input_video> <gesture>")
        return

    video_file = argv[1]

    try:
        gesture = Gesture(argv[2])
    except ValueError:
        valid = [g.value for g in Gesture]
        print(f"Invalid gesture {argv[2]}. Must be one of: {valid}")
        return

    hand_tracker = HandTracker()
    data_recorder = DataRecorder()

    cam = cv2.VideoCapture(video_file)
    if not cam.isOpened():
        raise ValueError(f"Could not open video file: {video_file}")

    try:
        frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        data_recorder.start_recording(gesture)

        while True:
            ret, frame = cam.read()
            if not ret:
                break

            result = hand_tracker.process_frame(frame)
            if result is not None:
                for hand in result.hand_landmarks:
                    for landmark in hand:
                        pixel_x = int(landmark.x * frame_width)
                        pixel_y = int(landmark.y * frame_height)
                        cv2.circle(frame, (pixel_x, pixel_y), RADIUS, COLOR,
                                   THICKNESS)

            cv2.imshow('Camera', frame)
            cv2.waitKey(1)

            if result is not None and result.hand_landmarks and data_recorder.is_recording:
                data_recorder.add_frame(
                    flatten_landmarks(result.hand_landmarks[0]))
                # check if 60 frames have been recorded
                if not data_recorder.is_recording:
                    break

    finally:
        hand_tracker.close()
        cam.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
