# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer.ui'
#
# Created by: PyQt4 UI code generator X.XX.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1300, 1000)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setBaseSize(QtCore.QSize(1600, 1200))
        MainWindow.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.plotTitle = QtGui.QLabel(self.centralwidget)
        self.plotTitle.setGeometry(QtCore.QRect(10, 250, 561, 51))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(43)
        sizePolicy.setVerticalStretch(149)
        sizePolicy.setHeightForWidth(self.plotTitle.sizePolicy().hasHeightForWidth())
        self.plotTitle.setSizePolicy(sizePolicy)
        self.plotTitle.setSizeIncrement(QtCore.QSize(5, 5))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.plotTitle.setFont(font)
        self.plotTitle.setText(_fromUtf8(""))
        self.plotTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.plotTitle.setObjectName(_fromUtf8("plotTitle"))
        self.formLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 0, 131, XXX))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setSpacing(5)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.XMin = QtGui.QLabel(self.formLayoutWidget)
        self.XMin.setObjectName(_fromUtf8("XMin"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.XMin)
        self.XMax = QtGui.QLabel(self.formLayoutWidget)
        self.XMax.setObjectName(_fromUtf8("XMax"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.XMax)
        self.YMin = QtGui.QLabel(self.formLayoutWidget)
        self.YMin.setObjectName(_fromUtf8("YMin"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.YMin)
        self.YMax = QtGui.QLabel(self.formLayoutWidget)
        self.YMax.setObjectName(_fromUtf8("YMax"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.YMax)
        self.changeLimits = QtGui.QPushButton(self.formLayoutWidget)
        self.changeLimits.setObjectName(_fromUtf8("changeLimits"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.changeLimits)
        self.reset_limit = QtGui.QPushButton(self.formLayoutWidget)
        self.reset_limit.setObjectName(_fromUtf8("reset_limit"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.reset_limit)
        self.yMax = QtGui.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yMax.sizePolicy().hasHeightForWidth())
        self.yMax.setSizePolicy(sizePolicy)
        self.yMax.setObjectName(_fromUtf8("yMax"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.yMax)
        self.yMin = QtGui.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yMin.sizePolicy().hasHeightForWidth())
        self.yMin.setSizePolicy(sizePolicy)
        self.yMin.setObjectName(_fromUtf8("yMin"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.yMin)
        self.xMax = QtGui.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xMax.sizePolicy().hasHeightForWidth())
        self.xMax.setSizePolicy(sizePolicy)
        self.xMax.setObjectName(_fromUtf8("xMax"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.xMax)
        self.xMin = QtGui.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xMin.sizePolicy().hasHeightForWidth())
        self.xMin.setSizePolicy(sizePolicy)
        self.xMin.setObjectName(_fromUtf8("xMin"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.xMin)
        self.formLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(129, 0, 251, 231))
        self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.contours = QtGui.QLabel(self.formLayoutWidget_2)
        self.contours.setObjectName(_fromUtf8("contours"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.contours)
        self.contour_type = QtGui.QComboBox(self.formLayoutWidget_2)
        self.contour_type.setObjectName(_fromUtf8("contour_type"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.contour_type)
        self.heatmap_lbl = QtGui.QLabel(self.formLayoutWidget_2)
        self.heatmap_lbl.setObjectName(_fromUtf8("heatmap_lbl"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.heatmap_lbl)
        self.heatMap = QtGui.QCheckBox(self.formLayoutWidget_2)
        self.heatMap.setObjectName(_fromUtf8("heatMap"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.heatMap)
        self.num_cntrs = QtGui.QLabel(self.formLayoutWidget_2)
        self.num_cntrs.setObjectName(_fromUtf8("num_cntrs"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.num_cntrs)
        self.contour_number = QtGui.QSpinBox(self.formLayoutWidget_2)
        self.contour_number.setMinimum(10)
        self.contour_number.setMaximum(1500)
        self.contour_number.setProperty("value", 50)
        self.contour_number.setObjectName(_fromUtf8("contour_number"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.contour_number)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_2)
        self.contourLogScale = QtGui.QCheckBox(self.formLayoutWidget_2)
        self.contourLogScale.setObjectName(_fromUtf8("contourLogScale"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.contourLogScale)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_3)
        self.withMesh = QtGui.QCheckBox(self.formLayoutWidget_2)
        self.withMesh.setText(_fromUtf8(""))
        self.withMesh.setChecked(True)
        self.withMesh.setObjectName(_fromUtf8("withMesh"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.withMesh)
        self.min_contours = QtGui.QLabel(self.formLayoutWidget_2)
        self.min_contours.setObjectName(_fromUtf8("min_contours"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.min_contours)
        self.cMin = QtGui.QLineEdit(self.formLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cMin.sizePolicy().hasHeightForWidth())
        self.cMin.setSizePolicy(sizePolicy)
        self.cMin.setText(_fromUtf8(""))
        self.cMin.setObjectName(_fromUtf8("cMin"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.cMin)
        self.max_cntr_lbl = QtGui.QLabel(self.formLayoutWidget_2)
        self.max_cntr_lbl.setObjectName(_fromUtf8("max_cntr_lbl"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.max_cntr_lbl)
        self.cMax = QtGui.QLineEdit(self.formLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cMax.sizePolicy().hasHeightForWidth())
        self.cMax.setSizePolicy(sizePolicy)
        self.cMax.setText(_fromUtf8(""))
        self.cMax.setObjectName(_fromUtf8("cMax"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.FieldRole, self.cMax)
        self.contourDisplay = QtGui.QPushButton(self.formLayoutWidget_2)
        self.contourDisplay.setObjectName(_fromUtf8("contourDisplay"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.LabelRole, self.contourDisplay)
        self.resetContour = QtGui.QPushButton(self.formLayoutWidget_2)
        self.resetContour.setObjectName(_fromUtf8("resetContour"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.FieldRole, self.resetContour)
        self.formLayoutWidget_3 = QtGui.QWidget(self.centralwidget)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(380, 0, 205, 233))
        self.formLayoutWidget_3.setObjectName(_fromUtf8("formLayoutWidget_3"))
        self.formLayout_3 = QtGui.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.overrideChkBox = QtGui.QCheckBox(self.formLayoutWidget_3)
        self.overrideChkBox.setChecked(False)
        self.overrideChkBox.setObjectName(_fromUtf8("overrideChkBox"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.overrideChkBox)
        self.label_8 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_8)
        self.skipPlot = QtGui.QSpinBox(self.formLayoutWidget_3)
        self.skipPlot.setMinimum(1)
        self.skipPlot.setMaximum(1500)
        self.skipPlot.setProperty("value", 1)
        self.skipPlot.setObjectName(_fromUtf8("skipPlot"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.skipPlot)
        self.label = QtGui.QLabel(self.formLayoutWidget_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label)
        self.withVof = QtGui.QCheckBox(self.formLayoutWidget_3)
        self.withVof.setText(_fromUtf8(""))
        self.withVof.setChecked(True)
        self.withVof.setObjectName(_fromUtf8("withVof"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.withVof)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_6)
        self.withMirror_x = QtGui.QCheckBox(self.formLayoutWidget_3)
        self.withMirror_x.setText(_fromUtf8(""))
        self.withMirror_x.setChecked(False)
        self.withMirror_x.setObjectName(_fromUtf8("withMirror_x"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.FieldRole, self.withMirror_x)
        self.pushButton = QtGui.QPushButton(self.formLayoutWidget_3)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.LabelRole, self.pushButton)
        self.clearPlot = QtGui.QPushButton(self.formLayoutWidget_3)
        self.clearPlot.setObjectName(_fromUtf8("clearPlot"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.FieldRole, self.clearPlot)
        self.nextPlot = QtGui.QPushButton(self.formLayoutWidget_3)
        self.nextPlot.setObjectName(_fromUtf8("nextPlot"))
        self.formLayout_3.setWidget(6, QtGui.QFormLayout.LabelRole, self.nextPlot)
        self.previousPlot = QtGui.QPushButton(self.formLayoutWidget_3)
        self.previousPlot.setObjectName(_fromUtf8("previousPlot"))
        self.formLayout_3.setWidget(6, QtGui.QFormLayout.FieldRole, self.previousPlot)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_7)
        self.withMirror_y = QtGui.QCheckBox(self.formLayoutWidget_3)
        self.withMirror_y.setText(_fromUtf8(""))
        self.withMirror_y.setChecked(False)
        self.withMirror_y.setObjectName(_fromUtf8("withMirror_y"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.FieldRole, self.withMirror_y)
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(30, 300, 1250, 650))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.tableVertex = QtGui.QTableWidget(self.centralwidget)
        self.tableVertex.setGeometry(QtCore.QRect(590, 0, 461, XXX))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableVertex.setFont(font)
        self.tableVertex.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableVertex.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableVertex.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableVertex.setRowCount(4)
        self.tableVertex.setColumnCount(5)
        self.tableVertex.setObjectName(_fromUtf8("tableVertex"))
        item = QtGui.QTableWidgetItem()
        self.tableVertex.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableVertex.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableVertex.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableVertex.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableVertex.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableVertex.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableVertex.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableVertex.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableVertex.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(0, 2, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(0, 3, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(0, 4, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(1, 0, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(1, 1, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(1, 2, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(1, 3, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(1, 4, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(2, 0, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(2, 1, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(2, 2, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(2, 3, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(2, 4, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(3, 0, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(3, 1, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(3, 2, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(3, 3, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableVertex.setItem(3, 4, item)
        self.tableVertex.horizontalHeader().setDefaultSectionSize(90)
        self.tableVertex.horizontalHeader().setMinimumSectionSize(19)
        self.tableCell = QtGui.QTableWidget(self.centralwidget)
        self.tableCell.setGeometry(QtCore.QRect(590, 160, 101, 61))
        self.tableCell.setSizeIncrement(QtCore.QSize(100, 1))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableCell.setFont(font)
        self.tableCell.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableCell.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableCell.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableCell.setRowCount(1)
        self.tableCell.setColumnCount(1)
        self.tableCell.setObjectName(_fromUtf8("tableCell"))
        item = QtGui.QTableWidgetItem()
        self.tableCell.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableCell.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableCell.setItem(0, 0, item)
        self.tableCell.horizontalHeader().setDefaultSectionSize(100)
        self.tableCell.horizontalHeader().setMinimumSectionSize(1)
        self.tableCell_2 = QtGui.QTableWidget(self.centralwidget)
        self.tableCell_2.setGeometry(QtCore.QRect(590, 230, 101, 61))
        self.tableCell_2.setSizeIncrement(QtCore.QSize(100, 1))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableCell_2.setFont(font)
        self.tableCell_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableCell_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableCell_2.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableCell_2.setRowCount(1)
        self.tableCell_2.setColumnCount(1)
        self.tableCell_2.setObjectName(_fromUtf8("tableCell_2"))
        item = QtGui.QTableWidgetItem()
        self.tableCell_2.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableCell_2.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableCell_2.setItem(0, 0, item)
        self.tableCell_2.horizontalHeader().setDefaultSectionSize(100)
        self.tableCell_2.horizontalHeader().setMinimumSectionSize(1)
        self.graphicsView.raise_()
        self.tableVertex.raise_()
        self.plotTitle.raise_()
        self.formLayoutWidget.raise_()
        self.formLayoutWidget_2.raise_()
        self.formLayoutWidget_3.raise_()
        self.tableCell.raise_()
        self.tableCell_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1300, 27))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menuBar)
        self.addPlot = QtGui.QAction(MainWindow)
        self.addPlot.setObjectName(_fromUtf8("addPlot"))
        self.colorOption = QtGui.QAction(MainWindow)
        self.colorOption.setObjectName(_fromUtf8("colorOption"))
        self.movie = QtGui.QAction(MainWindow)
        self.movie.setObjectName(_fromUtf8("movie"))
        self.operator_2 = QtGui.QAction(MainWindow)
        self.operator_2.setObjectName(_fromUtf8("operator_2"))
        self.background = QtGui.QAction(MainWindow)
        self.background.setObjectName(_fromUtf8("background"))
        self.countCellMasses = QtGui.QAction(MainWindow)
        self.countCellMasses.setObjectName(_fromUtf8("countCellMasses"))
        self.actionAdd_Plot = QtGui.QAction(MainWindow)
        self.actionAdd_Plot.setObjectName(_fromUtf8("actionAdd_Plot"))
        self.menuFile.addAction(self.addPlot)
        self.menuFile.addAction(self.colorOption)
        self.menuFile.addAction(self.movie)
        self.menuFile.addAction(self.operator_2)
        self.menuFile.addAction(self.background)
        self.menuFile.addAction(self.countCellMasses)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "GraphiX", None))
        self.XMin.setText(_translate("MainWindow", "Y Min:", None))
        self.XMax.setText(_translate("MainWindow", "Y Max:", None))
        self.YMin.setText(_translate("MainWindow", "X Min:", None))
        self.YMax.setText(_translate("MainWindow", "X Max:", None))
        self.changeLimits.setText(_translate("MainWindow", "Apply", None))
        self.reset_limit.setText(_translate("MainWindow", "Reset", None))
        self.contours.setText(_translate("MainWindow", "Contours:", None))
        self.heatmap_lbl.setText(_translate("MainWindow", "Color Map:", None))
        self.heatMap.setText(_translate("MainWindow", "Enable", None))
        self.num_cntrs.setText(_translate("MainWindow", "Num contours", None))
        self.label_2.setText(_translate("MainWindow", "Log scale", None))
        self.contourLogScale.setText(_translate("MainWindow", "Enable", None))
        self.label_3.setText(_translate("MainWindow", "With Mesh:", None))
        self.min_contours.setText(_translate("MainWindow", "Min:", None))
        self.max_cntr_lbl.setText(_translate("MainWindow", "Max:", None))
        self.contourDisplay.setText(_translate("MainWindow", "Contour", None))
        self.resetContour.setText(_translate("MainWindow", "Reset limits", None))
        self.overrideChkBox.setText(_translate("MainWindow", "Override", None))
        self.label_8.setText(_translate("MainWindow", "Stride:", None))
        self.label.setText(_translate("MainWindow", "With vof:", None))
        self.label_6.setText(_translate("MainWindow", "With x Mirror:", None))
        self.pushButton.setText(_translate("MainWindow", "Mesh", None))
        self.clearPlot.setText(_translate("MainWindow", "Clear", None))
        self.nextPlot.setText(_translate("MainWindow", "Next plot", None))
        self.previousPlot.setText(_translate("MainWindow", "Previous plot", None))
        self.label_7.setText(_translate("MainWindow", "With y Mirror:", None))
        item = self.tableVertex.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1", None))
        item = self.tableVertex.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2", None))
        item = self.tableVertex.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3", None))
        item = self.tableVertex.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "4", None))
        item = self.tableVertex.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Index", None))
        item = self.tableVertex.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "X", None))
        item = self.tableVertex.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Y", None))
        item = self.tableVertex.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "U", None))
        item = self.tableVertex.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "V", None))
        __sortingEnabled = self.tableVertex.isSortingEnabled()
        self.tableVertex.setSortingEnabled(False)
        self.tableVertex.setSortingEnabled(__sortingEnabled)
        item = self.tableCell.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1", None))
        item = self.tableCell.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Index", None))
        __sortingEnabled = self.tableCell.isSortingEnabled()
        self.tableCell.setSortingEnabled(False)
        self.tableCell.setSortingEnabled(__sortingEnabled)
        item = self.tableCell_2.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1", None))
        item = self.tableCell_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Index", None))
        __sortingEnabled = self.tableCell_2.isSortingEnabled()
        self.tableCell_2.setSortingEnabled(False)
        self.tableCell_2.setSortingEnabled(__sortingEnabled)
        self.menuFile.setTitle(_translate("MainWindow", "Options", None))
        self.addPlot.setText(_translate("MainWindow", "Add Plot", None))
        self.colorOption.setText(_translate("MainWindow", "Material Color", None))
        self.movie.setText(_translate("MainWindow", "Movie", None))
        self.operator_2.setText(_translate("MainWindow", "Operators", None))
        self.background.setText(_translate("MainWindow", "Background Color", None))
        self.countCellMasses.setText(_translate("MainWindow", "Count Cell mass", None))
        self.actionAdd_Plot.setText(_translate("MainWindow", "Add Plot", None))

