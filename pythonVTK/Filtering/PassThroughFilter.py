# 2021年12月31日

# 直通滤波

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QDialog,
    QApplication,
)


import PassThroughFilterUI


class Ui_PTFDialog(QDialog):

    def __init__(self):
        super(QDialog, self).__init__()

        self.ui = PassThroughFilterUI.Ui_PTFDialog()
        self.ui.setupUi(self)

        return

app = QApplication(sys.argv)
window = Ui_PTFDialog()
window.show()
sys.exit(app.exec_())

