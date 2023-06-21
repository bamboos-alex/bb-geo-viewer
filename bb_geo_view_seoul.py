import folium
import json
import geojson

from bb_geo_tran import UTM52N_To_LatLon
from bb_geo_db import find, find_manual_sql, find_by_point
from geojson import MultiLineString, Feature, FeatureCollection
from folium import Marker


meter = 5000 # meter
INIT_POINT = (324241.45472746145, 4152474.830050004) # 서초구립 반포도서관 사거리 127.011596 37.502491
#INIT_POINT = (313732.3108338943, 4161109.817388392) # 상암동 사거리 126.890584 37.578210
#INIT_POINT = (316605.046633, 4155231.821346) # 여의대로 126.9245642 37.5259637

flag_with_bg = True
pre_fix='a7'
name='seocho'
#post_fix='road-rank-not-1'
post_fix=''

if (flag_with_bg) :
    HTML_FILE_NAME='bb-map-bg-' + pre_fix + '-' + name + '-' + str(meter) + '-meter' + post_fix + '.html'
else :
    HTML_FILE_NAME='bb-map-' + pre_fix + '-' + name + '-' + str(meter) + '-meter' + post_fix + '.html'

# main ##

zoom_start=18
if (flag_with_bg) :
    m = folium.Map(
        location=UTM52N_To_LatLon(INIT_POINT[0], INIT_POINT[1]),
        zoom_start=zoom_start,
        tiles="OpenStreetMap"
    )
else :
    m = folium.Map(
        location=UTM52N_To_LatLon(INIT_POINT[0], INIT_POINT[1]),
        zoom_start=zoom_start,
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

            
        # filtering temporary
#        if (properties['roadRank'] == '1'):
#            continue

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
# a2Request = {"hdMapType" : "A2_LINK", "x" : INIT_POINT[0], "y": INIT_POINT[1], "meter": meter}
# a2LinkList = find_by_point(a2Request)
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


#a2_fields=['id', 'roadType', 'roadNo', 'direction', 'laneNo', 'maxSpeed', 'length', 'roadRank','linkType',  'fromNodeId', 'toNodeId',  'index']
a2_fields=['id', 'roadType', 'roadNo', 'direction', 'laneNo', 'length', 'roadRank','linkType',  'fromNodeId', 'toNodeId',  'index']

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

request = {"hdMapType" : "A7_LINK_SLICE", "x" : INIT_POINT[0], "y": INIT_POINT[1], "meter": meter}
a7LinkList = find_by_point(request)

print("#############################################")
print(a7LinkList);
print("#############################################")

def style_function_other(x):
    color = "#FF0000"

    a7_prop = x["properties"]

    
    #print (a7_prop)

    if (not a7_prop.get('roadLocationType')):
        print("no roadLocationType")
        return {"color": color}
    
    if (a7_prop["roadLocationType"] == "MAIN_ROAD") :

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
            
    elif (a7_prop["roadLocationType"] == "RAMP"):
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


#a7_fields=['id', 'roadLocationType','roadNo', 'direction', 'laneNo', 'maxSpeed','length', 'roadRank','linkType',  'prev', 'next', 'a2LinkId',  'indexInA2Link',  'minRow', 'maxRow',  'minColumn',  'maxColumn', 'index']
a7_fields=['id', 'roadLocationType','roadNo', 'direction', 'laneNo', 'length','roadRank', 'linkType',  'prev', 'next', 'a2LinkId',  'indexInA2Link',  'minRow', 'maxRow',  'minColumn',  'maxColumn', 'index']
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
