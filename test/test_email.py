import smtplib
import logging
from email.mime.text import MIMEText
from email.utils import formataddr

# Enable verbose debugging
smtplib.SMTP.debuglevel = 1
logging.basicConfig(level=logging.DEBUG)

def test_email_simple():
  try:
    # Email configuration
    smtp_server = "smtp.post.cz"
    port = 587
    sender_email = "max8@post.cz"
    password = "Posta8*"
    receiver_email = "max8@post.cz"

    # Create message
    message = MIMEText("This is a test email from Python!")
    message["Subject"] = "Test Email"
    message["From"] = formataddr(("Test Sender", sender_email))
    message["To"] = receiver_email

    # Create SMTP session
    print("Connecting to SMTP server...")
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()  # Enable TLS
    server.login(sender_email, password)
    
    # Send email
    print("Sending email...")
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("✓ Email sent successfully!")
    
    server.quit()
      
  except Exception as e:
      print(f"✗ Error: {e}")

# Run the test
test_email_simple()
