"""
Program to make an contour plot from a contour data file generated
by the Perple_X program WERAMI, for data file format see:
http://www.perplex.ethz.ch/faq/Perple_X_tab_file_format.txt
"""
# author: Ondrej Lexa
# website: petrol.natur.cuni.cz/~ondro
# last edited: April 16, 2014

import sys
import argparse

from pkg_resources import resource_filename

from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
import matplotlib
from scipy import ndimage

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')

from matplotlib import cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from mpl_toolkits.mplot3d import Axes3D

from .ui_pywerami import Ui_MainWindow
from .api import WeramiData

class OptionsForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(OptionsForm, self).__init__(parent)
        settings = QtCore.QSettings("LX", "pywerami")
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QWidget()
        formlayout = QtWidgets.QFormLayout(form)
        
        ## scale
        #self.scale = QLineEdit(repr(settings.value("scale", 1, type=float)), self)
        #self.scale.setValidator(QDoubleValidator(self.scale))
        #formlayout.addRow('Scale', self.scale)
        
        # not-a-number
        self.nan = QtWidgets.QLineEdit(settings.value("nan", "NaN", type=str), self)
        formlayout.addRow('Not a number', self.nan)

        form.setLayout(formlayout)
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        layout.addWidget(form)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        buttonBox.accepted.connect(self.check)
        buttonBox.rejected.connect(self.reject)

        self.setWindowTitle("PyWerami options")

    def check(self):
        try:
            np.float(self.nan.text())
            self.accept()
        except:
            QtWidgets.QMessageBox.warning(self, "Warning", "Not a number must be float number or NaN")

    def accept(self):
        settings = QtCore.QSettings("LX", "pywerami")
        #settings.setValue("scale", float(self.scale.text()))
        settings.setValue("nan", self.nan.text())
        QtWidgets.QDialog.accept(self)

class PyWeramiWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, filename=None, parent=None):
        super(PyWeramiWindow,self).__init__(parent)
        self.settings = QtCore.QSettings("LX", "pywerami")
        self.setupUi(self)
        self._fig = Figure(facecolor="white")
        self._ax = self._fig.add_subplot(111)

        self._canvas = FigureCanvas(self._fig)
        self._canvas.setParent(self.widget)
        self._canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.matplot.addWidget(self._canvas)
        self.mpl_toolbar = NavigationToolbar(self._canvas,self.widget)
        self.mpl_toolbar.hide()
        self.matplot.addWidget(self.mpl_toolbar)
        self.setWindowTitle('PyWerami')
        window_icon = resource_filename(__name__, 'images/pywerami.png')
        self.setWindowIcon(QtGui.QIcon(window_icon))

        #set combos
        self.cmaps = [m for m in cm.datad if not m.endswith("_r")]
        self.mapstyle.addItems(self.cmaps)

        # set validators
        self.levelmin.setValidator(QtGui.QDoubleValidator(self.levelmin))
        self.levelmax.setValidator(QtGui.QDoubleValidator(self.levelmax))
        self.levelnum.setValidator(QtGui.QIntValidator(self.levelmin))
        self.levelstep.setValidator(QtGui.QDoubleValidator(self.levelstep))
        self.clipmin.setValidator(QtGui.QDoubleValidator(self.clipmin))
        self.clipmax.setValidator(QtGui.QDoubleValidator(self.clipmax))
        
        # Set icons in toolbar
        self.actionOpen.setIcon(QtGui.QIcon.fromTheme('document-open'))
        self.actionSave.setIcon(QtGui.QIcon.fromTheme('document-save'))
        self.actionSaveas.setIcon(QtGui.QIcon.fromTheme('document-save-as'))
        self.actionImport.setIcon(QtGui.QIcon.fromTheme('x-office-spreadsheet'))
        self.actionHome.setIcon(self.mpl_toolbar._icon('home.png'))
        self.actionPan.setIcon(self.mpl_toolbar._icon('move.png'))
        self.actionZoom.setIcon(self.mpl_toolbar._icon('zoom_to_rect.png'))
        self.actionGrid.setIcon(QtGui.QIcon.fromTheme('format-justify-fill'))
        self.actionAxes.setIcon(self.mpl_toolbar._icon('qt4_editor_options.png'))
        self.actionSavefig.setIcon(self.mpl_toolbar._icon('filesave.png'))
        #self.action3D.setIcon(QtGui.QIcon.fromTheme(''))
        self.actionProperties.setIcon(QtGui.QIcon.fromTheme('preferences-other'))
        self.actionQuit.setIcon(QtGui.QIcon.fromTheme('application-exit'))
        self.actionAbout.setIcon(QtGui.QIcon.fromTheme('help-about'))
        
        self.actionImport.triggered.connect(self.import_data)
        self.actionHome.triggered.connect(self.mpl_toolbar.home)
        self.actionPan.triggered.connect(self.plotpan)
        self.actionZoom.triggered.connect(self.plotzoom)
        self.actionGrid.triggered.connect(self.plotgrid)
        self.actionAxes.triggered.connect(self.mpl_toolbar.edit_parameters)
        self.actionSavefig.triggered.connect(self.mpl_toolbar.save_figure)
        self.actionProperties.triggered.connect(self.edit_options)
        self.actionQuit.triggered.connect(self.close)
        if filename:
            self.import_data(filename)
        
        # ready
        self.statusbar.showMessage("Ready", 5000)

    def closeEvent(self,event):
        reply=QtWidgets.QMessageBox.question(self,'Message',"Are you sure to quit?",QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply==QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def import_data(self, filename=None):
        if not filename:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, "Import tab file", ".", "TAB (*.tab);;All files (*.*)")[0]
        if filename:
            self.data = WeramiData.from_tab(filename)

            # populate listview and setup properties
            self.props = {}
            self._model = QtGui.QStandardItemModel(self.listView)
            for var in self.data.dep:
                item = QtGui.QStandardItem(var)
                item.setCheckable(True)
                self._model.appendRow(item)
                self.default_var_props(var)

            self.listView.setModel(self._model)
            self.listView.show()
            # connect listview signals
            self.varSel = self.listView.selectionModel()
            self.varSel.selectionChanged.connect(self.on_var_changed)
            self._model.itemChanged.connect(self.plot)
            # buttons signals
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.apply_props)
            self.buttonBox.button(QtWidgets.QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore_props)
            self.contcolor.clicked.connect(self.contours_color)
            self.action3D.triggered.connect(self.switch3d)
            # signals to calculate step size
            self.levelmin.editingFinished.connect(self.step_from_levels)
            self.levelmax.editingFinished.connect(self.step_from_levels)
            self.levelnum.editingFinished.connect(self.step_from_levels)
            self.setlevels.toggled.connect(self.step_from_levels)
            
            # all done focus
            self.action3D.setChecked(False) # no 3d on import
            self.varSel.setCurrentIndex(self._model.index(0, 0), QtCore.QItemSelectionModel.ClearAndSelect | QtCore.QItemSelectionModel.Rows)
            self.listView.setFocus()
            self.plot()
            self.statusbar.showMessage("Data from {} imported".format(self.data.label), 5000)

    def contours_color(self):
    	col = QtGui.QColorDialog.getColor()
    	if col.isValid():
            self.contcolor.setStyleSheet("background-color: {}".format(col.name()))

    def step_from_levels(self):
        if self.setlevels.isChecked():
            step = (float(self.levelmax.text()) - float(self.levelmin.text())) / (int(self.levelnum.text()) - 1)
            self.levelstep.setText(repr(step))
            self.props[self.var]['step'] = step

    def default_var_props(self, var):
        data = self.data.get_var(var)
        prop = {}
        #levels
        prop['min'] = data.min()
        prop['max'] = data.max()
        prop['num'] = 10
        prop['step'] = (prop['max'] - prop['min']) / (prop['num'] - 1)
        prop['levels'] = 'num'
        prop['type'] = 'linear'
        #style
        prop['fill'] = False
        prop['opacity'] = 100
        prop['cmap'] = 'jet'
        prop['contours'] = 'color'
        prop['color'] = '#000000'
        prop['label'] = False
        #processing
        prop['resample'] = 1
        prop['median'] = 1
        prop['gauss'] = 0
        prop['clipmin'] = data.min()
        prop['clipmax'] = data.max()

        self.props[var] = prop

    def set_var_props(self, var):
        #levels
        self.levelmin.setText(repr(self.props[var]['min']))
        self.levelmax.setText(repr(self.props[var]['max']))
        self.levelnum.setText(repr(self.props[var]['num']))
        self.levelstep.setText(repr(self.props[var]['step']))
        if self.props[var]['levels'] == 'num':
            self.setlevels.setChecked(True)
        else:
            self.setstep.setChecked(True)
        if self.props[var]['type'] == 'linear':
            self.linlevel.setChecked(True)
        else:
            self.cdflevel.setChecked(True)
        #style
        if self.props[var]['fill']:
            self.fillstyle.setChecked(True)
        else:
            self.fillstyle.setChecked(False)
        self.opacity.setValue(self.props[var]['opacity'])
        self.mapstyle.setCurrentIndex(self.cmaps.index(self.props[var]['cmap']))
        self.contcolor.setStyleSheet("background-color: {}".format(self.props[var]['color']))
        if self.props[var]['contours'] == 'map':
            self.contcheckmap.setChecked(True)
        elif self.props[var]['contours'] == 'color':
            self.contcheckcolor.setChecked(True)
        else:
            self.contchecknone.setChecked(True)
        if self.props[var]['label']:
            self.contlabel.setChecked(True)
        else:
            self.contlabel.setChecked(False)
        #processing
        self.resample.setValue(self.props[var]['resample'])
        self.filtersize.setValue(self.props[var]['median'])
        self.filtersigma.setValue(self.props[var]['gauss'])
        self.clipmin.setText(repr(self.props[var]['clipmin']))
        self.clipmax.setText(repr(self.props[var]['clipmax']))

    def on_var_changed(self, selected):
        self.var = self.data.dep[selected.indexes()[0].row()]
        self.set_var_props(self.var)
        if self.action3D.isChecked():
            self.plot()

    def apply_props(self):
        #levels
        self.props[self.var]['min'] = float(self.levelmin.text())
        self.props[self.var]['max'] = float(self.levelmax.text())
        self.props[self.var]['num'] = int(self.levelnum.text())
        self.props[self.var]['step'] = float(self.levelstep.text())
        if self.setlevels.isChecked():
            self.props[self.var]['levels'] = 'num'
        else:
            self.props[self.var]['levels'] = 'step'
        if self.linlevel.isChecked():
            self.props[self.var]['type'] = 'linear'
        else:
            self.props[self.var]['type'] = 'cdf'
        #style
        if self.fillstyle.isChecked():
            self.props[self.var]['fill'] = True
        else:
            self.props[self.var]['fill'] = False
        self.props[self.var]['opacity'] = self.opacity.value()
        self.props[self.var]['cmap'] = str(self.mapstyle.currentText())
        self.props[self.var]['color'] = str(self.contcolor.palette().color(1).name())
        if self.contcheckmap.isChecked():
            self.props[self.var]['contours'] = 'map'
        elif self.contcheckcolor.isChecked():
            self.props[self.var]['contours'] = 'color'
        else:
            self.props[self.var]['contours'] = ''
        if self.contlabel.isChecked():
            self.props[self.var]['label'] = True
        else:
            self.props[self.var]['label'] = False
        #processing
        self.props[self.var]['resample'] = self.resample.value()
        self.props[self.var]['median'] = self.filtersize.value()
        self.props[self.var]['gauss'] = self.filtersigma.value()
        self.props[self.var]['clipmin'] = float(self.clipmin.text())
        self.props[self.var]['clipmax'] = float(self.clipmax.text())
        self.plot()

    def restore_props(self):
        self.default_var_props(self.var)
        self.set_var_props(self.var)
        self.plot()

    def edit_options(self):
        dlg = OptionsForm(self)
        dlg.exec_()

    def plotpan(self):
        self.actionZoom.setChecked(False)
        self.mpl_toolbar.pan()

    def plotzoom(self):
        self.actionPan.setChecked(False)
        self.mpl_toolbar.zoom()

    def plotgrid(self):
        self._ax.grid()
        self._canvas.draw()

    def switch3d(self):
        if not self.action3D.isChecked():
            self._fig.clear()
            self._ax = self._fig.add_subplot(111)
        else:
            self._fig.clear()
            self._ax = self._fig.add_subplot(111, projection='3d')
        self.plot()

    def plot(self):
        self._ax.cla()
        if not self.action3D.isChecked():
            extent = self.data.get_extent()
            i = 0
            while self._model.item(i):
                if self._model.item(i).checkState():
                    CS = None
                    var = str(self._model.item(i).text())
                    # get data, smooth and clip
                    data = self.data.get_var(var,nan=np.float(self.settings.value("nan", "NaN", type=str)))
                    if self.props[var]['resample'] > 1:
                        data = np.ma.array(ndimage.zoom(data.filled(0), self.props[var]['resample']), mask=ndimage.zoom(data.mask, self.props[var]['resample'], order=0))
                    if self.props[var]['median'] > 1:
                        data = np.ma.array(ndimage.median_filter(data, size=self.props[var]['median']*self.props[var]['resample']), mask=data.mask)
                    if self.props[var]['gauss'] > 0:
                        data = np.ma.array(ndimage.gaussian_filter(data, sigma=self.props[var]['gauss']*self.props[var]['resample']), mask=data.mask)
                    data = np.ma.masked_outside(data, self.props[var]['clipmin'], self.props[var]['clipmax'])
                    if self.props[var]['fill']:
                        self._ax.imshow(data, interpolation='none', origin='lower', extent=extent, aspect='auto', cmap=cm.get_cmap(self.props[var]['cmap']), alpha=self.props[var]['opacity']/100.0)
                    if self.props[var]['type'] == 'linear':
                        if self.props[var]['levels'] == 'num':
                            clevels = np.linspace(self.props[var]['min'], self.props[var]['max'], self.props[var]['num'])
                        else:
                            # trick to include max in levels
                            clevels = np.arange(self.props[var]['min'], self.props[var]['max'] + 10**np.ceil(np.log10(np.abs(self.props[var]['max']))), self.props[var]['step'])
                    else:
                        # cdf based on histogram binned acording to the Freedman-Diaconis rule
                        v = np.sort(data.compressed())
                        IQR = v[int(round((v.size-1) * float(0.75)))] - v[int(round((v.size-1) * float(0.25)))]
                        bin_size = 2 * IQR * v.size**(-1.0/3)
                        nbins = int(round(max(self.props[var]['num'], (v[-1]-v[0]) / (bin_size+0.001))))
                        hist, bin_edges = np.histogram(v, bins=nbins)
                        cdf = np.cumsum(hist)
                        cdfx = np.cumsum(np.diff(bin_edges)) + bin_edges[:2].sum()/2
                        clevels = np.interp(np.linspace(cdf[0],cdf[-1],self.props[var]['num'] + 2)[1:-1], cdf, cdfx)
                    if self.props[var]['contours'] == 'map':
                        CS = self._ax.contour(self.data.get_xrange(self.props[var]['resample']), self.data.get_yrange(self.props[var]['resample']), data, clevels, cmap=cm.get_cmap(self.props[var]['cmap']))
                    elif self.props[var]['contours'] == 'color':
                        CS = self._ax.contour(self.data.get_xrange(self.props[var]['resample']), self.data.get_yrange(self.props[var]['resample']), data, clevels, colors=self.props[var]['color'])
                    if self.props[var]['label'] and CS:
                        self._ax.clabel(CS, fontsize=8, inline=1)
                i += 1

            self._ax.axis(extent)
            self._ax.set_title(self.data.label)
        else:
            # get data, smooth and clip
            data = self.data.get_var(self.var)
            if self.props[self.var]['resample'] > 1:
                data = np.ma.array(ndimage.zoom(data.filled(0), self.props[self.var]['resample']), mask=ndimage.zoom(data.mask, self.props[self.var]['resample'], order=0))
            if self.props[self.var]['median'] > 1:
                data = np.ma.array(ndimage.median_filter(data, size=self.props[self.var]['median']*self.props[self.var]['resample']), mask=data.mask)
            if self.props[self.var]['gauss'] > 0:
                data = np.ma.array(ndimage.gaussian_filter(data, sigma=self.props[self.var]['gauss']*self.props[self.var]['resample']), mask=data.mask)
            data = np.ma.masked_outside(data, self.props[self.var]['clipmin'], self.props[self.var]['clipmax'])
            x,y = np.meshgrid(self.data.get_xrange(self.props[self.var]['resample']), self.data.get_yrange(self.props[self.var]['resample']))
            self._ax.plot_surface(x, y, data.filled(np.NaN), vmin=data.min(), vmax=data.max(), cmap=cm.get_cmap(self.props[self.var]['cmap']), linewidth=0.5, alpha=self.props[self.var]['opacity']/100.0)
            self._ax.view_init(azim=235, elev=30)

        self._ax.set_xlabel(self.data.ind[self.data.xvar]['name'])
        self._ax.set_ylabel(self.data.ind[self.data.yvar]['name'])
        self._fig.tight_layout()
        self._canvas.draw()


def process_cl_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store', nargs='?', default=None, help="Werami tab file")

    parsed_args, unparsed_args = parser.parse_known_args()
    return parsed_args, unparsed_args

def main():
    parsed_args, unparsed_args = process_cl_args()
    app = QtWidgets.QApplication(unparsed_args)
    MainWindow = PyWeramiWindow(parsed_args.filename)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

