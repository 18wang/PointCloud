# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainForm.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1192, 863)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 20, 981, 801))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1192, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_2 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.treeView = QtWidgets.QTreeView(self.dockWidgetContents_2)
        self.treeView.setGeometry(QtCore.QRect(0, 0, 201, 821))
        self.treeView.setObjectName("treeView")
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_2)
        self.actionxin = QtWidgets.QAction(MainWindow)
        self.actionxin.setObjectName("actionxin")
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actioncuiduiqi = QtWidgets.QAction(MainWindow)
        self.actioncuiduiqi.setObjectName("actioncuiduiqi")
        self.actionICP = QtWidgets.QAction(MainWindow)
        self.actionICP.setObjectName("actionICP")
        self.actionRPS = QtWidgets.QAction(MainWindow)
        self.actionRPS.setObjectName("actionRPS")
        self.actionzhitong = QtWidgets.QAction(MainWindow)
        self.actionzhitong.setObjectName("actionzhitong")
        self.actionCropHull = QtWidgets.QAction(MainWindow)
        self.actionCropHull.setObjectName("actionCropHull")
        self.actionopenStl = QtWidgets.QAction(MainWindow)
        self.actionopenStl.setObjectName("actionopenStl")
        self.menu.addAction(self.actionxin)
        self.menu.addAction(self.actionopen)
        self.menu.addAction(self.actionopenStl)
        self.menu_2.addAction(self.actionzhitong)
        self.menu_2.addAction(self.actionCropHull)
        self.menu_3.addAction(self.actioncuiduiqi)
        self.menu_3.addAction(self.actionICP)
        self.menu_3.addAction(self.actionRPS)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        # self.actionopen.triggered.connect(MainWindow.readtxt)
        # txt点云文件读取
        # self.actionopen.triggered.connect(MainWindow.readTxt)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "滤波"))
        self.menu_3.setTitle(_translate("MainWindow", "对齐"))
        self.actionxin.setText(_translate("MainWindow", "新建"))
        self.actionopen.setText(_translate("MainWindow", "读取点云"))
        self.actioncuiduiqi.setText(_translate("MainWindow", "cuiduiqi"))
        self.actionICP.setText(_translate("MainWindow", "ICP"))
        self.actionRPS.setText(_translate("MainWindow", "RPS"))
        self.actionzhitong.setText(_translate("MainWindow", "zhitong"))
        self.actionCropHull.setText(_translate("MainWindow", "CropHull"))
        self.actionopenStl.setText(_translate("MainWindow", "读取STL"))

