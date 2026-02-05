"""flask_example.py

Required packages:
- flask
- folium

Usage:

Start the flask server by running:

    $ python flask_example.py

And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import Flask, render_template_string

import folium
import requests

app = Flask(__name__)


@app.route("/")
def fullscreen():
    """Simple example of a fullscreen map."""
    m = folium.Map(location(35.1418663,-82.500888), zoom_start=7)
    return m.get_root().render()


@app.route("/iframe")
def iframe():

    geo_json_data = requests.get(
    "https://raw.githubusercontent.com/glynnbird/usstatesgeojson/refs/heads/master/north%20carolina.geojson"
    ).json()

    m = folium.Map(location=(35.53126396839661, -79.52843330891112), zoom_start=6)
    folium.GeoJson(geo_json_data).add_to(m)

    with open('data/po.json', 'r') as f:
        data = json.load(f)
        for item in data:
 
            folium.Marker(
                location=[item[latitude], item[longitude]],
                tooltip=item[city],
                popup=item[city],
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


@app.route("/components")
def components():
    """Extract map components and put those on a page."""
    m = folium.Map(
        width=800,
        height=600,
    )

    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head>
                    {{ header|safe }}
                </head>
                <body>
                    <h1>Using components</h1>
                    {{ body_html|safe }}
                    <script>
                        {{ script|safe }}
                    </script>
                </body>
            </html>
        """,
        header=header,
        body_html=body_html,
        script=script,
    )


if __name__ == "__main__":
    app.run(debug=True)
