import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QFileDialog,
    QWidget,
)

import mainwindow.window
import widget1.w1P
import widget1.w1

class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)

        self.ui = mainwindow.window.Ui_MainWindow()

        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.openW1)


    def openW1(self):

        self.w1 = widget1.w1P.Ui_widget1()
        self.w1.show()
        # result = w1.exec_()






if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
