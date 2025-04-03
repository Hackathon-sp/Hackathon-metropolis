import requests 
from send_email import send_confirmation_email  
import os
from dotenv import load_dotenv

load_dotenv()

def create_reservation(location_code, contact_number, first_name, email, start_at, stop_at):
    """Create a reservation by calling the external API."""
    url = "https://dev.parking.dev/v4/reservation"
    headers = {
        "Content-Type": "application/json",
        "clientKey": os.getenv('client_key'),
        "clientName": os.getenv('client_name'),
        "x-api-key": os.getenv('x_api_key')
    }
    payload = {
        
        "orderType": "RESERVATION",
        "location": "99999",
        "name": first_name,
        "countryCode": "+91",
        "email": email,
        "contactNumber": contact_number,
        "startAt": start_at,
        "stopAt": stop_at,
    }
    print('Creating reservation')
    response = requests.post(url, headers=headers, json=payload)  
    if response.status_code == 201:
        print("Reservation Created:")
        return response.json()  
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    

# if __name__ == "__main__":
    
#     response = create_reservation(
#         location_code="99999",
#         contact_number="9123456789",
#         first_name="John",
#         email="johncarter@testemail.com",
#         start_at="2025-07-14T10:00:00-05:00",
#         stop_at="2025-07-20T12:00:00-05:00"
#     )
#     print("Response from create_reservation:", response)
