import sys
import numpy as np
import MainForm
import vtk
from pathlib import Path

from Filtering.CropHull import Mouse_Pointcloud_Selection
from Filtering.PassThroughFilterUI import Ui_PTFDialog
from Filtering.PassThroughFilter import PassThroughFilter

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QFileDialog,
    QDialog,
)
from PyQt5.QtCore import pyqtSignal

# vtkInteractionStyle vtkRenderingOpenGL2 交互与显示，虽不直接使用，但需要import
from vtkmodules.vtkIOPLY import (
    vtkPLYReader,
)
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
    vtkCellArray,
)
from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkUnsignedCharArray,
    vtkPoints,
)
from vtkmodules.vtkIOGeometry import (
    vtkOBJReader,
    vtkSTLReader,
)
from vtkmodules.vtkInteractionWidgets import vtkScalarBarWidget
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
)
# 嵌入qt 默认引用
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

#class Ui_MainWindow(QtWidgets.QMainWindow):
class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        # 继承父类
        super(QMainWindow, self).__init__(parent)

        self.ui = MainForm.Ui_MainWindow()
        self.ui.setupUi(self)

#------------------ 自行添加的信号/槽 ------------------------------------
        self.ui.actionopen.triggered.connect(self.readFile)
        self.ui.actionCropHull.triggered.connect(self.cropHull)
        self.ui.actionzhitong.triggered.connect(self.passThrough)


#---------------------------------------------------------------------

        self.frame = QFrame()

        # 向 verticalLayout 中添加 vtkWidget
        self.vl = self.ui.verticalLayout
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        # 新建 vtkRenderer
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()


    def getFile(self):
        """
        qFileDialog文件读取
        :return: fileName
        """
        fileName, _ = QFileDialog.getOpenFileName(self,
            'Open file', './', '点云文件(*.txt *.ply *.obj *.stl);;彩色点云文件(*.txt)')
        return fileName

    def ReadPolyData(self, file_name):
        """
        文件名分析并读取
        :param file_name:
        :return: polydata
        """
        valid_suffixes = ['.obj', '.stl', '.ply', '.txt']
        path = Path(file_name)
        if path.suffix:
            ext = path.suffix.lower()
        if path.suffix not in valid_suffixes:
            print(f'No reader for this file suffix: {ext}')
            return None
        else:
            if ext == ".ply":
                reader = vtkPLYReader()
                reader.SetFileName(file_name)
                reader.Update()
                poly_data = reader.GetOutput()
            elif ext == ".obj":
                reader = vtkOBJReader()
                reader.SetFileName(file_name)
                reader.Update()
                poly_data = reader.GetOutput()
            elif ext == ".stl":
                reader = vtkSTLReader()
                reader.SetFileName(file_name)
                reader.Update()
                poly_data = reader.GetOutput()
            elif ext == ".txt":

                temp_data = np.loadtxt(file_name)

                isColorfulPoints = temp_data.shape[1] > 3
                if isColorfulPoints:
                    # 彩色点云数据
                    source_color = temp_data[:, 3:]
                    # 0-255 RGB彩色
                    source_color_int = [[int(i[0]*255), int(i[1]*255),
                                         int(i[2]*255)] for i in source_color]
                    colors = vtkUnsignedCharArray()
                    colors.SetNumberOfComponents(3)

                # 点云数据点
                source_data = temp_data[:, 0:3]

                # points cell color 类型
                points = vtkPoints()
                poly_data = vtkPolyData()
                vtkCells = vtkCellArray()

                # 插入cell
                for i, p in enumerate(source_data):
                    pointId = points.InsertNextPoint(p[:])  # 插入点
                    vtkCells.InsertNextCell(1)
                    vtkCells.InsertCellPoint(pointId)
                    if isColorfulPoints:
                        colors.InsertNextTypedTuple(source_color_int[i])

                poly_data.SetPoints(points)
                poly_data.SetVerts(vtkCells)
                if isColorfulPoints:
                    poly_data.GetPointData().SetScalars(colors)

            return poly_data


    def displayPolydata(self, polydata):
        """
        polydata显示
        :param polydata:
        :return:
        """
        # 添加polydata
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(polydata)

        actor = vtkActor()
        actor.SetMapper(mapper)
        self.ren.AddActor(actor)

        if False:

            # 绘制scalar_bar

            # scalar_bar 的 lut
            bar_lut = vtkLookupTable()
            bar_lut.Build()
            # create the scalar_bar
            scalar_bar = vtkScalarBarActor()
            scalar_bar.SetOrientationToHorizontal()
            scalar_bar.SetLookupTable(bar_lut)

            # create the scalar_bar_widget
            self.scalar_bar_widget = vtkScalarBarWidget()
            self.scalar_bar_widget.SetInteractor(self.iren)
            self.scalar_bar_widget.SetScalarBarActor(scalar_bar)
            self.scalar_bar_widget.On()

        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()

        return True


    def readFile(self):
        """
        文件读取
        :return: bool
        """
        # The source file
        file_name = self.getFile()
        self.polydata = self.ReadPolyData(file_name)
        self.displayPolydata(self.polydata)
        return True


    def cropHull(self):
        """
        区域选取函数
        :return: bool
        """

        # 定义 鼠标点云选取类
        style = Mouse_Pointcloud_Selection(self, self.ren, self.polydata)
        style.SetDefaultRenderer(self.ren)
        self.iren.SetInteractorStyle(style)
        # 添加 area_picker
        self.iren.SetPicker(style.area_picker)

        return True


    def passThrough(self):
        self.ptDialog = PTFDialog()
        self.ptDialog.SetPTF.connect(self.runPassThrough)


        self.ptDialog.show()

    def runPassThrough(self, params):
        pcd, fieldName, limits = params
        print('主窗口', params)








class PTFDialog(QDialog):
    SetPTF = pyqtSignal(list)

    def __init__(self):
        super(PTFDialog, self).__init__()

        self.ui = Ui_PTFDialog()
        self.ui.setupUi(self)

        self.ui.setBtn.clicked.connect(self.setPassThrough)
        self.ui.clearBtn.clicked.connect(self.clearPassThrough)
        self.ui.cancelBtn.clicked.connect(self.close)


    def setPassThrough(self):
        XYZ = self.ui.XYZcomboBox.currentText()
        logical = self.ui.logicalcomBox.currentText()
        value = self.ui.lineEdit.text()
        print(XYZ, logical, value)
        self.SetPTF.emit([XYZ, logical, value])

        pass


    def clearPassThrough(self):

        pass

        return






if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())

