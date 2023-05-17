import mariadb
import geojson
import json

def find(request):
    conn = mariadb.connect(
        user="ldm",
        password="ldm",
        host="127.0.0.1",
        database="next-ldm"
    )
    
    cur = conn.cursor()

    if (isinstance(request, dict)):
        hdMapType = request['hdMapType']

        if (request.get('roadNo')):
            if (request.get('direction')) :
                roadNo = request['roadNo']
                direction = request['direction']
                cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = '" + hdMapType + "' "
                + " and JSON_VALUE(properties, \"$.roadNo\") = '" + roadNo + "' "
                + " and JSON_VALUE(properties, \"$.direction\") = '" + direction + "' order by id asc;") 
            else :
                roadNo = request['roadNo']
                cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = '" + hdMapType + "' "
                + " and JSON_VALUE(properties, \"$.roadNo\") = '" + roadNo + "' order by id asc;") 
        else:
            cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = '" + hdMapType + "' order by id asc;") 
    elif request : 
        id = request
        cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where id = '" + id + "';") 
    else:
        cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A2_LINK' order by id asc;") 
 
    linkList = []
    for id, properties, geometry in cur :
        print(f"id={id}, properties={properties}, geometry={geometry}")   

        prop = json.loads(properties)
        geo = geojson.loads(geometry)
        
         
        link = {"id": id, "properties": prop, "geometry": geo}
        linkList.append(link)
        
    
    conn.close()

    return linkList
    

def find_manual_sql():
    conn = mariadb.connect(
        user="ldm",
        password="ldm",
        host="127.0.0.1",
        database="next-ldm"
    )
    
    cur = conn.cursor()

    cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'Z2_IC_JC';")

    linkList = []
    for id, properties, geometry in cur :
        print(f"id={id}, properties={properties}, geometry={geometry}")   

        prop = json.loads(properties)
        geo = geojson.loads(geometry)
        
         
        link = {"id": id, "properties": prop, "geometry": geo}
        linkList.append(link)
        
    
    conn.close()

    return linkList
