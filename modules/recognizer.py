import cv2
import json
import sqlite3
from datetime import datetime

from config import (
    CAMERA_INDEX,
    MODEL_FILE,
    LABELS_FILE,
    DATABASE,
    HAARCASCADE,
    CONFIDENCE_THRESHOLD
)

from modules.email_service import (
    send_checkin_email,
    send_checkout_email
)

cascade = cv2.CascadeClassifier(HAARCASCADE)


def get_student(student_id):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (student_id,)
    ).fetchone()

    conn.close()

    return student


def attendance_action(student, mode):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    row = conn.execute(
        """
        SELECT *
        FROM attendance
        WHERE student_id=?
        AND date=?
        """,
        (student["student_id"], today)
    ).fetchone()

    # ---------------- CHECK IN ---------------- #

    if mode == "checkin":

        if row is None:

            conn.execute(
                """
                INSERT INTO attendance
                (
                    student_id,
                    date,
                    check_in,
                    check_out,
                    status
                )
                VALUES
                (?, ?, ?, ?, ?)
                """,
                (
                    student["student_id"],
                    today,
                    now,
                    "",
                    "Present"
                )
            )

            conn.commit()
            conn.close()

            send_checkin_email(
                student["full_name"],
                student["email"],
                today,
                now
            )

            return "CHECKED IN"

        conn.close()
        return "ALREADY CHECKED IN"

    # ---------------- CHECK OUT ---------------- #

    if mode == "checkout":

        if row is None:

            conn.close()
            return "CHECK IN FIRST"

        if row["check_out"] != "":

            conn.close()
            return "ALREADY CHECKED OUT"

        conn.execute(
            """
            UPDATE attendance
            SET check_out=?
            WHERE id=?
            """,
            (
                now,
                row["id"]
            )
        )

        conn.commit()
        conn.close()

        send_checkout_email(
            student["full_name"],
            student["email"],
            today,
            now
        )

        return "CHECKED OUT"

    

def recognize_faces(mode):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_FILE)

    with open(LABELS_FILE, "r") as f:
        labels = json.load(f)

    labels = {int(k): v for k, v in labels.items()}

    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        return

    
    while True:

        ret, frame = camera.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = cascade.detectMultiScale(
            gray,
            1.2,
            5,
            minSize=(100,100)
        )

        for (x, y, w, h) in faces:

            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200,200))

            label, confidence = recognizer.predict(face)

            if confidence < CONFIDENCE_THRESHOLD:

                student_id = labels.get(label)

                if student_id is None:
                    continue

                student = get_student(student_id)

                if student is None:
                    continue

                status = attendance_action(student, mode)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    student["full_name"],
                    (x, y - 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    status,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 0),
                    2
                )

                cv2.imshow("AI Face Recognition Attendance", frame)

                # Keep the result on screen for 2 seconds
                cv2.waitKey(2000)

                camera.release()
                cv2.destroyAllWindows()

                return status

            else:

                cv2.rectangle(
                    frame,
                    (x,y),
                    (x+w,y+h),
                    (0,0,255),
                    2
                )

                cv2.putText(
                    frame,
                    "Unknown",
                    (x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,0,255),
                    2
                )

        cv2.imshow(
            "AI Face Recognition Attendance",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
    return "NO FACE DETECTED"