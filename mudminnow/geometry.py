import shapefile
import os
from shapely.geometry import LineString, MultiLineString

import math


class XS:
    '''Cross section class that holds individual 
    geometry of each cross section'''

    def __init__(self, fid, geom, z):
        self.fid = fid
        self.geom = geom
        self.z = z
        self.xs_reach_pnt = None

    def __repr__(self):
        return f'XS({self.fid}, {self.geom})'

    def station(self, reach_geom):
        '''Sets the cross section point that intersects the reach line, and 
        returns the station of the cross section along the parent reach'''
        self.xs_reach_pnt = LineString(self.geom).intersection(LineString(reach_geom))
        return LineString(reach_geom).project(self.xs_reach_pnt)
    
    def densify(self):
        '''Densify cross section line to improve interpolation scheme.
        Returns LineString with densified lines'''
        max_dist = 10.0
        line = LineString(self.geom)
        dense_geom = []
        if line.length > max_dist:
            for idx, pnt in enumerate(line.coords):
                dense_geom.append(pnt)

                if idx != (len(line.coords) - 1): # This avoids running the operation on the last coord
                    pnt_us = line.coords[idx+1]
                    pnt_ds = line.coords[idx]
                    dist = math.sqrt((pnt_us[0] - pnt_ds[0])**2 + (pnt_us[1] - pnt_ds[1])**2)
                    break_cnt = int(dist/max_dist) # Rounds down to get number of pnts to add

                    for brk in range(break_cnt):
                        pnt_dist = (brk+1)*max_dist
                        pnt_add = LineString([pnt_us, pnt_ds]).interpolate(pnt_dist) # Returns a point feature
                        dense_geom.append(pnt_add.coords)
        
        else:
            dense_geom = self.geom
        
        dense_geom = [(c[0], c[1], self.z) for c in dense_geom]
        
        return LineString(dense_geom)


class Reach:
    '''Reach class that represents individual reaches with 
    member cross sections'''

    def __init__(self, name, geom):
        self.name = name
        self.geom = geom
        self.xs = []
        self._xs_coords = []

    def __repr__(self):
        return f'Reach({self.name}, {self.geom})'

    def __len__(self):
        return(len(self.xs))

    def __getitem__(self, position):
        return self.xs[position]
    
    def boundary(self):
        return MultiLineString(self._xs_coords).convex_hull

    def add_xs(self, fid, xs_geom, z):
        self.xs.append(XS(fid, xs_geom, z))
        self._xs_coords.append(xs_geom)
    

class Geometry:
    'Geometry class that represents a group of reach classes'

    def __init__(self, xs_shp, reach_shp):
        if not type(xs_shp)==str:
            raise IOError('Give valid filepath string for xs_shp')
        if not type(reach_shp)==str:
            raise IOError('Give valid filepath string for reach_shp')
        if not os.path.isfile(xs_shp):
            raise IOError('xs_shp is not a valid filename')
        if not os.path.isfile(reach_shp):
            raise IOError('reach_shp is not a valid filename')

        self.xs_sf = shapefile.Reader(xs_shp)
        self.reach_sf = shapefile.Reader(reach_shp)
        self.reaches = []

    def __len__(self):
        return(len(self.reaches))

    def __getitem__(self, position):
        return self.reaches[position]

    def read(self):

        for reach_rec in self.reach_sf.shapeRecords():
            reach = Reach(reach_rec.record['ReachName'],
                          reach_rec.shape.points)

            for xs_rec in self.xs_sf.shapeRecords():
                if xs_rec.record['ReachName'] == reach_rec.record['ReachName']:
                    reach.add_xs(xs_rec.record.oid, xs_rec.shape.points, xs_rec.record['WSE'])

            self.reaches.append(reach)
     
        




        

