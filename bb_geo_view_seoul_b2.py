import folium
import json
import geojson

from bb_geo_tran import UTM52N_To_LatLon
from bb_geo_db import find, find_manual_sql, find_by_point
from geojson import MultiLineString, Feature, FeatureCollection
from folium import Marker


meter = 1000000 # meter
#INIT_POINT = (324241.45472746145, 4152474.830050004) # 서초구립 반포도서관 사거리 127.011596 37.502491
#INIT_POINT = (313732.3108338943, 4161109.817388392) # 상암동 사거리 126.890584 37.578210
#INIT_POINT = (316605.046633, 4155231.821346) # 여의대로 126.9245642 37.5259637
#INIT_POINT = (348279.67055360705, 4122768.853836476) # 양지터널 127.289516 37.239110
INIT_POINT = (349128.08450124,4122998.08846334) # 양지터널 B419BS324997 

flag_with_bg = False
pre_fix='b2'
name='all'
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
        if ('roadRank' not in properties):
            properties['roadRank'] = 'NULL'
        if ('direction' not in properties):
            properties['direction'] = 'NULL'

        if ('r_LinkId' not in properties):
            properties['r_LinkId'] = 'NULL'
        if ('l_LinkId' not in properties):
            properties['l_LinkId'] = 'NULL'
        if ('type' not in properties):
            properties['type'] = 'NULL'
        if ('kind' not in properties):
            properties['kind'] = 'NULL'
        if ('linePattern' not in properties):
            properties['linePattern'] = 'NULL'
        if ('lineNumber' not in properties):
            properties['lineNumber'] = 'NULL'
        if ('lineColor' not in properties):
            properties['lineColor'] = 'NULL'
            
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

# ## A2 Link

# # a2Request = {'hdMapType': "A2_LINK"}
# #a2LinkList = find(a2Request)
# a2Request = {"hdMapType" : "A2_LINK", "x" : INIT_POINT[0], "y": INIT_POINT[1], "meter": meter}
# a2LinkList = find_by_point(a2Request)

# print("#############################################")
# print (a2LinkList)
# print("#############################################")

# geo_xy = create_feature_collection(a2LinkList)
# geo_latlon = geojson.utils.map_tuples(convert_geojson_to_folium, geo_xy)

# ### A2 LINK Layer


# def style_function_a2(x):
#     color = "#3388ff"
#     a2_prop = x["properties"]
#     if (a2_prop["linkType"] == "1") :
#         if (a2_prop["index"] % 2 == 0):
#             color = "#bec8b9" 
#         else:
#             color = "#dfd6cd"
#     elif (a2_prop["linkType"] == "4"):
#         color = "#00cc99"
#         if (a2_prop["index"] % 2 == 0):
#             color = "#ec33ec" 
#         else:
#             color = "#ff97d1"

#     elif (a2_prop["linkType"] == "6"):
#         if (a2_prop["index"] % 2 == 0):
#             color = "#1034a6" 
#         else:
#             color = "#0779bf"

#     else:
#         color = "#fbbcec"
        

#     return {"color": color}


# #a2_fields=['id', 'roadType', 'roadNo', 'direction', 'laneNo', 'maxSpeed', 'length', 'roadRank','linkType',  'fromNodeId', 'toNodeId',  'index']
# a2_fields=['id', 'roadType', 'roadNo', 'direction', 'laneNo', 'length', 'roadRank','linkType',  'fromNodeId', 'toNodeId',  'index']

# tooltip = folium.GeoJsonTooltip(fields=a2_fields)
# popup = folium.GeoJsonPopup(fields=a2_fields)

# folium.GeoJson(
#     data=geo_latlon,
#     style_function=style_function_a2,
#     name='A2_LINK',
#     overlay=True,
#     tooltip=tooltip,
#     popup=popup
# ).add_to(m)


### B2 SURFACELINEMARK

request = {"hdMapType" : "B2_SURFACELINEMARK", "x" : INIT_POINT[0], "y": INIT_POINT[1], "meter": meter}
b2List = find_by_point(request)

print("#############################################")
print(b2List);
print("#############################################")

def style_function_other(x):
    color = "#FF0000"

    b2_prop = x["properties"]

    
    #print (b2_prop)

    lineType = int(b2_prop["type"][-1])  # e.g., type=212 lineType=XX2
    kindNumber = int(b2_prop["kind"])

    #print(lineType)

    if (not b2_prop.get('type')):
        print("no type")
        return {"color": color}
    
    if (lineType % 4 == 1) : # 실선
        if (b2_prop["index"] % 2 == 0):
            color = "#66CDAA"
        else:
            color = "#BADA55"
            
    elif (lineType % 4 == 2 ): # 점선
        if (b2_prop["index"] % 2 == 0):
            color = "#FA8072" 
        else:
            color = "#B74160"

    else: # 혼선
        if (b2_prop["index"] % 2 == 0):
            color = "#85649e" 
        else:
            color = "#4400cc"
    
    # if (b2_prop["kind"] == "501") :
    #     if (b2_prop["index"] % 2 == 0):
    #         color = "#990b11" 
    #     else:
    #         color = "#caacaf"
 
    # if (b2_prop["kind"] == "503"):
    #     if (b2_prop["index"] % 2 == 0):
    #         color = "#00cc99" 
    #     else:
    #         color = "#2eb561"
 

    return {"color": color}


b2_fields=['id', 'type', 'kind', 'r_LinkId', 'l_LinkId', 'index']
geo_tooltip = folium.GeoJsonTooltip(fields=b2_fields)
geo_popup = folium.GeoJsonPopup(fields=b2_fields)

geo_b2_xyz = create_feature_collection(b2List)
geo_b2_latlon = geojson.utils.map_tuples(convert_geojson_to_folium, geo_b2_xyz)


folium.GeoJson(
    data=geo_b2_latlon,
    style_function=style_function_other,
    name="B2_SURFACELINEMARK",
    overlay=True,
    tooltip=geo_tooltip,
    popup=geo_popup
).add_to(m)


### B4 SURFACELINEMARK VECTOR

request = {"hdMapType" : "B4_SURFACELINEMARK_VECTOR", "x" : INIT_POINT[0], "y": INIT_POINT[1], "meter": meter}
b4List = find_by_point(request)

print("#############################################")
print(b4List);
print("#############################################")

def style_function_other(x):
    color = "#FFFFFF"

    return {"color": color}


b4_fields=['id', 'type', 'kind', 'r_LinkId', 'l_LinkId', 'surfaceLineMarkId', 'linePattern', 'lineNumber','lineColor','index']
b4_geo_tooltip = folium.GeoJsonTooltip(fields=b4_fields)
b4_geo_popup = folium.GeoJsonPopup(fields=b4_fields)

geo_b4_xyz = create_feature_collection(b4List)
geo_b4_latlon = geojson.utils.map_tuples(convert_geojson_to_folium, geo_b4_xyz)


folium.GeoJson(
    data=geo_b4_latlon,
    style_function=style_function_other,
    name="B4_SURFACELINEMARK_VECTOR",
    overlay=True,
    tooltip=b4_geo_tooltip,
    popup=b4_geo_popup
).add_to(m)

folium.LayerControl(position='topright', collapsed=False).add_to(m)

m.save(HTML_FILE_NAME)
