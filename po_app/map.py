import folium
import requests
import json

from po_app import app, db
from po_app.models import PO
import sqlalchemy as sa

def bigmap():
    nc_center = [35.7596, -79.0193]
    nc_bounds = [[33.7, -84.4], [36.6, -75.3]]
    
    m = folium.Map(
        location=nc_center, 
        max_bounds=True,
        min_lat=nc_bounds[0][0], 
        max_lat=nc_bounds[1][0],
        min_lon=nc_bounds[0][1], 
        max_lon=nc_bounds[1][1],
        zoom_start=6.8,
        zoom_snap=0.1
    )

    po = db.session.scalars(sa.select(PO)).all()
    print(type(po))
    for item in po:
        marker_color = 'blue' if item.visited else 'cadetblue'
        google_link = f"https://www.google.com/maps/search/?api=1&query={item.latitude},{item.longitude}"

        popup_text = f"""
        <h4>{item.city}</h4>
        <b>Street:</b> {item.street}<br>
        <b>Zip:</b> {item.zip}<br>
        <b>Status:</b> {'✅ SEENT' if item.visited else '❌ NOT SEENT'}<br>
        <a href="{google_link}" target="_blank" style="color: blue; text-decoration: underline;">
            Get Directions
        </a>
        """

        pop_iframe = folium.IFrame(popup_text, width=200, height=150)
        popup = folium.Popup(pop_iframe, max_width=200)

        folium.Marker(
            location=[item.latitude, item.longitude],
            tooltip=item.city.title(),
            popup=popup,
            icon=folium.Icon(color=marker_color, icon='envelope'),   
        ).add_to(m)

    # set the iframe width and height
    m.get_root().width = "900px"
    m.get_root().height = "450px"
    
    iframe = m.get_root()._repr_html_()

    return iframe
