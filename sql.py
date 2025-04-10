import sqlite3
connections = sqlite3.connect('hotel.db')
cursor = connections.cursor()

create_table = """
CREATE TABLE HOTEL(
    hotel_name VARCHAR(100),
    hotel_address VARCHAR(100),
    location_id VARCHAR(10),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(25)
)
"""
cursor.execute(create_table)

# Insert data into the table
data = [
    ('Redmont Hotel Birmingham, Curio Collection by Hilton','2101 5th Ave N, Birmingham, AL 35203, United States', '51762', '2101 5th Ave N, Burmingham, AL', 'North Burmingham', 'AL'),
    ('Holiday Inn Express Kansas City Downtown','417 E 13th St, Kansas City, MO 64106, United States', '00970', '1401 Oak Kansas City, MO ', 'Kansas City', 'MO'),
    ('Courtyard Springfield Airport','3527 W Kearney St, Springfield, MO 65803, United States', '02855', '2300 N, Airport Boulevard, Springfield, MO ', 'Springfield', 'MO'),
    ('Courtyard Springfield Airport','3527 W Kearney St, Springfield, MO 65803, United States','03592', "1001, Gravier's St., New Orleans, LA", 'New Orleans', 'LA'),
    ('Hyatt Place New York / Chelsea', '140 W 24th St, New York, NY 10011, United States','06120', '133 west 22nd St, New York, New York', 'New York', 'NY'),
]

cursor.executemany("INSERT INTO HOTEL VALUES (?, ?, ?, ?, ?, ?)", data)

# Commit and close
connections.commit()
connections.close()