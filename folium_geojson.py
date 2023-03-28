import folium
import json
import geojson

from bb_geo_tran import UTM52N_To_LatLon

with open('./A217BR720009.json', mode='rt', encoding='utf-8') as f:
    geo_xy = json.loads(f.read())
    f.close()

## convert UTM52N -> WSG84 geo
def convert_geojson_to_folium(tuple):
    (lat, lon) = UTM52N_To_LatLon(tuple[0], tuple[1])
    return (lon, lat)

geo_latlon = geojson.utils.map_tuples(convert_geojson_to_folium, geo_xy)

m = folium.Map(
    location=UTM52N_To_LatLon(332020.85, 4128721.928),
    zoom_start=18
)

folium.GeoJson(
    geo_latlon,
    name='bamboos'
).add_to(m)

folium.LayerControl().add_to(m)

m.save('bb-map.html')
