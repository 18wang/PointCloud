## PyQt Demo 记录

前端时间和鲍讨论PyQt的事情, 看了一下也不是很复杂, 自己也有QT的基础, 于是打算上手练习一下, 也找到了一个*Pycharm+Python*的博客, 于是决定试试.

[参考博客](https://lovesoo.org/2020/03/14/pyqt-getting-started/)

---------------------------------
1、GUI开发框架简介
19年来，一直在做Android ROM相关测试，也有了一定的积累；20年，计划把之前完整的测试方案、脚本、工具进行整合复用。
第一期计划是开发一个GUI的测试工具，近期也进行了相关调研。

1.1 通用开发框架
electorn：基于node-js，跨平台，开发成本低，运行效率低
qt：基于C++，跨平台，效率高，开发成本高
javafx：基于java，主要用于跨平台桌面程序开发
flutter：基于dart语言，谷歌开源移动UI框架，可以快速在iOS和Android上构建高质量的原生用户界面
1.2 Python方案
PyQT：PyQt5是Qt v5的Python版本，功能强大复杂，提供QT Designer设计UI （GPL V3协议，开源，商用收费）
Pyside: PySide2是来自QT for Python项目的官方Python模块 （LGPL协议，闭源商用）
Tkinter：Python标准库，Tk GUI 工具包的接口 ，布局通过代码实现，简单易用，但开发效率低
WxPython：开源免费，提供wxFormbuilder，压缩版PyQT
因为现有脚本绝大多数是基于Python开发，同时调研了上述框架的官方支持力度及网络资料丰富程度，最终还是选用了最流行最强大的PyQt 。

本文主要详细介绍下PyQt5完整入门教程，包含环境配置，使用Qt Disinger设计UI，最终完成一个天气预报的GUI实例开发。

环境为：Windows 10 + Python 3.8 + PyCharm 2019.2

2、PyQt环境配置
2.1 PyQt5 及 pyqt5-tools 安装
PyQt当前最新版本为PyQt5 5.14.1

直接pip安装即可：

```cmd
pip install PyQt5
pip install pyqt5-tools
```

建议使用国内源，进行快速安装：

```cmd
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyqt5
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyqt5-tools
```

2.2 PyCharm配置环境
启动PyCharm后，新建一个PyQt5空项目后，需要配置Qt Designer、pyuic、pyrcc工具，相关配置方法如下：

2.2.1 Qt Designer
Qt Designer 是通过拖拽的方式放置控件，并实时查看控件效果进行快速UI设计。

最终生成.ui文件（实质上是XML格式的文件），可以通过pyuic5工具转换成.py文件。

在Pycharm中，依次打开 File - Settings - Tools - External Tools，点击 + Create Tool，配置如下：

```cmd
Name: QtDisigner
Program : C:\Python38\Lib\site-packages\pyqt5_tools\Qt\bin\designer.exe # 当前designer目录，请根据实际修改
Working directory: $FileDir$
QtDisigner
```

2.2.2 Qt Designer 汉化
默认Qt Designer是英文版的，可以使用翻译文件进行汉化，下载地址：百度网盘，提取码：kxvx

下载文件 designer_zh_CN.qm后， 拷贝至本地pyqt5_tools的translations文件夹下即可，示例目录：

1
C:\Python38\Lib\site-packages\pyqt5_tools\Qt\bin\translations
在PyCharm主界面，依次点击 Tools - External Tools - QtDisigner，即可启动中文界面的Qt Disigner

QtDisigner

2.2.3 PyUIC配置
PyUIC主要是把Qt Designer生成的.ui文件换成.py文件。

在Pycharm中，依次打开 File - Settings - Tools - External Tools，点击 + Create Tool，配置如下：

```cmd
Name: PyUIC
Program : C:\Python38\python.exe # 当前Python目录，请根据实际修改
Arguments: -m PyQt5.uic.pyuic $FileName$ -o $FileNameWithoutExtension$.py
Working directory: $FileDir$
PyUIC
```

2.2.4 PyRCC配置
PyRCC主要是把编写的.qrc资源文件换成.py文件。

在Pycharm中，依次打开 File - Settings - Tools - External Tools，点击 + Create Tool，配置如下：

```cmd
Name: PyRCC
Program : C:\Python38\Scripts\pyrcc5.exe # 当前rcc工具目录，请根据实际修改
Arguments: $FileName$ -o $FileNameWithoutExtension$_rc.py
Working directory: $FileDir$
PyRCC
```

3、实例开发
下面我们以一个简单的城市天气预报为例，演示使用PyQt5开发一个GUI程序的基本流程。

3.1 获取天气数据
主要逻辑是通过Http接口调用免费的API接口获取相关城市天气数据，详见天气API说明

如测试一下请求天津的天气，链接为：http://t.weather.sojson.com/api/weather/city/101030100

返回成功状态（status）为：200 ，失败为非200，返回数据为json数据，直接解析获取即可。

3.1 设计界面UI
打开Qt Designer，可参考下图设计Weather.ui:

Weather.ui

我们主要用到的控件有Button, GroupBox, Label,ComboBox,TextEdit，同时定义了两个按钮queryBtn及clearBtn，分别用来查询及清空天气数据。我们需要绑定槽函数，方法如下：

1) 在Qt Designer右下角选择 信号/槽编辑器，点击+号新增
2) 分别选择queryBtn及clearBtn，选择信号 clicked(), 接收者 Dialog 及槽 accept() （我没找到绑定自定义槽函数的方法…）

绑定槽函数

最后选择保存为 Weather.ui文件。

3.2 转换.ui文件为.py文件
在PyCharm中选中Weather.ui文件后，右键选择 External Tools - PyUIC，即可生成Weather.py，实际运行命令如下：

1
C:\Python38\python.exe -m PyQt5.uic.pyuic Weather.ui -o Weather.py
其中，我们需要把两个按钮绑定的槽函数：

```cmd
self.queryBtn.clicked.connect(Dialog.accept)
self.clearBtn.clicked.connect(Dialog.accept)
```

修改为自定义函数：

```cmd
self.queryBtn.clicked.connect(Dialog.queryWeather)
self.clearBtn.clicked.connect(Dialog.clearText)
```

最终Weather.py内容如下：

```Python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Weather.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 391, 241))
        self.groupBox.setObjectName("groupBox")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setGeometry(QtCore.QRect(20, 50, 351, 181))
        self.textEdit.setObjectName("textEdit")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(100, 20, 91, 20))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 20, 61, 21))
        self.label.setObjectName("label")
        self.queryBtn = QtWidgets.QPushButton(Dialog)
        self.queryBtn.setGeometry(QtCore.QRect(40, 250, 75, 23))
        self.queryBtn.setMaximumSize(QtCore.QSize(75, 16777215))
        self.queryBtn.setObjectName("queryBtn")
        self.clearBtn = QtWidgets.QPushButton(Dialog)
        self.clearBtn.setGeometry(QtCore.QRect(250, 250, 75, 23))
        self.clearBtn.setMaximumSize(QtCore.QSize(75, 16777215))
        self.clearBtn.setObjectName("clearBtn")
        
        self.retranslateUi(Dialog)
        self.queryBtn.clicked.connect(Dialog.queryWeather)
        self.clearBtn.clicked.connect(Dialog.clearText)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "城市天气预报"))
        self.comboBox.setItemText(0, _translate("Dialog", "北京"))
        self.comboBox.setItemText(1, _translate("Dialog", "上海"))
        self.comboBox.setItemText(2, _translate("Dialog", "天津"))
        self.label.setText(_translate("Dialog", "城市"))
        self.queryBtn.setText(_translate("Dialog", "查询"))
        self.clearBtn.setText(_translate("Dialog", "清空"))
```

3.3 调用MainDialog
在MainDialog中调用界面类Ui_Dialog，然后在其中中添加查询天气的业务逻辑代码，这样就做到了界面显示和业务逻辑的分离。

新增demo.py文件， 在MainDialog类中定义了两个槽函数queryWeather()和clearText(),以便在界面文件Weather.ui中定义的两个按钮(queryBtn 和clearBtn) 触发clicked 信号与这两个槽函数进行绑定。

完整代码如下:

```Python
# coding:utf-8

import sys
import Weather
from PyQt5.QtWidgets import QApplication, QDialog
import requests


class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = Weather.Ui_Dialog()
        self.ui.setupUi(self)
    
    def queryWeather(self):
        cityName = self.ui.comboBox.currentText()
        cityCode = self.getCode(cityName)
        
        r = requests.get("http://t.weather.sojson.com/api/weather/city/{}".format(cityCode))
        
        print(r.json())
        
        if r.json().get('status') == 200:
            weatherMsg = '城市：{}\n日期：{}\n天气：{}\nPM 2.5：{} {}\n温度：{}\n湿度：{}\n风力：{}\n\n{}'.format(
                r.json()['cityInfo']['city'],
                r.json()['data']['forecast'][0]['ymd'],
                r.json()['data']['forecast'][0]['type'],
                int(r.json()['data']['pm25']),
                r.json()['data']['quality'],
                r.json()['data']['wendu'],
                r.json()['data']['shidu'],
                r.json()['data']['forecast'][0]['fl'],
                r.json()['data']['forecast'][0]['notice'],
            )
        else:
            weatherMsg = '天气查询失败，请稍后再试！'
        
        self.ui.textEdit.setText(weatherMsg)
    
    def getCode(self, cityName):
        cityDict = {"北京": "101010100",
                    "上海": "101020100",
                    "天津": "101030100"}
        
        return cityDict.get(cityName, '101010100')
    
    def clearText(self):
        self.ui.textEdit.clear()


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())
```

最终运行显示效果如下：

运行结果

完整demo地址：https://github.com/lovesoo/test_demo/tree/master/PyQt5

4、参考资料
https://www.riverbankcomputing.com/static/Docs/PyQt5/

http://code.py40.com/face

《PyQt5快速开发与实战 PDF》 网盘地址 提取码：k3xx

------------------------

***几个注意要点:***
1. Qt Designer中ui的名称没有大小写之分, 所以导出的 .py 也默认全小写, 注意更正
2. 使用Pyinstaller打包的对象是 Main 而非 UI, 即
```
pyinstaller -F demo.py
```
