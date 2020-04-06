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


class OperatorDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(OperatorDialog, self).__init__(parent)
        self.formLayoutWidget_5 = QtGui.QWidget(self)
        self.formLayoutWidget_5.setGeometry(QtCore.QRect(1040, 30, 213, 222))
        self.formLayoutWidget_5.setObjectName(_fromUtf8("formLayoutWidget_5"))
        self.formLayout_5 = QtGui.QFormLayout(self.formLayoutWidget_5)
        self.formLayout_5.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_5.setObjectName(_fromUtf8("formLayout_5"))
        self.contours_3 = QtGui.QLabel(self.formLayoutWidget_5)
        self.contours_3.setObjectName(_fromUtf8("contours_3"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.LabelRole, self.contours_3)
        self.contour_type_3 = QtGui.QComboBox(self.formLayoutWidget_5)
        self.contour_type_3.setObjectName(_fromUtf8("contour_type_3"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.FieldRole, self.contour_type_3)
        self.min_contours_3 = QtGui.QLabel(self.formLayoutWidget_5)
        self.min_contours_3.setObjectName(_fromUtf8("min_contours_3"))
        self.formLayout_5.setWidget(1, QtGui.QFormLayout.LabelRole, self.min_contours_3)
        self.cMin_3 = QtGui.QLineEdit(self.formLayoutWidget_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cMin_3.sizePolicy().hasHeightForWidth())
        self.cMin_3.setSizePolicy(sizePolicy)
        self.cMin_3.setText(_fromUtf8(""))
        self.cMin_3.setObjectName(_fromUtf8("cMin_3"))
        self.formLayout_5.setWidget(1, QtGui.QFormLayout.FieldRole, self.cMin_3)
        self.cancelBtn = QtGui.QPushButton(self.formLayoutWidget_5)
        self.cancelBtn.setObjectName(_fromUtf8("cancelBtn"))
        self.formLayout_5.setWidget(2, QtGui.QFormLayout.FieldRole, self.cancelBtn)
        self.okBtn = QtGui.QPushButton(self.formLayoutWidget_5)
        self.okBtn.setObjectName(_fromUtf8("okBtn"))
        self.formLayout_5.setWidget(2, QtGui.QFormLayout.LabelRole, self.okBtn)
        self.cancelBtn.setText(_translate("MainWindow", "Cancel", None))
        self.min_contours_3.setText(_translate("MainWindow", "Y = ", None))
        self.contours_3.setText(_translate("MainWindow", "Contours:", None))
        self.okBtn.setText(_translate("MainWindow", "Ok", None))
        self.setLayout(self.formLayout_5)
        self.setWindowTitle("Operator Dialog")
        self.bt = QtGui.QDialogButtonBox()
        self.okBtn.setShortcut("Enter")
        self.connect(self.okBtn, QtCore.SIGNAL("clicked()"), self.ok_callback)
        self.connect(self.cancelBtn, QtCore.SIGNAL("clicked()"), self.cancel_callback)
        self.okBtn.setFocus()

    def ok_callback(self):
        self.setResult(1)
        self.accept()

    def cancel_callback(self):
        self.setResult(0)
        self.close()

    def get_result(self):
        return str(self.contour_type_3.currentText()), self.cMin_3.text()

    def insert_contours(self, cntr_names):
        for i in cntr_names:
            self.contour_type_3.addItem(_fromUtf8(i))
