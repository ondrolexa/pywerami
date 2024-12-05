"""
Program to make an contour plot from a contour data file generated
by the Perple_X program WERAMI, for data file format see:
http://www.perplex.ethz.ch/faq/Perple_X_tab_file_format.txt
"""
# author: Ondrej Lexa
# website: petrol.natur.cuni.cz/~ondro
# last edited: April 16, 2014

import numpy as np
from collections import Counter


class GridData:
    def __init__(self, version, label, ind, xvar, yvar, dep, data):
        self.version = version
        self.label = label
        self.ind = ind
        self.xvar = xvar
        self.yvar = yvar
        self.dep = dep
        self.data = data

    @classmethod
    def from_tab(cls, filename, xvar=0, yvar=1, degrees=False):
        with open(filename, 'r') as f:
            ln = f.readlines()

        version = ln[0].strip()
        label = ln[1].strip()
        ni = int(ln[2])  # number of independent variables

        if ni != 2:
            raise Exception('Only 2d tables are supported now')

        ind = []

        for i in range(ni):
            v = {}
            v['name'] = ln[3 + 4 * i].strip()
            v['num'] = int(ln[6 + 4 * i])
            if v['name'] == 'T(K)' and degrees:
                v['min'] = float(ln[4 + 4 * i]) - 273.15
                v['name'] = 'T(C)'
            else:
                v['min'] = float(ln[4 + 4 * i])
            v['max'] = v['min'] + float(ln[5 + 4 * i]) * (v['num'] - 1)
            ind.append(v)

        nd = int(ln[3 + 4 * ni])  # number of dependent properties
        dep = ln[4 + 4 * ni].split()[:nd]
        # Check for possible duplicates
        counts = Counter(dep)
        for s, num in counts.items():
            if num > 1:
                for suffix in range(1, num + 1):
                    dep[dep.index(s)] = s + str(suffix)
        datalist = []
        for j in range(5 + 4 * ni, len(ln)):
            datalist.append(ln[j].split()[:nd])

        dataarray = np.array(datalist, float)
        data = {}
        for col, var in enumerate(dep):
            data[var] = dataarray[:, col]

        try:
            dep.remove('T(K)')
            dep.remove('P(bar)')
        except Exception:
            pass
        return cls(version, label, ind, xvar, yvar, dep, data)

    @classmethod
    def from_tci(cls, filename, degrees=True):
        import scipy.io as sio
        import ntpath
        tci = sio.loadmat(filename)['pseudodata'][0]
        opt = {'currentDir', 'workingDir', 'InputData', 'TCversion', 'paths', 'SectionDetails'}
        dep = sorted(list(set(tci.dtype.names).difference(opt)))
        version = str(tci['TCversion'][0][0, 0])
        label = ntpath.basename(tci['paths'][0]['InputFilepath'][0, 0][0])
        xvar = 0
        yvar = 1
        x = tci['SectionDetails'][0][1, 0][0]
        y = tci['SectionDetails'][0][0, 0][0]
        if degrees:
            vx = dict(name='T(C)', min=x.min(), num=len(x), max=x.max())
        else:
            vx = dict(name='T(K)', min=x.min() + 273.15, num=len(x), max=x.max() + 273.15)
        vy = dict(name='p(kbar)', min=y.min(), num=len(y), max=y.max())
        ind = [vx, vy]
        data = {}
        dep = []
        for d in dep:
            if tci[d][0].dtype.names:
                for p in tci[d][0].dtype.names:
                    key = d + '-' + p
                    data[key] = tci[d][0][p][0, 0].flatten(order='C')
                    dep.append(key)
            else:
                data[d] = tci[d][0].flatten(order='C')
                dep.append(d)

        return cls(version, label, ind, xvar, yvar, dep, data)

    def get_xrange(self, divider=1):
        return np.linspace(self.ind[self.xvar]['min'], self.ind[self.xvar]['max'], divider * self.ind[self.xvar]['num'])

    def get_yrange(self, divider=1):
        return np.linspace(self.ind[self.yvar]['min'], self.ind[self.yvar]['max'], divider * self.ind[self.yvar]['num'])

    def get_extent(self):
        return self.ind[self.xvar]['min'], self.ind[self.xvar]['max'], self.ind[self.yvar]['min'], self.ind[self.yvar]['max']

    def get_var(self, var, nan=np.nan):
        if np.isnan(nan):
            return np.ma.array(self.data[var], mask=np.isnan(self.data[var])).reshape(self.ind[self.yvar]['num'], self.ind[self.xvar]['num'], order='C')
        else:
            return np.ma.array(self.data[var], mask=self.data[var] == nan).reshape(self.ind[self.yvar]['num'], self.ind[self.xvar]['num'], order='C')
