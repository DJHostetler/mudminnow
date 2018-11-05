from osgeo import gdal
import os

class DEM:

    '''DEM class for reading and editing geotiff DEM rasters'''

    def __init__(self,path):
        if type(path)==str and os.path.isfile(path):
            self.path=path
            self.raster=gdal.Open(path)
        elif type(path)==str and not os.path.isfile(path):
            raise IOError

    def x(self):
        return self.raster.RasterXSize

    def y(self):
        return self.raster.RasterYSize
    
    def bands(self):
        return self.raster.RasterCount

    def array(self):
        return self.raster.ReadAsArray()
    
    def clip(self, bounds):
        #gdal.Translate('/vsimem/clip.tif', )
        pass