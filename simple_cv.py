import cv2
import numpy as np
import gdal
import ogr
import osgeo.osr as osr
from numpy import gradient
from numpy import pi
from numpy import arctan
from numpy import arctan2
from numpy import sin
from numpy import cos
from numpy import sqrt


def default_mosaic_filename(dtm_input):
    mosaic_file_name = dtm_input.split('.')[0] + '_mosaic.tif'
    return mosaic_file_name


    # созданиие массива мозаики
def hillshade(array, azimuth, angle_altitude):
    x, y = gradient(array)
    slope = pi/2. - arctan(sqrt(x*x + y*y))
    aspect = arctan2(-x, y)
    azimuthrad = azimuth*pi / 180.
    altituderad = angle_altitude*pi / 180.

    shaded = sin(altituderad) * sin(slope)\
    + cos(altituderad) * cos(slope)\
    * cos(azimuthrad - aspect)
    return 255*(shaded + 1)/2


# функция создает мозаику с использованием исходного геофайла
def create_stored_mosaic(DTM_input, mosaic_file_name):
    dtm = gdal.Open(DTM_input)
    if dtm is None:
        return 'Открытый файл не является изображением'
    else:
        geo_info = dtm.GetGeoTransform()
        if geo_info == (0, 1, 0, 0, 0, 1):
            return 'Открытый файл не является изображением типа geo tiff.'
        else:
            dtm_prj = dtm.GetProjection()
            band = dtm.GetRasterBand(1)
            arr = band.ReadAsArray()
            hs_array = hillshade(arr, 180, 90)

            x_mosaic_size = dtm.RasterXSize
            y_mosaic_size = dtm.RasterYSize
            driver = gdal.GetDriverByName('GTiff')
            mosaic_dataset = driver.Create(
                mosaic_file_name,
                x_mosaic_size, y_mosaic_size,
                1,
                gdal.GDT_Byte
                )

            mosaic_dataset.SetProjection(dtm_prj)
            mosaic_dataset.GetRasterBand(1).WriteArray(hs_array)
            mosaic_dataset = None
            return ''


    # создание shp файла
def create_stored_shp(shp_name, dtm_input):
    driverName = "ESRI Shapefile"
    drv = ogr.GetDriverByName(driverName)
    ogrData = drv.CreateDataSource(shp_name)
    # открываем dtm и берем оттуда параметры проекции
    dtm = gdal.Open(dtm_input)
    dtm_prj = dtm.GetProjection()
    srs = osr.SpatialReference(wkt=dtm_prj)
    crat_layer = ogrData.CreateLayer(shp_name, srs, ogr.wkbPoint)

    # настраиваем поля
    fieldId = ogr.FieldDefn("Id", ogr.OFTString)
    fieldId.SetWidth(32)
    crat_layer.CreateField(fieldId)
    fieldDiam = ogr.FieldDefn("Diam_m", ogr.OFTReal)
    fieldDiam.SetWidth(18)
    fieldDiam.SetPrecision(1)
    crat_layer.CreateField(fieldDiam)
    crat_layer.CreateField(ogr.FieldDefn("Radius", ogr.OFTReal))
    crat_layer.CreateField(ogr.FieldDefn("Longitude", ogr.OFTReal))
    crat_layer.CreateField(ogr.FieldDefn("Latitude", ogr.OFTReal))
    crat_layer.CreateField(ogr.FieldDefn("Depth", ogr.OFTInteger64))


def bresenham_circle(x0, y0, radius):
    switch = 3 - (2 * radius)
    points = set()
    x = 0
    y = radius
    # first quarter/octant starts clockwise at 12 o'clock
    while x <= y:
        # first quarter first octant
        points.add((int(x0+x), int(y0+y)))
        # first quarter 2nd octant
        points.add((int(x0-x), int(y0+y)))
        # second quarter 3rd octant
        points.add((int(x0+x), int(y0-y)))
        # second quarter 4.octant
        points.add((int(x0-x), int(y0-y)))
        # third quarter 5.octant
        points.add((int(x0+y), int(y0+x)))
        # third quarter 6.octant
        points.add((int(x0-y), int(y0+x)))
        # fourth quarter 7.octant
        points.add((int(x0+y), int(y0-x)))
        # fourth quarter 8.octant
        points.add((int(x0-y), int(y0-x)))
        if switch < 0:
            switch = switch + (4 * x) + 6
        else:
            switch = switch + (4 * (x - y)) + 10
            y = y - 1
        x = x + 1
    return points


# find mean z for 4 circles of different radius
def store_normal_mean(x, y, pixel_radius, dtm_arr):

    # circle with basic radius
    normal_circle = bresenham_circle(x0=x, y0=y, radius=pixel_radius)
    norm_circle_list = []
    for point in normal_circle:
        try:
            norm_circle_list.append(dtm_arr[point[1]][point[0]])            
        except IndexError:
            continue
    norm_mean = sum(norm_circle_list) / len(norm_circle_list)
    return norm_mean


def store_small_mean(x, y, pixel_radius, dtm_arr):
    # circle with small radius
    small_circle = bresenham_circle(x0=x, y0=y, radius=pixel_radius - (pixel_radius / 100 * 20))
    small_circle_list = []
    for point in small_circle:
        try:
            small_circle_list.append(dtm_arr[point[1]][point[0]])
        except IndexError:
            continue
    small_mean = sum(small_circle_list) / len(small_circle_list)
    return small_mean


def store_surface_height(x, y, pixel_radius, dtm_arr):
    # circle with 30% bigger radius
    big_circle = bresenham_circle(x0=x, y0=y, radius=pixel_radius + pixel_radius / 100 * 30)
    big_circle_list = []
    for point in big_circle:
        try:
            big_circle_list.append(dtm_arr[point[1]][point[0]])
        except IndexError:
            continue
    big_mean = sum(big_circle_list) / len(big_circle_list)

    # circle with double radius
    bigger_circle = bresenham_circle(x0=x, y0=y, radius=pixel_radius * 2)
    bigger_circle_list = []
    for point in bigger_circle:
        try:
            bigger_circle_list.append(dtm_arr[point[1]][point[0]])
        except IndexError:
            continue
    bigger_mean = sum(bigger_circle_list) / len(bigger_circle_list)

    # circle with triple radius
    even_bigger_circle = bresenham_circle(x0=x, y0=y, radius=pixel_radius * 3)
    even_bigger_circle_list = []
    for point in even_bigger_circle:
        try:
            even_bigger_circle_list.append(dtm_arr[point[1]][point[0]])
        except IndexError:
            continue
    even_bigger_mean = sum(even_bigger_circle_list) / len(even_bigger_circle_list)
    surface_height = (big_mean + bigger_mean + even_bigger_mean) / 3
    return surface_height

def get_colorized_image(mosaic_file_path):
    # открытие исходной мозаики
    image = cv2.imread(mosaic_file_path, 0)
    marked_up_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return marked_up_image


def create_gradient(mosaic_file_path):
    image = cv2.imread(mosaic_file_path, 0)
    # laplasian
    dst = cv2.Laplacian(image, cv2.CV_64F, ksize=3)
    gradient_image = cv2.convertScaleAbs(dst)
    return gradient_image


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, marked_up_image):
        cv2.circle(marked_up_image, (self.x, self.y), self.radius, (0, 255, 0), 2)
        cv2.circle(marked_up_image, (self.x, self.y), 2, (0, 0, 255), 3)


# функция обнаружения кратеров и записи результатов в шейп-файл
def detect_craters(gradient_image, cv_start_radius=10, cv_max_radius=100, cv_param1=30, cv_param2=20, cv_min_distance=10):
    # обнаружение кругов
    detect_radius = cv_start_radius
    circle_list = []
    while detect_radius < cv_max_radius:
        circles = cv2.HoughCircles(gradient_image, cv2.HOUGH_GRADIENT, 1, cv_min_distance, param1=cv_param1, param2=cv_param2, minRadius=(detect_radius), maxRadius=(detect_radius+11))
        detect_radius += 10
        if circles is None:
            continue
        circles = np.uint16(np.around(circles))
        for circle_params in circles[0, :]:
            circle = Circle(circle_params[0], circle_params[1], circle_params[2])
            circle_list.append(circle)
    return circle_list


def store_features(dtm_input, circle_list, shp_name):
    dtm = gdal.Open(dtm_input)
    band = dtm.GetRasterBand(1)
    dtm_arr = band.ReadAsArray()
    geo_info = dtm.GetGeoTransform()
    assert geo_info[2] == 0
    # открываем шейп-файл
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(shp_name, 1)
    crat_layer = dataSource.GetLayer()
    confirm_stage_1st_list = []
    # заносим атрибутивную информацию в слой
    for crat_id, circle in enumerate(circle_list):
        store_circle(geo_info, dtm_arr, crat_layer, circle, crat_id, confirm_stage_1st_list)
    return crat_id


def store_circle(geo_info, dtm_arr, crat_layer, circle, crat_id, confirm_stage_1st_list):

    # получаем средние высоты кругов
    normal_z = store_normal_mean(circle.x, circle.y, circle.radius, dtm_arr)
    inner_z = store_small_mean(circle.x, circle.y, circle.radius, dtm_arr)
    surface_z = store_surface_height(circle.x, circle.y, circle.radius, dtm_arr)
    abs_depth = int(dtm_arr[int(circle.y)][int(circle.x)])
    # проверяем, подходящие высоты для кратера или нет
    if normal_z > inner_z and inner_z > abs_depth and (normal_z < surface_z + surface_z * 0.05 or normal_z > surface_z - surface_z * 0.05):
        crat =[circle.x, circle.y, circle.radius]
        confirm_stage_1st_list.append(crat)
        x_coord = geo_info[0] + float(circle.x) * geo_info[1]
        y_coord = geo_info[3] - float(circle.y) * geo_info[1]
        depth = surface_z - abs_depth
        pointCoord = [x_coord, y_coord]
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(pointCoord[0], pointCoord[1])
        featureDefn = crat_layer.GetLayerDefn()
        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(point)
        outFeature.SetField(0, crat_id)
        outFeature.SetField(1, float((circle.radius)*2*geo_info[1]))
        outFeature.SetField('Radius', float((circle.radius)*geo_info[1]))
        outFeature.SetField('Longitude', x_coord)
        outFeature.SetField('Latitude', y_coord)
        outFeature.SetField('Depth', depth)
        crat_layer.CreateFeature(outFeature)
        outFeature = None

# def store_confirmed_circle(confirm_stage_1st_list):
#     for conf_circle in confirm_stage_1st_list:
#         if conf_circle = 

def draw_circles(marked_up_image, circle_list, crat_id):
    for circle in circle_list:
        circle.draw(marked_up_image)
    cv2.imwrite('detected_crat.tif', marked_up_image)


if __name__ == "__main__":
    dtm_input = "C:\\projects\\craters_recognition\\GLD100_test.tif"
    mosaic_file_name = default_mosaic_filename(dtm_input)
    mosaic = create_stored_mosaic(dtm_input, mosaic_file_name)
    create_stored_shp("crat_circle.shp", dtm_input)
    grad = create_gradient(default_mosaic_filename(dtm_input))
    color_image = get_colorized_image(default_mosaic_filename(dtm_input))
    get_stored_info = store_features(dtm_input, detect_craters(grad), shp_name="crat_circle.shp")
    marked_up_image_filename = 'detected_crat.tif'
    draw_circles(color_image, detect_craters(grad), get_stored_info)
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Image', 600, 600)
    cv2.imshow('Image', color_image)

# закрывает все
cv2.waitKey(0)
cv2.destroyAllWindows()
