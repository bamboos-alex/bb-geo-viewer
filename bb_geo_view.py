import folium
import json
import geojson

from bb_geo_tran import UTM52N_To_LatLon
from bb_geo_db import find, find_manual_sql
from geojson import MultiLineString, Feature, FeatureCollection
from folium import Marker


HTML_FILE_NAME='bb-map-bg-a7-road-number-1-50.html'

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

## main ##

m = folium.Map(
    location=UTM52N_To_LatLon(332020.85, 4128721.928), # 신갈 JC
    zoom_start=10,
    # tiles=""
    tiles="OpenStreetMap"
)


## A2 Link

roadNo_50_Direction_E = {"roadNo": "50", "direction": "E"}
roadNo_50_Direction_S = {"roadNo": "50", "direction": "S"}
roadNo_50 = {"roadNo": "50", "direction": ""}
roadNo_1_Direction_E = {"roadNo": "1", "direction": "E"}
roadNo_1_Direction_S = {"roadNo": "1", "direction": "S"}
roadNo_1 = {"roadNo": "1", "direction": ""}
roadNo_null = {"roadNo": None, "direction": None}
roadNo_100_Direction_E = {"roadNo": "100", "direction": "E"}
roadNo_100_Direction_S = {"roadNo": "100", "direction": "S"}


a2Request_1 = {"hdMapType": "A2_LINK"}
a2Request_1.update(roadNo_1)
a2LinkList_1 = find(request=a2Request_1)

a2Request_50 = {"hdMapType": "A2_LINK"} 
a2Request_50.update(roadNo_50)
a2LinkList_50 = find(request=a2Request_50)


print("#############################################")
print (a2LinkList_1)
print("#############################################")
print (a2LinkList_50)
print("#############################################")

# geo_xy = create_feature_collection(a2LinkList_1_E)
geo_xy_1 = create_feature_collection(a2LinkList_1)
geo_latlon_1 = geojson.utils.map_tuples(convert_geojson_to_folium, geo_xy_1)

geo_xy_50 = create_feature_collection(a2LinkList_50)
geo_latlon_50 = geojson.utils.map_tuples(convert_geojson_to_folium, geo_xy_50)

### A2 LINK Layer

style_function = lambda x: {
    "color": "#3388ff" if int(x["properties"]["index"])%2 == 0 else "#80B5FF"
}
a2_fields=['id', 'roadType', 'roadNo', 'direction', 'laneNo', 'maxSpeed', 'length','roadRank','linkType',  'fromNodeId', 'toNodeId',  'index']

tooltip_1 = folium.GeoJsonTooltip(fields=a2_fields)
popup_1 = folium.GeoJsonPopup(fields=a2_fields)

tooltip_50 = folium.GeoJsonTooltip(fields=a2_fields)
popup_50 = folium.GeoJsonPopup(fields=a2_fields)

folium.GeoJson(
    data=geo_latlon_1,
    style_function=style_function,
    name='A2_LINK_RoadNo_1',
    overlay=True,
    tooltip=tooltip_1,
    popup=popup_1
).add_to(m)

folium.GeoJson(
    data=geo_latlon_50,
    style_function=style_function,
    name='A2_LINK_RoadNo_50',
    overlay=True,
    tooltip=tooltip_50,
    popup=popup_50
).add_to(m)



### A7 LINK SLICE Layer
a7Request_1 = {"hdMapType": "A7_LINK_SLICE"}
a7Request_1.update(roadNo_1)
a7LinkList_1 = find(request=a7Request_1)

a7Request_50 = {"hdMapType": "A7_LINK_SLICE"}
a7Request_50.update(roadNo_50)
a7LinkList_50 = find(request=a7Request_50)

print("#############################################")
print(a7LinkList_1);
print("#############################################")
print(a7LinkList_50)
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
            
    else:
        if (a7_prop["index"] % 2 == 0):
            color = "#FA8072" 
        else:
            color = "#B74160"

    return {"color": color}


a7_fields=['id', 'roadType','roadNo', 'direction', 'laneNo', 'maxSpeed','length', 'prev', 'next', 'a2LinkId',  'indexInA2Link',  'minRow', 'maxRow',  'minColumn',  'maxColumn', 'index']
geo_tooltip_1 = folium.GeoJsonTooltip(fields=a7_fields)
geo_popup_1 = folium.GeoJsonPopup(fields=a7_fields)


geo_tooltip_50 = folium.GeoJsonTooltip(fields=a7_fields)
geo_popup_50 = folium.GeoJsonPopup(fields=a7_fields)

geo_a7slice_xyz_1 = create_feature_collection(a7LinkList_1)
geo_a7slice_latlon_1 = geojson.utils.map_tuples(convert_geojson_to_folium, geo_a7slice_xyz_1)

geo_a7slice_xyz_50 = create_feature_collection(a7LinkList_50)
geo_a7slice_latlon_50 = geojson.utils.map_tuples(convert_geojson_to_folium, geo_a7slice_xyz_50)

folium.GeoJson(
    data=geo_a7slice_latlon_1,
    style_function=style_function_other,
    name="A7_LINK_SLICE_RoadNo_1",
    overlay=True,
    tooltip=geo_tooltip_1,
    popup=geo_popup_1
).add_to(m)

folium.GeoJson(
    data=geo_a7slice_latlon_50,
    style_function=style_function_other,
    name="A7_LINK_SLICE_RoadNo_50",
    overlay=True,
    tooltip=geo_tooltip_50,
    popup=geo_popup_50
).add_to(m)


# IC/JC point 
print("#############################################")
points = find_manual_sql();
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


folium.LayerControl(position='topright', collapsed=False).add_to(m)

m.save(HTML_FILE_NAME)
