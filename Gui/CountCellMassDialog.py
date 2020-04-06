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


class CountCellMassDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(CountCellMassDialog, self).__init__(parent)
        self.formLayoutWidget_4 = QtGui.QWidget(self)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(510, 0, 250, 250))
        self.formLayoutWidget_4.setObjectName(_fromUtf8("formLayoutWidget_4"))
        self.formLayout_4 = QtGui.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.mat_index = QtGui.QSpinBox(self.formLayoutWidget_4)
        self.mat_index.setMinimum(1)
        self.mat_index.setMaximum(25)
        self.mat_index.setProperty("value", 1)
        self.mat_index.setObjectName(_fromUtf8("mat_index"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.mat_index)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget_4)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)

        self.applyColor = QtGui.QPushButton(self.formLayoutWidget_4)
        self.applyColor.setObjectName(_fromUtf8("applyColor"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.applyColor)
        self.cancelColor = QtGui.QPushButton(self.formLayoutWidget_4)
        self.cancelColor.setObjectName(_fromUtf8("cancelColor"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.cancelColor)
        self.label = QtGui.QLabel(self.formLayoutWidget_4)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)

        self.applyColor.setText(_translate("MainWindow", "Apply", None))
        self.cancelColor.setText(_translate("MainWindow", "Cancel", None))
        self.label.setText(_translate("MainWindow", "Material Index:", None))
        self.setLayout(self.formLayout_4)
        self.connect(self.applyColor, QtCore.SIGNAL("clicked()"), self.ok_callback)
        self.connect(self.cancelColor, QtCore.SIGNAL("clicked()"), self.cancel_callback)
        self.setWindowTitle("Count Cell Mass of Polygon")
        self.applyColor.setFocus()
        self.mat_id = 0

    def ok_callback(self):
        self.setResult(1)
        self.accept()

    def cancel_callback(self):
        self.setResult(0)
        self.close()
