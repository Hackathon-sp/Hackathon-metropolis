import google.generativeai as genai
import os
import re
from dateutil import parser

def configure_gemini():
    genai.configure(api_key=os.getenv('GENAI_API_KEY'))

def clean_json_string(json_text):
    return re.sub(r"^```json|```$", "", json_text.strip()).strip()

def extract_reservation_info(email_text):
    """Sends the email text to Gemini API for processing."""

    print('Extracting Reservation Info')
    
    model = genai.GenerativeModel("gemini-1.5-pro")


    prompt = f"""
    Extract hotel reservation details from this email.
    Return the details in JSON format with these fields, the check in and check out time should be in the format YYYY-MM-DDTHH:MM:SS±HH:MM. If the check in and check out time 
    does not exist it in the mail set that time to 12PM
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

    return response.text 

def extract_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()
    return msg.get_payload(decode=True).decode()

def extract_address(data):
    location = data.get("location", "")
    city = data.get("city", "")
    state = data.get("state", "")
    country = data.get("country", "")
    zipcode = data.get("zip_code", "")
    return f"{location}, {city}, {state} {zipcode}, {country}"

def format_datetime(iso_string):
    dt = parser.isoparse(iso_string)  
    return dt.strftime("%B %d, %Y – %-I:%M %p")
