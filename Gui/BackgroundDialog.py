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


class BackgroundDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(BackgroundDialog, self).__init__(parent)
        self.formLayoutWidget_4 = QtGui.QWidget(self)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(510, 0, 231, 15))
        self.formLayoutWidget_4.setObjectName(_fromUtf8("formLayoutWidget_4"))
        self.formLayout_4 = QtGui.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # self.mat_index = QtGui.QSpinBox(self.formLayoutWidget_4)
        # self.mat_index.setMinimum(1)
        # self.mat_index.setMaximum(25)
        # self.mat_index.setProperty("value", 1)
        # self.mat_index.setObjectName(_fromUtf8("background_color"))
        # self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.mat_index)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget_4)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.mat_color = QtGui.QComboBox(self.formLayoutWidget_4)
        self.mat_color.setObjectName(_fromUtf8("background_color"))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.mat_color.addItem(_fromUtf8(""))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.mat_color)
        # self.label_4 = QtGui.QLabel(self.formLayoutWidget_4)
        # self.label_4.setObjectName(_fromUtf8("label_4"))
        # self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        # self.mat_color_txt = QtGui.QLineEdit(self.formLayoutWidget_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.mat_color_txt.sizePolicy().hasHeightForWidth())
        # self.mat_color_txt.setSizePolicy(sizePolicy)
        # self.mat_color_txt.setText(_fromUtf8(""))
        # self.mat_color_txt.setObjectName(_fromUtf8("mat_color_txt"))
        # self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.mat_color_txt)
        self.applyColor = QtGui.QPushButton(self.formLayoutWidget_4)
        self.applyColor.setObjectName(_fromUtf8("applyColor"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.applyColor)
        self.cancelColor = QtGui.QPushButton(self.formLayoutWidget_4)
        self.cancelColor.setObjectName(_fromUtf8("cancelColor"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.cancelColor)
        self.label = QtGui.QLabel(self.formLayoutWidget_4)
        self.label.setObjectName(_fromUtf8("label"))
        # self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)

        self.label_2.setText(_translate("MainWindow", "Background Color:", None))
        self.mat_color.setItemText(0, _translate("MainWindow", "White", None))
        self.mat_color.setItemText(29, _translate("MainWindow", "Black", None))
        self.mat_color.setItemText(1, _translate("MainWindow", "Dark Grey", None))
        self.mat_color.setItemText(2, _translate("MainWindow", "Pink", None))
        self.mat_color.setItemText(3, _translate("MainWindow", "Red", None))
        self.mat_color.setItemText(4, _translate("MainWindow", "Dark Red", None))
        self.mat_color.setItemText(5, _translate("MainWindow", "Web-Green", None))
        self.mat_color.setItemText(6, _translate("MainWindow", "Green", None))
        self.mat_color.setItemText(7, _translate("MainWindow", "Dark Spring Green", None))
        self.mat_color.setItemText(8, _translate("MainWindow", "Dark Green", None))
        self.mat_color.setItemText(9, _translate("MainWindow", "Royal Blue", None))
        self.mat_color.setItemText(10, _translate("MainWindow", "Navy", None))
        self.mat_color.setItemText(11, _translate("MainWindow", "Blue", None))
        self.mat_color.setItemText(12, _translate("MainWindow", "Web-Blue", None))
        self.mat_color.setItemText(13, _translate("MainWindow", "Dark Blue", None))
        self.mat_color.setItemText(14, _translate("MainWindow", "Steel Blue", None))
        self.mat_color.setItemText(15, _translate("MainWindow", "Aquamarine", None))
        self.mat_color.setItemText(16, _translate("MainWindow", "Light-Turquoise", None))
        self.mat_color.setItemText(17, _translate("MainWindow", "Cyan", None))
        self.mat_color.setItemText(18, _translate("MainWindow", "Dark Cyan", None))
        self.mat_color.setItemText(19, _translate("MainWindow", "Yellow", None))
        self.mat_color.setItemText(20, _translate("MainWindow", "Dark Yellow", None))
        self.mat_color.setItemText(21, _translate("MainWindow", "Orange", None))
        self.mat_color.setItemText(22, _translate("MainWindow", "Brown", None))
        self.mat_color.setItemText(23, _translate("MainWindow", "Khaki", None))
        self.mat_color.setItemText(24, _translate("MainWindow", "Purple", None))
        self.mat_color.setItemText(25, _translate("MainWindow", "Magenta", None))
        self.mat_color.setItemText(26, _translate("MainWindow", "Medium Purple", None))
        self.mat_color.setItemText(27, _translate("MainWindow", "Plum", None))
        self.mat_color.setItemText(28, _translate("MainWindow", "Dark-Plum", None))
        self.mat_color.setItemText(30, _translate("MainWindow", "Violet", None))
        self.mat_color.setItemText(31, _translate("MainWindow", "Dark-Violet", None))
        # self.label_4.setText(_translate("MainWindow", "Material Color:", None))
        self.applyColor.setText(_translate("MainWindow", "Apply", None))
        self.cancelColor.setText(_translate("MainWindow", "Cancel", None))
        # self.label.setText(_translate("MainWindow", "Material Index:", None))
        self.setLayout(self.formLayout_4)
        self.connect(self.applyColor, QtCore.SIGNAL("clicked()"), self.ok_callback)
        self.connect(self.cancelColor, QtCore.SIGNAL("clicked()"), self.cancel_callback)
        self.setWindowTitle("Background Color")
        self.applyColor.setFocus()

    def ok_callback(self):
        self.setResult(1)
        self.accept()

    def cancel_callback(self):
        self.setResult(0)
        self.close()
