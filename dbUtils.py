import sqlite3
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

def get_location_id_by_address(address):
    """Fetch location_id from the SQLite database using the hotel address."""
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()
    query = "SELECT location_id FROM HOTEL WHERE hotel_address = ?"
    cursor.execute(query, (address,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def getLocationByLatLong(latitude, longitude):
    """Fetch location_id from MySQL using latitude and longitude proximity."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    query = """
        SELECT l.LOCATION_ID, CONCAT_WS(', ', a.ADDRESS1, a.ADDRESS2, a.CITY) AS full_address,
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
        HAVING distance <= 0.5 
        ORDER BY distance ASC 
        LIMIT 1;
    """
    cursor.execute(query, (latitude, longitude, latitude))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_location_address(location_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    query = """
        SELECT  CONCAT_WS(', ', a.ADDRESS1, a.ADDRESS2, a.CITY) AS full_address
        FROM LOCATION.ADDRESS a 
        LEFT JOIN LOCATION.LOCATION l ON l.LOCATION_KEY = a.LOCATION_KEY 
        WHERE a.ADDRESS_TYPE_KEY = 2 
          AND l.LOCATION_ID =%s
    """
    cursor.execute(query, (location_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None