# importing geopy library and Nominatim class
from geopy.geocoders import Nominatim
import json
import time

# calling the Nominatim tool and create Nominatim class
loc = Nominatim(user_agent="po_app", timeout=10)

with open('po.json', 'r') as file:
    # Use json.load() to parse the file content into a Python object
    data = json.load(file)

dict_of_data = {item['zip']: item for item in data}

for z_code in dict_of_data:

    location = {'amenity': 'post_office', "city": dict_of_data[z_code]['city'], "state": dict_of_data[z_code]['state'], "zip": dict_of_data[z_code]['zip']}
    #location = dict_of_data[z_code]

    print("Location is of type: ", type(location), "Location = ", location)

    try: 
        getLoc = loc.geocode(location)
        
        if getLoc:
            dict_of_data[z_code].update({'latitude': getLoc.latitude, 'longitude': getLoc.longitude,})
            print('Resulting Address: ', getLoc.address)
            print("Lat/Long = ", getLoc.latitude, "/", getLoc.longitude)
            print(dict_of_data[z_code])
        else:
            print(f"No match found for {location['city']}")
            
    except Exception as e:
        print(f"Error connecting to service: {e}")    
 
    # printing latitude and longitude
    time.sleep(1)
    
# Convert the dictionary back into a list of objects
updated_list = list(dict_of_data.values())

# Writing the updated data back to the file
with open('po_latlong.json', 'w') as file:
    json.dump(updated_list, file, indent=4)

print("File updated successfully!")