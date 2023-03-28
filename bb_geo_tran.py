'''
좌표계 변환 함수 by Charlie
'''

from pyproj import Transformer, Proj

PROJ = '+proj=utm +zone=52 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs'

TRAN_4326_TO_32652 = Transformer.from_crs("EPSG:4326", "EPSG:32652")
TRAN_32652_TO_4326 = Transformer.from_crs("EPSG:32652", "EPSG:4326")
TRAN_3857_TO_4326 = Transformer.from_crs("EPSG:3857", "EPSG:4326")

def trans_4326_to_32652(lon, lat):
    return TRAN_4326_TO_32652.transform(lat, lon)


def trans_32652_to_4326(x, y):
    return TRAN_32652_TO_4326.transform(x, y)


def LatLon_To_UTM52N(Lat, Lon):
    p1 = Proj(PROJ, preserve_units=True)
    (x, y) = p1(Lat, Lon)
    return (x, y)


def UTM52N_To_LatLon(x, y):
    p1 = Proj(PROJ, preserve_units=True)
    (lat, lon) = p1(x, y, inverse=True)
    return (lon, lat)


def trans_3857_to_4326(x, y):
    return TRAN_3857_TO_4326.transform(x, y)
