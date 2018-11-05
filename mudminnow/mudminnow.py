import shapely

from dem import DEM
from geometry_v2 import Geometry


class Mapper:

    '''Mapper class for mapping cross section elevation
    data'''

    def __init__(self, xs_file, reach_file, dem_file):
        self.geometry = Geometry(xs_file, reach_file)
        self.dem = DEM(dem_file)

    def map(self):
        pass