#!/usr/bin/env python
"""
Program to make an contour plot from a contour data file generated
by the Perple_X program WERAMI, for data file format see:
http://www.perplex.ethz.ch/faq/Perple_X_tab_file_format.txt
"""
# author: Ondrej Lexa
# website: petrol.natur.cuni.cz/~ondro
# last edited: April 16, 2014

import sys
import argparse

from PyQt4 import QtGui
from pywerami.mainapp import PyWeramiWindow

def process_cl_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', action='store', nargs='?', default=None, help="Werami tab file")

    parsed_args, unparsed_args = parser.parse_known_args()
    return parsed_args, unparsed_args

if __name__ == '__main__':
    parsed_args, unparsed_args = process_cl_args()
    app = QtGui.QApplication(unparsed_args)
    #app.setWindowIcon(QIcon('pywerami.png'))
    MainWindow = PyWeramiWindow(parsed_args.filename)

    MainWindow.show()
    sys.exit(app.exec_())
