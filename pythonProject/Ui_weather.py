# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'weather.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 401, 301))
        self.groupBox.setObjectName("groupBox")
        self.clearBtn = QtWidgets.QPushButton(self.groupBox)
        self.clearBtn.setGeometry(QtCore.QRect(240, 240, 93, 28))
        self.clearBtn.setObjectName("clearBtn")
        self.queryBtn = QtWidgets.QPushButton(self.groupBox)
        self.queryBtn.setGeometry(QtCore.QRect(50, 240, 93, 28))
        self.queryBtn.setObjectName("queryBtn")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setGeometry(QtCore.QRect(30, 70, 301, 161))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 40, 72, 15))
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(200, 40, 87, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.retranslateUi(Dialog)
        self.queryBtn.clicked.connect(Dialog.queryWeather)
        self.clearBtn.clicked.connect(Dialog.clearText)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "城市天气预报"))
        self.clearBtn.setText(_translate("Dialog", "清空"))
        self.queryBtn.setText(_translate("Dialog", "查询"))
        self.label.setText(_translate("Dialog", "城市"))
        self.comboBox.setItemText(0, _translate("Dialog", "北京"))
        self.comboBox.setItemText(1, _translate("Dialog", "上海"))
        self.comboBox.setItemText(2, _translate("Dialog", "苏州"))
        self.comboBox.setItemText(3, _translate("Dialog", "天津"))

