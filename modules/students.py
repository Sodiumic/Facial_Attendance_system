import os
import shutil

from modules.database import get_connection
from config import DATASET_DIR


def add_student(student_id, full_name, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students(student_id, full_name, email)
        VALUES (?, ?, ?)
    """, (student_id, full_name, email))

    conn.commit()
    conn.close()


def get_all_students():
    conn = get_connection()

    students = conn.execute("""
        SELECT *
        FROM students
        ORDER BY full_name
    """).fetchall()

    conn.close()

    return students


def delete_student(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM attendance WHERE student_id=?",
        (student_id,)
    )

    cursor.execute(
        "DELETE FROM students WHERE student_id=?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    student_folder = os.path.join(DATASET_DIR, student_id)

    if os.path.exists(student_folder):
        shutil.rmtree(student_folder)