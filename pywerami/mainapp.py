"""
Program to make an contour plot from a contour data file generated
by the Perple_X program WERAMI, for data file format see:
http://www.perplex.ethz.ch/faq/Perple_X_tab_file_format.txt
"""
# author: Ondrej Lexa
# website: petrol.natur.cuni.cz/~ondro
# last edited: April 16, 2014

import sys
import os
import pickle
import gzip
import argparse

import importlib.resources as ires
import importlib.metadata as imeta

from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np
import matplotlib
from scipy import ndimage

from matplotlib import cm
# from matplotlib import ticker
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from mpl_toolkits.mplot3d import Axes3D

from .ui_pywerami import Ui_MainWindow
from .api import GridData

try:
    __version__ = imeta.version("pywerami")
except imeta.PackageNotFoundError:
    __version__ = "unknown"

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')


class PyWeramiWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, filename=None, parent=None):
        super(PyWeramiWindow, self).__init__(parent)
        self.settings = QtCore.QSettings("LX", "pywerami")
        self.setupUi(self)
        self._fig = Figure(facecolor="white")
        self._ax = self._fig.add_subplot(111)

        self._canvas = FigureCanvas(self._fig)
        self._canvas.setParent(self.widget)
        self._canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.matplot.addWidget(self._canvas)
        self.mpl_toolbar = NavigationToolbar(self._canvas, self.widget)
        self.mpl_toolbar.hide()
        self.matplot.addWidget(self.mpl_toolbar)
        self.setWindowTitle('PyWerami')
        window_icon = str(ires.files("pywerami").joinpath("images/pywerami.png"))
        self.setWindowIcon(QtGui.QIcon(window_icon))
        self.about_dialog = AboutDialog(__version__)

        # set combos
        self.cmaps = ['viridis', 'inferno', 'plasma', 'magma', 'Blues', 'BuGn', 'BuPu',
                      'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd', 'PuBu', 'PuBuGn',
                      'PuRd', 'Purples', 'RdPu', 'Reds', 'YlGn', 'YlGnBu', 'YlOrBr',
                      'YlOrRd', 'afmhot', 'autumn', 'bone', 'cool', 'copper', 'gist_heat',
                      'gray', 'hot', 'pink', 'spring', 'summer', 'winter', 'BrBG', 'bwr',
                      'coolwarm', 'PiYG', 'PRGn', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu',
                      'RdYlGn', 'Spectral', 'seismic', 'gist_earth', 'terrain', 'ocean',
                      'gist_stern', 'brg', 'CMRmap', 'cubehelix', 'gnuplot', 'gnuplot2',
                      'gist_ncar', 'nipy_spectral', 'jet', 'rainbow', 'gist_rainbow',
                      'hsv', 'flag', 'prism']
        self.mapstyle.addItems(self.cmaps)

        # set validators
        self.levelmin.setValidator(QtGui.QDoubleValidator(self.levelmin))
        self.levelmax.setValidator(QtGui.QDoubleValidator(self.levelmax))
        self.levelnum.setValidator(QtGui.QIntValidator(self.levelnum))
        self.levelstep.setValidator(QtGui.QDoubleValidator(self.levelstep))
        self.clipmin.setValidator(QtGui.QDoubleValidator(self.clipmin))
        self.clipmax.setValidator(QtGui.QDoubleValidator(self.clipmax))

        # Set icons in toolbar
        self.actionOpen.setIcon(QtGui.QIcon.fromTheme('document-open'))
        self.actionSave.setIcon(QtGui.QIcon.fromTheme('document-save'))
        self.actionSaveas.setIcon(QtGui.QIcon.fromTheme('document-save-as'))
        self.actionImport.setIcon(QtGui.QIcon.fromTheme('document-new'))
        self.actionHome.setIcon(self.mpl_toolbar._icon('home.png'))
        self.actionPan.setIcon(self.mpl_toolbar._icon('move.png'))
        self.actionZoom.setIcon(self.mpl_toolbar._icon('zoom_to_rect.png'))
        self.actionGrid.setIcon(QtGui.QIcon.fromTheme('format-justify-fill'))
        self.actionAxes.setIcon(self.mpl_toolbar._icon('qt4_editor_options.png'))
        self.actionSavefig.setIcon(self.mpl_toolbar._icon('filesave.png'))
        # self.action3D.setIcon(QtGui.QIcon.fromTheme(''))
        self.actionProperties.setIcon(QtGui.QIcon.fromTheme('preferences-other'))
        self.actionQuit.setIcon(QtGui.QIcon.fromTheme('application-exit'))
        self.actionAbout.setIcon(QtGui.QIcon.fromTheme('help-about'))

        # connect signals
        self.actionOpen.triggered.connect(self.openProject)
        self.actionSave.triggered.connect(self.saveProject)
        self.actionSaveas.triggered.connect(self.saveProjectAs)
        self.actionImport.triggered.connect(self.import_data)
        self.actionHome.triggered.connect(self.mpl_toolbar.home)
        self.actionPan.triggered.connect(self.plotpan)
        self.actionZoom.triggered.connect(self.plotzoom)
        self.actionGrid.triggered.connect(self.plotgrid)
        self.actionAxes.triggered.connect(self.mpl_toolbar.edit_parameters)
        self.actionSavefig.triggered.connect(self.mpl_toolbar.save_figure)
        self.actionProperties.triggered.connect(self.edit_options)
        self.actionQuit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about_dialog.exec)

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
        # almost done
        self.ready = False
        self.changed = False
        self.project = None

        if filename:
            self.import_data(filename)

        # ready
        self.statusbar.showMessage("Ready", 5000)

    def closeEvent(self, event):
        if self.changed:
            quit_msg = 'Project have been changed. Save ?'
            qb = QtWidgets.QMessageBox
            reply = qb.question(self, 'Message', quit_msg,
                                qb.Cancel | qb.Discard | qb.Save, qb.Save)

            if reply == qb.Save:
                self.do_save()
                if self.project is not None:
                    event.accept()
                else:
                    event.ignore()
            elif reply == qb.Discard:
                event.accept()
            else:
                event.ignore()

    def import_data(self, filename=None):
        if not filename:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, "Import data file", ".", "Perple_X Table (*.tab *.TAB);;TCInvestigator (*.tci *.TCI)")[0]
        if filename:
            if filename.lower().endswith('.tab'):
                self.data = GridData.from_tab(filename, degrees=self.settings.value("degrees", False, type=bool))
            elif filename.lower().endswith('.tci'):
                self.data = GridData.from_tci(filename, degrees=self.settings.value("degrees", False, type=bool))
            else:
                raise Exception('Unsupported file format')
            # populate listview and setup properties
            self.datafilename = filename
            self.ready = True
            self.project = None
            self.changed = True
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
            try:
                self.varSel.selectionChanged.disconnect()
            except Exception:
                pass
            self.varSel.selectionChanged.connect(self.on_var_changed)
            try:
                self._model.itemChanged.disconnect()
            except Exception:
                pass
            self._model.itemChanged.connect(self.plot)

            # all done focus
            self.action3D.setChecked(False)  # no 3d on import
            self.varSel.setCurrentIndex(self._model.index(0, 0), QtCore.QItemSelectionModel.ClearAndSelect | QtCore.QItemSelectionModel.Rows)
            self.listView.setFocus()
            self.plot()
            self.statusbar.showMessage("Data from {} imported".format(self.data.label), 5000)

    def openProject(self, checked, projfile=None):
        """Open pywerami project
        """
        if self.changed:
            quit_msg = 'Project have been changed. Save ?'
            qb = QtWidgets.QMessageBox
            reply = qb.question(self, 'Message', quit_msg,
                                qb.Discard | qb.Save,
                                qb.Save)

            if reply == qb.Save:
                self.do_save()
        if projfile is None:
            qd = QtWidgets.QFileDialog
            filt = 'pywermi project (*.pwp)'
            projfile = qd.getOpenFileName(self, 'Open project',
                                          os.path.expanduser('~'),
                                          filt)[0]
        if os.path.exists(projfile):
            stream = gzip.open(projfile, 'rb')
            data = pickle.load(stream)
            stream.close()
            # set actual working dir in case folder was moved
            self.datafilename = data['datafilename']
            self.import_data(self.datafilename)
            self.props = data['props']
            # all done
            self.ready = True
            self.project = projfile
            self.changed = False
            # all done focus
            self.action3D.setChecked(False)  # no 3d on import
            self.varSel.setCurrentIndex(self._model.index(0, 0), QtCore.QItemSelectionModel.ClearAndSelect | QtCore.QItemSelectionModel.Rows)
            self.listView.setFocus()
            self.plot()
            self.statusbar.showMessage("Project loaded.", 5000)

    def saveProject(self):
        """Save project
        """
        if self.ready:
            if self.project is None:
                filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save current project',
                                                                 os.path.dirname(self.datafilename),
                                                                 'pywerami project (*.pwp)')[0]
                if filename:
                    if not filename.lower().endswith('.pwp'):
                        filename = filename + '.pwp'
                    self.project = filename
                    self.do_save()
            else:
                self.do_save()

    def saveProjectAs(self):
        """Save project as
        """
        if self.ready:
            filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save current project as',
                                                             os.path.dirname(self.datafilename),
                                                             'pywerami project (*.pwp)')[0]
            if filename:
                if not filename.lower().endswith('.pwp'):
                    filename = filename + '.pwp'
                self.project = filename
                self.do_save()

    def do_save(self):
        """Do saving of poject
        """
        if self.project:
            # put to dict
            data = {'datafilename': self.datafilename,
                    'props': self.props}
            # do save
            stream = gzip.open(self.project, 'wb')
            pickle.dump(data, stream)
            stream.close()
            self.changed = False
            self.statusBar().showMessage('Project saved.')

    def contours_color(self):
        if self.ready:
            col = QtWidgets.QColorDialog.getColor()
            if col.isValid():
                self.contcolor.setStyleSheet("background-color: {}".format(col.name()))

    def step_from_levels(self):
        if self.ready:
            if int(self.levelnum.text()) < 2:
                self.levelnum.setText('2')
            if float(self.levelmax.text()) < float(self.levelmin.text()):
                self.levelmin.setText(self.levelmax.text())
            if self.setlevels.isChecked():
                step = (float(self.levelmax.text()) - float(self.levelmin.text())) / (int(self.levelnum.text()) - 1)
                self.levelstep.setText(str(step))
                self.props[self.var]['step'] = step
                self.changed = True

    def default_var_props(self, var):
        if self.ready:
            data = self.data.get_var(var)
            prop = {}
            # levels
            prop['min'] = data.min()
            prop['max'] = data.max()
            prop['num'] = 10
            prop['step'] = (prop['max'] - prop['min']) / (prop['num'] - 1)
            prop['levels'] = 'num'
            prop['type'] = 'linear'
            # style
            prop['fill'] = False
            prop['cbar'] = False
            prop['opacity'] = 100
            prop['cmap'] = 'viridis'
            prop['contours'] = 'color'
            prop['color'] = '#000000'
            prop['label'] = False
            prop['digits'] = 3
            # processing
            prop['resample'] = 1
            prop['median'] = 1
            prop['gauss'] = 0
            prop['clipmin'] = data.min()
            prop['clipmax'] = data.max()

            self.props[var] = prop

    def set_var_props(self, var):
        if self.ready:
            # levels
            self.levelmin.setText(str(self.props[var]['min']))
            self.levelmax.setText(str(self.props[var]['max']))
            self.levelnum.setText(str(self.props[var]['num']))
            self.levelstep.setText(str(self.props[var]['step']))
            if self.props[var]['levels'] == 'num':
                self.setlevels.setChecked(True)
            else:
                self.setstep.setChecked(True)
            if self.props[var]['type'] == 'linear':
                self.linlevel.setChecked(True)
            else:
                self.cdflevel.setChecked(True)
            # style
            if self.props[var]['fill']:
                self.fillstyle.setChecked(True)
            else:
                self.fillstyle.setChecked(False)
            if self.props[var].get('cbar', False):
                self.checkCBar.setChecked(True)
            else:
                self.checkCBar.setChecked(False)
            self.opacity.setValue(self.props[var]['opacity'])
            self.mapstyle.setCurrentIndex(self.cmaps.index(self.props[var]['cmap']))
            self.contcolor.setStyleSheet("background-color: {}".format(self.props[var]['color']))
            self.labelDigits.setValue(self.props[var]['digits'])
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
            # processing
            self.resample.setValue(self.props[var]['resample'])
            self.filtersize.setValue(self.props[var]['median'])
            self.filtersigma.setValue(self.props[var]['gauss'])
            self.clipmin.setText(str(self.props[var]['clipmin']))
            self.clipmax.setText(str(self.props[var]['clipmax']))

    def on_var_changed(self, selected):
        if self.ready:
            self.var = self.data.dep[selected.indexes()[0].row()]
            self.set_var_props(self.var)
            if self.action3D.isChecked():
                self.plot()

    def apply_props(self):
        if self.ready:
            # levels
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
            # style
            if self.fillstyle.isChecked():
                self.props[self.var]['fill'] = True
            else:
                self.props[self.var]['fill'] = False
            if self.checkCBar.isChecked():
                self.props[self.var]['cbar'] = True
            else:
                self.props[self.var]['cbar'] = False
            self.props[self.var]['opacity'] = self.opacity.value()
            self.props[self.var]['cmap'] = str(self.mapstyle.currentText())
            self.props[self.var]['color'] = str(self.contcolor.palette().color(1).name())
            self.props[self.var]['digits'] = self.labelDigits.value()
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
            # processing
            self.props[self.var]['resample'] = self.resample.value()
            self.props[self.var]['median'] = self.filtersize.value()
            self.props[self.var]['gauss'] = self.filtersigma.value()
            self.props[self.var]['clipmin'] = float(self.clipmin.text())
            self.props[self.var]['clipmax'] = float(self.clipmax.text())
            self.changed = True
            self.plot()

    def restore_props(self):
        if self.ready:
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
        if self.ready:
            self.plot()

    def plot(self, item=None):
        if self.ready:
            if not self.action3D.isChecked():
                self._fig.clear()
                self._ax = self._fig.add_subplot(111)
            else:
                self._fig.clear()
                self._ax = self._fig.add_subplot(111, projection='3d')
            if item:
                index = self._model.createIndex(item.row(), item.column())
                if index.isValid():
                    self.listView.setCurrentIndex(index)
            if not self.action3D.isChecked():
                extent = self.data.get_extent()
                i = 0
                while self._model.item(i):
                    if self._model.item(i).checkState():
                        CS = None
                        var = str(self._model.item(i).text())
                        # get data, smooth and clip
                        data = self.data.get_var(var, nan=float(self.settings.value("nan", "NaN", type=str)))
                        if self.props[var]['resample'] > 1:
                            data = np.ma.array(ndimage.zoom(data.filled(0), self.props[var]['resample']), mask=ndimage.zoom(data.mask, self.props[var]['resample'], order=0))
                        if self.props[var]['median'] > 1:
                            data = np.ma.array(ndimage.median_filter(data, size=self.props[var]['median'] * self.props[var]['resample']), mask=data.mask)
                        if self.props[var]['gauss'] > 0:
                            data = np.ma.array(ndimage.gaussian_filter(data, sigma=self.props[var]['gauss'] * self.props[var]['resample']), mask=data.mask)
                        data = np.ma.masked_outside(data, self.props[var]['clipmin'], self.props[var]['clipmax'])
                        if self.props[var]['fill']:
                            img = self._ax.imshow(data, interpolation='none', origin='lower', extent=extent, aspect='auto', cmap=cm.get_cmap(self.props[var]['cmap']), alpha=self.props[var]['opacity'] / 100.0)
                            if self.props[var]['cbar']:
                                cbar = self._fig.colorbar(img)
                                cbar.ax.set_ylabel(var)
                        if self.props[var]['min'] == self.props[var]['max']:
                            clevels = np.array([self.props[var]['min']])
                        else:
                            if self.props[var]['type'] == 'linear':
                                if self.props[var]['levels'] == 'num':
                                    clevels = np.linspace(self.props[var]['min'], self.props[var]['max'], self.props[var]['num'])
                                else:
                                    # trick to include max in levels
                                    clevels = np.arange(self.props[var]['min'], self.props[var]['max'] + np.finfo(np.float32).eps, self.props[var]['step'])
                            else:
                                # cdf based on histogram binned acording to the Freedman-Diaconis rule
                                data = np.ma.masked_outside(data, self.props[var]['min'], self.props[var]['max'])
                                v = np.sort(data.compressed())
                                v = v[np.invert(np.isnan(v))]
                                IQR = v[int(round((v.size - 1) * float(0.75)))] - v[int(round((v.size - 1) * float(0.25)))]
                                bin_size = 2 * IQR * v.size**(-1.0 / 3)
                                nbins = int(round(max(self.props[var]['num'], (v[-1] - v[0]) / (bin_size + 0.001))))
                                hist, bin_edges = np.histogram(v, bins=nbins)
                                cdf = np.cumsum(hist)
                                cdfx = np.cumsum(np.diff(bin_edges)) + bin_edges[:2].sum() / 2
                                # clevels = np.interp(np.linspace(cdf[0],cdf[-1],self.props[var]['num'] + 2)[1:-1], cdf, cdfx)
                                clevels = np.interp(np.linspace(cdf[0], cdf[-1], self.props[var]['num']), cdf, cdfx)
                        clevels = np.round(10**self.props[var]['digits'] * clevels) / 10**self.props[var]['digits']
                        # Contour levels must be increasing
                        clevels = np.append(clevels[:1], clevels[1:][np.diff(clevels) > 0])
                        if self.props[var]['contours'] == 'map':
                            CS = self._ax.contour(self.data.get_xrange(self.props[var]['resample']), self.data.get_yrange(self.props[var]['resample']), data, clevels, cmap=cm.get_cmap(self.props[var]['cmap']))
                        elif self.props[var]['contours'] == 'color':
                            CS = self._ax.contour(self.data.get_xrange(self.props[var]['resample']), self.data.get_yrange(self.props[var]['resample']), data, clevels, colors=self.props[var]['color'])
                        if self.props[var]['label'] and CS:
                            self._ax.clabel(CS, fontsize=8, inline=1, fmt='%g')
                    i += 1

                self._ax.axis(extent)
                self._ax.set_title(self.data.label)
            else:
                # get data, smooth and clip
                data = self.data.get_var(self.var)
                if self.props[self.var]['resample'] > 1:
                    data = np.ma.array(ndimage.zoom(data.filled(0), self.props[self.var]['resample']), mask=ndimage.zoom(data.mask, self.props[self.var]['resample'], order=0))
                if self.props[self.var]['median'] > 1:
                    data = np.ma.array(ndimage.median_filter(data, size=self.props[self.var]['median'] * self.props[self.var]['resample']), mask=data.mask)
                if self.props[self.var]['gauss'] > 0:
                    data = np.ma.array(ndimage.gaussian_filter(data, sigma=self.props[self.var]['gauss'] * self.props[self.var]['resample']), mask=data.mask)
                data = np.ma.masked_outside(data, self.props[self.var]['clipmin'], self.props[self.var]['clipmax'])
                x, y = np.meshgrid(self.data.get_xrange(self.props[self.var]['resample']), self.data.get_yrange(self.props[self.var]['resample']))
                img = self._ax.plot_surface(x, y, data.filled(np.nan), vmin=data.min(), vmax=data.max(), cmap=cm.get_cmap(self.props[self.var]['cmap']), linewidth=0.5, alpha=self.props[self.var]['opacity'] / 100.0)
                self._ax.view_init(azim=235, elev=30)
                if self.props[self.var]['cbar']:
                    cbar = self._fig.colorbar(img)
                    cbar.ax.set_ylabel(self.var)

            self._ax.set_xlabel(self.data.ind[self.data.xvar]['name'])
            self._ax.set_ylabel(self.data.ind[self.data.yvar]['name'])
            self._fig.tight_layout()
            self._canvas.draw()


class OptionsForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(OptionsForm, self).__init__(parent)
        settings = QtCore.QSettings("LX", "pywerami")
        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QWidget()
        formlayout = QtWidgets.QFormLayout(form)

        # scale
        # self.scale = QLineEdit(str(settings.value("scale", 1, type=float)), self)
        # self.scale.setValidator(QDoubleValidator(self.scale))
        # formlayout.addRow('Scale', self.scale)

        # not-a-number
        self.nan = QtWidgets.QLineEdit(settings.value("nan", "NaN", type=str), self)
        self.degrees = QtWidgets.QCheckBox("Temperature in degrees")
        if settings.value("degrees", False, type=bool):
            self.degrees.setChecked(True)
        formlayout.addRow('Not a number', self.nan)
        formlayout.addRow(self.degrees)

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
            float(self.nan.text())
            self.accept()
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Warning", "Not a number must be float number or NaN")

    def accept(self):
        settings = QtCore.QSettings("LX", "pywerami")
        # settings.setValue("scale", float(self.scale.text()))
        settings.setValue("nan", self.nan.text())
        settings.setValue("degrees", self.degrees.isChecked())
        QtWidgets.QDialog.accept(self)


class AboutDialog(QtWidgets.QDialog):
    """About dialog
    """
    def __init__(self, version, parent=None):
        """Display a dialog that shows application information."""
        super(AboutDialog, self).__init__(parent)

        self.setWindowTitle('About')
        self.resize(300, 100)

        about = QtWidgets.QLabel('PyWerami {}\nstand-alone program to make an countour/3D plot from a contour data'.format(version))
        about.setAlignment(QtCore.Qt.AlignCenter)

        author = QtWidgets.QLabel('Ondrej Lexa')
        author.setAlignment(QtCore.Qt.AlignCenter)

        github = QtWidgets.QLabel('GitHub: <a href="https://github.com/ondrolexa/pywerami">ondrolexa</a>')
        github.setAlignment(QtCore.Qt.AlignCenter)
        github.setOpenExternalLinks(True)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignVCenter)

        self.layout.addWidget(about)
        self.layout.addWidget(author)
        self.layout.addWidget(github)

        self.setLayout(self.layout)


def process_cl_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store', nargs='?', default=None, help="Data file")

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
