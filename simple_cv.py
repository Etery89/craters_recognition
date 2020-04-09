import cv2
import numpy as np
from matplotlib import pyplot as plt
import gdal
import ogr
import osgeo
import osgeo.osr as osr
from osgeo import gdal
from numpy import gradient
from numpy import pi
from numpy import arctan
from numpy import arctan2
from numpy import sin
from numpy import cos
from numpy import sqrt
from numpy import zeros
from numpy import uint8


def create_mosaic_file_path(dtm_input):
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
def create_mosaic(DTM_input, mosaic_file_name):
    dtm = gdal.Open(DTM_input)
    dtm_prj = dtm.GetProjection()
    band = dtm.GetRasterBand(1)
    arr = band.ReadAsArray()
    hs_array = hillshade(arr, 180, 90)

    x_mosaic_size = dtm.RasterXSize
    y_mosaic_size = dtm.RasterYSize
    driver = gdal.GetDriverByName('GTiff')
    mosaic_dataset = driver.Create(mosaic_file_name, x_mosaic_size, y_mosaic_size, 1, gdal.GDT_Byte)

    mosaic_dataset.SetProjection(dtm_prj)
    mosaic_dataset.GetRasterBand(1).WriteArray(hs_array)
    mosaic_dataset = None
    return mosaic_file_name


def first_button(mosaic):
    # mosaic_image = cv2.imread(mosaic, 0)
    # cv2.namedWindow('dataset', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('dataset', 800, 800)
    # cv2.imshow('dataset',mosaic_image)


    #создание shp файла
    def create_shp():
        driverName = "ESRI Shapefile"
        drv = ogr.GetDriverByName(driverName)
        ogrData = drv.CreateDataSource("crat_circle.shp")

        dtm = gdal.Open(dtm_input) 
        dtm_prj = dtm.GetProjection()
        srs = osr.SpatialReference(wkt=dtm_prj)
        crat_layer = ogrData.CreateLayer("crat_circle", srs, ogr.wkbPoint)

        #настраиваем поля
        fieldId = ogr.FieldDefn("Id", ogr.OFTString)
        fieldId.SetWidth(32)
        crat_layer.CreateField(fieldId)
        fieldDiam = ogr.FieldDefn("Diam_m", ogr.OFTReal)
        fieldDiam.SetWidth(18)
        fieldDiam.SetPrecision(1)
        crat_layer.CreateField(fieldDiam)
        crat_layer.CreateField(ogr.FieldDefn("Latitude", ogr.OFTReal))
        crat_layer.CreateField(ogr.FieldDefn("Longitude", ogr.OFTReal))
    create_shp()


    # #создаем тестовый объект
    # pointCoord = [-124.4577, 48.0135]
    # point = ogr.Geometry(ogr.wkbPoint)
    # point.AddPoint(pointCoord[0],pointCoord[1])
    # print(type(pointCoord[1]))
    # featureDefn = layer.GetLayerDefn()
    # outFeature = ogr.Feature(featureDefn)
    # outFeature.SetGeometry(point)
    # outFeature.SetField(0, 1)
    # outFeature.SetField(1, 1)
    # layer.CreateFeature(outFeature)
    # outFeature = None



    # перебираем все пиксели растра
    # print(xsize, ysize)
    # print(raster)
    # print(raster[1][1])


    #открытие исходной мозаики
    # mosaic = dtm_input.split('.')[0] + '_mosaic.tif'
    image = cv2.imread(mosaic, 0)
    #cv2.imshow("Image", image)

    image = cv2.GaussianBlur(image, (3, 3), 0)
    cimg = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # cv2.namedWindow('Blur', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('Blur', 800, 800)
    # cv2.imshow("Blur", image)

    # #открываем вторую ЦМР
    # gdalData = gdal.Open( "APOLLO17_DTM_150CM_180_45.tif")
    # xsize = gdalData.RasterXSize
    # ysize = gdalData.RasterYSize
    # raster = gdalData.ReadAsArray()

    # перебираем все пиксели растра
    # print(xsize, ysize)
    # print(raster)
    # print(raster[1][1])

    #нормализация исходной мозаики
    # normalizedImg = np.zeros((800, 800))
    # normalizedImg = cv2.normalize(image,  normalizedImg, 150, 255, cv2.NORM_MINMAX)
    # edges = cv2.Canny(normalizedImg,10,200)


    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)  # x
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)  # y
    gradient1 = cv2.subtract(sobelx, sobely)
    gradient1 = cv2.convertScaleAbs(gradient1)

    # laplacian = cv2.Laplacian(image,cv2.CV_64F)
    # gradient_blur = cv2.GaussianBlur(gradient, (3, 3), 0)

    # cv2.namedWindow('Lap', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('Lap', 800, 800)
    # cv2.imshow('Lap',laplacian)

    # cv2.namedWindow('x', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('x', 800, 800)
    # cv2.imshow('x',sobelx)

    # cv2.namedWindow('y', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('y', 800, 800)
    # cv2.imshow('y',sobely)

    # cv2.namedWindow('gr', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('gr', 800, 800)
    # cv2.imshow('gr',gradient1)

    # cv2.namedWindow('Norm', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('Norm', 800, 800)
    # cv2.imshow('Norm',normalizedImg)

    # cv2.namedWindow('Edge', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('Edge', 800, 800)
    # cv2.imshow('Edge',edges)


    # dtm = gdal.Open(DTM_input) 
    # dtm_prj = dtm.GetProjection()
    # band = dtm.GetRasterBand(1)  
    # arr = band.ReadAsArray()
    # функция обнаружения кратеров и записи результатов в шейп-файл
    def crater_recognition(gradient1, cv_start_radius = 100, cv_max_radius = 200, cv_param1 = 30, cv_param2 = 20, cv_min_distance = 100):
        # circles = circle_detector.detect(gradient1)
        # dtm_input = "C:\\projects\\craters_recognition\\GLD100_test.tif"
        dtm = gdal.Open(dtm_input) 
        dtm_prj = dtm.GetProjection()
        band = dtm.GetRasterBand(1)  
        dtm_arr = band.ReadAsArray()
        x_mosaic_size = dtm.RasterXSize
        y_mosaic_size = dtm.RasterYSize
        geo_info = dtm.GetGeoTransform()
        # print(geo_info)
        # открываем шейп-файл
        driver = ogr.GetDriverByName('ESRI Shapefile')
        dataSource = driver.Open("crat_circle.shp", 1)
        crat_layer = dataSource.GetLayer()

        gradient2 = gradient1
        # обнаружение кругов и отрисовка их на том же изображении
        crat_id = 0
        radius = cv_start_radius
        while radius < cv_max_radius:
            circles = cv2.HoughCircles(gradient1, cv2.HOUGH_GRADIENT, 1, cv_min_distance, param1=cv_param1, param2=cv_param2, minRadius=(radius), maxRadius=(radius+11))
            radius += 10
            if circles is None:
                continue
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # num_i = list(map(float, i))
                # нарисовать окружности
                print(i)
                cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

                #заносим атрибутивную информацию в слой
                x_coord = geo_info[0] + float(i[0]) * geo_info[1]
                y_coord = geo_info[3] - float(i[1]) * geo_info[1]
                pointCoord = [x_coord, y_coord]
                # print(pointCoord)
                # print(type(pointCoord[1]))
                point = ogr.Geometry(ogr.wkbPoint)
                point.AddPoint(pointCoord[0],pointCoord[1])
                featureDefn = crat_layer.GetLayerDefn()
                outFeature = ogr.Feature(featureDefn)
                outFeature.SetGeometry(point)
                outFeature.SetField(0, crat_id)
                outFeature.SetField(1, float(i[2])*2)
                outFeature.SetField('Latitude', x_coord)
                outFeature.SetField('Longitude', y_coord)
                crat_layer.CreateFeature(outFeature)
                outFeature = None
                crat_id += 1
        print(crat_id)
        cv2.imwrite('detected_crat.tif', cimg)
        cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Image', 600, 600)
        cv2.imshow('Image', cimg)
        # повторная обработка
        # radius = cv_start_radius
        # while radius < cv_max_radius:
        #     circles = cv2.HoughCircles(gradient1, cv2.HOUGH_GRADIENT, 1, cv_min_distance, param1=cv_param1, param2=cv_param2, minRadius=(radius), maxRadius=(radius+10))
        #     radius += 10
        #     if circles is None:
        #         continue
        #     circles = np.uint16(np.around(circles))
        #     for i in circles[0, :]:
        #         # num_i = list(map(float, i))
        #         # нарисовать окружности
        #         print('yes')
        #         cv2.circle(cimg, (i[0], i[1]), i[2], (255, 255, 0), 2)
        #         cv2.circle(cimg, (i[0], i[1]), 2, (0, 255, 255), 3) 
        #     cv2.imwrite('detected_crat.tif', cimg)
        #     cv2.namedWindow('2', cv2.WINDOW_NORMAL)
        #     cv2.resizeWindow('2', 600, 600)
        #     cv2.imshow('2', cimg)
            
    print('end')
    crater_recognition(gradient1)
    # сохраняет получившееся изображение и открывает его 




if __name__ == "__main__":
    dtm_input = "C:\\projects\\craters_recognition\\GLD100_test.tif"
    mosaic_file_name = create_mosaic_file_path(dtm_input)
    mosaic = create_mosaic(dtm_input, mosaic_file_name)
    first_button(mosaic)
    #закрывает все
    cv2.waitKey(0)
    cv2.destroyAllWindows()
