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

def find_by_point(request):
    conn = mariadb.connect(
        user="ldm",
        password="ldm",
        host="127.0.0.1",
        database="next-ldm"
    )
    
    cur = conn.cursor()

    hdMapType = request['hdMapType']
    x = request['x']
    y = request['y']
    geometry = 'POINT(' + f'{x}'  + ',' + f'{y}' + ')'
    meter = request['meter']
    meter_string = f'{meter}'

    cur.execute("select id, properties, ST_AsGeoJSON(geometry2D) from HD_MAP where HD_MAP.hdMapType = '" + hdMapType
                + "' and ST_DISTANCE(HD_MAP.geometry2D, " + geometry + ") <= " + meter_string
                + " ORDER BY ST_DISTANCE(HD_MAP.geometry2D, " +  geometry + ") ASC;")

    linkList = []
    for id, properties, geometry in cur :
        print(f"id={id}, properties={properties}, geometry={geometry}")   

        prop = json.loads(properties)
        geo = geojson.loads(geometry)
        
         
        link = {"id": id, "properties": prop, "geometry": geo}
        linkList.append(link)
        
    
    conn.close()

    return linkList


### test ####   
# request = {"hdMapType" : "A7_LINK_SLICE", "x" : 332967.7981256369, "y": 4141269.55194718, "meter": 2000}
# points = find_by_point(request)
# print (points)