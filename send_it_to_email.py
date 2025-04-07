import os
import smtplib
import mimetypes
from email.message import EmailMessage
from datetime import datetime
import getpass

# ==== CONFIGURATION ====
ATTENDANCE_FOLDER = r"D:\Project\face_recognition_project"

def find_latest_attendance_file():
    files = [f for f in os.listdir(ATTENDANCE_FOLDER) if f.endswith((".csv", ".xlsx"))]
    if not files:
        return None
    files.sort(key=lambda x: os.path.getmtime(os.path.join(ATTENDANCE_FOLDER, x)), reverse=True)
    return os.path.join(ATTENDANCE_FOLDER, files[0])

def get_email_input():
    print("✉️  Enter sender details:")
    sender_email = input("From (your email): ").strip()
    sender_password = getpass.getpass("App Password (input hidden): ")

    recipients_raw = input("To (recipient email(s), comma-separated): ").strip()
    recipients = [email.strip() for email in recipients_raw.split(",") if email.strip()]

    return sender_email, sender_password, recipients

def send_email_with_attachment(subject, body, attachment_path, sender_email, sender_password, recipients):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg.set_content(body)

    # Attach the file
    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type, mime_subtype = mime_type.split('/')
    with open(attachment_path, 'rb') as file:
        msg.add_attachment(file.read(),
                           maintype=mime_type,
                           subtype=mime_subtype,
                           filename=os.path.basename(attachment_path))

    # Send email via Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

    print(f"\n✅ Email sent from {sender_email} to: {', '.join(recipients)}")

def main():
    print("\n📤 Attendance Email Sender\n" + "-"*35)
    file_path = find_latest_attendance_file()
    if not file_path:
        print("❌ No attendance file found.")
        return

    sender_email, sender_password, recipients = get_email_input()
    if not sender_email or not sender_password or not recipients:
        print("⚠️ Incomplete input. Aborting send.")
        return

    subject = "📅 Attendance Report"
    body = f"""Hi,

Please find attached the latest attendance report.

Sent on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."""

    try:
        send_email_with_attachment(subject, body, file_path, sender_email, sender_password, recipients)
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    main()



### app password = potcyyuhkjrcradb