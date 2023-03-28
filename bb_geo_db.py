import mariadb
import geojson

def findA2Link():
    conn = mariadb.connect(
        user="ldm",
        password="ldm",
        host="127.0.0.1",
        database="next-ldm"
    )
    
    cur = conn.cursor()
   
    cur.execute("select id, ST_AsGeoJSON(geometry2D) from HD_MAP hm where hdMapType = 'A2_LINK' and ST_DISTANCE(ST_GEOMFROMTEXT('POINT(332020.85 4128721.928)'), geometry2D) < 1000 order by id asc;")
 
    a2linkList = []
    for id, geometry in cur :
        #print(f"id={id}, geometry={geometry}")   

        geo = geojson.loads(geometry)
         
        a2link = {"id": id, "geometry": geo}
        a2linkList.append(a2link)
        
    
    conn.close()

    return a2linkList
    
    
# a2Link = findA2Link()

# print(a2Link)

