import future_builtins
import sys
import time
import platform
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


class MovieDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(MovieDialog, self).__init__(parent)
        self.formLayoutWidget_4 = QtGui.QWidget(self)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(1040, 30, 213, 222))
        self.formLayoutWidget_4.setObjectName(_fromUtf8("formLayoutWidget_4"))
        self.formLayout_4 = QtGui.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.label_9 = QtGui.QLabel(self.formLayoutWidget_4)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_9)
        self.movieStride = QtGui.QSpinBox(self.formLayoutWidget_4)
        self.movieStride.setMinimum(1)
        self.movieStride.setMaximum(1500)
        self.movieStride.setProperty("value", 1)
        self.movieStride.setObjectName(_fromUtf8("movieStride"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.movieStride)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget_4)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_5)
        self.startIndex = QtGui.QLineEdit(self.formLayoutWidget_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startIndex.sizePolicy().hasHeightForWidth())
        self.startIndex.setSizePolicy(sizePolicy)
        self.startIndex.setText(_fromUtf8(""))
        self.startIndex.setObjectName(_fromUtf8("startIndex"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.startIndex)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget_4)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_6)
        self.endIndex = QtGui.QLineEdit(self.formLayoutWidget_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endIndex.sizePolicy().hasHeightForWidth())
        self.endIndex.setSizePolicy(sizePolicy)
        self.endIndex.setText(_fromUtf8(""))
        self.endIndex.setObjectName(_fromUtf8("endIndex"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.endIndex)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget_4)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_7)
        self.timeInterval = QtGui.QLineEdit(self.formLayoutWidget_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeInterval.sizePolicy().hasHeightForWidth())
        self.timeInterval.setSizePolicy(sizePolicy)
        self.timeInterval.setText(_fromUtf8(""))
        self.timeInterval.setObjectName(_fromUtf8("timeInterval"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.FieldRole, self.timeInterval)
        self.label_10 = QtGui.QLabel(self.formLayoutWidget_4)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout_4.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_10)
        self.plot_type = QtGui.QComboBox(self.formLayoutWidget_4)
        self.plot_type.setObjectName(_fromUtf8("plot_type"))
        self.plot_type.addItem(_fromUtf8(""))
        self.plot_type.addItem(_fromUtf8(""))
        self.plot_type.addItem(_fromUtf8(""))
        self.formLayout_4.setWidget(4, QtGui.QFormLayout.FieldRole, self.plot_type)
        self.contours = QtGui.QLabel(self.formLayoutWidget_4)
        self.contours.setObjectName(_fromUtf8("contours_2"))
        self.formLayout_4.setWidget(5, QtGui.QFormLayout.LabelRole, self.contours)
        self.contour_type_3 = QtGui.QComboBox(self.formLayoutWidget_4)
        self.contour_type_3.setObjectName(_fromUtf8("contour_type_3"))
        self.formLayout_4.setWidget(5, QtGui.QFormLayout.FieldRole, self.contour_type_3)
        self.cancelBtn = QtGui.QPushButton(self.formLayoutWidget_4)
        self.cancelBtn.setObjectName(_fromUtf8("cancelBtn"))
        self.formLayout_4.setWidget(8, QtGui.QFormLayout.FieldRole, self.cancelBtn)
        self.okBtn = QtGui.QPushButton(self.formLayoutWidget_4)
        self.okBtn.setObjectName(_fromUtf8("okBtn"))
        self.formLayout_4.setWidget(8, QtGui.QFormLayout.LabelRole, self.okBtn)
        self.cancelBtn.setText(_translate("MainWindow", "Cancel", None))
        self.label_9.setText(_translate("MainWindow", "Stride:", None))
        self.label_5.setText(_translate("MainWindow", "Start Index:", None))
        self.label_6.setText(_translate("MainWindow", "End Index:", None))
        self.label_7.setText(_translate("MainWindow", "Time Interval:", None))
        self.label_10.setText(_translate("MainWindow", "Plot type:", None))
        self.plot_type.setItemText(0, _translate("MainWindow", "Mesh", None))
        self.plot_type.setItemText(1, _translate("MainWindow", "Contour", None))
        self.plot_type.setItemText(2, _translate("MainWindow", "Color Map", None))
        self.contours.setText(_translate("MainWindow", "Contours:", None))
        self.okBtn.setText(_translate("MainWindow", "Ok", None))
        self.setLayout(self.formLayout_4)
        self.setWindowTitle("Movie Dialog")
        self.bt = QtGui.QDialogButtonBox()
        self.connect(self.okBtn, QtCore.SIGNAL("clicked()"), self.ok_callback)
        self.connect(self.cancelBtn, QtCore.SIGNAL("clicked()"), self.cancel_callback)
        self.okBtn.setFocus()

    def ok_callback(self):
        self.setResult(1)
        self.accept()

    def cancel_callback(self):
        self.setResult(0)
        self.close()

    def insert_defaults(self, cntr_names, start, end):
        for i in cntr_names:
            self.contour_type_3.addItem(_fromUtf8(i))
        self.startIndex.setText(start)
        self.endIndex.setText(end)
        self.timeInterval.setText(str(1))
