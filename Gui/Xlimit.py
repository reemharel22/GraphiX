import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import platform
import MenuBar
import ui_designergui

class Xlimit(QDialogButtonBox, ui_designergui.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Xlimit, self).__init__(parent)
        self.setupUi(self)
        self.changeXLim.addAction()
