import sys
from PyQt5 import QtWidgets
from picodeFileSelect import Window
import os
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mywindow = Window()
    mywindow.show()
    sys.exit(app.exec_())
