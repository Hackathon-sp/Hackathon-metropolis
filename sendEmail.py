import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()

def send_confirmation_email(to_email, location, start_time, end_time):
    print("Sending Email")

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "hackathon949@gmail.com"
    smtp_password = os.getenv("SMTP_PASS")

    subject = "Your Parking Reservation is Confirmed"

    # Plain text version for fallback
    plain_text = f"""Dear Customer,

Your parking reservation is confirmed!

Location: {location}
Reservation Time: {start_time} to {end_time}

Thank you for choosing Metropolis.
"""

    # HTML content with placeholders
    html_content = f"""
    <html>
    <head>
      <style>
        body {{ font-family: Arial, sans-serif; }}
        .container {{ max-width: 600px; margin: auto; }}
        .header {{ background-color: #5f59ff; padding: 30px; text-align: center; }}
        .header img {{ height: 40px; }}
        .content {{ padding: 30px; }}
        .content h2 {{ color: #5f59ff; }}
        .details {{ margin-top: 20px; background: #f7f7f7; padding: 20px; border-radius: 6px; }}
        .details p {{ margin: 5px 0; }}
        .footer {{ background-color: #000; color: #fff; text-align: center; padding: 20px; font-size: 12px; }}
        .button {{ background-color: #5f59ff; color: #FFFFFF; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <img src="https://images.squarespace-cdn.com/content/v1/63f5420164157b677f73c82c/2e4bd485-e7ee-4f14-bea8-f1268e65152b/Metropolis_FullLogo_Black_08302019.png" alt="Metropolis Logo" />
        </div>
        <div class="content">
          <h2>Your Parking Is Reserved</h2>
          <p>Dear Customer,</p>
          <p>Thank you for choosing Metropolis. Your parking reservation is confirmed!</p>

          <div class="details">
            <p><strong>Location:</strong> {location}</p>
            <p><strong>Reservation Time:</strong> {start_time} to {end_time}</p>
          </div>
        </div>
        <div class="footer">
          © 2025 Metropolis. All rights reserved.
        </div>
      </div>
    </body>
    </html>
    """

    # Create MIME message
    msg = MIMEMultipart("alternative")
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach both plain text and HTML versions
    msg.attach(MIMEText(plain_text, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print("Confirmation email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    # Sample test call
    send_confirmation_email(
        to_email="sjha@spplus.com",
        location="123 Main St, Los Angeles, CA",
        start_time="April 10, 2025 – 2:00 PM",
        end_time="4:00 PM",
    )









