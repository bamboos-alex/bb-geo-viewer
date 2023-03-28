import folium
import json
import geojson

from bb_geo_tran import UTM52N_To_LatLon
from bb_geo_db import findA2Link
from geojson import MultiLineString, Feature, FeatureCollection


# with open('./A217BR720009.json', mode='rt', encoding='utf-8') as f:
#     geo_xy = json.loads(f.read())
#     f.close()

def create_feature_collection(a2LinkList):
    feature_list = []
    for a2Link in a2LinkList:
        id = a2Link['id']
        geometry = a2Link['geometry']
        property = {"id": id}
        feature = Feature(properties=property, geometry=geometry, id=id)
        feature_list.append(feature)
    
    print(feature_list)   
    feature_collection = FeatureCollection(feature_list)

    return feature_collection
        

## convert UTM52N -> WSG84 geo
def convert_geojson_to_folium(tuple):
    (lat, lon) = UTM52N_To_LatLon(tuple[0], tuple[1])
    return (lon, lat)

## main ##

a2linkList = findA2Link()
print (a2linkList)

geo_xy = create_feature_collection(a2linkList)
geo_latlon = geojson.utils.map_tuples(convert_geojson_to_folium, geo_xy)

m = folium.Map(
    location=UTM52N_To_LatLon(332020.85, 4128721.928), # 신갈 JC
    zoom_start=14,
    tiles=""
)

style_function = lambda x: {
    "color": "#3388ff"
}

folium.GeoJson(
    data=geo_latlon,
    style_function=style_function,
    name='bamboos',
    overlay=True
).add_to(m)


style_function_other = lambda x: {
    "color": "#FF0000"
}

geo_other = geojson.utils.map_coords(lambda x: x, geo_latlon)
# geo_other = geo_latlon

folium.GeoJson(
    data=geo_other,
    style_function=style_function_other,
    name="other",
    overlay=True
).add_to(m)

folium.LayerControl().add_to(m)

m.save('bb-map.html')
