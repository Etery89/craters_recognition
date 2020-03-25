import cv2
import numpy as np
from matplotlib import pyplot as plt
import gdal
import ogr
import osgeo
import osgeo.osr as osr

def initial_data(mosaic_input, DTM_input, shp_output, cv_start_radius = 100, cv_max_radius = 200, cv_param1 = 30, cv_param2 = 20, cv_min_distance = 10):
    #открытие исходной мозаики
    image = cv2.imread(mosaic_input, 0)
    #cv2.imshow("Image", image)

    image = cv2.medianBlur(image,5)
    cimg = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)

    #создание shp файла
    driverName = "ESRI Shapefile"
    drv = ogr.GetDriverByName( driverName )
    ogrData = drv.CreateDataSource( shp_output)

    #выбираем проекцию
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(9001)

    #создаем слой
    layer = ogrData.CreateLayer( "crat_circle", None, ogr.wkbPoint )

    #настраиваем поля
    fieldId = ogr.FieldDefn( "Id", ogr.OFTString )
    fieldId.SetWidth( 32 ) 
    layer.CreateField(fieldId)
    fieldDiam = ogr.FieldDefn( "Diam_m", ogr.OFTReal ) 
    fieldDiam.SetWidth( 18 )
    fieldDiam.SetPrecision( 1 ) 
    layer.CreateField(fieldDiam)
    layer.CreateField(ogr.FieldDefn("Latitude", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("Longitude", ogr.OFTReal))

    #создаем тестовый объект
    pointCoord = [-124.4577, 48.0135]
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(pointCoord[0],pointCoord[1])
    print(type(pointCoord[1]))
    featureDefn = layer.GetLayerDefn()
    outFeature = ogr.Feature(featureDefn)
    outFeature.SetGeometry(point)
    outFeature.SetField(0, 1)
    outFeature.SetField(1, 1)
    layer.CreateFeature(outFeature)
    outFeature = None

    #открываем ЦМР
    gdalData = gdal.Open(DTM_input)
    xsize = gdalData.RasterXSize
    ysize = gdalData.RasterYSize
    raster = gdalData.ReadAsArray()

    # перебираем все пиксели растра
    # print(xsize, ysize)
    # print(raster)
    # print(raster[1][1])



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
    normalizedImg = np.zeros((800, 800))
    normalizedImg = cv2.normalize(image,  normalizedImg, 150, 255, cv2.NORM_MINMAX)
    edges = cv2.Canny(normalizedImg,30,80)

    # laplacian = cv2.Laplacian(image,cv2.CV_64F)

    # cv2.namedWindow('Lap', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('Lap', 800, 800)
    # cv2.imshow('Lap',laplacian)


    # cv2.namedWindow('Norm', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('Norm', 800, 800)
    # cv2.imshow('Norm',normalizedImg)

    # cv2.namedWindow('Edge', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('Edge', 800, 800)
    # cv2.imshow('Edge',edges)

    # обнаружение кругов и отрисовка их на том же изображении
    radius = cv_start_radius
    while radius < cv_max_radius: 
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1 , cv_min_distance, param1=cv_param1,param2=cv_param2,minRadius=(radius),maxRadius=(radius+10))
        radius += 10
        if circles is None:
            continue
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # нарисовать окружности
            print(i, i[0], i[1])
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

            #заносим атрибутивную информацию в слой
            crat_id = 0
            pointCoord = [float(i[0]), float(i[1])]
            print(pointCoord)
            print(type(pointCoord[1]))
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(pointCoord[0],pointCoord[1])
            featureDefn = layer.GetLayerDefn()
            outFeature = ogr.Feature(featureDefn)
            outFeature.SetGeometry(point)
            outFeature.SetField(0, crat_id)
            outFeature.SetField(1, float(i[2])*2)
            outFeature.SetField('Latitude', float(i[0]))
            outFeature.SetField('Longitude', float(i[1]))
            layer.CreateFeature(outFeature)
            outFeature = None
            crat_id += 1

    # сохраняет получившееся изображение и открывает его 
    cv2.imwrite('detected_crat.tif',cimg)
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Image', 600, 600)
    cv2.imshow('Image',cimg)

    #закрывает все
    ogrData.Destroy()
    gdalData = None
    cv2.waitKey(0)
    cv2.destroyAllWindows()

initial_data("APOLLO17_DTM_150CM_180_45.tif", "APOLLO17_DTM_150CM.tiff", "crat_circle.shp")

