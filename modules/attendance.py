import sqlite3
from datetime import datetime

from config import DATABASE


def get_today_attendance():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    today = datetime.now().strftime("%Y-%m-%d")

    rows = conn.execute(
        """
        SELECT
            a.*,
            s.full_name,
            s.email
        FROM attendance a
        JOIN students s
        ON a.student_id=s.student_id
        WHERE a.date=?
        ORDER BY a.check_in
        """,
        (today,)
    ).fetchall()

    conn.close()

    return rows


def get_all_attendance():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT
            a.*,
            s.full_name,
            s.email
        FROM attendance a
        JOIN students s
        ON a.student_id=s.student_id
        ORDER BY a.date DESC,
                 a.check_in DESC
        """
    ).fetchall()

    conn.close()

    return rows