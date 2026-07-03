from data_types import Gesture
from hand_tracker import HandTracker
from data_recorder import DataRecorder
import cv2
import mediapipe as mp

_RADIUS = 5
_COLOR = (0, 255, 0)
_THICKNESS = 2

keyToGesture: dict[str, Gesture] = {
    '1' : Gesture.GRAB,
    '2' : Gesture.PINCH_OPEN,
    '3' : Gesture.PINCH_CLOSE,
}

def _flatten_landmarks(landmarks) -> list[float]:
    flat = []
    for landmark in landmarks:
        flat.extend([landmark.x, landmark.y, landmark.z])
    return flat


def main():
    hand_tracker = HandTracker()
    data_recorder = DataRecorder()

    cam = cv2.VideoCapture(1)

    try:
        frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        while True:
            ret, frame = cam.read()
            if not ret:
                continue

            result = hand_tracker.process_frame(frame)
            if result is not None:
                for hand in result.hand_landmarks:
                    for landmark in hand:
                        pixel_x = int(landmark.x * frame_width)
                        pixel_y = int(landmark.y * frame_height)
                        cv2.circle(frame, (pixel_x, pixel_y), _RADIUS, _COLOR, _THICKNESS)

            cv2.imshow('Camera', frame)

            key: int = cv2.waitKey(1)

            if key != -1:
                char_pressed = chr(key)
                if char_pressed == 'q':
                    break
                elif char_pressed in keyToGesture:
                    data_recorder.start_recording(keyToGesture[char_pressed])
            
            if result is not None and result.hand_landmarks and data_recorder.is_recording:
                data_recorder.add_frame(_flatten_landmarks(result.hand_landmarks[0]))



    finally:
        hand_tracker.close()
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()