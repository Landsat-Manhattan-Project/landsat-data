from osgeo import gdal, ogr
import shapely.geometry
import shapely.wkt
import datetime

paths_landsat_8 = {
    "1": {
        "day" : 1,
        "path" : [110, 126, 142, 158, 174, 190, 206, 222, 5, 21, 37, 53, 69, 85]
    },
    "2": {
        "day" : 2,
        "path" : [101, 117, 133, 149, 165, 181, 197, 213, 229, 12, 28, 44, 60, 76, 92]
    },
    "3": {
        "day" : 3,
        "path" : [108, 124, 140, 156, 172, 188, 204, 220, 3, 19, 35, 51, 67, 83]
    },
    "4": {
        "day" : 4,
        "path" : [99, 115, 131, 147, 163, 179, 195, 211, 227, 10, 26, 42, 58, 74, 90]
    },
    "5": {
        "day" : 5,
        "path" : [106, 122, 138, 154, 170, 186, 202, 218, 1, 17, 33, 49, 65, 81, 97]
    },
    "6": {
        "day" : 6,
        "path" : [113, 129, 145, 161, 177, 193, 209, 225, 8, 24, 40, 56, 72, 88]
    },
    "7": {
        "day" : 7,
        "path" : [104, 120, 136, 152, 168, 184, 200, 216, 232, 15, 31, 47, 63, 79, 95]
    },
    "8": {
        "day" : 8,
        "path" : [111, 127, 143, 159, 175, 191, 207, 223, 6, 22, 38, 54, 70, 86]
    },
    "9": {
        "day" : 9,
        "path" : [102, 118, 134, 150, 166, 182, 198, 214, 230, 13, 29, 45, 61, 77, 93]
    },
    "10": {
        "day" : 10,
        "path" : [109, 125, 141, 157, 173, 189, 205, 221, 4, 20, 36, 52, 68, 84]
    },
    "11": {
        "day" : 11,
        "path" : [100, 116, 132, 148, 164, 180, 196, 212, 228, 11, 27, 43, 59, 75, 91]
    },
    "12": {
        "day" : 12,
        "path" : [107, 123, 139, 155, 171, 187, 203, 219, 2, 18, 34, 50, 66, 82]
    },
    "13": {
        "day" : 13,
        "path" : [98, 114, 130, 146, 162, 178, 194, 210, 226, 9, 25, 41, 57, 73, 89]
    },
    "14": {
        "day" : 14,
        "path" : [105, 121, 137, 153, 169, 185, 201, 217, 233, 16, 32, 48, 64, 80, 96]
    },
    "15": {
        "day" : 15,
        "path" : [112, 128, 144, 160, 176, 192, 208, 224, 7, 23, 39, 55, 71, 87]
    },
    "16": {
        "day" : 16,
        "path" : [103, 119, 135, 151, 167, 183, 199, 215, 231, 14, 30, 46, 62, 78, 94]
    }
}

paths_landsat_9 = {
    "1" : {
        "day" : 1,
        "path" : [102, 118, 134, 150, 166, 182, 198, 214, 230, 13, 29, 45, 61, 77, 93]
    },
    "2" : {
        "day" : 2,
        "path" : [93, 109, 125, 141, 157, 173, 189, 205, 221, 4, 20, 36, 52, 68, 84]
    },
    "3" : {
        "day" : 3,
        "path" : [100, 116, 132, 148, 164, 180, 196, 212, 228, 11, 27, 43, 59, 75, 91]
    },
    "4" : {
        "day" : 4,
        "path" : [91, 107, 123, 139, 155, 171, 187, 203, 219, 2, 18, 34, 50, 66, 82]
    },
    "5" : {
        "day" : 5,
        "path" : [98, 114, 130, 146, 162, 178, 194, 210, 226, 9, 25, 41, 57, 73, 89]
    },
    "6" : {
        "day" : 6,
        "path" : [105, 121, 137, 153, 169, 185, 201, 217, 233, 16, 32, 48, 64, 80, 96]
    },
    "7" : {
        "day" : 7,
        "path" : [96, 112, 128, 144, 160, 176, 192, 208, 224, 7, 23, 39, 55, 71, 87]
    },
    "8" : {
        "day" : 8,
        "path" : [103, 119, 135, 151, 167, 183, 199, 215, 231, 14, 30, 46, 62, 78, 94]
    },
    "9" : {
        "day" : 9,
        "path" : [94, 110, 126, 142, 158, 174, 190, 206, 222, 5, 21, 37, 53, 69, 85]
    },
    "10" : {
        "day" : 10,
        "path" : [101, 117, 133, 149, 165, 181, 197, 213, 229, 12, 28, 44, 60, 76, 92]
    },
    "11" : {
        "day" : 11,
        "path" : [92, 108, 124, 140, 156, 172, 188, 204, 220, 3, 19, 35, 51, 67, 83]
    },
    "12" : {
        "day" : 12,
        "path" : [99, 115, 131, 147, 163, 179, 195, 211, 227, 10, 26, 42, 58, 74, 90]
    },
    "13" : {
        "day" : 13,
        "path" : [90, 106, 122, 138, 154, 170, 186, 202, 218, 1, 17, 33, 49, 65, 81]
    },
    "14" : {
        "day" : 14,
        "path" : [97, 113, 129, 145, 161, 177, 193, 209, 225, 8, 24, 40, 56, 72, 88]
    },
    "15" : {
        "day" : 15,
        "path" : [104, 120, 136, 152, 168, 184, 200, 216, 232, 15, 31, 47, 63, 79, 95]
    },
    "16" : {
        "day" : 16,
        "path" : [111, 127, 143, 159, 175, 191, 207, 223, 6, 22, 38, 54, 70, 86, 95]
    }
}

def point_is_there(feature, point, mode):
  geometry = feature.GetGeometryRef()
  shape = shapely.wkt.loads(geometry.ExportToWkt())
  if point.within(shape) and feature['MODE'] == mode:
    return True
  else:
    return False

def get_future_date(lat, lon):

  shapefile = ogr.Open("/content/WRS2_descending.shp")
  layer = shapefile.GetLayer(0)
  point = shapely.geometry.Point(lon, lat)
  mode = 'D'

  i = 0
  while not point_is_there(layer.GetFeature(i), point, mode):
    i += 1

  feature = layer.GetFeature(i)
  path = feature['PATH']
  row = feature['ROW']

  day_landsat_8 = next((value['day'] for value in paths_landsat_8.values() if path in value["path"]), None)
  day_landsat_9 = next((value['day'] for value in paths_landsat_9.values() if path in value["path"]), None)

  start_date = datetime.datetime(2024, 9, 4)
  today = datetime.datetime.now()
  near_date = None

  while near_date is None:
    start_date += datetime.timedelta(16)
    if start_date >= today and (start_date - today).days < 16:
      near_date = start_date

  final_date_landsat_8 = near_date + datetime.timedelta(day_landsat_8 - 1)
  final_date_landsat_9 = near_date + datetime.timedelta(day_landsat_9 - 1)
  
  return(final_date_landsat_8, final_date_landsat_9)