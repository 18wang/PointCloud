# coding:utf-8

import sys
import Ui_weather
from PyQt5.QtWidgets import QApplication, QDialog
import requests


class MainDialog(QDialog):
    def __init__(self, parent=None):
        print(0)
        super(QDialog, self).__init__(parent)
        self.ui = Ui_weather.Ui_Dialog()
        self.ui.setupUi(self)

    def queryWeather(self):
        print(1)
        cityName = self.ui.comboBox.currentText()
        cityCode = self.getCode(cityName)
        
        r = requests.get("http://t.weather.itboy.net/api/weather/city/{}".format(cityCode))
        
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
        print(2)
        cityDict = {"北京": "101010100",
                    "上海": "101020100",
                    "苏州": "101190401",
                    "天津": "101030100"}
        
        return cityDict.get(cityName, '101010100')
    
    def clearText(self):
        print(3)
        self.ui.textEdit.clear()


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())
