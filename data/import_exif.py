from exif import Image
import os
from datetime import datetime

with open('../po_app/static/Moncure.jpg', 'rb') as image_file:
    image = Image(image_file)
    visited = datetime.strptime(image.datetime, '%Y:%m:%d %H:%M:%S')

    print(f"EXIF data says: {image.datetime}")
    print(f"Datetime says: {datetime.strftime(visited, '%B %d, %Y')}")