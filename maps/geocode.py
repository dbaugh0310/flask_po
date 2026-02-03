# importing geopy library and Nominatim class
from geopy.geocoders import Nominatim
import json
import time

# calling the Nominatim tool and create Nominatim class
loc = Nominatim(user_agent="po_app")

with open('po.json', 'r') as file:
    # Use json.load() to parse the file content into a Python object
    data = json.load(file)

dict_of_data = {item['zip']: item for item in data}

for z_code in dict_of_data:
    inner_dict = dict_of_data[z_code]
    inner_dict['street'] = inner_dict.pop('address')

    #location = dict_of_data[zip]['street'], dict_of_data[zip]['city'], dict_of_data[zip]['state']
    location = dict_of_data[z_code]

    print(type(location))
    print(location)

    # entering the location name
    #getLoc = loc.geocode(location)
    #dict_of_data[zip].update({'latitude': getLoc.latitude, 'longitude': getLoc.longitude})

    # printing address
    #print('Resulting Address')
    #print(getLoc.address)

    # printing latitude and longitude
    #print("Latitude = ", getLoc.latitude, "\n")
    #print("Longitude = ", getLoc.longitude)
    #print(dict_of_data[zip])
    #time.sleep(5)