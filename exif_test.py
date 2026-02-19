import exif
import os
import json
from datetime import datetime

with open('data/po.json', 'r') as f:
    data = json.load(f)
    
for item in data:
    if item['visited']:
        image_name = ''.join(word.capitalize() for word in item["city"].split(' ')) + ".jpg"
        image_path = os.path.join('po_app', 'static', image_name)
        print(image_path)
        
        
        with open(image_path, 'rb') as image_file:
            exif_data = exif.Image(image_file)
            if exif_data.has_exif:   
                if exif_data.get("datetime"):
                    # visited_date = datetime.strptime(exif_data.datetime, "%Y:%m:%d %H:%M:%S")
                    item['visited_date'] = exif_data.datetime
                    print(f"{item['zip']} was visited on {item['visited_date']}")
            else:
                item['visited_date'] = None
                print(f"{item['zip']} was visited on {item['visited_date']}")
                
with open('data/po_time.json', 'w') as file:
    json.dump(data, file, indent=4)
                
                    
                    

# filename = 'po_app/static/Saxapahaw.jpg'

# with open(filename, 'rb') as img_file:
#     image = exif.Image(img_file)
#     list_all = sorted(image.list_all())
#     for tag in list_all:
#         print(f"{tag}: {image.get(tag)}")
#     image_date = datetime.strptime(image.datetime, "%Y:%m:%d %H:%M:%S")
#     print(image_date.strftime("%B %d, %Y"))
        
    #print(f"{os.path.splitext(os.path.basename(filename))[0]} was visited on {image_date.strftime("%B %d, %Y")}")