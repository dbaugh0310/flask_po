import requests
import json
import time

# USGS Structures API Endpoint for Post Offices (Layer 2 or 3 in the MapServer)
USGS_URL = "https://carto.nationalmap.gov/arcgis/rest/services/structures/MapServer/3/query"

def get_official_coordinates(zip_code):
    params = {
        'where': f"ZIP = '{zip_code}'",
        'outFields': 'LATITUDE,LONGITUDE,NAME',
        'f': 'json'
    }
    try:
        response = requests.get(USGS_URL, params=params, timeout=10)
        data = response.json()
        if data.get('features'):
            # Return the first match's attributes
            attrs = data['features'][0]['attributes']
            return attrs['LATITUDE'], attrs['LONGITUDE']
    except Exception as e:
        print(f"Error checking {zip_code}: {e}")
    return None, None

# Load your local data
with open('po.json', 'r') as f:
    po_data = json.load(f)

for po in po_data:
    zip_code = po['zip']
    official_lat, official_lon = get_official_coordinates(zip_code)
    
    if official_lat:
        # Check if your current coordinates are 'significantly' different 
        # (e.g., more than 0.01 degrees, roughly 1km)
        lat_diff = abs(po['latitude'] - official_lat)
        lon_diff = abs(po['longitude'] - official_lon)
        
        if lat_diff > 0.01 or lon_diff > 0.01:
            print(f"⚠️ DISCREPANCY found for {po['city']} ({zip_code})")
            print(f"   Current: {po['latitude']}, {po['longitude']}")
            print(f"   Official: {official_lat}, {official_lon}")
            
            # Auto-fix: Uncomment the line below to update your JSON data
            # po['latitude'], po['longitude'] = official_lat, official_lon
    
    # Be kind to the API
    time.sleep(0.2)

# Save the audited file
with open('po_audited.json', 'w') as f:
    json.dump(po_data, f, indent=4)