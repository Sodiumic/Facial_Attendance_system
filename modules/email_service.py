import smtplib

from email.message import EmailMessage


# MY GMAIL DETAILS
SENDER_EMAIL = "twadedeji@gmail.com"
APP_PASSWORD = "qahwuwdwsurwqtoa"


def send_email(receiver, subject, body):

    try:

        msg = EmailMessage()

        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver

        msg.set_content(body)

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                SENDER_EMAIL,
                APP_PASSWORD
            )

            smtp.send_message(msg)

        print(f"Email sent to {receiver}")

    except Exception as e:

        print("Email Error:", e)


def send_checkin_email(
    name,
    email,
    date,
    time
):

    body = f"""
Hello {name},

Your attendance has been recorded successfully.

CHECK IN DETAILS

Date : {date}

Time : {time}

Status : CHECKED IN

Have a productive day.

AI Face Recognition Attendance System
"""

    send_email(
        email,
        "Attendance Check In",
        body
    )


def send_checkout_email(
    name,
    email,
    date,
    time
):

    body = f"""
Hello {name},

Your check out has been recorded successfully.

CHECK OUT DETAILS

Date : {date}

Time : {time}

Status : CHECKED OUT

Goodbye and see you again.

AI Face Recognition Attendance System
"""

    send_email(
        email,
        "Attendance Check Out",
        body
    )