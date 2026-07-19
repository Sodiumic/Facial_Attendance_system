import os
import time
import cv2

from config import (
    CAMERA_INDEX,
    DATASET_DIR,
    HAARCASCADE
)

cascade = cv2.CascadeClassifier(HAARCASCADE)


def show_message(frame, text, color=(0, 255, 255)):

    cv2.putText(
        frame,
        text,
        (25, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        3
    )


def capture_faces(student_id):

    folder = os.path.join(DATASET_DIR, student_id)
    os.makedirs(folder, exist_ok=True)

    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        print("Cannot open camera.")
        return False

    poses = [
        "LOOK STRAIGHT",
        "TURN LEFT",
        "TURN RIGHT",
        "LOOK UP",
        "LOOK DOWN"
    ]

    image_number = 1

    for pose in poses:

        # ---------- Countdown ----------

        for sec in [3, 2, 1]:

            while True:

                ret, frame = camera.read()

                if not ret:
                    camera.release()
                    cv2.destroyAllWindows()
                    return False

                show_message(frame, f"{pose}  ({sec})")

                cv2.imshow("Student Registration", frame)

                if cv2.waitKey(1) == ord("q"):
                    camera.release()
                    cv2.destroyAllWindows()
                    return False

                start = time.time()

                while time.time() - start < 1:

                    cv2.imshow("Student Registration", frame)

                    if cv2.waitKey(1) == ord("q"):
                        camera.release()
                        cv2.destroyAllWindows()
                        return False

                    pass

                break

        # ---------- Capture 10 images ----------

        captured = 0
        last_capture = time.time()

        while captured < 10:

            ret, frame = camera.read()

            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = cascade.detectMultiScale(
                gray,
                1.2,
                5,
                minSize=(100, 100)
            )

            show_message(frame, pose)

            cv2.putText(
                frame,
                f"Image {image_number}/50",
                (25, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            for (x, y, w, h) in faces:

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                if time.time() - last_capture >= 0.35:

                    face = gray[y:y+h, x:x+w]
                    face = cv2.resize(face, (200, 200))

                    filename = os.path.join(
                        folder,
                        f"{image_number}.jpg"
                    )

                    cv2.imwrite(filename, face)

                    image_number += 1
                    captured += 1
                    last_capture = time.time()

            cv2.imshow("Student Registration", frame)

            if cv2.waitKey(1) == ord("q"):
                camera.release()
                cv2.destroyAllWindows()
                return False

    # ---------- Finished ----------

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        show_message(
            frame,
            "REGISTRATION COMPLETE!",
            (0, 255, 0)
        )

        cv2.imshow("Student Registration", frame)

        if cv2.waitKey(2000):
            break

    camera.release()
    cv2.destroyAllWindows()

    print("50 images captured successfully.")

    return True