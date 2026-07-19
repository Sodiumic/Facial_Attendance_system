from flask import Flask, render_template, request, redirect

from modules.database import create_tables

from modules.students import (
    add_student,
    get_all_students,
    delete_student
)

from modules.face_capture import capture_faces
from modules.trainer import train_model
from modules.recognizer import recognize_faces

from modules.attendance import (
    get_today_attendance,
    get_all_attendance
)

app = Flask(__name__)

create_tables()


@app.route("/")
def dashboard():

    return render_template("dashboard.html")


@app.route("/students")
def students():

    return render_template(
        "students.html",
        students=get_all_students()
    )


@app.route("/delete/<student_id>")
def delete(student_id):

    delete_student(student_id)

    return redirect("/students")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        student_id = request.form["student_id"]
        full_name = request.form["full_name"]
        email = request.form["email"]

        add_student(
            student_id,
            full_name,
            email
        )

        success = capture_faces(student_id)

        if not success:
            return "Face registration was cancelled."

        return redirect("/train")

    return render_template("register_student.html")


@app.route("/train")
def train():

    success, message = train_model()

    return render_template(
        "train_result.html",
        success=success,
        message=message
    )

@app.route("/attendance")
def attendance():

    return render_template(
        "attendance.html",
        attendance=get_today_attendance()
    )


@app.route("/checkin")
def checkin():

    recognize_faces("checkin")

    return redirect("/attendance")


@app.route("/checkout")
def checkout():

    recognize_faces("checkout")

    return redirect("/attendance")


@app.route("/reports")
def reports():

    return render_template(
        "reports.html",
        attendance=get_all_attendance()
    )


if __name__ == "__main__":
    app.run(debug=True)