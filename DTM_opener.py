import cv2
import numpy as np
from matplotlib import pyplot as plt
import gdal
import ogr
import osgeo


gdalData = gdal.Open( "APOLLO17_DTM_150CM.tiff")

# print ("Driver short name", gdalData.GetDriver().ShortName)
# print ("Driver long name", gdalData.GetDriver().LongName)
# print ("Raster size", gdalData.RasterXSize, "x", gdalData.RasterYSize)
# print ("Number of bands", gdalData.RasterCount)
# print ("Projection", gdalData.GetProjection())
# print ("Geo transform", gdalData.GetGeoTransform())

xsize = gdalData.RasterXSize
ysize = gdalData.RasterYSize
# получаем растр в виде массива
raster = gdalData.ReadAsArray()
# перебираем все пиксели растра
print(raster)
print(raster[1][1])
