import folium
import json
import geojson

from bb_geo_tran import UTM52N_To_LatLon
from bb_geo_db import find
from geojson import MultiLineString, Feature, FeatureCollection


# with open('./A217BR720009.json', mode='rt', encoding='utf-8') as f:
#     geo_xy = json.loads(f.read())
#     f.close()

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

roadNo_50_Direction_E = {"roadNo": "50", "direction": "E"}
roadNo_50_Direction_S = {"roadNo": "50", "direction": "S"}
roadNo_50 = {"roadNo": "50", "direction": ""}
roadNo_1_Direction_E = {"roadNo": "1", "direction": "E"}
roadNo_1_Direction_S = {"roadNo": "1", "direction": "S"}
roadNo_1 = {"roadNo": "1", "direction": ""}
roadNo_null = {"roadNo": None, "direction": None}
roadNo_100_Direction_E = {"roadNo": "100", "direction": "E"}
roadNo_100_Direction_S = {"roadNo": "100", "direction": "S"}


# a2LinkList_50_E = findA2Link(request=roadNo_50_Direction_E)
# a2LinkList_50_S = findA2Link(request=roadNo_50_Direction_S)

a2Reuqset = {"hdMapType": "A2_LINK"}
a2Reuqset.update(roadNo_1)
a2LinkList_1 = find(request=a2Reuqset)

a2Reuqset.update(roadNo_50)
a2LinkList_50 = find(request=a2Reuqset)

# a2LinkList_1_E = findA2Link(request=roadNo_1_Direction_E)
# a2LinkList_1_S = findA2Link(request=roadNo_1_Direction_S)
# a2LinkList_100_E = findA2Link(request=roadNo_100_Direction_E)
# a2LinkList_100_S = findA2Link(request=roadNo_100_Direction_S)

a2LinkList = []
a2LinkList.extend(a2LinkList_1)
a2LinkList.extend(a2LinkList_50)
# a2LinkList = a2LinkList_50_E
# a2LinkList.extend(a2LinkList_50_S)
# a2LinkList.extend(a2LinkList_1_E)
# a2LinkList.extend(a2LinkList_1_S)
# a2LinkList.extend(a2LinkList_100_E)
# a2LinkList.extend(a2LinkList_100_S)

# a2linkList = findA2Link("")
# a2linkList = findA2Link("A217BR720009")
# print (a2linkList)

# geo_xy = create_feature_collection(a2LinkList_1_E)
geo_xy = create_feature_collection(a2LinkList)
geo_latlon = geojson.utils.map_tuples(convert_geojson_to_folium, geo_xy)

m = folium.Map(
    location=UTM52N_To_LatLon(332020.85, 4128721.928), # 신갈 JC
    zoom_start=10,
    # tiles=""
    tiles="OpenStreetMap"
)

### A2 LINK Layer

style_function = lambda x: {
    "color": "#3388ff" if int(x["properties"]["index"])%2 == 0 else "#80B5FF"
}
a2_fields=['id', 'roadType', 'roadNo', 'direction', 'laneNo', 'maxSpeed', 'length','roadRank','linkType',  'fromNodeId', 'toNodeId',  'index']
tooltip = folium.GeoJsonTooltip(fields=a2_fields)
popup = folium.GeoJsonPopup(fields=a2_fields)

folium.GeoJson(
    data=geo_latlon,
    style_function=style_function,
    name='A2_LINK',
    overlay=True,
    tooltip=tooltip,
    popup=popup
).add_to(m)


### A7 LINK SLICE Layer
a7Request = {"hdMapType": "A7_LINK_SLICE"}
a7Request.update(roadNo_1)
a7LinkList_1 = find(request=a7Request)
a7Request.update(roadNo_50)
a7LinkList_50 = find(request=a7Request)
# a7LinkList_50_E = findA7Link(request=roadNo_50_Direction_E)
# a7LinkList_50_S = findA7Link(request=roadNo_50_Direction_S)
# a7LinkList_1_E = findA7Link(request=roadNo_1_Direction_E)
# a7LinkList_1_S = findA7Link(request=roadNo_1_Direction_S)
# a7LinkList_100_E = findA7Link(request=roadNo_100_Direction_E)
# a7LinkList_100_S = findA7Link(request=roadNo_100_Direction_S)

a7LinkList = []
a7LinkList.extend(a7LinkList_1)
a7LinkList.extend(a7LinkList_50)
# a7LinkList.extend(a7LinkList_50_E)
# a7LinkList.extend(a7LinkList_50_S)
#a7LinkList.extend(a7LinkList_1_E)
#a7LinkList.extend(a7LinkList_1_S)
# a7LinkList.extend(a7LinkList_100_E)
# a7LinkList.extend(a7LinkList_100_S)

# a7LinkSliceList = findA7LinkSlice("A219AG640002_A7000001")

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

# geo_a7slice_xyz = geojson.loads(open("./a7slice_youngin_4km.geojson", 'r').read())
geo_a7slice_xyz = create_feature_collection(a7LinkList)
geo_a7slice_latlon = geojson.utils.map_tuples(convert_geojson_to_folium, geo_a7slice_xyz)

a7_fields=['id', 'roadType','roadNo', 'direction', 'laneNo', 'maxSpeed','length', 'prev', 'next', 'a2LinkId',  'indexInA2Link',  'minRow', 'maxRow',  'minColumn',  'maxColumn', 'index']
geo_tooltip = folium.GeoJsonTooltip(fields=a7_fields)
geo_popup = folium.GeoJsonPopup(fields=a7_fields)

folium.GeoJson(
    data=geo_a7slice_latlon,
    style_function=style_function_other,
    name="A7_LINK_SLICE",
    overlay=True,
    tooltip=geo_tooltip,
    popup=geo_popup
).add_to(m)

folium.LayerControl(position='topright', collapsed=False).add_to(m)

m.save('bb-map-bg-road-number-1-50.html')
