import json
from datetime import datetime
import requests
from zoneinfo import ZoneInfo  # Only in Python 3.9+
import os
from dotenv import load_dotenv

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to .env file
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(env_path)  # Load .env from the script's directory

url_login = "https://ppaportal.portlink.co/api/accounts/login"

session = requests.Session()

payload = {
    "email": os.getenv('EMAIL'),
    "password": os.getenv('PASSWORD')
}

response = session.post(url_login, json=payload)

def getDataAPI(session, url):
    '''
    Function that collects the data for a given URL using the provided session.
    Returns the 'data' field from the JSON response if successful, else None.
    '''
    try:
        response = session.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

        json_data = response.json()
        return json_data.get('data', None)  # Return 'data' field or None if missing

    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return None

# url for the API with the job board information
url_currentVesselTraffic = "https://ppaportal.portlink.co/api/pdams/GetCurrentVesselTraffic"

currentVesselTraffic = getDataAPI(session, url_currentVesselTraffic)

# url for the API with the position report information
url_positionReport = 'https://ppaportal.portlink.co/api/map/PositionReport'
positionReport = getDataAPI(session, url_positionReport)

# Save them both into one object
collected_data = {
    'currentVesselTraffic': currentVesselTraffic,
    'positionReport': positionReport
}

# Get the current timestamp in a safe filename format
vancouver_time = datetime.now(ZoneInfo("America/Vancouver"))
timestamp = vancouver_time.strftime('%Y-%m-%d_%H-%M-%S')

# Path to data folder relative to the script
filename = f"{timestamp}.json"
data_folder = os.path.join(BASE_DIR, "data")
file_path = os.path.join(data_folder, filename)

# Ensure data folder exists
os.makedirs(data_folder, exist_ok=True)


# Dump to file
with open(file_path, 'w') as f:
    json.dump(collected_data, f, indent=2)

print(f"Saved data to {filename}")
