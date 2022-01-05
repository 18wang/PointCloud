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
        GlobalRegistration.resize(202, 142)
        self.cancel = QtWidgets.QPushButton(GlobalRegistration)
        self.cancel.setGeometry(QtCore.QRect(120, 100, 61, 25))
        self.cancel.setObjectName("cancel")
        self.ok = QtWidgets.QPushButton(GlobalRegistration)
        self.ok.setGeometry(QtCore.QRect(10, 100, 61, 25))
        self.ok.setObjectName("ok")
        self.formLayoutWidget = QtWidgets.QWidget(GlobalRegistration)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 10, 157, 71))
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

        self.retranslateUi(GlobalRegistration)
        QtCore.QMetaObject.connectSlotsByName(GlobalRegistration)

    def retranslateUi(self, GlobalRegistration):
        _translate = QtCore.QCoreApplication.translate
        GlobalRegistration.setWindowTitle(_translate("GlobalRegistration", "Dialog"))
        self.cancel.setText(_translate("GlobalRegistration", "退出"))
        self.ok.setText(_translate("GlobalRegistration", "确定"))
        self.voxelSize.setText(_translate("GlobalRegistration", "1"))
        self.label_2.setText(_translate("GlobalRegistration", "点云距离阈值:"))
        self.distanceThreshold.setText(_translate("GlobalRegistration", "2"))
        self.label.setText(_translate("GlobalRegistration", "体素大小:"))

