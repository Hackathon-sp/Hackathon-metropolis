import imaplib
import email
import google.generativeai as genai
from email.header import decode_header
import time
from geopy.geocoders import Nominatim
import json
# Email account credentials
EMAIL_HOST = "imap.gmail.com"
EMAIL_USER = "hackathon949@gmail.com"
EMAIL_PASS = "fsgs iiqs jfsf fhnn"

# Gemini API Key
GENAI_API_KEY = "AIzaSyCVyCvxN2G9IaDcwSadza53fJCoqFCEUe4"

def configure_gemini():
    """Configures Gemini API"""
    genai.configure(api_key=GENAI_API_KEY)

def extract_email_body(msg):
    """Extracts the plain text body from an email."""
    body = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = msg.get_payload(decode=True).decode()
    
    return body

def extract_reservation_info(email_text):
    """Sends the email text to Gemini API for processing."""

    print('Inside extract res info')
    
    model = genai.GenerativeModel("gemini-1.5-pro")


    prompt = f"""
    Extract hotel reservation details from this email.
    Return the details in JSON format with these fields:
    - hotel_name
    - location
    - city
    - state
    - check_in
    - check_out
    - zip code (if present in the mail)
    - reservation_number

    Also give me the latitude and longitude of the location, and the zipcode of the location if it is not present in the mail
    - latitude
    - lognitude
    - zip code

    Email:
    {email_text}
    """

    response = model.generate_content(prompt)

    return response.text  # Returns JSON output from Gemini

def check_email():
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(EMAIL_HOST)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        # Search for unread emails
        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()

        for email_id in email_ids:
            _, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes) and encoding:
                        subject = subject.decode(encoding)
                    
                    sender = msg.get("From")
                    print(f"New Email from {sender}: {subject}")

                    # Extract email body
                    email_body = extract_email_body(msg)
                    print("Email Body Extracted")

                    # Send email body to Gemini API
                    reservation_info = extract_reservation_info(email_body)
                    print("Extracted Reservation Info:", reservation_info)

                    # print(type(reservation_info))

                    # json_data = json.loads(reservation_info)

                    # getLatLong(json_data)

        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

# def getLatLong(body):
#     print('inside lat long')
#     geolocator = Nominatim(user_agent = "hotel_locator")
#     address = body.location + ','+ body.city + body.state
#     print(address)
#     location = geolocator.geocode(address)
#     if(location):
#         print(location.latitude)
#         print(location.longitude)
#     else:
#         print('adf')

if __name__ == "__main__":
    configure_gemini()  # Initialize Gemini API
    while True:
        print('Reading Email Data')
        check_email()
        time.sleep(60)  # Check every 60 seconds
