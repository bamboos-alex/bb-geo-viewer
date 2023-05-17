import folium
import json
import geojson

from bb_geo_tran import UTM52N_To_LatLon
from bb_geo_db import find, find_manual_sql
from geojson import MultiLineString, Feature, FeatureCollection
from folium import Marker

flag_with_bg = True

if (flag_with_bg) :
    HTML_FILE_NAME='bb-map-bg-pangyo.html'
else :
    HTML_FILE_NAME='bb-map-pangyo.html'

# main ##

if (flag_with_bg) :
    m = folium.Map(
        location=UTM52N_To_LatLon(332967.7981256369, 4141269.55194718), # 판교테크노중앙 사거리
        zoom_start=15,
        tiles="OpenStreetMap"
    )
else :
    m = folium.Map(
        location=UTM52N_To_LatLon(332967.7981256369, 4141269.55194718), # 판교테크노중앙 사거리
        zoom_start=15,
        tiles=""
    )


def create_feature_collection(linkList):
    feature_list = []
    index = 1
    for link in linkList:
        id = link['id']
        properties = link['properties']
        properties['index'] = index
        geometry = link['geometry']

        if ('roadNo' not in properties):
            properties['roadNo'] = 'NULL'

        if ('direction' not in properties):
            properties['direction'] = 'NULL'

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

## A2 Link

a2Request = {'hdMapType': "A2_LINK"}
a2LinkList = find(a2Request)

print("#############################################")
print (a2LinkList)
print("#############################################")

geo_xy = create_feature_collection(a2LinkList)
geo_latlon = geojson.utils.map_tuples(convert_geojson_to_folium, geo_xy)

### A2 LINK Layer


def style_function_a2(x):
    color = "#3388ff"
    a2_prop = x["properties"]
    if (a2_prop["linkType"] == "1") :
        if (a2_prop["index"] % 2 == 0):
            color = "#bec8b9" 
        else:
            color = "#dfd6cd"
    elif (a2_prop["linkType"] == "4"):
        color = "#00cc99"
        if (a2_prop["index"] % 2 == 0):
            color = "#ec33ec" 
        else:
            color = "#ff97d1"

    elif (a2_prop["linkType"] == "6"):
        if (a2_prop["index"] % 2 == 0):
            color = "#1034a6" 
        else:
            color = "#0779bf"

    else:
        color = "#fbbcec"
        

    return {"color": color}


a2_fields=['id', 'roadType', 'roadNo', 'direction', 'laneNo', 'maxSpeed', 'length','roadRank','linkType',  'fromNodeId', 'toNodeId',  'index']

tooltip = folium.GeoJsonTooltip(fields=a2_fields)
popup = folium.GeoJsonPopup(fields=a2_fields)

folium.GeoJson(
    data=geo_latlon,
    style_function=style_function_a2,
    name='A2_LINK',
    overlay=True,
    tooltip=tooltip,
    popup=popup
).add_to(m)


### A7 LINK SLICE Layer
a7Request = {"hdMapType": "A7_LINK_SLICE"}
a7LinkList = find(request=a7Request)

print("#############################################")
print(a7LinkList);
print("#############################################")

def style_function_other(x):
    color = "#FF0000"

    a7_prop = x["properties"]

    
    #print (a7_prop)
    
    if (a7_prop["roadType"] == "MAIN_ROAD") :

        if (a7_prop["length"] == 100):        
            if (a7_prop["index"] % 2 == 0):
                color = "#66CDAA"
            else:
                color = "#BADA55"
        else:
            if (a7_prop["index"] % 2 == 0):
                color = "#B6FCD5"
            else:
                color = "#D3FFCE"
            
    elif (a7_prop["roadType"] == "RAMP"):
        if (a7_prop["index"] % 2 == 0):
            color = "#FA8072" 
        else:
            color = "#B74160"
    else:
        if (a7_prop["index"] % 2 == 0):
            color = "#edb3eb" 
        else:
            color = "#ec33ec"
    
    if (a7_prop["linkType"] == "1") :
        if (a7_prop["index"] % 2 == 0):
            color = "#990b11" 
        else:
            color = "#caacaf"
 
    if (a7_prop["linkType"] == "4"):
        if (a7_prop["index"] % 2 == 0):
            color = "#00cc99" 
        else:
            color = "#2eb561"
 

    return {"color": color}


a7_fields=['id', 'roadType','roadNo', 'direction', 'laneNo', 'maxSpeed','length','roadRank','linkType',  'prev', 'next', 'a2LinkId',  'indexInA2Link',  'minRow', 'maxRow',  'minColumn',  'maxColumn', 'index']
geo_tooltip = folium.GeoJsonTooltip(fields=a7_fields)
geo_popup = folium.GeoJsonPopup(fields=a7_fields)

geo_a7slice_xyz = create_feature_collection(a7LinkList)
geo_a7slice_latlon = geojson.utils.map_tuples(convert_geojson_to_folium, geo_a7slice_xyz)


folium.GeoJson(
    data=geo_a7slice_latlon,
    style_function=style_function_other,
    name="A7_LINK_SLICE",
    overlay=True,
    tooltip=geo_tooltip,
    popup=geo_popup
).add_to(m)

folium.LayerControl(position='topright', collapsed=False).add_to(m)

m.save(HTML_FILE_NAME)
