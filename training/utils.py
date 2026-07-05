def flatten_landmarks(landmarks) -> list[float]:
    flat = []
    for landmark in landmarks:
        flat.extend([landmark.x, landmark.y, landmark.z])
    return flat