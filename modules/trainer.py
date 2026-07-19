import cv2
import json
import os
import numpy as np

from config import (
    DATASET_DIR,
    MODEL_FILE,
    LABELS_FILE
)


def train_model():

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    labels = []

    label_map = {}

    current_label = 0

    for student_id in sorted(os.listdir(DATASET_DIR)):

        folder = os.path.join(
            DATASET_DIR,
            student_id
        )

        if not os.path.isdir(folder):
            continue

        label_map[current_label] = student_id

        for image in os.listdir(folder):

            image_path = os.path.join(
                folder,
                image
            )

            img = cv2.imread(
                image_path,
                cv2.IMREAD_GRAYSCALE
            )

            if img is None:
                continue

            faces.append(img)
            labels.append(current_label)

        current_label += 1

    if len(faces) == 0:
        return False, "No training images found."

    recognizer.train(
        faces,
        np.array(labels)
    )

    recognizer.save(MODEL_FILE)

    with open(
        LABELS_FILE,
        "w"
    ) as f:

        json.dump(
            label_map,
            f
        )

    return True, "Training completed successfully."