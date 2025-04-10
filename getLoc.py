import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


def getLocationByLatLong(latitude , longitude):
    """Fetch location_id from MySQL using an exact match for the address."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    query = """
        SELECT l.LOCATION_ID,
        (3958.8 * ACOS(
            COS(RADIANS(%s)) * COS(RADIANS(LATITUDE)) * 
            COS(RADIANS(LONGITUDE) - RADIANS(%s)) + 
            SIN(RADIANS(%s)) * SIN(RADIANS(LATITUDE))
        )) AS distance
        FROM LOCATION.ADDRESS a 
        LEFT JOIN LOCATION.LOCATION l ON l.LOCATION_KEY = a.LOCATION_KEY 
        WHERE a.ADDRESS_TYPE_KEY = 2 
          AND l.IS_AVAILABLE_TO_SELL = 1 
          AND l.IS_PUBLISHED_TO_WEB = 1 
          AND l.IS_CLOSED = 0
        HAVING distance <= 0.3 
        ORDER BY distance ASC 
        LIMIT 10;
    """
    cursor.execute(query, (latitude,longitude,latitude))

    result = cursor.fetchone()
    conn.close()
    print(result)

    return result[0] if result else None
