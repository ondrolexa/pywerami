"""
Program to make an contour plot from a contour data file generated
by the Perple_X program WERAMI, for data file format see:
http://www.perplex.ethz.ch/faq/Perple_X_tab_file_format.txt
"""
# author: Ondrej Lexa
# website: petrol.natur.cuni.cz/~ondro
# last edited: April 16, 2014

import numpy as np

class WeramiData(object):
    @classmethod
    def from_tab(self, filename='luca3_1.tab', xvar=0, yvar=1):
        obj = self()
        with open(filename,'r') as f:
            ln = f.readlines()

        obj.version = ln[0].strip()
        obj.label = ln[1].strip()
        ni = int(ln[2])  # number of independent variables

        if ni != 2:
            raise Exception('Only 2d tables are supported now')

        obj.ind = []

        for i in range(ni):
            v={}
            v['name'] = ln[3 + 4*i].strip()
            v['min'] = float(ln[4 + 4*i])
            v['num'] = int(ln[6 + 4*i])
            v['max'] = v['min'] + float(ln[5 + 4*i]) * (v['num'] - 1)
            obj.ind.append(v)
        obj.xvar = xvar
        obj.yvar = yvar

        nd = int(ln[3+4*ni])  # number of dependent properties
        obj.dep = ln[4+4*ni].split()[:nd]
        data = []
        for j in range(5+4*ni,len(ln)):
            data.append(ln[j].split()[:nd])

        data = np.array(data, float)
        obj.data = {}
        for col,var in enumerate(obj.dep):
            obj.data[var] = data[:,col]

        return obj

    def get_xrange(self, divider=1):
        return np.linspace(self.ind[self.xvar]['min'], self.ind[self.xvar]['max'], divider*self.ind[self.xvar]['num'])

    def get_yrange(self, divider=1):
        return np.linspace(self.ind[self.yvar]['min'], self.ind[self.yvar]['max'], divider*self.ind[self.yvar]['num'])

    def get_extent(self):
        return self.ind[self.xvar]['min'], self.ind[self.xvar]['max'], self.ind[self.yvar]['min'], self.ind[self.yvar]['max']

    def get_var(self, var, nan=np.NaN):
        if np.isnan(nan):
            return np.ma.array(self.data[var], mask=np.isnan(self.data[var])).reshape(self.ind[self.yvar]['num'], self.ind[self.xvar]['num'], order='C')
        else:
            return np.ma.array(self.data[var], mask=self.data[var]==nan).reshape(self.ind[self.yvar]['num'], self.ind[self.xvar]['num'], order='C')


