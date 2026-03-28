from integrations.email_sender import send_email

# 🔥 CHANGE THIS to your receiving email
TO_EMAIL = "vivekkunal3432@gmail.com"

subject = "✅ OpsPilot Test Email"
body = """
Hello 👋

This is a test email from OpsPilot AI Agent.

If you received this, your SMTP setup is working correctly ✅

🚀 Ready for hackathon demo!
"""

send_email(TO_EMAIL, subject, body)