from modlib.devices import AiCamera
from modlib.apps import Annotator
from modlib.models.zoo import Posenet
import cv2
import numpy as np
from sentry.Sentry import Sentry

device = AiCamera()
model = Posenet()
device.deploy(model)

annotator = Annotator()
sentry = Sentry()

FACIAL_KEYPOINTS = [0, 1, 2, 3, 4]  # nose, leftEye, rightEye, leftEar, rightEar

def get_face_square_bbox(pose, keypoint_scores, width, height, threshold=0.3, padding=40):
    points = []
    for i in FACIAL_KEYPOINTS:
        if keypoint_scores[i] >= threshold:
            y = int(pose[2 * i] * height)
            x = int(pose[2 * i + 1] * width)
            points.append((x, y))

    if not points:
        return None

    # Center point
    xs, ys = zip(*points)
    center_x = int(sum(xs) / len(xs))
    center_y = int(sum(ys) / len(ys))

    # Get bounding box dimensions
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    face_width = x_max - x_min
    face_height = y_max - y_min

    # Side of the square = max of width/height + padding
    side = max(face_width, face_height) + 2 * padding
    half = side // 2

    # Calculate square box
    x1 = max(center_x - half, 0)
    y1 = max(center_y - half, 0)
    x2 = min(center_x + half, width)
    y2 = min(center_y + half, height)

    return x1, y1, x2, y2

with device as stream:
    for frame in stream:
        poses = frame.detections
        frame_matrix = frame.image
        height, width, _ = frame_matrix.shape


        for i in range(poses.n_detections):
            if poses.confidence[i] < 0.3:
                continue

            face_bbox = get_face_square_bbox(poses.keypoints[i], poses.keypoint_scores[i], width, height)
            if face_bbox:
                x1, y1, x2, y2 = face_bbox
                square_face_crop = frame_matrix[y1:y2, x1:x2]

                # Show the square cropped face
                cv2.imshow(f"Square Face {i}", square_face_crop)

                # Predict mood
                mood = sentry.classify_mood(square_face_crop)
                print(f"Mood for face {i}: {mood}")

                if mood == sentry.moodEnum.SAD:
                    sentry.fire_shin_attack()

        annotator.annotate_poses(frame, poses)

        frame.display()

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()
