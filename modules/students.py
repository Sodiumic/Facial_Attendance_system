import os
import pandas as pd

from config import STUDENTS_FILE


class StudentManager:

    def __init__(self):
        self.create_student_file()

    def create_student_file(self):
        """
        Creates students.csv if it does not exist.
        """

        if not os.path.exists(STUDENTS_FILE):

            df = pd.DataFrame(columns=[
                "Student ID",
                "First Name",
                "Last Name",
                "Email",
                "Department",
                "Level",
                "Date Registered"
            ])

            df.to_csv(STUDENTS_FILE, index=False)

    def register_student(
        self,
        student_id,
        first_name,
        last_name,
        email,
        department,
        level,
        date_registered
    ):

        df = pd.read_csv(STUDENTS_FILE)

        # Check duplicate ID
        if student_id in df["Student ID"].astype(str).values:
            return False, "Student ID already exists."

        # Check duplicate Email
        if email.lower() in df["Email"].astype(str).str.lower().values:
            return False, "Email already exists."

        new_student = pd.DataFrame([{
            "Student ID": student_id,
            "First Name": first_name,
            "Last Name": last_name,
            "Email": email,
            "Department": department,
            "Level": level,
            "Date Registered": date_registered
        }])

        df = pd.concat([df, new_student], ignore_index=True)

        df.to_csv(STUDENTS_FILE, index=False)

        return True, "Student registered successfully."

    def view_students(self):

        df = pd.read_csv(STUDENTS_FILE)

        return df