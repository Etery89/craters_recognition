import ogr


def calculate_dd(shp_name):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(shp_name, 1)
    crat_layer = dataSource.GetLayer()
    dd_name = ogr.FieldDefn("Dd", ogr.OFTReal)
    dd_name.SetWidth(18)
    dd_name.SetPrecision(2)
    featDef = crat_layer.GetLayerDefn()
    if featDef.GetFieldDefn(5) is None:
        print('create dd')
        crat_layer.CreateField(dd_name)

    for crat_feature in crat_layer:
        diam = crat_feature.GetField('diam_m')
        depth = crat_feature.GetField('Depth')
        dd = float(depth / diam)
        crat_feature.SetField('Dd', dd)
        crat_layer.SetFeature(crat_feature)


if __name__ == "__main__":
    # dtm_input = "C:\\projects\\craters_recognition\\GLD100_test.tif"
    shp_name = "crat_circle.shp"
    calculate_dd(shp_name)
