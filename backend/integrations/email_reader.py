import imaplib
import email
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ID")
PASSWORD = os.getenv("EMAIL_PASSWORD")


def read_latest_email():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()

    if not email_ids:
        return None

    latest_email_id = email_ids[-1]
    status, data = mail.fetch(latest_email_id, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])

    from email.utils import parseaddr
    sender = parseaddr(msg["from"])[1]

    subject = msg["subject"] or ""

    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode(errors="ignore")
                break
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    content = subject if subject else body[:100]

    return {
    "subject": subject.strip(),
    "body": body.strip(),
    "sender": sender
}