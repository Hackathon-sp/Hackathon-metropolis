import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()

def send_confirmation_email(to_email, customer_name):
    """Send a confirmation email to the customer."""
    # Email configuration
    smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
    smtp_port = 587  # Replace with your SMTP port
    smtp_user = "hackathon949@gmail.com"  # Replace with your email
    smtp_password = os.getenv("SMTP_PASS")  # Replace with your email password

    # Create the email content
    subject = "Reservation Confirmation"
    body = f"Dear {customer_name},\n\nYour reservation has been confirmed!\n\nThank you for choosing our service."

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print("Confirmation email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_confirmation_email("sjha@spplus.com", "Test")