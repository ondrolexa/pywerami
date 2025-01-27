# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pywerami.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from qtpy import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(754, 523)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("pywerami.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.listView = QtWidgets.QListView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView.setObjectName("listView")
        self.verticalLayout.addWidget(self.listView)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.levelstab = QtWidgets.QWidget()
        self.levelstab.setObjectName("levelstab")
        self.gridLayout = QtWidgets.QGridLayout(self.levelstab)
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.levelstab)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.levelmin = QtWidgets.QLineEdit(self.levelstab)
        self.levelmin.setObjectName("levelmin")
        self.gridLayout.addWidget(self.levelmin, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.levelstab)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.levelmax = QtWidgets.QLineEdit(self.levelstab)
        self.levelmax.setObjectName("levelmax")
        self.gridLayout.addWidget(self.levelmax, 1, 1, 1, 1)
        self.setlevels = QtWidgets.QRadioButton(self.levelstab)
        self.setlevels.setChecked(True)
        self.setlevels.setObjectName("setlevels")
        self.stepGroup = QtWidgets.QButtonGroup(MainWindow)
        self.stepGroup.setObjectName("stepGroup")
        self.stepGroup.addButton(self.setlevels)
        self.gridLayout.addWidget(self.setlevels, 2, 0, 1, 1)
        self.levelnum = QtWidgets.QLineEdit(self.levelstab)
        self.levelnum.setObjectName("levelnum")
        self.gridLayout.addWidget(self.levelnum, 2, 1, 1, 1)
        self.setstep = QtWidgets.QRadioButton(self.levelstab)
        self.setstep.setObjectName("setstep")
        self.stepGroup.addButton(self.setstep)
        self.gridLayout.addWidget(self.setstep, 3, 0, 1, 1)
        self.levelstep = QtWidgets.QLineEdit(self.levelstab)
        self.levelstep.setObjectName("levelstep")
        self.gridLayout.addWidget(self.levelstep, 3, 1, 1, 1)
        self.linlevel = QtWidgets.QRadioButton(self.levelstab)
        self.linlevel.setChecked(True)
        self.linlevel.setObjectName("linlevel")
        self.levelGroup = QtWidgets.QButtonGroup(MainWindow)
        self.levelGroup.setObjectName("levelGroup")
        self.levelGroup.addButton(self.linlevel)
        self.gridLayout.addWidget(self.linlevel, 4, 0, 1, 1)
        self.cdflevel = QtWidgets.QRadioButton(self.levelstab)
        self.cdflevel.setObjectName("cdflevel")
        self.levelGroup.addButton(self.cdflevel)
        self.gridLayout.addWidget(self.cdflevel, 4, 1, 1, 1)
        self.tabWidget.addTab(self.levelstab, "")
        self.styletab = QtWidgets.QWidget()
        self.styletab.setObjectName("styletab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.styletab)
        self.gridLayout_2.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.styletab)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.mapstyle = QtWidgets.QComboBox(self.styletab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mapstyle.sizePolicy().hasHeightForWidth())
        self.mapstyle.setSizePolicy(sizePolicy)
        self.mapstyle.setObjectName("mapstyle")
        self.gridLayout_2.addWidget(self.mapstyle, 0, 1, 1, 1)
        self.contcheckcolor = QtWidgets.QRadioButton(self.styletab)
        self.contcheckcolor.setChecked(True)
        self.contcheckcolor.setObjectName("contcheckcolor")
        self.contourGroup = QtWidgets.QButtonGroup(MainWindow)
        self.contourGroup.setObjectName("contourGroup")
        self.contourGroup.addButton(self.contcheckcolor)
        self.gridLayout_2.addWidget(self.contcheckcolor, 5, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.styletab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.opacity = QtWidgets.QSlider(self.styletab)
        self.opacity.setMaximum(100)
        self.opacity.setProperty("value", 100)
        self.opacity.setOrientation(QtCore.Qt.Horizontal)
        self.opacity.setObjectName("opacity")
        self.gridLayout_2.addWidget(self.opacity, 1, 1, 1, 1)
        self.contcheckmap = QtWidgets.QRadioButton(self.styletab)
        self.contcheckmap.setObjectName("contcheckmap")
        self.contourGroup.addButton(self.contcheckmap)
        self.gridLayout_2.addWidget(self.contcheckmap, 4, 0, 1, 1)
        self.contchecknone = QtWidgets.QRadioButton(self.styletab)
        self.contchecknone.setObjectName("contchecknone")
        self.contourGroup.addButton(self.contchecknone)
        self.gridLayout_2.addWidget(self.contchecknone, 4, 1, 1, 1)
        self.contcolor = QtWidgets.QPushButton(self.styletab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contcolor.sizePolicy().hasHeightForWidth())
        self.contcolor.setSizePolicy(sizePolicy)
        self.contcolor.setStyleSheet("background-color: #000000")
        self.contcolor.setText("")
        self.contcolor.setObjectName("contcolor")
        self.gridLayout_2.addWidget(self.contcolor, 5, 1, 1, 1)
        self.fillstyle = QtWidgets.QCheckBox(self.styletab)
        self.fillstyle.setObjectName("fillstyle")
        self.gridLayout_2.addWidget(self.fillstyle, 2, 0, 1, 1)
        self.contlabel = QtWidgets.QCheckBox(self.styletab)
        self.contlabel.setObjectName("contlabel")
        self.gridLayout_2.addWidget(self.contlabel, 3, 0, 1, 1)
        self.labelDigits = QtWidgets.QSpinBox(self.styletab)
        self.labelDigits.setMaximum(6)
        self.labelDigits.setProperty("value", 3)
        self.labelDigits.setObjectName("labelDigits")
        self.gridLayout_2.addWidget(self.labelDigits, 3, 1, 1, 1)
        self.checkCBar = QtWidgets.QCheckBox(self.styletab)
        self.checkCBar.setObjectName("checkCBar")
        self.gridLayout_2.addWidget(self.checkCBar, 2, 1, 1, 1)
        self.tabWidget.addTab(self.styletab, "")
        self.processtab = QtWidgets.QWidget()
        self.processtab.setObjectName("processtab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.processtab)
        self.gridLayout_3.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_11 = QtWidgets.QLabel(self.processtab)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 0, 0, 1, 1)
        self.resample = QtWidgets.QSpinBox(self.processtab)
        self.resample.setPrefix("")
        self.resample.setMinimum(1)
        self.resample.setMaximum(10)
        self.resample.setObjectName("resample")
        self.gridLayout_3.addWidget(self.resample, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.processtab)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 1, 0, 1, 1)
        self.filtersize = QtWidgets.QSpinBox(self.processtab)
        self.filtersize.setPrefix("")
        self.filtersize.setMinimum(1)
        self.filtersize.setMaximum(10)
        self.filtersize.setObjectName("filtersize")
        self.gridLayout_3.addWidget(self.filtersize, 1, 1, 1, 1)
        self.smoothlabel = QtWidgets.QLabel(self.processtab)
        self.smoothlabel.setObjectName("smoothlabel")
        self.gridLayout_3.addWidget(self.smoothlabel, 2, 0, 1, 1)
        self.filtersigma = QtWidgets.QDoubleSpinBox(self.processtab)
        self.filtersigma.setPrefix("")
        self.filtersigma.setDecimals(1)
        self.filtersigma.setMaximum(4.0)
        self.filtersigma.setSingleStep(0.1)
        self.filtersigma.setObjectName("filtersigma")
        self.gridLayout_3.addWidget(self.filtersigma, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.processtab)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 3, 0, 1, 1)
        self.clipmin = QtWidgets.QLineEdit(self.processtab)
        self.clipmin.setObjectName("clipmin")
        self.gridLayout_3.addWidget(self.clipmin, 3, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.processtab)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 4, 0, 1, 1)
        self.clipmax = QtWidgets.QLineEdit(self.processtab)
        self.clipmax.setObjectName("clipmax")
        self.gridLayout_3.addWidget(self.clipmax, 4, 1, 1, 1)
        self.tabWidget.addTab(self.processtab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setMinimumSize(QtCore.QSize(250, 0))
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Apply
            | QtWidgets.QDialogButtonBox.RestoreDefaults
        )
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(
            self.buttonBox, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(400, 0))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.matplot = QtWidgets.QVBoxLayout()
        self.matplot.setSpacing(0)
        self.matplot.setObjectName("matplot")
        self.verticalLayout_3.addLayout(self.matplot)
        self.horizontalLayout.addWidget(self.widget)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 754, 20))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.toolBar.setAllowedAreas(
            QtCore.Qt.LeftToolBarArea | QtCore.Qt.TopToolBarArea
        )
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionSaveas = QtWidgets.QAction(MainWindow)
        self.actionSaveas.setObjectName("actionSaveas")
        self.actionProperties = QtWidgets.QAction(MainWindow)
        self.actionProperties.setObjectName("actionProperties")
        self.actionHome = QtWidgets.QAction(MainWindow)
        self.actionHome.setObjectName("actionHome")
        self.actionPan = QtWidgets.QAction(MainWindow)
        self.actionPan.setCheckable(True)
        self.actionPan.setObjectName("actionPan")
        self.actionZoom = QtWidgets.QAction(MainWindow)
        self.actionZoom.setCheckable(True)
        self.actionZoom.setObjectName("actionZoom")
        self.actionAxes = QtWidgets.QAction(MainWindow)
        self.actionAxes.setObjectName("actionAxes")
        self.actionSavefig = QtWidgets.QAction(MainWindow)
        self.actionSavefig.setObjectName("actionSavefig")
        self.actionGrid = QtWidgets.QAction(MainWindow)
        self.actionGrid.setCheckable(True)
        self.actionGrid.setObjectName("actionGrid")
        self.action3D = QtWidgets.QAction(MainWindow)
        self.action3D.setCheckable(True)
        self.action3D.setObjectName("action3D")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menu_File.addAction(self.actionImport)
        self.menu_File.addAction(self.actionOpen)
        self.menu_File.addAction(self.actionSave)
        self.menu_File.addAction(self.actionSaveas)
        self.menu_File.addAction(self.actionSavefig)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionProperties)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionQuit)
        self.menuView.addAction(self.actionAxes)
        self.menuView.addAction(self.action3D)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.toolBar.addAction(self.actionImport)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSaveas)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addAction(self.actionPan)
        self.toolBar.addAction(self.actionZoom)
        self.toolBar.addAction(self.actionAxes)
        self.toolBar.addAction(self.actionSavefig)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionGrid)
        self.toolBar.addAction(self.action3D)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionProperties)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyWerami 3"))
        self.label_3.setText(_translate("MainWindow", "Dependent variables:"))
        self.label_4.setText(_translate("MainWindow", "Minimum"))
        self.label_5.setText(_translate("MainWindow", "Maximum"))
        self.setlevels.setText(_translate("MainWindow", "Levels"))
        self.setstep.setText(_translate("MainWindow", "Step"))
        self.linlevel.setText(_translate("MainWindow", "Linear"))
        self.cdflevel.setText(_translate("MainWindow", "CDF based"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.levelstab), _translate("MainWindow", "Levels")
        )
        self.label.setText(_translate("MainWindow", "Color map"))
        self.contcheckcolor.setText(_translate("MainWindow", "Single color"))
        self.label_2.setText(_translate("MainWindow", "Opacity"))
        self.contcheckmap.setText(_translate("MainWindow", "Colormap"))
        self.contchecknone.setText(_translate("MainWindow", "None"))
        self.fillstyle.setText(_translate("MainWindow", "Filled contours"))
        self.contlabel.setText(_translate("MainWindow", "Labeling"))
        self.labelDigits.setPrefix(_translate("MainWindow", "Digits: "))
        self.checkCBar.setText(_translate("MainWindow", "Colorbar"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.styletab), _translate("MainWindow", "Style")
        )
        self.label_11.setText(_translate("MainWindow", "Resampling grid"))
        self.label_7.setText(_translate("MainWindow", "Median filter size"))
        self.smoothlabel.setText(_translate("MainWindow", "Gauss filter sigma"))
        self.label_8.setText(_translate("MainWindow", "Clip minimum"))
        self.label_9.setText(_translate("MainWindow", "Clip maximum"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.processtab),
            _translate("MainWindow", "Processing"),
        )
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen.setText(_translate("MainWindow", "&Open project"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open pywerami project"))
        self.actionSave.setText(_translate("MainWindow", "&Save project"))
        self.actionSave.setIconText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "Save pywerami project"))
        self.actionImport.setText(_translate("MainWindow", "&New project"))
        self.actionImport.setIconText(_translate("MainWindow", "New"))
        self.actionImport.setToolTip(
            _translate("MainWindow", "New project from data file")
        )
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setToolTip(_translate("MainWindow", "Quit"))
        self.actionSaveas.setText(_translate("MainWindow", "Save project as..."))
        self.actionSaveas.setIconText(_translate("MainWindow", "Save as"))
        self.actionSaveas.setToolTip(
            _translate("MainWindow", "Save pywerami project as")
        )
        self.actionProperties.setText(_translate("MainWindow", "Options"))
        self.actionProperties.setToolTip(_translate("MainWindow", "Options"))
        self.actionHome.setText(_translate("MainWindow", "Home"))
        self.actionHome.setToolTip(_translate("MainWindow", "Default zoom"))
        self.actionPan.setText(_translate("MainWindow", "Pan"))
        self.actionPan.setToolTip(_translate("MainWindow", "Pan"))
        self.actionZoom.setText(_translate("MainWindow", "Zoom"))
        self.actionZoom.setToolTip(_translate("MainWindow", "Zoom to rectangle"))
        self.actionAxes.setText(_translate("MainWindow", "Plot properties"))
        self.actionAxes.setIconText(_translate("MainWindow", "Properties"))
        self.actionAxes.setToolTip(_translate("MainWindow", "Plot properties"))
        self.actionSavefig.setText(_translate("MainWindow", "Export figure..."))
        self.actionSavefig.setIconText(_translate("MainWindow", "Export"))
        self.actionSavefig.setToolTip(_translate("MainWindow", "Export figure"))
        self.actionGrid.setText(_translate("MainWindow", "Grid"))
        self.actionGrid.setToolTip(_translate("MainWindow", "Show grid"))
        self.action3D.setText(_translate("MainWindow", "3D"))
        self.action3D.setToolTip(_translate("MainWindow", "View active variable in 3D"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setToolTip(_translate("MainWindow", "About PyWerami"))
