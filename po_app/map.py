import folium
import requests
import json

from po_app import app, db
from po_app.models import PO
from flask import url_for
import sqlalchemy as sa

def smallmap(zip):
    po = db.first_or_404(sa.select(PO).where(PO.zip == zip))
    center = [po.latitude, po.longitude]
    marker_color = 'blue' if po.visited else 'cadetblue'
            
    m = folium.Map(
    location=center, 
    zoom_start=14
    )

    folium.Marker(
        location=[po.latitude, po.longitude],
        tooltip=po.city.title(),
        icon=folium.Icon(color=marker_color, icon='envelope'),   
    ).add_to(m)

    # set the iframe width and height
    # m.get_root().width = "200"
    # m.get_root().height = "200"
    m.get_root().width = "100%"
    m.get_root().ratio = "100%"
    
    iframe = m.get_root()._repr_html_()

    return iframe

def bigmap():
    nc_center = [35.42, -79.01]
    nc_bounds = [[31.87, -87.6], [39.32, -68.3]] #[vert, horiz], bottom left, top right
    
    m = folium.Map(
        location=nc_center, 
        max_bounds=True,
        min_lat=nc_bounds[0][0], 
        max_lat=nc_bounds[1][0],
        min_lon=nc_bounds[0][1], 
        max_lon=nc_bounds[1][1],
        zoom_start=6.8,
        zoom_snap=0.1,
        tiles=None
    )
    group_visited = folium.FeatureGroup("Visited").add_to(m)
    group_not_visited = folium.FeatureGroup("Not Visited").add_to(m)
    folium.TileLayer("OpenStreetMap", overlay=True, control=False).add_to(m)    
    folium.LayerControl().add_to(m)


    po = db.session.scalars(sa.select(PO)).all()
    for item in po:
        marker_color = 'blue' if item.visited else 'cadetblue'
        google_link = f"https://www.google.com/maps/search/?api=1&query={item.latitude},{item.longitude}"
        local_link = url_for('zip', zip=str(item.zip), _external=True)

        popup_text = f"""
        <a href="{local_link}" target="_parent"><h4>{item.city}</h4></a>
        <b>Street:</b> {item.street}<br>
        <b>Zip:</b> {item.zip}<br>
        <b>Status:</b> {'✅ SEENT' if item.visited else '❌ NOT SEENT'}<br>
        <a href="{google_link}" target="_blank">
            Get Directions
        </a>
        """

        pop_iframe = folium.IFrame(popup_text, width=200, height=175)
        popup = folium.Popup(pop_iframe)

        if item.visited:
            folium.Marker(
                location=[item.latitude, item.longitude],
                tooltip=item.city.title(),
                popup=popup,
                icon=folium.Icon(color=marker_color, icon='envelope'),   
            ).add_to(group_visited)
        else:
            folium.Marker(
                location=[item.latitude, item.longitude],
                tooltip=item.city.title(),
                popup=popup,
                icon=folium.Icon(color=marker_color, icon='envelope'),   
            ).add_to(group_not_visited)

    # set the iframe width and height
    m.get_root().width = '100%'
    m.get_root().ratio = '40%'
    
    iframe = m.get_root()._repr_html_()
    
    # render = m.get_root().render()
    # iframe = folium.IFrame(render, width='200px', height='200px').render()

    return iframe
