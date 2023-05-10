import mariadb
import geojson
import json

# def findA2Link(request):
#     conn = mariadb.connect(
#         user="ldm",
#         password="ldm",
#         host="127.0.0.1",
#         database="next-ldm"
#     )
    
#     cur = conn.cursor()

#     if (isinstance(request, dict)):
#         roadNo = request['roadNo']
#         direction = request['direction']
#         cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A2_LINK' "
#                     + " and JSON_VALUE(properties, \"$.roadNo\") = '" + roadNo + "' "
#                     + " and JSON_VALUE(properties, \"$.direction\") = '" + direction + "' order by id asc;") 
#     elif request : 
#         a2LinkId = request
#         cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A2_LINK' and id = '" + a2LinkId + "';") 
#     else:
#         cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A2_LINK' and ST_DISTANCE(ST_GEOMFROMTEXT('POINT(332020.85 4128721.928)'), geometry2D) < 10000 order by id asc;")
#         # cur.execute("select id, ST_AsGeoJSON(geometry2D) from HD_MAP hm where (hdMapType = 'A2_LINK') and (JSON_VALUE(properties, '$.roadNo') = '1') and (ST_DISTANCE(ST_GEOMFROMTEXT('POINT(332020.85 4128721.928)'), geometry2D) < 1000)  order by id asc;")
 
#     linkList = []
#     for id, properties, geometry in cur :
#         print(f"id={id}, properties={properties}, geometry={geometry}")

#         prop = json.loads(properties)
#         geo = geojson.loads(geometry)
         
#         link = {"id": id, "properties": prop, "geometry": geo}
#         linkList.append(link)
        
    
#     conn.close()

#     return linkList
    
    
# a2Link = findA2Link()
# a2Link = findA2Link(a2LinkId="A217BR720009")

# roadNoAndDirection = {"roadNo": "50", "direction": "E"}
# a2Link = findA2Link(request=roadNoAndDirection)
# print(a2Link)

def findLink(request):
    conn = mariadb.connect(
        user="ldm",
        password="ldm",
        host="127.0.0.1",
        database="next-ldm"
    )
    
    cur = conn.cursor()

    # cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A2_LINK' and JSON_VALUE(properties, '$.direction') IS NULL order by id asc;") 
    # cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A2_LINK' and JSON_VALUE(properties, '$.roadNo') = '1' order by id asc;") 
    
    if (isinstance(request, dict)):
        roadNo = request['roadNo']
        direction = request['direction']
        hdMapType = request['hdMapType']

        if (not roadNo):
             cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = '" + hdMapType + "' "
            + " and JSON_VALUE(properties, \"$.roadNo\") IS NULL order by id asc;") 
        elif (direction) :
            cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = '" + hdMapType + "' "
            + " and JSON_VALUE(properties, \"$.roadNo\") = '" + roadNo + "' "
            + " and JSON_VALUE(properties, \"$.direction\") = '" + direction + "' order by id asc;") 
        else :
            cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = '" + hdMapType + "' "
            + " and JSON_VALUE(properties, \"$.roadNo\") = '" + roadNo + "' order by id asc;") 
    elif request : 
        id = request
        cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = '" + hdMapType +  "' and id = '" + id + "';") 
    else:
        cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = '" + hdMapType + "' order by id asc;") 
    #     # cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A7_LINK_SLICE' order by id asc;") 
    #     # cur.execute("select id, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A7_LINK_SLICE' and ST_DISTANCE(ST_GEOMFROMTEXT('POINT(332020.85 4128721.928)'), geometry2D) < 10000 order by id asc;")
    #     # cur.execute("select id, ST_AsGeoJSON(geometry2D) from HD_MAP hm where (hdMapType = 'A7_LINK_SLICE') and (JSON_VALUE(properties, '$.roadNo') = '1') and (ST_DISTANCE(ST_GEOMFROMTEXT('POINT(332020.85 4128721.928)'), geometry2D) < 1000)  order by id asc;")
 
    linkList = []
    for id, properties, geometry in cur :
        print(f"id={id}, properties={properties}, geometry={geometry}")   

        prop = json.loads(properties)
        geo = geojson.loads(geometry)
        
         
        link = {"id": id, "properties": prop, "geometry": geo}
        linkList.append(link)
        
    
    conn.close()

    return linkList
    
    
# a7Link = findA7LinkSlice("")
# a7Link = findA7LinkSlice(a7Id="A219AG640002_A7000001")
# print(a7Link)

# a7Request = {"roadNo": "50", "direction": "E", "hdMapType": "A7_LINK_SLICE"}
# a7Link = findLink(request=a7Request)
# print(a7Link)

# a2Request = {"roadNo": "50", "direction": "E", "hdMapType": "A2_LINK"}
# a2Request = {"roadNo": None, "direction": "E", "hdMapType": "A2_LINK"}
# a2Link = findLink(request=a2Request)
# print(a2Link)