# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PassThroughFilterUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_PTFDialog(object):
    def setupUi(self, PTFDialog):
        PTFDialog.setObjectName("PTFDialog")
        PTFDialog.resize(320, 240)
        PTFDialog.setMinimumSize(QtCore.QSize(200, 100))
        PTFDialog.setMaximumSize(QtCore.QSize(500, 300))
        PTFDialog.setToolTip("")
        PTFDialog.setSizeGripEnabled(False)
        self.formLayoutWidget = QtWidgets.QWidget(PTFDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 251, 131))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.comboBox_2 = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_2)
        self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.formLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.buttonBox)

        self.retranslateUi(PTFDialog)
        self.buttonBox.accepted.connect(PTFDialog.accept)
        self.buttonBox.rejected.connect(PTFDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PTFDialog)

    def retranslateUi(self, PTFDialog):
        _translate = QtCore.QCoreApplication.translate
        PTFDialog.setWindowTitle(_translate("PTFDialog", "Dialog"))
        self.comboBox.setItemText(0, _translate("PTFDialog", "X"))
        self.comboBox.setItemText(1, _translate("PTFDialog", "Y"))
        self.comboBox.setItemText(2, _translate("PTFDialog", "Z"))
        self.comboBox_2.setItemText(0, _translate("PTFDialog", ">="))
        self.comboBox_2.setItemText(1, _translate("PTFDialog", ">"))
        self.comboBox_2.setItemText(2, _translate("PTFDialog", "<"))
        self.comboBox_2.setItemText(3, _translate("PTFDialog", "<="))
        self.comboBox_2.setItemText(4, _translate("PTFDialog", "="))

