from __future__ import division
import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import MainWindow
import argparse
import threading
import os
authors_help = """Authors: Re'em Harel (January 2019)"""
description_help = """
*********************************************
----------------- Run Graphix Fast Visualization tool -----------------



"""


def main(f_path, qt):
    app = QApplication(sys.argv)

    mw = MainWindow.MainWindow(f_path, qt)
    mw.show()
    app.exec_()
    mw.end_program()
    time.sleep(0.5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=description_help
                                     , epilog=authors_help)
    parser.add_argument("-f", action='store', dest='f_path', help="Path of output file"
                        , default="/home/sc/reemh/Desktop/Leeor_Visual/data/FOR_REEM_plot")

    parser.add_argument("-qt", action='store_true', dest="qt", help="Use qt terminal.")

    if os.path.expanduser('~/').__contains__("edensh"):
        print "We do not allow Eden to use GraphiX until further notice"
        exit(1)
    options = parser.parse_args()

    main(options.f_path, options.qt)
