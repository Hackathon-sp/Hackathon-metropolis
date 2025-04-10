import imaplib, email
from email.header import decode_header
import os
import json
from dotenv import load_dotenv
from utils import extract_reservation_info, clean_json_string, extract_email_body, extract_address, format_datetime
from dbUtils import get_location_id_by_address, getLocationByLatLong, get_location_address
from reservation import create_reservation
from sendEmail import send_confirmation_email

load_dotenv()

def check_email():
    try:
        mail = imaplib.IMAP4_SSL(os.getenv('EMAIL_HOST'))
        mail.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()

        for email_id in email_ids:
            _, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    subject = subject.decode(encoding) if isinstance(subject, bytes) and encoding else subject
                    sender = msg.get("From")

                    print(f"New Email from {sender}: {subject}")
                    email_body = extract_email_body(msg)
                    reservation_info = extract_reservation_info(email_body)
                    print(reservation_info)
                    res_string = clean_json_string(reservation_info)
                    info = json.loads(res_string)

                    address = extract_address(info)
                    location_id = get_location_id_by_address(address)

                    if not location_id:
                        location_id = getLocationByLatLong(info.get("latitude"), info.get("longitude"))

                    locationAddress = get_location_address(location_id)
                    print(locationAddress)
                    if location_id:
                        res = create_reservation(location_id, info.get("check_in"), info.get("check_out"))
                        startTime = format_datetime(info.get("check_in"))
                        endTime = format_datetime(info.get("check_out"))
                        print(res)
                        send_confirmation_email("sjha@spplus.com", locationAddress, startTime, endTime)

                    else:
                        print("Could not find any location")

        mail.logout()
    except Exception as e:
        print(f"Error: {e}")
