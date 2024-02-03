import streamlit as st
import random
import requests
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

df = df[pd.isna(df['latitude'])]

print(df)

from geopy.geocoders import Nominatim

# Assuming df is your DataFrame and it contains a column named 'Bar' with the names of the bars

# Initialize the Nominatim geocoder
geolocator = Nominatim(user_agent="streamlitTest")


# entering the location name
getLoc = geolocator.geocode("Chaos - Geologisk Fredagsbar")

# printing address
print(getLoc.address)

# printing latitude and longitude
print("Latitude = ", getLoc.latitude, "\n")
print("Longitude = ", getLoc.longitude)


# Define a function to fetch latitude and longitude
def fetch_lat_lon(bar_name):
    try:
        time.sleep(3)
        location = geolocator.geocode(bar_name + ", Aarhus")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching location for {bar_name}: {e}")
        time.sleep(3)
        return None, None

# Apply the function to each row in the DataFrame
df['latitude'], df['longitude'] = zip(*df['Bar'].apply(lambda x: fetch_lat_lon(x)))

# Now df should have 'latitude' and 'longitude' columns filled with the respective data

print(df)