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


class FileDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(FileDialog, self).__init__(parent)
        self.formLayoutWidget_3 = QtGui.QWidget(self)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(510, 0, 231, 0))
        self.formLayoutWidget_3.setObjectName(_fromUtf8("formLayoutWidget_3"))
        self.formLayout_3 = QtGui.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.file_option_lbl = QtGui.QLabel(self.formLayoutWidget_3)
        self.file_option_lbl.setObjectName(_fromUtf8("file_option_lbl"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.file_option_lbl)
        self.file_cmdln_lbl = QtGui.QLabel(self.formLayoutWidget_3)
        self.file_cmdln_lbl.setObjectName(_fromUtf8("file_cmdln_lbl"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.file_cmdln_lbl)
        self.filePath = QtGui.QLineEdit(self.formLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filePath.sizePolicy().hasHeightForWidth())
        self.filePath.setSizePolicy(sizePolicy)
        self.filePath.setText(_fromUtf8(""))
        self.filePath.setObjectName(_fromUtf8("filePath"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.filePath)
        self.label_8 = QtGui.QLabel(self.formLayoutWidget_3)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_8)
        self.cancelBtn = QtGui.QPushButton(self.formLayoutWidget_3)
        self.cancelBtn.setObjectName(_fromUtf8("cancelBtn"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.FieldRole, self.cancelBtn)
        self.okBtn = QtGui.QPushButton(self.formLayoutWidget_3)
        self.okBtn.setObjectName(_fromUtf8("okBtn"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.LabelRole, self.okBtn)
        self.applyChkBox = QtGui.QCheckBox(self.formLayoutWidget_3)
        self.applyChkBox.setChecked(True)
        self.applyChkBox.setObjectName(_fromUtf8("applyChkBox"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.applyChkBox)
        self.file_cmdln_lbl.setText(_translate("MainWindow", "File Path:", None))
        self.applyChkBox.setText(_translate("MainWindow", "Add another plot", None))
        self.cancelBtn.setText(_translate("MainWindow", "Cancel", None))
        self.okBtn.setText(_translate("MainWindow", "Ok", None))
        self.setLayout(self.formLayout_3)
        self.setWindowTitle("Add Plot")
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
