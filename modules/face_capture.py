import os
import sys
import cv2
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CAMERA_INDEX


def test_camera():
    camera = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("Could not open the camera.")
        return

    print("Camera started.")
    print("Press Q to close.")

    while True:
        ret, frame = camera.read()

        if not ret:
            print("Failed to read from the camera.")
            break

        cv2.imshow("Camera Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    test_camera()