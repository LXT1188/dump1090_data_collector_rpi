import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cartopy.crs as ccrs
from datetime import datetime

# SQLite database file
DB_FILE = 'adsb_data.db'

# Create a connection to the SQLite database
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# Fetch all data from the adsb_data table
c.execute('SELECT hex, flight, time, lat, lon, altitude FROM adsb_data')
data = c.fetchall()

# Close the database connection
conn.close()

# Parse the time column into datetime objects and sort the data by time
data = [(row[0], row[1], datetime.strptime(row[2], '%a %b %d %H:%M:%S %Y'), row[3], row[4], row[5]) for row in data]
data.sort(key=lambda x: x[2])

# Extract latitude, longitude, and altitude data, ensuring no None values
lats = np.array([row[3] for row in data if row[3] is not None])
lons = np.array([row[4] for row in data if row[4] is not None])
alts = np.array([row[5] for row in data if row[5] is not None])

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Dictionary to store flight paths
flight_paths = {}

# Organize data by aircraft
for row in data:
    hex_code = row[0]
    if hex_code not in flight_paths:
        flight_paths[hex_code] = {'lats': [], 'lons': [], 'alts': []}
    flight_paths[hex_code]['lats'].append(row[3])
    flight_paths[hex_code]['lons'].append(row[4])
    flight_paths[hex_code]['alts'].append(row[5])

# Plot the flight paths in 3D
for hex_code, path in flight_paths.items():
    lats = np.array(path['lats'])
    lons = np.array(path['lons'])
    alts = np.array(path['alts'])
    ax.plot(lons, lats, alts, label=hex_code)

# Set labels
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Altitude (m)')

# Make the plane axes transparent
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

# Show the plot
plt.show()
