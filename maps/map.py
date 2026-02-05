from flask import Flask, render_template_string

import folium
import requests
import json

app = Flask(__name__)


@app.route("/")
def fullscreen():
    """Simple example of a fullscreen map."""
    m = folium.Map(location(35.1418663,-82.500888), zoom_start=7)
    return m.get_root().render()


@app.route("/iframe")
def iframe():
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

    with open('po_latlong.json', 'r') as f:
        data = json.load(f)
        for item in data:
            marker_color = 'blue' if item['visited'] == "true" else 'cadetblue'
            google_link = f"https://www.google.com/maps/search/?api=1&query={item['latitude']},{item['longitude']}"

            popup_text = f"""
            <h4>{item['city']}</h4>
            <b>Street:</b> {item['street']}<br>
            <b>Zip:</b> {item['zip']}<br>
            <b>Status:</b> {'✅ SEENT' if item['visited'] == 'true' else '❌ NOT SEENT'}<br>
            <a href="{google_link}" target="_blank" style="color: blue; text-decoration: underline;">
                Get Directions
            </a>
            """
            
            pop_iframe = folium.IFrame(popup_text, width=200, height=150)
            popup = folium.Popup(pop_iframe, max_width=200)
 
            folium.Marker(
                location=[float(item['latitude']), float(item['longitude'])],
                tooltip=item['city'].title(),
                popup=popup,
                icon=folium.Icon(color=marker_color, icon='envelope'),   
            ).add_to(m)

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    <h1>Using an iframe</h1>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=iframe,
    )


@app.route("/<zip>")
def zip():

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

    with open('po_latlong.json', 'r') as f:
        data = json.load(f)
        for item in data:
            marker_color = 'blue' if item['visited'] == "true" else 'cadetblue'
            google_link = f"https://www.google.com/maps/search/?api=1&query={item['latitude']},{item['longitude']}"

            popup_text = f"""
            <h4>{item['city']}</h4>
            <b>Street:</b> {item['street']}<br>
            <b>Zip:</b> {item['zip']}<br>
            <b>Status:</b> {'✅ SEENT' if item['visited'] == 'true' else '❌ NOT SEENT'}<br>
            <a href="{google_link}" target="_blank" style="color: blue; text-decoration: underline;">
                Get Directions
            </a>
            """
            
            pop_iframe = folium.IFrame(popup_text, width=200, height=150)
            popup = folium.Popup(pop_iframe, max_width=200)
 
            folium.Marker(
                location=[float(item['latitude']), float(item['longitude'])],
                tooltip=item['city'].title(),
                popup=popup,
                icon=folium.Icon(color=marker_color, icon='envelope'),   
            ).add_to(m)

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    <h1>Using an iframe</h1>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=iframe,
    )

if __name__ == "__main__":
    app.run(debug=True)
