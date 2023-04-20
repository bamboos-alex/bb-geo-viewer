import mariadb
import geojson
import json

def findA2Link(a2LinkId):
    conn = mariadb.connect(
        user="ldm",
        password="ldm",
        host="127.0.0.1",
        database="next-ldm"
    )
    
    cur = conn.cursor()
    
    if a2LinkId: 
        cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A2_LINK' and id = '" + a2LinkId + "';") 
    else:
        cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A2_LINK' and ST_DISTANCE(ST_GEOMFROMTEXT('POINT(332020.85 4128721.928)'), geometry2D) < 10000 order by id asc;")
        # cur.execute("select id, ST_AsGeoJSON(geometry2D) from HD_MAP hm where (hdMapType = 'A2_LINK') and (JSON_VALUE(properties, '$.roadNo') = '1') and (ST_DISTANCE(ST_GEOMFROMTEXT('POINT(332020.85 4128721.928)'), geometry2D) < 1000)  order by id asc;")
 
    linkList = []
    for id, properties, geometry in cur :
        print(f"id={id}, properties={properties}, geometry={geometry}")

        prop = json.loads(properties)
        geo = geojson.loads(geometry)
         
        link = {"id": id, "properties": prop, "geometry": geo}
        linkList.append(link)
        
    
    conn.close()

    return linkList
    
    
# a2Link = findA2Link()
# a2Link = findA2Link(a2LinkId="A217BR720009")
# print(a2Link)

def findA7LinkSlice(a7Id):
    conn = mariadb.connect(
        user="ldm",
        password="ldm",
        host="127.0.0.1",
        database="next-ldm"
    )
    
    cur = conn.cursor()
    
    if a7Id: 
        cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A7_LINK_SLICE' and id = '" + a7Id + "';") 
    else:
        cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A7_LINK_SLICE' order by id asc;") 
        #cur.execute("select id, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A7_LINK_SLICE' and ST_DISTANCE(ST_GEOMFROMTEXT('POINT(332020.85 4128721.928)'), geometry2D) < 10000 order by id asc;")
        # cur.execute("select id, ST_AsGeoJSON(geometry2D) from HD_MAP hm where (hdMapType = 'A7_LINK_SLICE') and (JSON_VALUE(properties, '$.roadNo') = '1') and (ST_DISTANCE(ST_GEOMFROMTEXT('POINT(332020.85 4128721.928)'), geometry2D) < 1000)  order by id asc;")
 
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

