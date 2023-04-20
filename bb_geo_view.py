import folium
import json
import geojson

from bb_geo_tran import UTM52N_To_LatLon
from bb_geo_db import findA2Link, findA7LinkSlice
from geojson import MultiLineString, Feature, FeatureCollection


# with open('./A217BR720009.json', mode='rt', encoding='utf-8') as f:
#     geo_xy = json.loads(f.read())
#     f.close()

def create_feature_collection(a2LinkList):
    feature_list = []
    index = 1
    for a2Link in a2LinkList:
        id = a2Link['id']
        properties = a2Link['properties']
        properties['index'] = index
        geometry = a2Link['geometry']

        feature = Feature(properties=properties, geometry=geometry, id=id)
        feature_list.append(feature)

        index = index + 1

    # print(feature_list)   
    feature_collection = FeatureCollection(feature_list)

    return feature_collection
        

## convert UTM52N -> WSG84 geo
def convert_geojson_to_folium(tuple):
    (lat, lon) = UTM52N_To_LatLon(tuple[0], tuple[1])
    return (lon, lat)

## main ##

a2linkList = findA2Link("")
# a2linkList = findA2Link("A217BR720009")
# print (a2linkList)

geo_xy = create_feature_collection(a2linkList)
geo_latlon = geojson.utils.map_tuples(convert_geojson_to_folium, geo_xy)

m = folium.Map(
    location=UTM52N_To_LatLon(332020.85, 4128721.928), # 신갈 JC
    zoom_start=17,
    tiles=""
)

### A2 LINK Layer

style_function = lambda x: {
    "color": "#3388ff" if int(x["properties"]["index"])%2 == 0 else "#80B5FF"
}
tooltip = folium.GeoJsonTooltip(fields=['id', 'roadType', 'roadNo', 'direction', 'laneNo', 'maxSpeed', 'length','roadRank','linkType',  'fromNodeId', 'toNodeId',  'index'])

folium.GeoJson(
    data=geo_latlon,
    style_function=style_function,
    name='A2_LINK',
    overlay=True,
    tooltip=tooltip
).add_to(m)


### A7 LINK SLICE Layer

a7LinkSliceList = findA7LinkSlice("")
# a7LinkSliceList = findA7LinkSlice("A219AG640002_A7000001")

# style_function_other = lambda x: {
#     #"color": "#FF0000" if int(x["properties"]["indexInA2Link"])%2 == 0 else "#00FF00"
#     "color": "#FF0000" if int(x["properties"]["index"])%2 == 0 else "#00FF00"
# }


def style_function_other(x):
    color = "#FF0000"

    a7_prop = x["properties"]

    
    print (a7_prop)
    
    if (a7_prop["roadType"] == "MAIN_ROAD") :
        if (a7_prop["index"] % 2 == 0):
            color = "#66CDAA"
        else:
            color = "#D3FFCE"
    else:
        if (a7_prop["index"] % 2 == 0):
            color = "#FA8072" 
        else:
            color = "#B74160"

    return {"color": color}

# geo_a7slice_xyz = geojson.loads(open("./a7slice_youngin_4km.geojson", 'r').read())
geo_a7slice_xyz = create_feature_collection(a7LinkSliceList)
geo_a7slice_latlon = geojson.utils.map_tuples(convert_geojson_to_folium, geo_a7slice_xyz)
geo_tooltip = folium.GeoJsonTooltip(fields=['id', 'roadType','roadNo', 'direction', 'laneNo', 'maxSpeed','length', 'prev', 'next', 'a2LinkId',  'indexInA2Link',  'minRow', 'maxRow',  'minColumn',  'maxColumn', 'index'])

folium.GeoJson(
    data=geo_a7slice_latlon,
    style_function=style_function_other,
    name="A7_LINK_SLICE",
    overlay=True,
    tooltip=geo_tooltip
).add_to(m)

folium.LayerControl().add_to(m)

m.save('bb-map.html')
