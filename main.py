import imaplib
import email
import google.generativeai as genai
from email.header import decode_header
import time
from geopy.geocoders import Nominatim
import json
from reservation import create_reservation
import sqlite3
import re
import os
from dotenv import load_dotenv
from getLoc import getLocationByLatLong

load_dotenv()


def clean_json_string(json_text):
    """Removes triple backticks and 'json' label using regex."""
    return re.sub(r"^```json|```$", "", json_text.strip()).strip()

def get_location_id_by_address(address):
    """Fetch location_id from the SQLite database using the hotel address."""

    print(address)
    
    # Connect to SQLite database
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    # SQL query to find the location_id
    query = "SELECT location_id FROM HOTEL WHERE hotel_address = ?"
    cursor.execute(query, (address,))
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Close connection
    conn.close()

    # Return location_id if found, else None
    return result[0] if result else None
# Email account credentials




def configure_gemini():
    """Configures Gemini API"""
    genai.configure(api_key=os.getenv('GENAI_API_KEY'))

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
    Return the details in JSON format with these fields, the check in and check out time should be in the format YYYY-MM-DDTHH:MM:SS±HH:MM
    Also searcg google for the exact latitude and longitude of the location, and the zipcode of the location if it is not present in the mail
    - hotel_name
    - location
    - city
    - state
    - country
    - check_in
    - check_out
    - zip_code (if present in the mail)
    - reservation_number
    - latitude
    - lognitude

    Email:
    {email_text}
    """

    response = model.generate_content(prompt)

    return response.text  # Returns JSON output from Gemini

def extract_address(data):
    location = data.get("location", "")
    city = data.get("city", "")
    state = data.get("state", "")
    country = data.get("country", "")
    zipcode= data.get("zip_code","")
    
    # Combine the extracted data into an address string
    address = f"{location}, {city}, {state} {zipcode}, {country}"
    return address

def check_email():
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(os.getenv('EMAIL_HOST'))
        mail.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
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


                    res_string = clean_json_string(reservation_info)
                    print("Extracted Reservation Info:", reservation_info)

                    info = json.loads(res_string)
                    address= extract_address(info)
                    print(address)

                    location_id = get_location_id_by_address(address)
                    if(location_id==None):
                       latitude= info.get("latitude","")
                       longitude = info.get("longitude","")
                       location_id = getLocationByLatLong(latitude, longitude)

                    if(location_id):
                        print('creating reservation')
                        res = create_reservation(location_id, info.get('check_in'), info.get('check_out'))
                        print(res)
                    else:
                        print("Could not find any location")


        mail.logout()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    configure_gemini()  
    while True:
        print('Reading Email Data')
        check_email()
        time.sleep(10) 
