from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtSql import *
from PyQt4.QtNetwork import *


class GnuplotWidget(QWidget):
    def __init__(self, id = 0, parent=None):
        super(GnuplotWidget, self).__init__(parent)
        self.m_id = id
        self.m_view = QGraphicsView()
        qb_layout = QVBoxLayout()
        qb_layout.setContentsMargins(0, 0, 0, 0)
        qb_layout.addWidget(self.m_view)
        qls = QLocalServer()
        qls.lis
        self.setLayout(qb_layout)
        self.eventHandler = Event