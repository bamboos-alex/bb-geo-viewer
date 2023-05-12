import folium
import json

from bb_geo_tran import UTM52N_To_LatLon
from bb_geo_db import find_manual_sql

from folium.plugins import MarkerCluster
from folium import Marker

## convert UTM52N -> WSG84 geo
def convert_geojson_to_folium(tuple):
    (lat, lon) = UTM52N_To_LatLon(tuple[0], tuple[1])
    return (lon, lat)

points = find_manual_sql();

m = folium.Map(
    location=UTM52N_To_LatLon(332020.85, 4128721.928), # 신갈 JC
    zoom_start=10,
    # tiles=""
    tiles="OpenStreetMap"
)

for point in points:
    print(point)

   # print(point['geometry']['coordinates'])
    (lon, lat) = convert_geojson_to_folium(point['geometry']['coordinates'])
    
    location = [lat, lon]
    name=point['properties']['name']
    id=point['id']
    #popup='id=' + id + ' name='+ name
    properties = point['properties']
    popup=json.dumps(properties, indent=2)

   # print(location)

    Marker(location=location, popup=popup).add_to(m)

m.save('bb-map-bg-Z2_IC_JC.html')

