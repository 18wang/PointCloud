# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GlobalRegistrationUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GlobalRegistration(object):
    def setupUi(self, GlobalRegistration):
        GlobalRegistration.setObjectName("GlobalRegistration")
        GlobalRegistration.resize(230, 152)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GlobalRegistration.sizePolicy().hasHeightForWidth())
        GlobalRegistration.setSizePolicy(sizePolicy)
        GlobalRegistration.setMinimumSize(QtCore.QSize(230, 152))
        GlobalRegistration.setMaximumSize(QtCore.QSize(230, 152))
        GlobalRegistration.setBaseSize(QtCore.QSize(0, 0))
        self.formLayoutWidget = QtWidgets.QWidget(GlobalRegistration)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 10, 188, 126))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.voxelSize = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.voxelSize.setObjectName("voxelSize")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.voxelSize)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.distanceThreshold = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.distanceThreshold.setObjectName("distanceThreshold")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.distanceThreshold)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.ok = QtWidgets.QPushButton(self.formLayoutWidget)
        self.ok.setObjectName("ok")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.ok)
        self.cancel = QtWidgets.QPushButton(self.formLayoutWidget)
        self.cancel.setObjectName("cancel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cancel)

        self.retranslateUi(GlobalRegistration)
        QtCore.QMetaObject.connectSlotsByName(GlobalRegistration)

    def retranslateUi(self, GlobalRegistration):
        _translate = QtCore.QCoreApplication.translate
        GlobalRegistration.setWindowTitle(_translate("GlobalRegistration", "Dialog"))
        self.voxelSize.setText(_translate("GlobalRegistration", "1"))
        self.label_2.setText(_translate("GlobalRegistration", "点云距离阈值:"))
        self.distanceThreshold.setText(_translate("GlobalRegistration", "2"))
        self.label.setText(_translate("GlobalRegistration", "体素大小:"))
        self.label_3.setText(_translate("GlobalRegistration", "下采样:"))
        self.comboBox.setItemText(0, _translate("GlobalRegistration", "1"))
        self.comboBox.setItemText(1, _translate("GlobalRegistration", "1/2"))
        self.comboBox.setItemText(2, _translate("GlobalRegistration", "1/4"))
        self.comboBox.setItemText(3, _translate("GlobalRegistration", "1/8"))
        self.comboBox.setItemText(4, _translate("GlobalRegistration", "1/16"))
        self.comboBox.setItemText(5, _translate("GlobalRegistration", "1/32"))
        self.comboBox.setItemText(6, _translate("GlobalRegistration", "1/64"))
        self.comboBox.setItemText(7, _translate("GlobalRegistration", "1/128"))
        self.ok.setText(_translate("GlobalRegistration", "确定"))
        self.cancel.setText(_translate("GlobalRegistration", "退出"))

