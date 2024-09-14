import requests
import sqlite3
import json
import time

# URL of the dump1090 JSON feed
DUMP1090_URL = 'http://localhost:8080/data.json'

# SQLite database file
DB_FILE = 'adsb_data.db'

# Create a connection to the SQLite database
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# Create a table to store ADS-B data
c.execute('''
    CREATE TABLE IF NOT EXISTS adsb_data (
        hex TEXT,
        flight TEXT,
        time TEXT, 
        lat REAL,
        lon REAL,
        altitude INTEGER,
        speed INTEGER,
        gs REAL,
        track REAL,
        seen_pos REAL,
        seen REAL,
        rssi REAL
    )
''')
conn.commit()

def fetch_data():
    response = requests.get(DUMP1090_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

def insert_data(data):
    for aircraft in data:
        c.execute('''
            INSERT INTO adsb_data (hex, flight, time, lat, lon, altitude, speed, gs, track, seen_pos, seen, rssi)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            aircraft.get('hex'),
            aircraft.get('flight'),
            time.ctime(),
            aircraft.get('lat'),
            aircraft.get('lon'),
            aircraft.get('altitude'),
            aircraft.get('speed'), 
            aircraft.get('gs'),
            aircraft.get('track'),
            aircraft.get('seen_pos'),
            aircraft.get('seen'),
            aircraft.get('rssi')
        ))
    conn.commit()

def main():
    while True:
        data = fetch_data()
        if data:
            insert_data(data)
        time.sleep(5)  # Fetch data every 5 seconds

if __name__ == '__main__':
    main()
