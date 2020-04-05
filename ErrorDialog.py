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


class ErrorDialog(QtGui.QErrorMessage):
    def __init__(self, parent=None, msg=""):
        super(ErrorDialog, self).__init__(parent)
        self.showMessage(msg)
        self.setWindowTitle("Error")
        self.show()