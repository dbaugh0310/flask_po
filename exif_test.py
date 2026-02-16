import exif
import os
from datetime import datetime

filename = 'po_app/static/Moncure.jpg'

with open(filename, 'rb') as img_file:
    image = exif.Image(img_file)
    # list_all = sorted(image.list_all())
    # for tag in list_all:
    #     print(f"{tag}: {image.get(tag)}")
    image_date = datetime.strptime(image.datetime, "%Y:%m:%d %H:%M:%S")
    print(image_date.strftime("%B %d, %Y"))
    print(image_date.time())
        
    #print(f"{os.path.splitext(os.path.basename(filename))[0]} was visited on {image_date.strftime("%B %d, %Y")}")
# 2010:04:04 13:28:20