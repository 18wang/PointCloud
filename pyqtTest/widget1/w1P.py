import w1
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QFileDialog,
    QWidget,
)

class Ui_widget1(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.ui = w1.Ui_widget1()
        self.ui.setupUi(self)



app = QApplication(sys.argv)
window = Ui_widget1()
window.show()
sys.exit(app.exec_())