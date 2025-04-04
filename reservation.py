import requests 
import os
from dotenv import load_dotenv

load_dotenv()

def create_reservation(location,  startAt, stopAt, contactNumber = "9123456789", name= 'xxx', email = 'xxx@email.com',):
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
        "location": location,
        "name": name,
        "countryCode": "+91",
        "email": email,
        "contactNumber": contactNumber,
        "startAt": startAt,
        "stopAt": stopAt,
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